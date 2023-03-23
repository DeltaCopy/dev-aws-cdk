#!/usr/bin/env python3

from aws_cdk import core

from EC2InstanceStack import EC2InstanceStack
from RoleStack import RoleStack
from PipelineStack import PipelineStack

app = core.App()
env = core.Environment(region="eu-west-1",account="010185063177")


#CodeDeployStack(app,"ec2-instance",create_ec2_instance=True,env=env)

props = {'namespace': 'cdk-demo'}


roles = RoleStack(app,f"{props['namespace']}-role", props)
pipeline = PipelineStack(app,f"{props['namespace']}-pipeline",roles.outputs)
pipeline.add_dependency(roles)
ec2instance = EC2InstanceStack(app,f"{props['namespace']}-ec2",roles.outputs,env=env)
#ec2instance.add_dependency(roles)

app.synth()
