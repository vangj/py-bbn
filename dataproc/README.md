# Notes

```
gcloud dataproc batches submit pyspark demo.py \
  --batch=pybbn-demo \
  --container-image=gcr.io/vangjee/pybbn \
  --region='us-central1' \
  --deps-bucket=gs://pybbn \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar
```