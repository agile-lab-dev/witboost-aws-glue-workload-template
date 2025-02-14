# "Raw data processor"

- [Overview](#overview)
- [Usage](#usage)

## Overview

Deploy this component to create a Glue Job to run your spark workload.

Refer to the [Witboost Starter Kit repository](https://github.com/agile-lab-dev/witboost-starter-kit) for information on the Tech Adapter that can be used to deploy components created with this Template.

### What's a Workload

Workload refers to any data processing step (ETL, job, transformation etc.) that is applied to data in a Data Product. Workloads can pull data from sources external to the Data Mesh or from an Output Port of a different Data Product or from Storage Areas inside the same Data Product, and persist it for further processing or serving.

### Glue Job

AWS Glue is a serverless data integration service that makes it easy for analytics users to discover, prepare, move, and integrate data from multiple sources. You can use it for analytics, machine learning, and application development. 
It also includes additional productivity and data ops tooling for authoring, running jobs, and implementing business workflows.

### Job implementation

This template offers you a scaffold to develop the logic of your glue job. The `job` folder is your starting point. Some important info:

### Job CI/CD

The CI/CD prepared for this repo contains two main steps:
- Testing: linting and tests are performed against the `job` folder
- Deploy: the `job/main.py` script is published in the target S3 container

## Git hooks

Hooks are programs you can place in a hooks directory to trigger actions at certain points in git’s execution. Hooks that don’t have the executable bit set are ignored.

The hooks are all stored in the hooks subdirectory of the Git directory. In most projects, that’s .git/hooks.

Out of the many available hooks supported by Git, we use pre-commit hook in order to check the code changes before each commit. If the hook returns a non-zero exit status, the commit is aborted.

### Available hooks

The `git-hooks` folder contains hooks that will help your development experience. Run the below command to install the configured hooks. Pre-commit will then run on every commit.

```bash
pre-commit install
```

## Usage

To get information on how to use this template, refer to this [document](./docs/index.md).