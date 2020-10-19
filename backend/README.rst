====================
overstroomik-service
====================


.. image:: https://travis-ci.com/Deltares/overstroomik-service.svg?branch=master
    :target: https://travis-ci.com/Deltares/overstroomik-service

.. image:: https://pyup.io/repos/github/Deltares/overstroomik-service/shield.svg
     :target: https://pyup.io/repos/github/Deltares/overstroomik-service/
     :alt: Updates



Kubernetes Deployment for overstroomik backend


* Free software: MIT license
* Documentation: https://overstroomik-service.readthedocs.io.

Installation
------------
pip install -r requirements_dev.txt

Running
-------
"make run" or "uvicorn overstroomik_service.main:app --reload"

Testing
-------
"make test" or "pytest"

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
