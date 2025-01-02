# Asset Management System Deployment Guide

There are two ways to deploy this Asset Management System:

## 1. GitHub Deployment (Recommended)

This method uses GitHub Actions for automated deployment through AWS CDK Pipeline.

### Prerequisites:
1. An AWS account
2. GitHub repository access
3. The following environment variables set up in your GitHub repository secrets:
   - AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
   - AWS_REGION

### Steps:
1. Push your code to GitHub
2. GitHub Actions will automatically trigger the deployment pipeline
3. The system will be deployed using AWS CDK Pipeline

## 2. Local Development Deployment

Use this method if you want to deploy directly from your local machine.

### Prerequisites:
1. Python 3.8 or higher installed
2. AWS CLI installed and configured with your credentials
3. Node.js and npm installed (for CDK)
4. AWS CDK CLI installed (`npm install -g aws-cdk`)

### Steps:
1. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Deploy the stack:
   ```bash
   cdk deploy
   ```

### Note for M1/M2 Mac Users
Ensure Python is installed as a universal2 binary. You may need to reinstall Python using:
```bash
brew install python@3.8 --universal2
```

## Monitoring Deployment
- You can monitor the deployment progress in the AWS CloudFormation console
- For GitHub deployments, check the Actions tab in your GitHub repository
- For local deployments, watch the terminal output for progress

## Troubleshooting
- Ensure all AWS credentials are properly configured
- Check CloudWatch logs for any deployment issues
- Verify all required IAM permissions are in place
- For local deployment issues, try running `cdk doctor` to verify your setup