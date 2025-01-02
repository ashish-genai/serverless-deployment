# Local Deployment Instructions

To deploy this CDK application directly from VS Code:

1. Make sure you have AWS credentials configured properly in your local environment:
   - Either through AWS CLI (`aws configure`)
   - Or by setting AWS environment variables

2. Install the required dependencies:
   ```bash
   npm install -g aws-cdk
   pip install -r requirements.txt
   ```

3. Deploy the application:
   ```bash
   cdk deploy
   ```

The pipeline is now configured to use your local code as the source instead of pulling from a repository.