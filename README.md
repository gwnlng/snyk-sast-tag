![Snyk logo](https://snyk.io/style/asset/logo/snyk-print.svg)

# snyk-sast-tag

## Description
This script applies 1 or more [project tag](https://docs.snyk.io/snyk-admin/snyk-projects/project-tags) to a Snyk monitored Code Analysis project.

### **Note**

:memo: Set your environment variable SNYK_TOKEN

### Command-line Parameters

| Option/Argument   | Description                                         | Example            |
|-------------------|-----------------------------------------------------|--------------------|
| --project-tags    | Project Tags                                        | key1=value1        |
| --help            | Shows this message and exit                         |                    |
| json_filepath     | Snyk Code output JSON filepath                      | ./mycodejson.json  |

## Quick-start
```bash
pip install -r requirements.txt
```

### Build and Run Example
To create tags key1:value1, key2:value2 to a project, use command:
```bash
python snyk-sast-tag.py "<snyk_code_output_json_filepath>" --project-tags="key1=value1,key2=value2"
```

## Use
Download the OS specific self-executable from [Releases](https://github.com/gwnlng/snyk-sast-tag/releases) page and run it.
```bash
./snyk-sast-tag-Linux "<snyk_code_output_json_filepath>" --project-tags="key1=value1,key2=value2"
```
