from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Intro to Spark').master("local[*]").getOrCreate()
sc = spark.sparkContext

#############################################

import pandas as pd
import numpy as np
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")
from pyspark.sql.functions import round, expr, from_unixtime, unix_timestamp, date_format, count, concat, lit, col
from pyspark.sql.types import IntegerType
from IPython.core.display import HTML

base_path = "/home/jovyan/work"
csv_path = os.path.join(base_path, 'data/taxis.csv')

taxis_df = spark.read.format("csv").option("inferSchema", "true")\
                .option("timestampFormat","yyyy-MM-dd HH:mm:ss")\
                .option("header", "true")\
                .option("mode", "DROPMALFORMED")\
                .load(csv_path)

taxis_df = taxis_df.coalesce(32)
print(taxis_df.show(5))