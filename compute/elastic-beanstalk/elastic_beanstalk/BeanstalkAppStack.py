from aws_cdk import (
    core,
    aws_elasticbeanstalk as elastic_beanstalk,
    aws_s3
)


class BeanstalkAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        def createApplication(application_name):
            elastic_beanstalk.CfnApplication(
                self,
                "Elastic-Beanstalk",
                application_name=application_name,
                description="AWS Elastic Beanstalk Demo",
            )            

        # The code that defines your stack goes here
        createApplication(props['application_name'])

        BeanstalkAppVersionStack(self,"BeanstalkAppVersionStack",props,**kwargs)

class BeanstalkAppVersionStack(core.NestedStack):
    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        app_version = elastic_beanstalk.CfnApplicationVersion(
            self,
            "application_version",
            application_name=props['application_name'],
            source_bundle=elastic_beanstalk.CfnApplicationVersion.SourceBundleProperty(
                s3_bucket=props['s3bucket_name'],
                s3_key=props['s3bucket_obj_key']
            ),
            
        )

        

