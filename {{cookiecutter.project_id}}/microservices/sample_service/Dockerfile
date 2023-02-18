ARG BASE_IMG
FROM ${BASE_IMG}

WORKDIR /opt
COPY requirements.txt service_requirements.txt

# add endline in case not there
RUN awk 1 requirements.txt > requirements.txt
RUN cat service_requirements.txt >> requirements.txt

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 8888

# ENTRYPOINT [ "python", "main.py", "--prod=True" ]
ENTRYPOINT [ "python", "main.py" ]
