FROM python:3.8-slim-buster
RUN useradd myproj
WORKDIR /home/myproj

COPY requirements.txt requirements.txt

RUN pip install pip --upgrade
RUN pip install fastapi pydantic redis rq uvicorn

COPY *.py ./

RUN chown -R myproj:myproj ./

USER myproj
CMD uvicorn api:app --host 0.0.0.0 --port 5057