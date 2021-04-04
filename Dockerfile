FROM python:3.8.0

WORKDIR /restapi

ADD restapi.py .

RUN pip install flask flask_restful flask_sqlalchemy

COPY test.log .

COPY MyDB.db . 


CMD [ "python", "./restapi.py"]