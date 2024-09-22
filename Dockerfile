FROM python:3.10-slim

RUN apt update && apt install nginx -y

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

COPY . .

RUN pip install -r requirements.txt

WORKDIR app
COPY run.sh .
COPY .env .

RUN chmod +x run.sh

CMD ["./run.sh"]
