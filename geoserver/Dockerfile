FROM oscarfonts/geoserver:2.23.0

ENV GEOSERVER_DATA_DIR /var/local/overstroomik

# Make data directory
RUN mkdir ${GEOSERVER_DATA_DIR}

# Tomcat environment
ENV CATALINA_OPTS "-server -Djava.awt.headless=true \
	-Xms768m -Xmx1560m -XX:+UseConcMarkSweepGC -XX:NewSize=48m \
	-DGEOSERVER_DATA_DIR=${GEOSERVER_DATA_DIR}"

# These last 2 images are not always up to date so we do an extra update step
#  update and cleanup
RUN apt-get update && apt-get -y upgrade && apt-get clean && rm -rf /var/lib/apt/lists/*

# H2 Extension
RUN rm /usr/local/geoserver/WEB-INF/lib/h2-1.1.119.jar
RUN rm -rf /usr/local/tomcat/webapps.dist/*

# copy data to the geoserver folder
COPY data_dir/ ${GEOSERVER_DATA_DIR}

# tomcat user right for log
RUN chown -R tomcat:tomcat ${GEOSERVER_DATA_DIR}


