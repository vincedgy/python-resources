# Build Image part
FROM python:3.7-slim-buster

ENV TZ=Europe/Paris
RUN ln -s -f /usr/share/zoneinfo/$TZ /etc/localtime

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir pipenv

RUN groupadd -r worker && useradd -m -r -g worker worker

USER worker
WORKDIR /home/worker

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker . .
RUN pipenv lock -r > requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
CMD ["python", "-u", "tee-schedule.py"]