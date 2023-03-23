#!/usr/bin/env python3

from aws_cdk import core
from rds.RDSDBStack import RDSDBStack
from rds.NetworkStack import NetworkStack
from rds.EC2Stack import EC2Stack

props = {
            'namespace':'RDS',
            'vpc_name':'vpc-rds',
            'instance_name':'rds-webserver',
            'instance_type':'t2.small',
            'instance_key':'####',
            'image_id':'ami-031a03cb800ecb0d5',
            'wan_ip':'########',
            'db_master_username': 'tutorial_user',
            'db_instance_identifier':'tutorial-db-instance',
            'db_instance_engine':'MYSQL',
            'db_name':'sample'
        }


env = core.Environment(region="#####",account="######")

app = core.App()
network_stack = NetworkStack(app, f"{props['namespace']}-network",props,env=env)

ec2_stack = EC2Stack(app,f"{props['namespace']}-ec2",network_stack.outputs,env=env)
ec2_stack.add_dependency(network_stack)


rds_stack = RDSDBStack(app, f"{props['namespace']}-db",network_stack.output_props,env=env)
rds_stack.add_dependency(network_stack)


app.synth()
