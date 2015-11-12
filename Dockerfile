FROM resin/raspberrypi2-python

RUN apt-get update \
	&& apt-get install -yq \
    	python-pyaudio \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install rpi_ws281x pubnub==3.7.3

WORKDIR /usr/src/app

CMD [ "python", "blank_leds.py" ]

COPY app /usr/src/app
