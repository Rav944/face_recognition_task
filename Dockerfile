FROM python:3.9
RUN mkdir /app
WORKDIR /app
RUN cd /app
COPY analyzer /app/analyzer
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000