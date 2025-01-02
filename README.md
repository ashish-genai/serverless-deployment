# Asset Management System

A comprehensive asset management application built with FastAPI and deployed as a serverless application on AWS.

## Features

- Inventory management (CRUD operations for assets)
- Asset type management
- Order processing (track incoming and outgoing orders)
- Asset tracking across departments
- Role-based access control (Administrator, Manager, Employee)
- Comprehensive reporting system
- Serverless architecture for scalability and cost-effectiveness
- Activity logging
- DynamoDB for data storage

## Requirements

- AWS Account
- AWS CLI configured with appropriate permissions
- Python 3.9+ (ensure you're using the macOS/universal2 version)
- Node.js 14+ and npm (for AWS CDK)
- AWS CDK CLI
- Xcode Command Line Tools (for macOS)
- Homebrew (recommended for macOS package management)
- GitHub account (for deployment)

## Installation

> **Note for Apple Silicon (M1/M2) Mac Users**: 
> Ensure you're using the universal2 version of Python. If using Homebrew, this is handled automatically.
> If you encounter any ARM64 compatibility issues, you may need to run:
> ```bash
> arch -x86_64 zsh  # Or your preferred shell
> ```
> before running the installation commands.

1. Clone the repository:
```bash
git clone https://github.com/your-username/asset-management-system.git
cd asset-management-system
```

2. Install dependencies:

For macOS, first ensure Xcode Command Line Tools are installed:
```bash
xcode-select --install
```

Then install the required packages:
```bash
# Using Homebrew (recommended for macOS)
brew install python@3.9 node

# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Install AWS CDK CLI
npm install -g aws-cdk
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS configuration
```

4. Configure AWS and deploy:
```bash
aws configure  # Set up your AWS credentials
cdk bootstrap
```

## Deployment

### GitHub Deployment (Recommended)

1. Push your code to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. The GitHub Actions workflow will automatically trigger deployment to AWS.
   You can monitor the deployment progress in the Actions tab of your GitHub repository.

### Local Development (Alternative)

If you need to test changes locally before pushing to GitHub:

1. Synthesize the CloudFormation template:
```bash
cdk synth
```

2. Deploy the stack:
```bash
cdk deploy
```

3. For development with hot-reload:
```bash
cdk watch
```

## Usage

1. After deployment, you will receive the API Gateway URL and Cognito User Pool details.
2. Use the Cognito User Pool to create and manage users.
3. Access the API using the provided API Gateway URL.
4. Use the Cognito tokens for authentication when making API requests.
5. API documentation is available at `https://<api-gateway-url>/api/docs`

## Security

- API Gateway with Cognito authorizer for secure API access
- Cognito User Pools for user authentication and authorization
- HTTPS enabled by default
- JWT-based authentication
- Role-based access control
- Input validation
- DynamoDB encryption at rest

## AWS Resources

This project utilizes the following AWS services:

- AWS Lambda for serverless compute
- Amazon API Gateway for API management
- Amazon DynamoDB for data storage
- Amazon S3 for static asset storage
- Amazon Cognito for user authentication and authorization
- Amazon CloudFront for content delivery
- AWS CDK for infrastructure as code and deployment

## License

MIT