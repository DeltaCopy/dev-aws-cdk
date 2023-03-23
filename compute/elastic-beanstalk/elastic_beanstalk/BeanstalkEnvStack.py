from aws_cdk import (
    core,
    aws_elasticbeanstalk as elastic_beanstalk
)

import boto3

class BeanstalkEnvStack(core.Stack):

    def createEnvironment(self,application_name,environment_name,solution_stack_name):

        # get the latest application version

        client = boto3.client('elasticbeanstalk')

        application_versions = client.describe_application_versions(
            ApplicationName=application_name
        )

        version_label = None

        if(len(application_versions['ApplicationVersions'])> 0):
            version_label = application_versions['ApplicationVersions'][0]['VersionLabel']

        beanstalk_env_config_template = elastic_beanstalk.CfnConfigurationTemplate(
                self,
                "Elastic-Beanstalk-Env-Config",
                application_name=application_name,
                solution_stack_name=solution_stack_name,
                option_settings=[
                                    elastic_beanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty(
                                        namespace="aws:autoscaling:asg",option_name="MinSize",value="2"
                                    ),

                                    elastic_beanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty(
                                        namespace="aws:autoscaling:asg",option_name="MaxSize",value="4"
                                    )
                                ]
                                
        )

        beanstalk_env = elastic_beanstalk.CfnEnvironment(
            self,
            "Elastic-Beanstalk-Environment",
            application_name=application_name,
            environment_name=environment_name,
            solution_stack_name=solution_stack_name,
            version_label=version_label,
            
            option_settings=[
                                elastic_beanstalk.CfnEnvironment.OptionSettingProperty(
                                    namespace="aws:autoscaling:asg",option_name="MinSize",value="2"
                                ),
                                 elastic_beanstalk.CfnEnvironment.OptionSettingProperty(
                                    namespace="aws:autoscaling:asg",option_name="MaxSize",value="4"
                                ),
                                
                            ]
        )

        
      

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.createEnvironment(props['application_name'],props['environment_name'],props['solution_stack_name'])

       
