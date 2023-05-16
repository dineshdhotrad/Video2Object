export TMP=/tmp/build
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get upgrade -qq

apt-get install -y  \
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
  libsuitesparse-dev

mkdir -p $TMP && cd $TMP

# Install OpenMVG
git clone -b develop --recursive https://github.com/openMVG/openMVG.git ${TMP}/openmvg && \
  cd openmvg && git checkout tags/v2.0 && cd .. && \
  mkdir ${TMP}/openmvg_build && cd ${TMP}/openmvg_build && \
  cmake -DCMAKE_BUILD_TYPE=RELEASE . ../openmvg/src -DCMAKE_INSTALL_PREFIX=/opt/openmvg && \
  make -j4  && \
  make install

# Install eigen
git clone https://gitlab.com/libeigen/eigen.git --branch 3.4 ${TMP}/eigen && \
  mkdir ${TMP}/eigen_build && cd ${TMP}/eigen_build && \
  cmake . ../eigen && \
  make -j4 && \
  make install 

# Get vcglib
git clone https://github.com/cdcseacave/VCG.git ${TMP}/vcglib

# Install ceres solver
git clone https://ceres-solver.googlesource.com/ceres-solver ${TMP}/ceres_solver && \
  mkdir ${TMP}/ceres_build && cd ${TMP}/ceres_build && \
  cmake . ../ceres_solver/ -DMINIGLOG=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF && \
  make -j4 && \
  make install

# Install openmvs
git clone https://github.com/cdcseacave/openMVS.git ${TMP}/openmvs && \
  cd openmvs && git checkout tags/v2.1.0 && cd .. && \
  mkdir ${TMP}/openmvs_build && cd ${TMP}/openmvs_build && \
  cmake . ../openmvs -DCMAKE_BUILD_TYPE=Release -DVCG_DIR="../vcglib" -DCMAKE_INSTALL_PREFIX=/opt/openmvs && \
  make -j4 && \
  make install

echo 'Add following to your .bashrc file to add commands to your PATH'
echo 'PATH=/opt/openmvs/bin/OpenMVS:/opt/openmvg/bin:$PATH'