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

import qsc

def is_in_path(program):
    path_folders = os.getenv("PATH").split(os.pathsep)

    if qsc.is_windows():
        program += ".exe"

    for folder in path_folders:
        path = os.path.join(folder, program)

        if os.path.isfile(path):
           return True

    return False

def check_requirements():
    print("Requirements:\n")

    print("Perl - ", end="")

    success = True

    if not is_in_path("perl"):
        print("Not found")
        success = False
    else:
        print("Ok")

    print("Python (Optional) - ", end="")

    if not is_in_path("python"):
        print("Found")
    else:
        print("Ok")

    print("")

    return success
