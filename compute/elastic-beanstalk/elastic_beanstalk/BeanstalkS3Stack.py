from aws_cdk import (
    core,
    aws_s3,
    aws_s3_deployment,
    aws_s3_assets,
)

import os

class BeanstalkS3Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str,props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        s3_bucket_asset = aws_s3_assets.Asset(
            self,
            "s3-asset",
            path=os.path.abspath(props['s3_asset'])
        )

        output = core.CfnOutput(
            self,
            "S3_object_url",
            value=s3_bucket_asset.s3_object_url,
            description="S3 object url"
        )

        output = core.CfnOutput(
            self,
            "S3_object_key",
            value=s3_bucket_asset.s3_object_key,
            description="S3 object key"
        )

        output = core.CfnOutput(
            self,
            "S3_bucket_name",
            value=s3_bucket_asset.s3_bucket_name,
            description="S3 bucket name"
        )

        self.output_props = props.copy()
        self.output_props['s3bucket_name'] = s3_bucket_asset.s3_bucket_name
        self.output_props['s3bucket_obj_key'] = s3_bucket_asset.s3_object_key


        # pass objects to another stack



    @property
    def outputs(self):
        return self.output_props



       

        
        