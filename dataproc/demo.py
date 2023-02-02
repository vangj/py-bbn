from typing import Any, List
from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pybbn.graph.dag import Bbn
from pybbn.graph.jointree import JoinTree, EvidenceBuilder
from pybbn.pptc.inferencecontroller import InferenceController
from google.cloud import storage
import json
import pandas as pd


def get_bbn_dict() -> Any:
  client = storage.Client()
  bucket = client.get_bucket('pybbn')
  blob = bucket.blob('covid-bbn.json')
  data = blob.download_as_string()
  return json.loads(data)

def get_jt_dict() -> Any:
  client = storage.Client()
  bucket = client.get_bucket('pybbn')
  blob = bucket.blob('covid-jt.json')
  data = blob.download_as_string()
  return json.loads(data)

def get_bbn(d=None) -> Bbn:
  if d is None:
    bbn = Bbn.from_dict(get_bbn_dict())
  else:
    bbn = Bbn.from_dict(d)
  return bbn

def get_jt(d=None) -> JoinTree:
  if d is None:
    jt = JoinTree.from_dict(get_jt_dict())
  else:
    jt = JoinTree.from_dict(d)
  jt = InferenceController.apply_from_serde(jt)
  return jt

def do_inference(r: Row, fields: List[str], target: str, jt_dict: Any = None, jt: JoinTree = None) -> Row:
  def get_evidence(name):
    ev = EvidenceBuilder() \
      .with_node(jt.get_bbn_node_by_name(name)) \
      .with_evidence(r[name], 1.0) \
      .build()
    return ev

  if jt is None:
    jt = get_jt(jt_dict)
  
  evidences = [get_evidence(n) for n in fields if n != target and pd.notna(r[n])]

  jt.unobserve_all()
  jt.update_evidences(evidences)

  posteriors = jt.get_posteriors()
  rhs = {f'{target}_{v}': p for v, p in posteriors[target].items()}
  lhs = {n: r[n] for n in fields}
  m = {**lhs, **rhs}

  row = Row(**m)
  return row

print('starting')
spark = SparkSession \
        .builder \
        .appName('Py-BBN Inference Demo') \
        .config('gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar') \
        .config('temporaryGcsBucket', 'pybbn') \
        .config('viewsEnabled', 'true') \
        .config('materializationDataset', 'pybbn') \
        .getOrCreate()
sqlContext = SQLContext(spark)

print('reading in SQL data')
sql = '''SELECT *
FROM `vangjee.pybbn.covid`
'''
df = spark.read.format('bigquery').load(sql)

fields = df.columns

print('acquiring join tree dictionary')
jt_dict = get_jt_dict()

print('acquiring join tree')
jt = get_jt(jt_dict)

print('creating rdd')
rdd = df \
  .rdd \
  .repartition(80) \
  .map(lambda r: do_inference(r, fields, 'covid', jt_dict, jt)) \
  .cache()

print(f'rdd count = {rdd.count()}')

print('getting target values')
target_values = rdd \
  .flatMap(lambda r: [(k, 1) for k, _ in r.asDict().items() if k.startswith('covid')]) \
  .reduceByKey(lambda a, b: a + b) \
  .sortByKey() \
  .map(lambda tup: tup[0]) \
  .collect()
print(f'target values: {target_values}')

print('creating schema')
struct_fields = [StructField(f, StringType(), True) for f in fields] + \
  [StructField(f, FloatType(), True) for f in target_values]
schema = StructType(struct_fields)
  

print('creating data frame')
output = sqlContext.createDataFrame(rdd, schema=schema)

print('persisting data frame')
output.write \
    .format('bigquery') \
    .mode('overwrite') \
    .save('vangjee.pybbn.covid_inference')

print('done')