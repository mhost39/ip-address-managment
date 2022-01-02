
FROM python:3.8

RUN apt-get update -y 
WORKDIR /ip-adress-managment
COPY ./requirements.txt /ip-adress-managment/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /ip-adress-managment

CMD [ "python", "./app.py" ]
