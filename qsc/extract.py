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

from pathlib import Path
import tarfile

import qsc

def extract_release(release):
    name = f"qt-everywhere-src-{release}"

    archive_path = Path("archives") / (name + ".tar.xz")

    print("Extracting...", end="", flush=True)

    if qsc.USE_CACHE and Path(name).is_dir():
        print("Cached")
        return

    with tarfile.open(archive_path) as f:
        f.extractall(".")

    print("Done")
