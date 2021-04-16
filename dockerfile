FROM continuumio/anaconda3
COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR "/app"
RUN pip install -r /tmp/requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "doc.py" ]