import sys
from pyspark.sql import SparkSession, DataFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, year, month, dayofmonth
from pyspark.context import SparkContext


def read_data_from_s3(spark: SparkSession, sourcePath):
    """
    Function to read data from a data source

    Args:
        spark (SparkSession): PySpark session object
        sourcePath (String): S3 path

    Returns:
        DataFrame: Dataframe object containing the data after transform

    """
    df = spark.read.parquet(f"{sourcePath}")
    return df


def transform(spark: SparkSession, df: DataFrame) -> DataFrame:
    """
    Function to extract and transform dataframe columns with date
    to get day, month and year.

    Args:
        spark (SparkSession): PySpark session object
        df (DataFrame): Dataframe object containing the data before transform

    Returns:
        DataFrame: Dataframe object containing the data after transform
    """
    return (
        df.withColumn("release_year", year(col("release_date")))
        .withColumn("release_month", month(col("release_date")))
        .withColumn("release_dayofmonth", dayofmonth(col("release_date")))
    )


def write_to_iceberg(spark: SparkSession, df, catalog, database, table):
    """
    Function to write data on a destination

    Args:
        spark (SparkSession): PySpark session object
        df (DataFrame): Dataframe object containing the data before transform
        table_name (String): Iceberg table where data will be appended

    """

    # Create the database if it doesn't exist
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog}.{database}")

    # SQL to create the Iceberg table in Glue Catalog
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {catalog}.{database}.{table} (
        id INT,
        name STRING,
        genre STRING,
        release_date STRING,
        release_year STRING,
        release_month STRING,
        release_dayofmonth STRING
    )
    USING iceberg
    PARTITIONED BY (genre)
    """

    # Execute SQL to create the table
    spark.sql(create_table_sql)

    df.write.format("iceberg").mode("append").save(f"{catalog}.{database}.{table}")


def pipeline(spark: SparkSession, source_path, catalog, database, table):
    """
    Function to model the pipeline
    """

    df = read_data_from_s3(spark, source_path)
    df_transformed = transform(spark, df)
    write_to_iceberg(spark, database, df_transformed, catalog, database, table)


if __name__ == "__main__":

    args = getResolvedOptions(
        sys.argv, ["JOB_NAME", "SOURCE_PATH", "GLUE_CATALOG", "GLUE_DATABASE"]
    )

    # catalog and database names are provided by Witboost as job parameters
    # this is where you can create tables
    catalog = args["GLUE_CATALOG"]
    database = args["GLUE_DATABASE"]

    table = "movies"

    # Initialize Job
    glueContext = GlueContext(SparkContext.getOrCreate())
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)

    # Start pipeline
    pipeline(spark, database, args["source_path"], catalog, database, table)

    job.commit()
