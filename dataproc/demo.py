from typing import Any, List
from pyspark.sql import SparkSession, SQLContext, Row
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

def do_inference(r: Row, fields: List[str], jt_dict: Any, target: str) -> Row:
  def get_evidence(name):
    ev = EvidenceBuilder() \
      .with_node(jt.get_bbn_node_by_name(name)) \
      .with_evidence(r[name], 1.0) \
      .build()
    return ev

  jt = get_jt(jt_dict)
  evidences = [get_evidence(n) for n in fields if n != target and pd.notna(r[n])]
  jt.update_evidences(evidences)

  posteriors = jt.get_posteriors()
  rhs = {f'{target}_{v}': p for v, p in posteriors[target].items()}
  lhs = {n: r[n] for n in fields}
  m = {**lhs, **rhs}

  row = Row(**m)
  return row

spark = SparkSession \
        .builder \
        .appName('Py-BBN Inference Demo') \
        .config('gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar') \
        .config('temporaryGcsBucket', 'pybbn') \
        .config('viewsEnabled', 'true') \
        .config('materializationDataset', 'pybbn') \
        .getOrCreate()
sqlContext = SQLContext(spark)

sql = '''SELECT *
FROM `vangjee.pybbn.covid`
LIMIT 100
'''
df = spark.read.format('bigquery').load(sql)

fields = df.columns
jt_dict = get_jt_dict()

rdd = df.rdd.map(lambda r: do_inference(r, fields, jt_dict, 'covid'))

output = sqlContext.createDataFrame(rdd, verifySchema=False, samplingRatio=1.0)
output.write \
    .format('bigquery') \
    .mode('overwrite') \
    .save('vangjee.pybbn.covid_inference')