{%- set domainNameNormalized = values.identifier.split(".")[0] | replace(r/[^\w]/g, "") %}
{%- set dataProductNameNormalized = values.identifier.split(".")[1] | replace(r/[^\w]/g, "") %}
{%- set dataProductMajorVersion = values.identifier.split(".")[2] | replace(r/[^\w]/g, "") %}
{%- set componentNameNormalized = values.identifier.split(".")[3] | replace(r/[^\w]/g, "") %}

### Component Metadata

| Field name              | Example value                  |
|:------------------------|:-------------------------------|
| **Name**                | ${{ values.name }}             |
| **Description**         | ${{ values.description }}      |
| **Domain**              | ${{ values.domain }}           |
| **Data Product**        | ${{ values.dataproduct }}      |
| **_Identifier_**        | ${{ values.identifier }}       |
| **_Development Group_** | ${{ values.developmentGroup }} |

## Glue job

### Infrastructure

| Field name             | Example value                                                          | Description                                                               |
|:-----------------------|:-----------------------------------------------------------------------|:--------------------------------------------------------------------------|
| **Region**             | ${{values.region}}                                                     | The AWS region where the resources are deployed.                          |
| **Worker Type**        | ${{values.workerType}}                                                 | The type of worker nodes to use for execution.                            |
| **Number of Workers**  | ${{values.numberOfWorkers}}                                            | The number of worker nodes allocated for the task.                        |
| **Execution Class**    | {% if values.isFlex == true %} FLEX {% else %} STANDARD {% endif %}    | The class of execution, e.g., FLEX for cost-optimized or STANDARD.        |

### Authorization

| Field name             | Example value                         | Description                                                               |
|:-----------------------|:--------------------------------------|:--------------------------------------------------------------------------|
| **IAM Role**           | ${{ values.iamRole }}                    | The ARN of the IAM role used for execution permissions.                   |

### Job

| Field name             | Example value                         | Description                                                               |
|:-----------------------|:--------------------------------------|:--------------------------------------------------------------------------|
| **Script Name**        | ${{ values.scriptName}}               | The name of the script to be executed.                                    |
| **Timeout**            | ${{ values.timeout }}                 | The maximum time (in seconds) allowed for the task to run.                |

### Glue Catalog

| Field name             | Example value                         | Description                                                               |
|:-----------------------|:--------------------------------------|:--------------------------------------------------------------------------|
| **Warehouse Location** | ${{ values.warehouseLocation }}       | The base location in S3 where the warehouse data is stored.               |
| **Catalog Name**       | ${{ values.catalogName }}             | The name of the AWS Glue Data Catalog used for metadata storage.          |

### Job Parameters

The *Glue Job Tech Adapter* automatically attaches a number of default [parameters](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html) to the Glue Job instance.
Additionaly you can specify other parameters, which will be appended to the default ones, potentially overriding them.

**Default parameters**

| Key                                  | Value                                                                                     |
|:-------------------------------------|:------------------------------------------------------------------------------------------|
| **--conf**                           | spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions    |
| **--conf**                           | spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO                 |
| **--conf**                           | spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog                      |
| **--conf**                           | spark.sql.catalog.glue_catalog.warehouse=`warehouseLocation`                              |
| **--conf**                           | spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog       |
| **--conf**                           | spark.sql.defaultCatalog=glue_catalog                                                        |
| **--datalake-formats**               | iceberg                                                                                   |
| **--enable-job-insights**            | true                                                                                      |
| **--enable-metrics**                 | true                                                                                      |
| **--enable-continuous-cloudwatch-log** | true                                                                                      |
| **--job-language**                   | python                                                                                    |
| **--enable-spark-ui**                | true                                                                                      |