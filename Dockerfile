#FROM python:3.12.10-alpine
FROM python:3.11.9-bullseye
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod 777 -R /app

#CMD ["python", "app.py"] 
## You can use this line to run the app directly but it's better to use a shell script for more complex setups.
CMD ["bash", "start"]
