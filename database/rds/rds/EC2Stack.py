from aws_cdk import (
    core,
    aws_ec2 as ec2,
 
)


class EC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ec2inst = ec2.CfnInstance(
            self,
            "ec2instance1",
            subnet_id=props['public_subnet_id'],
            security_group_ids=[props['webserver_sg_id']],
            instance_type=props['instance_type'],
            image_id=props['image_id'],
            key_name=props['instance_key']
            
        )

        ec2inst.tags.set_tag(key="Name",value="rds-webserver")


        core.CfnOutput(
            self,
            "ec2-public-ip",
            value=ec2inst.attr_public_ip
        )
        
        core.CfnOutput(
            self,
            "ec2-public-dns-name",
            value=ec2inst.attr_public_dns_name
        )