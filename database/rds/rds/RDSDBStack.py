from aws_cdk import (
    core,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_secretsmanager as sm
)

import json


class RDSDBStack(core.Stack):

    def getDBEngine(self,engine):
        if(engine == 'MYSQL'):
            return rds.DatabaseInstanceEngine.MYSQL
        if(engine == 'ORACLE-EE'):
            return rds.DatabaseInstanceEngine.ORACLE_EE
        

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        engine = self.getDBEngine(props['db_instance_engine'])

        '''
        db_inst = rds.DatabaseInstance(
            self,
            "rds-instance",
            master_username=props['db_master_username'],
            instance_identifier=props['db_instance_identifier'],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,ec2.InstanceSize.SMALL),
            vpc=ec2.Vpc.from_lookup(self,"vpclookup",vpc_name=props['vpc_name']),
            engine=engine,
            deletion_protection=False,
            security_groups=[ec2.SecurityGroup.from_security_group_id(self,"db-sg",security_group_id=props['private_db_sg_id'])],
            removal_policy=core.RemovalPolicy.DESTROY,
        )
        '''
        my_obj = {
            "db-master-username": props['db_master_username']
        }
        # create new secret in SecretsManager
        secret = sm.Secret(self,
                            "db-user-password-secret",
                            description="db master user password",
                            secret_name="db-master-user-password",
                            generate_secret_string=sm.SecretStringGenerator(
                                secret_string_template=json.dumps(my_obj),
                                generate_string_key="db-master-user-password"
                            )
        )

        db_inst = rds.CfnDBInstance(
            self,
            "rds-instance",
            engine=props['db_instance_engine'],
            db_subnet_group_name=props['db_subnet_group_name'],
            db_instance_identifier=props['db_instance_identifier'],
            db_instance_class="db.t2.micro",
            deletion_protection=False,
            vpc_security_groups=[props['private_db_sg_id']],
            allocated_storage="20",
            master_username=props['db_master_username'],
            master_user_password=secret.secret_value_from_json("db-master-user-password").to_string(),
            db_name=props['db_name']            
        )
    
        
        
        
      