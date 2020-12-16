# Overstroomik helm-chart

Here you find the helm chart to install overstroomik webservice and geoserver in a kubernetes cluster.

## Installation

You need [helm3](https://helm.sh/docs/intro/install/) to install this chart. To install overstroom run the following command.

    helm install <name> <path to overstroomik helm chart>
    
## Configuration

You can configure the installation by adjusting the values.yaml or by providing your own configuration. All values missing in your own configuration file will be used from the default values.yaml. The --values option in the helm install command can be used to provide your own configuration file:

    helm install --values <path to config.yaml> <name> <path to overstroomik helm chart>

### configartion options

The following options are available in the values.yaml

- replicacount on top of the values specifies the number of pods for bot backend and geoserver if autoscaling is not enabled
- Use the images section to specify the docker image for backend and geoserver.
- In the geoserver section autoscaling can be enabled based on either CPU or Memory usage
- In the backend section autoscaling can be enabled based on either CPU or Memory usage. Also two environment variables are required for the backend. Note that the GEOSERVER_URL should match the name of geoserver deploymend. In the next example "overstroomik-geoserver" in GEOSERVER_URL refers to the geoserver name.


        geoserver:
            name: "overstroomik-geoserver"
        backend:
            environment_variables:
                GEOSERVER_URL: http://overstroomik-geoserver:8080/geoserver

- In the ingress section a name should be provided. This name is visible in the kubernetes cluster. The host is specifies the url of the application and in services sections ingress for both Geoserver and Backend is defined. Note that the names of these services refer to the names defined in the geoserver and backend section. These should match.

## Deployment

Installing this chart will give you the following installation in the kubernetes cluster:

 - Geoserver deployment
 - Backend deployment
 - Geoserver service
 - Backend service
 - Geoserver Horizontal Pod Autoscaler (if enabled in values.yaml)
 - Backend Horizontal Pod Autoscaler (if enabled in values.yaml)
 - ingress for both Geoserver and Backend

Check deployment, Conto

    kubectl get pods

Check service:

    kubectl get service

Check Horizontal Pod Autoscaler

    kubectl get hpa

Check ingress

    kubectl get ingress

If ingress is correctly configured and deployment is succesful, the follwing urls should be available:

- <ingress_url>/by_location?latitude=52.017825&longitude=4.3359123

example output:

    {
        "webservice": {
            "status": "No error",
            "version": "1.0.0"
        },
        "location": {
            "search_field": null,
            "latitude": 52.01759004,
            "longitude": 4.33613331,
            "rd_x": 82851.006,
            "rd_y": 448214.677,
            "address": "Haantje",
            "municipality": "Rijswijk",
            "zipcode": "2288CX"
        },
        "data": {
            "flood_type": "binnen dijkring, mogelijk overstroombaar",
            "maximum_water_depth": 0.0,
            "probability_of_flooding": "middelgrote kans: 1/30 tot 1/300 per jaar",
            "evacuation_percentage": 12.0,
            "safety_board_id": 15
        }
    }


Webservice.status = "No error" is the important output to look at.

- <ingress_url>/geoserver/overstroomik/wms?service=WMS&version=1.1.0&request=GetMap&layers=overstroomik%3Aadministratieve_grenzen_veiligheidsregios&bbox=634.5732789819012%2C306594.5543000576%2C284300.0254094796%2C636981.7698870874&width=659&height=768&srs=EPSG%3A28992&styles=&format=image%2Fpng

This should respond with an image of the Netherlands.



