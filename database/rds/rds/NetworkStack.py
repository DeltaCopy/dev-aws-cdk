from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_rds as rds
)


class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
    

        # Create VPC

        
        vpc = ec2.CfnVPC(
            self,
            "tutorial-vpc",
            cidr_block="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True

        )

        vpc.tags.set_tag(key="Name",value=props['vpc_name'])
        
        # Create Routing table for private subnet
        route_table_private = ec2.CfnRouteTable(
            self,
            "rtb-private",
            vpc_id=vpc.ref
        )


        route_table_private.tags.set_tag(key="Name",value="RDS Private Routing Table")


        # Create Routing table for public subnet
        route_table_public = ec2.CfnRouteTable(
            self,
            "rtb-public",
            vpc_id=vpc.ref
        )

        
        route_table_public.tags.set_tag(key="Name",value="RDS Public Routing Table")


        # Create public subnet

        public_subnet = ec2.CfnSubnet(
            self,
            "public_subnet_1",
            cidr_block="10.0.0.0/24",
            vpc_id=vpc.ref,
            map_public_ip_on_launch=True,
            availability_zone="eu-west-1a"
        )

        # Create Elastic ip
        eip = ec2.CfnEIP(
            self,
            "elastic_ip",
        )

        # Create internet gateway

        inet_gateway = ec2.CfnInternetGateway(
            self,
            "rds-igw",
            tags=[core.CfnTag(key="Name",value="rds-igw")]
        )

        ec2.CfnVPCGatewayAttachment(
            self,
            "igw-attachment",
            vpc_id=vpc.ref,
            internet_gateway_id=inet_gateway.ref
        )

        # Create CfnNatGateway

        nat_gateway = ec2.CfnNatGateway(
            self,
            "natgateway",
            allocation_id=eip.attr_allocation_id,
            subnet_id=public_subnet.ref
        )

        # Create private subnet 1
        private_subnet_1 = ec2.CfnSubnet(
            self,
            "private-subnet1",
            cidr_block="10.0.1.0/24",
            vpc_id=vpc.ref,
            availability_zone="eu-west-1b"
        )

        # Create private subnet 2
        private_subnet_2 = ec2.CfnSubnet(
            self,
            "private-subnet2",
            cidr_block="10.0.2.0/24",
            vpc_id=vpc.ref,
            availability_zone="eu-west-1c"
        )

        public_subnet.tags.set_tag(key="Name",value="subnet-rds-public")
        private_subnet_1.tags.set_tag(key="Name",value="subnet-rds-private-1")
        private_subnet_2.tags.set_tag(key="Name",value="subnet-rds-private-2")

        # Associate private subnet with the created routing table
        ec2.CfnSubnetRouteTableAssociation(
                self,
                "rtb-assoc-priv001",
                route_table_id=route_table_private.ref,
                subnet_id=private_subnet_1.ref
        )

        ec2.CfnSubnetRouteTableAssociation(
                self,
                "rtb-assoc-priv002",
                route_table_id=route_table_private.ref,
                subnet_id=private_subnet_2.ref
        )

        ec2.CfnSubnetRouteTableAssociation(
            self,
            "rtb-assoc-public",
            route_table_id=route_table_public.ref,
            subnet_id=public_subnet.ref
        )

       

        

        # Create security groups

        # public web server

        webserver_sec_group = ec2.CfnSecurityGroup(
            self,
            "webserver-sec-group",
            group_description="webserver security group",
            vpc_id=vpc.ref,
            
        )

        ssh_ingress = ec2.CfnSecurityGroupIngress(
            self,
            "sec-group-ssh-ingress",
            ip_protocol="tcp",
            cidr_ip=props['wan_ip']+"/32",
            from_port=22,
            to_port=22,
            group_id=webserver_sec_group.ref
        )

        http_ingress = ec2.CfnSecurityGroupIngress(
            self,
            "sec-group-http-ingress",
            ip_protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_ip="0.0.0.0/0",
            group_id=webserver_sec_group.ref
        )

        webserver_sec_group.tags.set_tag(key="Name",value="sg-rds-webserver")

        
        # Private DB Instance

        db_sec_group = ec2.CfnSecurityGroup(
            self,
            "dbserver-sec-group",
            group_description="DB Instance Security Group",
            vpc_id=vpc.ref
        )

        db_sec_group.tags.set_tag(key="Name",value="sg-rds-db")

        db_ingress = ec2.CfnSecurityGroupIngress(
            self,
            "sec-group-db-ingress",
            ip_protocol="tcp",
            from_port=3306,
            to_port=3306,
            group_id=db_sec_group.ref,
            source_security_group_id=webserver_sec_group.ref
        )

         
        db_sg = rds.CfnDBSubnetGroup(
            self,
            "rds_db_subnet_group",
            db_subnet_group_description="RDS DB Subnet Group",
            db_subnet_group_name="sgp-rds-db",
            subnet_ids=[private_subnet_1.ref,private_subnet_2.ref]
        )

        self.output_props = props.copy()
        self.output_props['webserver_sg_id'] = webserver_sec_group.ref
        self.output_props['public_subnet_id'] =  public_subnet.ref
        self.output_props['private_db_sg_id'] = db_sec_group.ref
        self.output_props['db_subnet_group_name'] = "sgp-rds-db"
        
        

    @property
    def outputs(self):
        return self.output_props
    
