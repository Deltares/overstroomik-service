====================
overstroomik-service
====================


.. image:: https://travis-ci.com/Deltares/overstroomik-service.svg?branch=master
    :target: https://travis-ci.com/Deltares/overstroomik-service

.. image:: https://pyup.io/repos/github/Deltares/overstroomik-service/shield.svg
     :target: https://pyup.io/repos/github/Deltares/overstroomik-service/
     :alt: Updates

Kubernetes Deployment for overstroomik backend

* backend folder for Python app
* etl folder for data migration and geoserver configuration
* geoserver folder for GeoServer installation

Running
=======

We make use of Docker and Docker-compose::

    docker-compose up -d

