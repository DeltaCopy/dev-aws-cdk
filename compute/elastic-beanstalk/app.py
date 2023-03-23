#!/usr/bin/env python3

from aws_cdk import core

from elastic_beanstalk.BeanstalkAppStack import BeanstalkAppStack
from elastic_beanstalk.BeanstalkEnvStack import BeanstalkEnvStack
from elastic_beanstalk.BeanstalkS3Stack import BeanstalkS3Stack

app = core.App()

props = {
            'namespace': 'ElasticBeanstalk',
            'application_name':'GettingStartedApp2', 
            'environment_name': 'GettingStartedEnv2',
            'solution_stack_name': '64bit Amazon Linux 2018.03 v2.15.5 running Go 1.14.4',
            's3_asset' : 'assets/go-v3.zip'
        }

s3_bucket = BeanstalkS3Stack(
            app,
            f"{props['namespace']}-s3",
            props
)

beanstalk_app = BeanstalkAppStack(
                app,
                f"{props['namespace']}-app",
                s3_bucket.outputs
)

beanstalk_app.add_dependency(s3_bucket)

beanstalk_env = BeanstalkEnvStack(
                app,
                f"{props['namespace']}-env",
                props,

)

beanstalk_env.add_dependency(beanstalk_app)

app.synth()

