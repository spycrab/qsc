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


"""All the download related stuff goes here"""

from pathlib import Path
import qsc
import requests
import shutil

def source_url(release):
    base_release = release[:release.rfind('.')]
    return qsc.REPO_SRC_PATH.format(qsc.REPO_BASE_URL, base_release, release)

def download_file(url, path):
    with requests.get(url, stream=True) as request:
        with open(path, "wb") as file:
            shutil.copyfileobj(request.raw, file)

def download_release(release):
    url = source_url(release)
    archive_dir = Path("archives")
    download_path = archive_dir / f"qt-everywhere-src-{release}.tar.xz"

    print(f"Downloading Qt {release}...", end="", flush=True)

    archive_dir.mkdir(exist_ok=True)

    if qsc.USE_CACHE and download_path.is_file():
        print("Cached")
        return

    download_file(url, download_path)

    print("Done")
