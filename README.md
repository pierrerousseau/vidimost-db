Vidimost-db
===========

Application to store data.


Requirements
============

* git bash
* python 3
* virtualenv (pip)
* virtualenvwrapper / virtualenvwrapper-win (pip)
* doit (pip)


Start
=====

* (optional) source /usr/local/bin/virtualenvwrapper_lazy.sh
* mkvirtualenv vidimost-db / workon vidimost-db
* doit install
* (optional) doit docker_build


Launch
======

* doit list
    * doit uvicorn
    * doit mongo
        * doit mongo -p down
    * doit add-element -c 123 -v 456 -l "test"
    * doit list-elements
* once launched visit : http://localhost:8000
