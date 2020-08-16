## qsc

Qt SDK Creator - A tool for automatically downloading, building and stripping down Qt

## Examples

See the ``examples`` folder.

## Usage

[Python](https://www.python.org) and [Perl](http://strawberryperl.com) must be installed manually.

The compiler to use must be manually installed prior to using qsc. Currently this means Visual Studio should be installed. `compiler` in the manifest specifies which exact version of VS to use.

Install python packages required for qsc:
```
py -m pip install -r requirements.txt
```

See the [definition of `REPO_BASE_URL` and `REPO_SRC_PATH`](qsc/__init__.py) for where qsc will pull the Qt sources from. You can browse these URLs and discover available versions to place in the manifest `release` tag.

Compose a manifest file describing the build to perform. See [examples folder](examples) for previously-used manifests.

To run the build, point python to the [qsc directory](qsc) as a module:
```
py -m qsc manifest.yml
```

NOTE: For an out-of-tree build, you need to place the qsc repository in the python path. For example:
```
set PYTHONPATH=c:\src\qsc
```

## Resolving "ERROR: Building QtQml requires Python"

If your manifest dictates that QtQml should be built, the build will try to find and execute `python`. This can be problematic as `python` will always exist in the `%PATH%`, but may be a dummy which prompts to install python from the Windows Store (even if you have some other instance of python installed).

To workaround, find your working python install directory:
```
py -c "import os,sys; print([x for x in sys.path if os.path.basename(x).startswith('python') and os.path.basename(x).endswith('zip')])"
```

Then, prefix this to `%PATH%` in your current shell.

For example:
```
set PATH=%LOCALAPPDATA%\Programs\Python\Python37;%PATH%
```

## License

This program is licensed under the GNU General Public License v3 (or later).  
See [LICENSE](LICENSE).