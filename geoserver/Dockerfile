FROM oscarfonts/geoserver:2.23.0

# These last 2 images are not always up to date so we do an extra update step
#  update and cleanup
RUN apt-get update && apt-get -y upgrade && apt-get clean && rm -rf /var/lib/apt/lists/*

# H2 Extension
RUN rm /usr/local/geoserver/WEB-INF/lib/h2-1.1.119.jar
RUN rm -rf /usr/local/tomcat/webapps.dist/*

COPY data_dir/ /var/local/geoserver
