# Notes

```
gcloud dataproc batches submit pyspark demo.py \
  --properties=spark.driver.cores=4,park.executor.cores=4,spark.executor.instances=20,spark.dynamicAllocation.initialExecutors=20,spark.dynamicAllocation.minExecutors=10,spark.dynamicAllocation.maxExecutors=20,spark.dataproc.driver.disk.size=250g,spark.dataproc.executor.disk.size=250g \
  --batch=pybbn-demo-3 \
  --container-image=gcr.io/vangjee/pybbn \
  --region='us-central1' \
  --deps-bucket=gs://pybbn \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar

gcloud dataproc batches describe pybbn-demo-3
gcloud dataproc batches cancel pybbn-demo-3 --region=us-central1
gcloud dataproc batches delete pybbn-demo-3 --region=us-central1
```