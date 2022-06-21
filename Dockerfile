FROM debian:bullseye-slim


RUN apt-get update


RUN apt-get install --assume-yes --no-install-recommends --quiet \

    python3 \

    python3-pip \

    ffmpeg


RUN pip install --no-cache --upgrade pip setuptools


RUN pip3 install numpy \

    scikit-learn \

    torch \

    nltk \

    matplotlib \

    h5py \

    sentencepiece


ADD . /mypackage/


ENTRYPOINT ["python", "-m", "mypackage.script"]
