FROM nvidia/cuda:11.7.1-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get upgrade -qq

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq
RUN apt-get install -y  \
  build-essential \
  cmake \
  git \
  graphviz \
  libatlas-base-dev \
  libboost-filesystem-dev \
  libboost-iostreams-dev \
  libboost-program-options-dev \
  libboost-regex-dev \
  libboost-serialization-dev \
  libboost-system-dev \
  libboost-test-dev \
  libboost-graph-dev \
  libcgal-dev \
  libcgal-qt5-dev \
  libfreeimage-dev \
  libgflags-dev \
  libglew-dev \
  libglu1-mesa-dev \
  libgoogle-glog-dev \
  libjpeg-dev \
  libopencv-dev \
  libpng-dev \
  libqt5opengl5-dev \
  libsuitesparse-dev \
  libtiff-dev \
  libxi-dev \
  libxrandr-dev \
  libxxf86vm-dev \
  libxxf86vm1 \
  mediainfo \
  mercurial \
  qtbase5-dev \
  libatlas-base-dev \
  libsuitesparse-dev \
  libcgal-dev \
  libcgal-qt5-dev \
  python3

# OpenCV
RUN DEBIAN_FRONTEND=noninteractive apt-get -yq install libopencv-dev

# CGAL
RUN apt-get -yq install libcgal-dev libcgal-qt5-dev

WORKDIR /tmp/build

# Install openmvg
RUN git clone -b develop --recursive https://github.com/openMVG/openMVG.git openmvg && \
  mkdir openmvg_build && cd openmvg_build && \
  cmake -DCMAKE_BUILD_TYPE=RELEASE . ../openmvg/src -DCMAKE_INSTALL_PREFIX=/opt/openmvg && \
  make -j4  && \
  make install

# Install eigen
RUN git clone https://gitlab.com/libeigen/eigen.git --branch 3.4 && \
  mkdir eigen_build && cd eigen_build && \
  cmake . ../eigen && \
  make -j4 && \
  make install 

# Get vcglib
RUN git clone https://github.com/cdcseacave/VCG.git vcglib 

# Install ceres solver
RUN git clone https://ceres-solver.googlesource.com/ceres-solver ceres_solver && \
  mkdir ceres_build && cd ceres_build && \
  cmake . ../ceres_solver/ -DMINIGLOG=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF && \
  make -j4 && \
  make install

# Install openmvs
RUN git clone https://github.com/cdcseacave/openMVS.git openmvs && \
  mkdir openmvs_build && cd openmvs_build &&\
	cmake . ../openmvs -DCMAKE_INSTALL_PREFIX=/opt/openmvs -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT=../vcglib -DOpenMVS_USE_CUDA=ON -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs/ -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda/ -DCUDA_INCLUDE_DIRS=/usr/local/cuda/include/ -DCUDA_CUDART_LIBRARY=/usr/local/cuda/lib64 -DCUDA_NVCC_EXECUTABLE=/usr/local/cuda/bin/ && \
  make -j4 &&\
	make install

COPY scripts/ /opt/video2object/scripts
COPY video2object.py /opt/video2object/video2object.py
COPY requirements.txt /opt/video2object/requirements.txt

RUN pip3 install -r /opt/video2object/requirements.txt
RUN echo ptools soft core unlimited >> /etc/security/limits.conf
RUN echo ptools hard core unlimited >> /etc/security/limits.conf
RUN groupadd -r user && useradd -r -g user user

USER user
WORKDIR /
ENV PATH=/opt/openmvs/bin/OpenMVS:/opt/openmvg/bin:/opt/cmvs/bin:/opt/colmap/bin:/opt/video2object:$PATH