FROM python:3.8
WORKDIR /home
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY resources/ /resources/
COPY ./labellize.py .
RUN apt-get update
RUN apt-get install -y python3-tk
ENTRYPOINT ["python","labellize.py"]
