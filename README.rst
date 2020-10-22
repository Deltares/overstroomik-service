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

Running in a Kubernets cluster
==============================

A helm chart is available to install Overstroomik in a Kubernetes cluster::

    helm install overstroomik helm/overstroomik

By default ingress is disabled. port-forward can be used to access the pods in your local cluster. First get the name of the deployed pod::
    kubectl get pods

Create port-forward to access the pod from localhost. Geoserver is running on port 8080 and the backend on 80::
    kubectl port-forward <podname> <local port>:<pod port>

Ingress and autoscaling can be enabled in helm/values.yaml. Update the installation with changed configuration::
    helm upgrade overstroomik helm/overstroomik

Delete the instalation::
    helm delete overstroomik


