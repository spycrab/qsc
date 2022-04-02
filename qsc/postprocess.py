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

"""Postprocess installation directory"""

import os
from pathlib import Path
import shutil
import re
import tarfile


def postprocess_dir(basedir, config):

    os.chdir(basedir)

    entries = [str(x) for x in Path(".").rglob("*")]

    # delete
    for delete in config.get("delete", []):
        delete = delete.replace("/", os.sep)
        if delete in entries:
            print("Deleting {}...".format(delete))

            entries.remove(delete)

            if os.path.isdir(delete):
                shutil.rmtree(delete)
            elif os.path.isfile(delete):
                os.remove(delete)

    # delete_regex
    for delete_regex in config.get("delete_regex", []):
        for e in entries:
            if not os.path.exists(e):
                continue

            if re.fullmatch(delete_regex, e):
                print("Deleting {} based on regex '{}'...".format(e, delete_regex))

                if os.path.isdir(e):
                    shutil.rmtree(e)
                elif os.path.isfile(e):
                    os.remove(e)

    if config.get('archive_pdbs', False):
        with tarfile.open('pdbs.tar.xz', 'w:xz') as archive:
            print('archiving pdbs...')
            for path in Path(".").rglob("*.pdb"):
                    print(path)
                    archive.add(path)
                    path.unlink()
