FROM rayproject/ray:2.3.0-py310-cu116@sha256:2efbceab43c95be9409316080c388c449616b49c6d0952c5ac70a43b3fce3093
USER root
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
RUN apt update && \
    apt install -y  --no-install-recommends  build-essential python3-pip python3-dev libglib2.0-0 \
    libgl1-mesa-glx  libsm6 libxrender1 libxext6 nvidia-cuda-toolkit gcc && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* \
COPY . /app
RUN pip install --upgrade pip
RUN pip install -U --no-cache-dir -r requirements.txt
RUN pip install https://github.com/KaiyangZhou/deep-person-reid/archive/master.zip
WORKDIR /app
ENV PATH=/usr/local/cuda-11.6/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64:$LD_LIBRARY_PATH
