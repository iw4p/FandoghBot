FROM python:3.5-slim-stretch

WORKDIR /app

COPY requirements.txt /app/
COPY bot.py /app/

RUN pip3 install -r requirements.txt
RUN pip3 install fandogh-cli --upgrade 

CMD python bot.py