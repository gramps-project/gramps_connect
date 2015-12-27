# Gramps Connect

Gramps Connect is a web-based application for genealogy. It uses the Gramps API for data, reports, import/export, etc.

* Designed for collaboration and large databases
* Multi-user, password protected
* Support IIIF Image Server API - http://iiif.io/api/image/2.1/

Requirements
------------

* Python3
* tornado
* PIL
* gramps >= 5.0

Running
-------

```shell
python3 -m gramps_connect.app --database="My Family Tree"
```

Common Flags
------------

* --debug
* --port
* --hostname
* --database
* --sitename

Common variations
-----------------

```shell
PYTHONPATH=/path/to/gramps python3 -m gramps_connect.app

python3 -m gramps_connect.app --help

python3 -m gramps_connect.app --debug=True --base_dir=/path/to/templates
```
