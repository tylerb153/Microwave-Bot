# syntax=docker/dockerfile:1

FROM python:3.14.6-slim

RUN apt-get update
RUN apt-get install -y libopus0 ffmpeg


RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "bot.py"]