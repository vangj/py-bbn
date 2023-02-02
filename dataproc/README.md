# Notes

```
gcloud dataproc batches submit pyspark demo.py \
  --properties=spark.driver.cores=4 \
  --properties=spark.executor.cores=4 \
  --properties=spark.executor.instances=20 \
  --properties=spark.dynamicAllocation.initialExecutors=20 \
  --properties=spark.dynamicAllocation.minExecutors=10 \
  --properties=spark.dynamicAllocation.maxExecutors=20 \
  --batch=pybbn-demo-3 \
  --container-image=gcr.io/vangjee/pybbn \
  --region='us-central1' \
  --deps-bucket=gs://pybbn \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar

gcloud dataproc batches describe pybbn-demo-3
gcloud dataproc batches cancel pybbn-demo-3 --region=us-central1
gcloud dataproc batches delete pybbn-demo-3 --region=us-central1
```