FROM python:3.10-slim

RUN mkdir /telegram
COPY telegram/requirements.txt /telegram

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --user -r /telegram/requirements.txt

COPY telegram /telegram

