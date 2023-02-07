# Notes

```
gcloud dataproc batches submit pyspark demo.py \
  --properties=spark.driver.cores=4,park.executor.cores=4,spark.executor.instances=20,spark.dynamicAllocation.initialExecutors=20,spark.dynamicAllocation.minExecutors=10,spark.dynamicAllocation.maxExecutors=20,spark.dataproc.driver.disk.size=250g,spark.dataproc.executor.disk.size=250g \
  --batch=pybbn-demo \
  --container-image=gcr.io/vangjee/pybbn \
  --region='us-central1' \
  --deps-bucket=gs://pybbn \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar \
  --history-server-cluster=projects/vangjee/regions/us-central1/clusters/mutipurpose-phs-cluster
  

gcloud dataproc batches describe pybbn-demo
gcloud dataproc batches cancel pybbn-demo --region=us-central1
gcloud dataproc batches delete pybbn-demo --region=us-central1
```