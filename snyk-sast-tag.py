import typer
import requests
import os
import json


SNYK_TOKEN = os.getenv("SNYK_TOKEN", None)
version = "2024-03-12"
content_type = "application/vnd.api+json"
header_auth = f"token {SNYK_TOKEN}"
headers = {
    'Content-Type': content_type,
    'Authorization': header_auth
}


def read_snyk_metadata(json_filepath):
    """
    Returns the project id from the json file
    :param json_filepath: Code test json output file
    :return org_id: snyk org id
    :return project_id: snyk project id
    """
    try:
        with open(json_filepath, 'r') as f:
            code_json = json.load(f)

        if code_json:
            report_url = code_json["runs"][0]["properties"]["uploadResult"]["reportUrl"]
            # get the org slug from e.g. https://app.snyk.io/org/<org_slug>
            app_host = report_url.split("/")[2]
            api_host = app_host.replace("app", "api")
            base_api_url = f"https://{api_host}/rest"
            org_slug = report_url.split("/")[4]
            org_id = get_org_id(base_api_url, org_slug)
            # get the project id
            project_id = code_json["runs"][0]["properties"]["uploadResult"]["projectId"]
            return base_api_url, org_id, project_id
    except FileNotFoundError as fnfe:
        raise Exception(f"unable to find snyk code test json output file: {json_filepath}", fnfe)


def get_org_id(base_api_url, org_slug):
    """
    Returns the org id from the org slug
    :param base_api_url: snyk api url
    :param org_slug: snyk org slug
    :return org_id: snyk org id
    """
    api_link = f"orgs?version={version}&slug={org_slug}"
    api_url = f"{base_api_url}/{api_link}"
    payload = {}
    response = requests.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        org_id = response_json["data"][0]["id"]
        return org_id
    else:
        raise Exception(f"unable to get org id with response status: {response.status_code}-{response.text}")


def main(json_filepath, project_tags: str = None):
    """
    Calls Snyk Projects update REST API
    :param json_filepath: Code test json output file
    :param project_tags: comma separated key=value pairs
    :return:
    """
    if SNYK_TOKEN is None:
        raise Exception("SNYK_TOKEN environment variable is required")
    if project_tags is None:
        raise ValueError(f"--project-tags is required")
    if "=" not in project_tags:
        raise ValueError(f"project tags must be in the format key1=value1,key2=value2,...")

    key_value_list = project_tags.split(",")
    tags_list = []
    for item in key_value_list:
        try:
            k, v = item.split("=")
            tags_list.append({"key": k, "value": v})
        except ValueError:
            # Handle cases where the string is not in the expected format (key=value)
            pass

    org_id_project_id = read_snyk_metadata(json_filepath)
    base_api_url = org_id_project_id[0]
    org_id = org_id_project_id[1]
    project_id = org_id_project_id[2]
    api_link = f"orgs/{org_id}/projects/{project_id}?version={version}"
    api_url = f"{base_api_url}/{api_link}"
    payload = {
        "data": {
            "attributes": {
                "tags": tags_list,
            },
            "id": project_id,
            "relationships": {
            },
            "type": "project"
        }
    }

    try:
        response = requests.request("PATCH", api_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("project tags updated")
        else:
            print(f"project tags update failed with response status: {response.status_code}-{response.text}")
    except Exception as err:
        raise Exception(f"unable to update project tags with requests error", err)


if __name__ == "__main__":
    typer.run(main)
