# Local Source Pipeline Update

The error occurred because `CodePipelineSource.directory()` is no longer a valid method in AWS CDK Pipelines. For local development, we should use `CodePipelineSource.connection()`.

The pipeline has been updated to use:
```python
input=cdk.pipelines.CodePipelineSource.connection(
    "local-source",
    "main",
    connection_arn="arn:aws:codestar-connections:region:account:connection/dummy"
)
```

To make this work locally:

1. Initialize your local Git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a CodeStar connection in AWS Console:
   - Go to Developer Tools > Settings > Connections
   - Create a connection (can be to any provider as we're using local source)
   - Copy the connection ARN

3. Update the code:
   - Replace the connection_arn with your actual connection ARN
   - Replace "region" and "account" with your AWS region and account ID

This configuration allows you to use AWS CodePipeline with a local Git repository without requiring GitHub hosting.