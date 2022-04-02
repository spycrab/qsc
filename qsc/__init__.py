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


import os
import platform

def is_windows():
    return platform.system() == "Windows"

# Paths
BASE_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_PATH, "data")

WINBUILD_PATH = os.path.join(DATA_PATH, "winbuild.bat")

# Settings
REPO_BASE_URL = "https://download.qt.io/"
REPO_SRC_PATH = "{0}/official_releases/qt/{1}/{2}/single/qt-everywhere-src-{2}.tar.xz"

USE_CACHE = True