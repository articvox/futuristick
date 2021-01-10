FROM python:3.8-slim-buster
ARG CRON

RUN mkdir /futuristick
ADD . /futuristick/
RUN pip install -r /futuristick/requirements.txt

RUN apt-get update && apt-get -y install cron
RUN (crontab -l ; echo "$CRON /usr/local/bin/python /futuristick/bot.py >> /var/log/cron.log 2>&1") | crontab

CMD cron && touch /var/log/cron.log && tail -f /var/log/cron.log