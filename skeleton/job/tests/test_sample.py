import os
import boto3
import subprocess  # nosec B404
from src.main import transform
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType


SOURCE_NAME = "raw"
TABLE_NAME = "movies"
S3_BUCKET_NAME = "data-s3"
ENDPOINT_URL = "http://127.0.0.1:5000/"


def initialize_test(spark: SparkSession):
    """
    Function to setup and initialize test case execution

    Args:
        spark (SparkSession): PySpark session object

    Returns:
        process: Process object for the moto server that was started
    """
    process = subprocess.Popen(  # nosec B607
        "/home/glue_user/.local/bin/moto_server -p5000",
        stdout=subprocess.PIPE,
        shell=True,  # nosec B602
        preexec_fn=os.setsid,
    )

    s3 = boto3.resource(  # nosec B106
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id="FakeKey",
        aws_secret_access_key="FakeSecretKey",
        aws_session_token="FakeSessionToken",
        region_name="us-east-1",
    )
    s3.create_bucket(
        Bucket=S3_BUCKET_NAME,
    )

    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", "dummy-value")
    hadoop_conf.set("fs.s3a.secret.key", "dummy-value")
    hadoop_conf.set("fs.s3a.endpoint", ENDPOINT_URL)
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

    values = [
        (1, "Harry Potter and the Philosopher's Stone", "Fantasy", "1997-06-26"),
        (2, "Dune", "Science Fiction", "1965-08-01"),
        (3, "Pride and Prejudice", "Romance", "1813-01-28"),
        (4, "1984", "Dystopian", "1949-06-08"),
        (5, "The Great Gatsby", "Literary Fiction", "1925-04-10"),
        (6, "Murder on the Orient Express", "Mystery", "1934-01-01"),
        (7, "The Hobbit", "Fantasy", "1937-09-21"),
    ]

    schema = StructType(
        [
            StructField("id", LongType(), False),
            StructField("name", StringType(), False),
            StructField("genre", StringType(), False),
            StructField("release_date", StringType(), False),
        ]
    )

    df = spark.createDataFrame(values, schema)

    df.write.parquet(f"s3://{S3_BUCKET_NAME}/{SOURCE_NAME}")
    return process


def compare_schema(schema_a: StructType, schema_b: StructType) -> bool:
    """
    Utility method to compare two schema and return the results of comparison

    Args:
        schema_a (StructType): Schema for comparison
        schema_b (StructType): Schema for comparison

    Returns:
        bool: Result of schema comparison
    """
    print(schema_a)
    print(schema_b)
    return len(schema_a) == len(schema_b) and all(
        (a.name, a.dataType) == (b.name, b.dataType) for a, b in zip(schema_a, schema_b)
    )


# Test to verify data transformation
def test_transform(glueContext: GlueContext):
    """
    Test case to test the transform function

    Args:
        glueContext (GlueContext): Test Glue context object
    """
    spark = glueContext.spark_session
    input_data = spark.createDataFrame(
        [(1, "Harry Potter and the Philosopher's Stone", "Fantasy", "1997-06-26")],
        ["id", "name", "genre", "release_date"],
    )
    output_schema = StructType(
        [
            StructField("id", LongType(), False),
            StructField("name", StringType(), False),
            StructField("genre", StringType(), False),
            StructField("release_date", StringType(), False),
            StructField("release_year", IntegerType(), False),
            StructField("release_month", IntegerType(), False),
            StructField("release_dayofmonth", IntegerType(), False),
        ]
    )
    real_output = transform(spark, input_data)
    assert compare_schema(real_output.schema, output_schema)  # nosec assert_used
