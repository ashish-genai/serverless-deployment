import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_cognito as cognito,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    pipelines,
    aws_cloudfront_origins as origins,
    Stage,
    Environment
)
from constructs import Construct

class AssetManagementStack(Stack):
    def __init__(self, scope: Construct, id: str, stage_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create DynamoDB tables with GSI
        user_table = dynamodb.Table(
            self, "Users",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        asset_table = dynamodb.Table(
            self, "Assets",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            sort_key=dynamodb.Attribute(
                name="department",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        # Add GSI for department queries
        asset_table.add_global_secondary_index(
            index_name="department-index",
            partition_key=dynamodb.Attribute(
                name="department",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="name",
                type=dynamodb.AttributeType.STRING
            )
        )

        order_table = dynamodb.Table(
            self, "Orders",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            sort_key=dynamodb.Attribute(
                name="created_at",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add GSI for created_by queries
        order_table.add_global_secondary_index(
            index_name="created_by-index",
            partition_key=dynamodb.Attribute(
                name="created_by",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="created_at",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Add GSI for asset_id queries
        order_table.add_global_secondary_index(
            index_name="asset-id-index",
            partition_key=dynamodb.Attribute(
                name="asset_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="created_at",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Create S3 bucket for static files
        static_bucket = s3.Bucket(self, "StaticAssets",
        removal_policy=cdk.RemovalPolicy.DESTROY, enforce_ssl=True)

        # Create Cognito User Pool
        user_pool = cognito.UserPool(
            self, "AssetManagementUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
            )
        )

        client = user_pool.add_client(
            "app-client",
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID],
                callback_urls=[f"https://{stage_name}.yourdomain.com/callback"]
            )
        )

        # Create Lambda layer for common dependencies
        dependencies_layer = _lambda.LayerVersion(
            self, "DependenciesLayer",
            code=_lambda.Code.from_asset("lambda/layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="Common dependencies for Lambda functions"
        )

        # Create Lambda Functions
        auth_lambda = _lambda.Function(
            self, "AuthFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[dependencies_layer],
            handler="app.handler.handler",
            code=_lambda.Code.from_asset("lambda/auth"),
            environment={
                "USER_POOL_ID": user_pool.user_pool_id,
                "CLIENT_ID": client.user_pool_client_id,
                "USERS_TABLE": user_table.table_name,
                "ASSETS_TABLE": asset_table.table_name,
                "ORDERS_TABLE": order_table.table_name
            },
            memory_size=256,
            timeout=cdk.Duration.seconds(30)
        )

        asset_lambda = _lambda.Function(
            self, "AssetFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="app.handler.handler",
            layers=[dependencies_layer],
            code=_lambda.Code.from_asset("lambda/app"),
            environment={
                "ASSETTABLE": asset_table.table_name
            }
        )

        order_lambda = _lambda.Function(
            self, "OrderFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="app.handler.handler",
            layers=[dependencies_layer],
            code=_lambda.Code.from_asset("lambda/app"),
            environment={
                "ORDERTABLE": order_table.table_name,
                "ASSETTABLE": asset_table.table_name
            }
        )

        # Grant permissions
        user_table.grant_read_write_data(auth_lambda)
        asset_table.grant_read_write_data(asset_lambda)
        order_table.grant_read_write_data(order_lambda)
        asset_table.grant_read_data(order_lambda)

        # Create API Gateway with CloudWatch logging
        api = apigw.RestApi(
            self, "AssetManagementAPI",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            ),
            deploy_options=apigw.StageOptions(
                stage_name=stage_name,
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                metrics_enabled=True
            )
        )

        # Add Cognito Authorizer
        auth = apigw.CognitoUserPoolsAuthorizer(
            self, "AssetManagementAuthorizer",
            cognito_user_pools=[user_pool]
        )

        # Add API routes
        api.root.add_resource("auth").add_method(
            "POST",
            apigw.LambdaIntegration(auth_lambda)
        )

        assets = api.root.add_resource("assets")
        assets.add_method(
            "GET",
            apigw.LambdaIntegration(asset_lambda),
            authorizer=auth
        )
        assets.add_method(
            "POST",
            apigw.LambdaIntegration(asset_lambda),
            authorizer=auth
        )

        orders = api.root.add_resource("orders")
        orders.add_method(
            "GET",
            apigw.LambdaIntegration(order_lambda),
            authorizer=auth
        )
        orders.add_method(
            "POST",
            apigw.LambdaIntegration(order_lambda),
            authorizer=auth
        )

        # Create CloudFront distribution
        distribution = cloudfront.Distribution(
            self, "AssetManagementDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(static_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            )
        )

        # Output values
        cdk.CfnOutput(self, "APIUrl", value=api.url)
        cdk.CfnOutput(self, "UserPoolId", value=user_pool.user_pool_id)
        cdk.CfnOutput(self, "ClientId", value=client.user_pool_client_id)
        cdk.CfnOutput(self, "DistributionDomain", value=distribution.distribution_domain_name)

class AssetManagementStage(Stage):
    def __init__(self, scope: Construct, id: str, stage_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        AssetManagementStack(self, 'AssetManagement', stage_name=stage_name)

class AssetManagementPipeline(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create the pipeline
        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.git_hub(
                    "your-username/asset-management-system",
                    "main",
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        pipeline = cdk.pipelines.CodePipeline(
            self, "Pipeline",
            synth=cdk.pipelines.ShellStep(
                "Synth",
                input=cdk.pipelines.NoSource(),  # Use NoSource for local development without a repository
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        staging = AssetManagementStage(
            self, "Staging",
            stage_name="staging",
            env=Environment(
                account=kwargs["env"].account,
                region=kwargs["env"].region
            )
        )

        staging_stage = pipeline.add_stage(
            staging,
            pre=[
                cdk.pipelines.ShellStep(
                    "UnitTest",
                    commands=["pip install pytest", "pytest"]
                )
            ]
        )

        production = AssetManagementStage(
            self, "Production",
            stage_name="prod",
            env=Environment(
                account=kwargs["env"].account,
                region=kwargs["env"].region
            )
        )

        pipeline.add_stage(
            production,
            pre=[
                cdk.pipelines.ManualApprovalStep("PromoteToProduction")
            ]
        )

app = cdk.App()
AssetManagementPipeline(
    app, "AssetManagementPipeline",
    env=Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region")
    )
)
app.synth()
