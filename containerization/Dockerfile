FROM python:3.11-slim AS requirements

RUN mkdir /app

COPY snyk-sast-tag.py /app/snyk-sast-tag.py
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --quiet -U pip
RUN pip install --user -r /app/requirements.txt

RUN rm /app/requirements.txt

# now we create our final container, runtime
FROM python:3.13-rc-bullseye AS runtime
# now we use multistage containers to then copy the requirements from the other container
COPY --from=requirements /root/.local /root/.local

RUN pip freeze > requirements.txt

ENTRYPOINT ["tail", "-f", "/dev/null"]
