# Local Source Pipeline Update

The error occurred because `CodePipelineSource.directory()` is no longer a valid method in AWS CDK Pipelines. For local development without GitHub, we should use `CodePipelineFileSource` instead.

The pipeline has been updated to use:
```python
input=cdk.pipelines.CodePipelineFileSource(".")
```

This configuration will use your local directory as the source for the pipeline, which is ideal for local development and testing scenarios where the code is not hosted in a remote repository.

Note: Make sure you have the latest version of AWS CDK installed to use this feature.