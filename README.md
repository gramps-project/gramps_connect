# gramps_connect

Gramps Connect is a web-based application for geneaology

Requirements
------------

* Python3
* tornado
* PIL
* gramps 5.0

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

Common variations
-----------------

```shell
PYTHONPATH=/path/to/gramps python3 -m gramps_connect.app

python3 -m gramps_connect.app --help

python3 -m gramps_connect.app --debug=True --base_dir=/path/to/templates
```
