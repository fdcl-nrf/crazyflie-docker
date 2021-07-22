# https://stackoverflow.com/a/63944890/7312249
FROM ubuntu:bionic

RUN : \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
	software-properties-common \
	&& add-apt-repository -y ppa:deadsnakes \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
	python3.8-venv \
	# https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/building-and-flashing/build/
	# CF: install a toolchain
	&& add-apt-repository -y ppa:team-gcc-arm-embedded/ppa \
	&& apt-get install -y gcc-arm-embedded make git \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& :

RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /build-firmware
