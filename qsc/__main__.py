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


"""QSC Main module"""

import argparse
import os
from pathlib import Path

import yaml

import qsc
from qsc.download import download_release, download_file
from qsc.extract import extract_release
from qsc.postprocess import postprocess_dir
from qsc.requirements import check_requirements

def parse_args():
    parser = argparse.ArgumentParser(description="QSC builds your own custom Qt")
    parser.add_argument("--cache", dest="use_cache", action="store_true")
    parser.add_argument("--no-cache", dest="use_cache", action="store_false")
    parser.add_argument("--continue", dest="do_continue", action="store_true")
    parser.add_argument("--mirror", dest="mirror", default="https://download.qt.io/")
    parser.add_argument("manifest")

    parser.set_defaults(use_cache=True, do_continue=False)

    args = parser.parse_args()

    qsc.USE_CACHE = args.use_cache
    qsc.REPO_BASE_URL = args.mirror

    return args

if __name__ == "__main__":
    args = parse_args()

    print("qsc 0.1 (c) spycrab0\n")

    if not check_requirements():
        print("Not all requirements for building Qt are in PATH. Can't continue.")
        exit(1)

    basedir = os.getcwd()

    config = yaml.load(open(args.manifest, "r"), Loader=yaml.BaseLoader)

    release = config["release"]
    build_dir = release+"_"+config["name"]+".build"
    compiler = config["compiler"]

    download_release(release)
    extract_release(release)

    if os.path.isdir(build_dir):
        if not args.do_continue:
            print("Build directory already exists - aborting (specify --continue to ignore)")
            exit(1)
    else:
        os.mkdir(build_dir)

    os.chdir(build_dir)

    if compiler["name"] == "visual_studio":
        if not qsc.is_windows():
            print("Only supported on Windows!")
            exit(1)

        os.putenv("VS_VERSION", compiler["version"])
        os.putenv("VS_EDITION", compiler["edition"])
        os.putenv("VCVARSALL", compiler.get("vcvarsall", ""))
        os.putenv("USE_VS", "1")
    else:
        print("Unknown compiler '{}'".format(compiler.name))
        exit(1)

    output_path = os.path.join(basedir, "dist", config["name"]+"_"+release)
    os.makedirs(output_path, exist_ok=True)

    os.putenv("RELEASE", release)
    os.putenv("OUTNAME", output_path)

    # Platform
    platform = config.get("platform")
    if platform is not None:
        os.putenv("QT_PLATFORM", "-platform "+platform)

    host_path = config.get("host_path")
    if host_path is not None:
        host_path = "-qt-host-path " + str(Path(host_path).resolve())
        os.putenv("QT_HOST_PATH", host_path)

    # Config options

    configure = config["configure"]

    configure_options = ""

    if configure:
        # -nomake
        for entry in configure.get("nomake", []):
            configure_options += " -nomake "+entry

        # -skip
        for entry in configure.get("skip", []):
            configure_options += " -skip "+entry

        # -feature / -no-feature
        for entry in configure.get("feature", []):
            value = configure["feature"][entry]
            if value == "true":
                configure_options += " -feature-" + entry
            else:
                configure_options += " -no-feature-" + entry

        # additional options
        if configure.get("additional_parameters", False):
            configure_options += " "+configure["additional_parameters"]

    os.putenv("QT_CONFIGURE_OPTIONS", configure_options)

    if qsc.is_windows():
        os.system(qsc.WINBUILD_PATH)
    else:
        print("Not supported yet, sorry :/")
        exit(1)

    # Post process output
    postprocess_dir(output_path, config.get("postprocess", {}))

    print("Done. Result in {}".format(output_path))