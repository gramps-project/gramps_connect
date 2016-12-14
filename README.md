As of 16th Decemember 2016 this version of gramps_connect remains experimental code. It was never actually released.

If anyone is interested in developing a web front-end for Gramps, then I would be happy to help.

See: https://github.com/gramps-project/gramps_connect/commit/80f1332a98055c3acf98d5212bf34f53653c7f8e

# Gramps Connect

Gramps Connect is an experiemental web-based application for genealogy. It uses the Gramps API for data, reports, import/export, etc.

Planned to be for:

* Collaboration and large databases
* Multi-user, password protected
* Support IIIF Image Server API - http://iiif.io/api/image/2.1/

Requirements
------------

* Python3
* tornado
* PIL
* gramps = to experimental "gep-033-select-api" branch only
* simplejson

Installation
-------------

Experimental installation information:

You will need to get the experimental "gep-033-select-api" branch for Gramps from github:

```shell
git clone --depth 1 https://github.com/gramps-project/gramps.git --branch geps/gep-033-select-api --single-branch gramps
cd gramps
python3 setup.py build
```

At that point you can run Gramps directly (using the Gramps.py program in the above folder) and use it for gramps_connect (see below).

You can also get gramps_connect from github:

```shell
git clone --depth 1 https://github.com/gramps-project/gramps_connect.git
cd gramps_connect
```

Running
-------

You can run gramps_connect directly from either the downloaded directory, or from the installed version.

Installed version:

```shell
python3 -m gramps_connect.app --config="familytree.conf"
```
Downloaded versions:

```shell
cd gramps_connect
PYTHONPATH=../gramps:. python3 -m gramps_connect.app --config="familytree.conf"
```

Where `familytree.conf` contains options and values, such as:

```python
port = 8000
database = "My Family Tree"
username = "demo"
```

If you do not provide `--password` (a crypt-based password) on the command-line or in the config file then a plaintext password will be interactively requested, and the crypt generated.

Options:
------------

* --database
* --username
* --password
* --debug
* --port
* --hostname
* --sitename
* --data_dir
* --home_dir
* --xsrf

Common variations
-----------------

```shell
PYTHONPATH=/path/to/gramps python3 -m gramps_connect.app --database="Smith Family" --username=demo

python3 -m gramps_connect.app --help

python3 -m gramps_connect.app --debug --base_dir=/path/to/templates --database="Smith Family" --username=demo
```
