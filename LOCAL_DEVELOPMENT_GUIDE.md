# Local Development Guide

For local development without GitHub or any remote repository, it's recommended to use direct CDK deployment instead of setting up a pipeline. The pipeline has been temporarily disabled in the code.

## Local Development Setup

1. Make sure you have the AWS CDK CLI installed:
```bash
npm install -g aws-cdk
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials in your environment:
```bash
aws configure
```

## Development Workflow

1. Make your changes to the code

2. Deploy directly using CDK:
```bash
cdk deploy
```

Or use watch mode for continuous development:
```bash
cdk watch
```

The watch mode will:
- Monitor your files for changes
- Automatically redeploy when changes are detected
- Provide immediate feedback

## Benefits of this Approach

1. Simpler setup - no pipeline configuration needed
2. Faster development cycle
3. Works completely locally
4. No Git or GitHub requirements
5. No AWS CodeStar connections needed
6. Direct deployment feedback

## When Ready for CI/CD

When you're ready to set up CI/CD:

1. Uncomment the pipeline code in `cdk_app.py`
2. Choose the appropriate source configuration:
   - For GitHub: Use `CodePipelineSource.gitHub()`
   - For other Git providers: Use `CodePipelineSource.connection()`
3. Configure the necessary connections in AWS
4. Deploy the pipeline