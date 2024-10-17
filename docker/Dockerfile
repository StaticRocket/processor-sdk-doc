# SPDX-License-Identifier: GPL-2.0

# Copyright (C) 2024 Randolph Sapp
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <https://www.gnu.org/licenses/>.

FROM debian:stable-slim

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y \
		--no-install-recommends \
		dumb-init \
		git \
		gosu \
		make \
		python3-pip \
		ripgrep \
		zip \
	&& echo "**** create abc user and make our folders ****" \
	&& useradd -u 1000 -U -d /config -s /bin/false abc \
	&& usermod -G users abc \
	&& mkdir /build && chown abc:abc /build \
	&& mkdir /config && chown abc:abc /config \
	&& echo "**** cleanup ****" \
	&& apt-get autoremove \
	&& apt-get clean \
	&& rm -rf \
		/tmp/* \
		/var/cache/debconf/*-old \
		/var/lib/apt/lists/* \
		/var/lib/dpkg/status-old \
		/var/lib/sgml-base/supercatalog.old \
		/var/log/apt/term.log \
		/var/tmp/*

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
	python3 -m pip install -r /tmp/requirements.txt --no-cache-dir \
		--break-system-packages

COPY root/ /

WORKDIR /build
VOLUME /build

ENTRYPOINT ["/init"]
CMD ["/bin/bash"]
