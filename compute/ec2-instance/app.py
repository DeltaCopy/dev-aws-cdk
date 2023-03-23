#!/usr/bin/env python3

from aws_cdk import core

from ec2_instance.ec2_instance_stack import Ec2InstanceStack


app = core.App()
env = core.Environment(region="######",account="######")

Ec2InstanceStack(app, "ec2-instance",env=env)
app.synth()
