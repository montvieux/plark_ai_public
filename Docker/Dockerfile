FROM nvcr.io/nvidia/tensorflow:19.10-py3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update \
    && apt-get -y install \
    python3.6-tk \
    curl \
    cmake \
    default-jre \
    git \
    jq \
    libfontconfig1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libopenmpi-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#jupyter notebook password
#cloudywithachanceofamonia
ADD jupyter_notebook_config.json /root/.jupyter/jupyter_notebook_config.json

ADD requirements.txt /usr/local/requirements.txt
RUN pip install --upgrade -r /usr/local/requirements.txt

ADD run_servers.sh /run_servers.sh
WORKDIR /
CMD sh run_servers.sh && tail -f /dev/null

#############################
# Instructions
#############################
# STEPS For Container
# Build the docker image
#       - sudo docker build -t plark_ai .
# Each time a new conda package or pip requirement is needed, this command must be rerun to rebuild the image
# Note that most of the installed packages from before are cached by docker to save time
# To run the docker container:
#       - sudo docker run --gpus 'device=0' -v /home/aidanjones/repos/plark_ai/Components:/Components -v /datasets/plark_ai:/data -p 8892:8888 -p 5003:5000 -it --shm-size=8192m plark_ai /bin/bash 
# To run a tensorboard server:
#       - sudo docker run -v /datasets/plark_ai/agents/models/test_20200325_184254:/tensorboard_store -p 6006:6006 tensorflow/tensorflow:1.12.0 tensorboard --logdir=/tensorboard_store
#
# STEPS FOR JUPYTER
# Inside the container, run jupyter:
#        - jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root &
# Note: the port 8888 is the docker containers local port which you mapped to port 8892 on the server
# sh run_servers.sh &