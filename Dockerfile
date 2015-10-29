# ultimately this would be resin/%%RESIN_MACHINE_NAME%%-python-dev
FROM registry.resin.io/digtaldisplay/f04fbad79a83344a17012dbb3863149a1f08d99a

RUN pip install rpi_ws281x

COPY app /usr/src/app

WORKDIR /usr/src/app

CMD ["python","main.py"]
