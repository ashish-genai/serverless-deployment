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

## Installation

> **Note for Apple Silicon (M1/M2) Mac Users**: 
> Ensure you're using the universal2 version of Python. If using Homebrew, this is handled automatically.
> If you encounter any ARM64 compatibility issues, you may need to run:
> ```bash
> arch -x86_64 zsh  # Or your preferred shell
> ```
> before running the installation commands.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/asset-management.git
cd asset-management
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

4. Deploy the application using AWS CDK:
```bash
cdk bootstrap
cdk deploy
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