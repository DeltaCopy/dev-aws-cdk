from aws_cdk import (
    core,
    aws_iam as iam,
)

import random


class RoleStack(core.Stack):
    def createRole(self,policyArn,servicePrincipal,roleName):


        iamRole = iam.Role(
            self,
            "role" + str(random.random()),
            role_name=roleName,
            assumed_by=iam.ServicePrincipal(servicePrincipal,),
        )
        
        iamRole.add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(
                self, "managedpolicy" + str(random.random()), managed_policy_arn=policyArn
            )
        )

        #print(iam.Role.role_arn)
        return iamRole.role_arn

    def __init__(self, scope: core.Construct, id: str,  props, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)
        # The code that defines your stack goes here

        # Create roles

        
        ec2roleArn = self.createRole(
            "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeploy",
            "ec2",
            "EC2InstRole"
        )
        
        
        deployroleArn = self.createRole(
            "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole",
            "codedeploy",
            "CodeDeployRole"
        )

        self.output_props = props.copy()
        self.output_props['deployrole'] = deployroleArn
        self.output_props['ec2role'] = ec2roleArn

    # pass objects to another stack
    @property
    def outputs(self):
        return self.output_props
        