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

ifeq ($(CONTAINER_TOOL),)
  $(info CONTAINER_TOOL unset, checking if docker is present...)
  ifneq ($(shell which docker 2> /dev/null),)
    $(info Using docker for build...)
    CONTAINER_TOOL := docker
  else ifneq ($(shell which podman 2> /dev/null),)
    $(info Using podman for build...)
    CONTAINER_TOOL := podman
  endif
endif

.PHONY: all setup
all: Dockerfile setup
	$(CONTAINER_TOOL) build . -t texasinstruments/processor-sdk-doc \
		$(BUILD_ARGS)

setup: requirements.txt

requirements.txt:
	cp -ar ../requirements.txt .
