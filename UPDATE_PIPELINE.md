## Pipeline Source Update Required

The error occurred because `CodePipelineSource.directory()` is no longer a valid method in AWS CDK Pipelines. The code has been updated to use `CodePipelineSource.gitHub()` instead.

To make this work:

1. Replace "your-github-username" in the code with your actual GitHub username
2. Make sure your repository is hosted on GitHub
3. If this is a private repository, you should use `CodePipelineSource.connection()` instead and set up a GitHub connection in AWS CodeStar

Example for private repositories:
```python
input=cdk.pipelines.CodePipelineSource.connection(
    "your-github-username/serverless-deployment",
    "main",
    connection_arn="arn:aws:codestar-connections:region:account:connection/xxxxx"
)
```

You'll need to:
1. Create a connection in AWS CodeStar Connections
2. Update the connection ARN in the code
3. Make sure the connection is in "Available" status