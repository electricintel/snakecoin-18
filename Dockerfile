FROM python:2.7
ADD . /snakecoin
WORKDIR /snakecoin
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "api.py"]
