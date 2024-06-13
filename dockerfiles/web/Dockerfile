FROM python:3.10-slim

COPY web_django/requirements.txt .

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

COPY web_django/ .


