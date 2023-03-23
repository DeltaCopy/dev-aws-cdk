from aws_cdk import (
    core,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codecommit as code_commit,
    aws_s3 as s3,
    aws_codedeploy as code_deploy,
    aws_ec2 as ec2,
    aws_iam as iam,
)

import random


class PipelineStack(core.Stack):

    def createAll(self, roleArn,namespace):

        # Pipeline requires a bucket for versioning

        artifact_bucket = s3.Bucket(
            self,
            "SourceBucket",
            bucket_name=f"{namespace}-{core.Aws.ACCOUNT_ID}",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
            
        )

        # Create a server application
        serverApplication = code_deploy.ServerApplication(
            self, "MyDemoApplication", application_name="MyDemoApplication",
        )

        # Create a code deployment group, defines which instances to deploy to and how fast to deploy to them

        # ServerDeploymentGroup = A CodeDeploy Deployment Group that deploys to EC2/on-premise instances.
        code_deploy.ServerDeploymentGroup(
            self,
            "CodeDeploymentGroup",
            application=serverApplication,
            deployment_group_name="MyDemoDeploymentGroup",
            role=iam.Role.from_role_arn(self, "role", role_arn=roleArn),
            deployment_config=code_deploy.ServerDeploymentConfig.ONE_AT_A_TIME,
            ec2_instance_tags=code_deploy.InstanceTagSet(
                # any instance with tags satisfying
                # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
                # will match this group
                {"Name": ["MyCodePipelineDemo"],},
            ),
        )

        code_commit.Repository(self, "CodeCommitRepository",repository_name="MyDemoRepo",)        

        pipeline = codepipeline.Pipeline(
            self, "code-pipeline",
            pipeline_name="MyFirstPipeline",
            artifact_bucket=artifact_bucket,
        )

        source_stage = pipeline.add_stage(stage_name="Source")
        deploy_stage = pipeline.add_stage(stage_name="Deploy")

        source_output = codepipeline.Artifact(artifact_name='source')

        source_stage.add_action(
            codepipeline_actions.CodeCommitSourceAction(
                action_name="Source",
                repository=code_commit.Repository.from_repository_name(self,"code_repo",repository_name="MyDemoRepo"),
                run_order=1,
                output=source_output,
            )
        )

        deploy_stage.add_action(
            codepipeline_actions.CodeDeployServerDeployAction(
                deployment_group=code_deploy.ServerDeploymentGroup.from_server_deployment_group_attributes(
                    self,
                    "server_code_deploy_group",
                    application=code_deploy.ServerApplication.from_server_application_name(self,"server_app",server_application_name="MyDemoApplication"),
                    deployment_group_name="MyDemoDeploymentGroup",
                ),
                action_name="Deploy",
                input=source_output
            )
        )

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # The code that defines your stack goes here
        env = kwargs.get("env")

        roleArn = props["deployrole"]
        namespace = props['namespace']

        self.createAll(roleArn,namespace)

