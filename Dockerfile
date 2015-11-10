# ultimately this would be resin/%%RESIN_MACHINE_NAME%%-python-dev
FROM registry.resin.io/digtaldisplay/f04fbad79a83344a17012dbb3863149a1f08d99a

RUN apt-get update && apt-get install -yq \
    python-pyaudio && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install rpi_ws281x pubnub==3.7.3

COPY app /usr/src/app

WORKDIR /usr/src/app

#CMD ["python","noiseLevel.py"]
CMD ["python","noiseLevel.py"]
