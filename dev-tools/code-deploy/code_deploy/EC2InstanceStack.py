from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam
)


class EC2InstanceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # The code that defines your stack goes here


        vpcId = "vpc-6a56a20e"
        instanceName = "MyCodePipelineDemo"
        instanceType = "t2.micro"
        amiName = "amzn2-ami-hvm-2.0.20200520.1-x86_64-gp2"
        keyPair = "cdk-dev"

        
        roleArn = props["ec2role"]
        env = kwargs['env']

        userData = "yum -y update; yum install -y ruby aws-cli; cd /home/ec2-user; aws s3 cp s3://aws-codedeploy-{}/latest/install . --region {}; chmod +x install; ./install auto".format(
            env.region, env.region
        )

        vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id=vpcId,)

        sec_group = ec2.SecurityGroup(
            self, "sec-group",security_group_name="sg_pipelinedemo", vpc=vpc, allow_all_outbound=True,
        )

        sec_group.add_ingress_rule( 
            peer=ec2.Peer.ipv4("82.27.169.197/32"),
            description="Allow SSH connection",
            connection=ec2.Port.tcp(22),
        )

        
        sec_group.add_ingress_rule(
             peer=ec2.Peer.ipv4("82.27.169.197/32"),
            description="Allow HTTP connection",
            connection=ec2.Port.tcp(80),
        )

        ec2_instance = ec2.Instance(
            self,
            "ec2-instance",
            instance_name=instanceName,
            instance_type=ec2.InstanceType(instanceType),
            machine_image=ec2.MachineImage().lookup(name=amiName),
            vpc=vpc,
            security_group=sec_group,
            key_name=keyPair,
            role=iam.Role.from_role_arn(self,"ec2role",role_arn=roleArn),
        
        )

        ec2_instance.add_user_data(userData)

        core.Tag.add(self, key="Name", value="MyCodePipelineDemo")