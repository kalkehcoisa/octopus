FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt && \
    mkdir -p /var/log/web && \
    python -m nltk.downloader punkt averaged_perceptron_tagger
CMD ["python", "web/run.py"]