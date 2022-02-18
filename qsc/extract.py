# QSC (Qt SDK Creator) - A tool for automatically downloading, building and stripping down Qt
# Copyright (C) 2020 spycrab0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Extracting archives and stuff"""

import os
import tarfile

import qsc

def extract_release(release):
    name = "qt-everywhere-src-{}".format(release)

    tar_path = os.path.join("archives", name+".tar.xz")
    
    print("Extracting...", end="", flush=True)
    
    if qsc.USE_CACHE and os.path.isdir(name):
        print("Cached")
        return
    
    with tarfile.open(tar_path) as tar:
        tar.extractall(".")

    print("Done")
