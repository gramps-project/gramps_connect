# gramps_connect

Gramps Connect is a web-based application for geneaology

Requirements
------------

* tornado
* gramps 5.0

Running
-------

```shell
python3 -m gramps_connect.app
```

Common variations
-----------------

```shell
PYTHONPATH=/path/to/gramps python3 -m gramps_connect.app

python3 -m gramps_connect.app --help

python3 -m gramps_connect.app --debug=True --base_dir=/path/to/templates
```
