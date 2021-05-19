FROM python:3.7-slim 

WORKDIR /opt
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8889

# ENTRYPOINT [ "python", "main.py", "--prod=True" ]
ENTRYPOINT [ "python", "main.py" ]
