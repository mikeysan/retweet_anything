FROM python:3.8.6-alpine
COPY bots/config.py /bots/
COPY bots/followback.py /bots/
COPY bots/favretweet.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "favretweet.py"]