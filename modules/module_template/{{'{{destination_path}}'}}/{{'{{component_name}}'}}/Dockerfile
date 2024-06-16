{% raw %}{% if depend_on_common == true -%}
ARG COMMON_IMAGE
FROM ${COMMON_IMAGE}
{% else %}
FROM python:3.9-slim
{%- endif %}


WORKDIR /opt
COPY requirements.txt service_requirements.txt

# add endline in case not there
RUN awk 1 requirements.txt > requirements.txt
RUN cat service_requirements.txt >> requirements.txt

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 9001

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ENTRYPOINT [ "python", "main.py", "--prod=True" ]
ENTRYPOINT [ "python", "main.py" ]
{% endraw %}