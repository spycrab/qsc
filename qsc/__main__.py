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
import zipfile

import yaml

import qsc
from qsc.download import download_release, download_file
from qsc.extract import extract_release
from qsc.postprocess import postprocess_dir
from qsc.requirements import check_requirements, is_jom_present

def parse_args():
    parser = argparse.ArgumentParser(description="QSC builds your own custom Qt")
    parser.add_argument("--cache", dest="use_cache", action="store_true")
    parser.add_argument("--no-cache", dest="use_cache", action="store_false")
    parser.add_argument("--jom", dest="use_jom", action="store_true")
    parser.add_argument("--no-jom", dest="use_jom", action="store_false")
    parser.add_argument("--continue", dest="do_continue", action="store_true")
    parser.add_argument("--mirror", dest="mirror", default="https://download.qt.io/")
    parser.add_argument("manifest")

    parser.set_defaults(use_cache=True, use_jom=True, do_continue=False)

    args = parser.parse_args()

    qsc.USE_CACHE = args.use_cache
    qsc.USE_JOM = args.use_jom
    qsc.REPO_BASE_URL = args.mirror
    
    return args

def install_jom():
    if os.path.isfile(os.path.join("jom", "jom.exe")):
        return

    if not os.path.isdir("jom"):
        os.mkdir("jom")

    os.chdir("jom")

    url = qsc.REPO_JOM_PATH.format(qsc.REPO_BASE_URL)

    download_path = "jom.zip"

    download_file(url, download_path)

    with zipfile.ZipFile(download_path, "r") as zip:
        zip.extract("jom.exe")
        
    os.remove("jom.zip")
    os.chdir("..")
        
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

    if qsc.USE_JOM and qsc.is_windows():
        if not is_jom_present():
            print("Jom not present, using own...")
            install_jom()
            os.putenv("PATH", os.environ["PATH"]+";"+os.path.join(os.getcwd(), "jom"))

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
        os.putenv("USE_VS", "1")
    else:
        print("Unknown compiler '{}'".format(compiler.name))
        exit(1)
    
    output_path = os.path.join(basedir, "dist", config["name"]+"_"+release)
    
    os.putenv("RELEASE", release)
    os.putenv("OUTNAME", output_path)
    
    platform = ""
    
    # Platform
    if config.get("cross", False) == "true":
        platform = "-xplatform "+config["platform"]+ " -external-hostbindir "+config["hostbindir"]
    elif config.get("platform", False):
        platform = "-platform "+config["platform"]

    os.putenv("QT_PLATFORM", platform)
    
    os.putenv("USE_JOM", str(int(qsc.USE_JOM and compiler["name"] == "visual_studio")))
    
    # Config options
    
    configure = config["configure"]
    
    configure_options = ""
    
    # Use mp if we're not using jom
    if not args.use_jom and compiler["name"] == "visual_studio":
        configure_options += " -mp"
    
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