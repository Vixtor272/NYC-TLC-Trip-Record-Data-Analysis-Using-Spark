FROM jupyter/pyspark-notebook:latest

USER root
RUN apt-get update && apt-get install -y build-essential curl
# Python deps
RUN pip install --no-cache-dir requests python-dotenv snowflake-connector-python pyarrow
# Si quieres usar spark-snowflake connector, agregar los jars apropiados:
# COPY /path/to/spark-snowflake_2.12-<ver>.jar /opt/spark/jars/
USER jovyan
