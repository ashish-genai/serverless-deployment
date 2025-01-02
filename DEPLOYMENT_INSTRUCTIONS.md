# CDK Deployment Instructions

The pipeline has been disabled for local development. This is the recommended approach when working locally without GitHub or any remote repository.

## Local Development Setup

1. Install prerequisites:
```bash
npm install -g aws-cdk
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

## Development Workflow

Use one of these approaches:

1. Direct deployment:
```bash
cdk deploy
```

2. Watch mode (recommended for development):
```bash
cdk watch
```

The watch mode will:
- Monitor your files for changes
- Automatically redeploy when changes are detected
- Provide immediate feedback

## Benefits

- No pipeline configuration needed
- Faster development cycle
- Works completely locally
- No Git/GitHub requirements
- Immediate feedback on changes

## Re-enabling the Pipeline

When you're ready to set up CI/CD:

1. Uncomment the pipeline code in `cdk_app.py`
2. Choose the appropriate source configuration based on your needs:
   ```python
   # For GitHub:
   input=cdk.pipelines.CodePipelineSource.gitHub("owner/repo", "branch")
   
   # For other Git providers:
   input=cdk.pipelines.CodePipelineSource.connection("owner/repo", "branch", 
       connection_arn="arn:aws:codestar-connections:region:account:connection/xxx")
   ```