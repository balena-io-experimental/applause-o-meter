# ultimately this would be resin/%%RESIN_MACHINE_NAME%%-python-dev
FROM registry.resin.io/digtaldisplay/f04fbad79a83344a17012dbb3863149a1f08d99a

# RUN apt-get update && apt-get install -yq \
#     swig \
#     scons && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*
#
# COPY vendor /usr/src/app

RUN pip install rpi_ws281x

COPY app /usr/src/app

WORKDIR /usr/src/app

# RUN cd rpi_ws281x && scons && cd python && python setup.py install

CMD ["python","main.py"]
