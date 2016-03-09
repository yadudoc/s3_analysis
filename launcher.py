#!/usr/bin/env python
import csv
import config_manager as cm
import bottle
import datetime
from datetime import datetime, timedelta

DRY_RUN=False 

def load_mapping_csvs(filename) :
    rdr = csv.DictReader(open(filename, 'r'))
    return list(rdr)


def init():
    mappings = load_mapping_csvs("ami_mapping.csv")
    for m in mappings:
        print m
    return mappings


def start_instance(app, image_id, instance_type) :

    userdata = open("userdata.sh", 'r').read()

    role="arn:aws:iam::968994658855:instance-profile/god_mode"
    
    deadline = datetime.now() + timedelta(hours=1)
    
    status = app.config["ec2.conn"].request_spot_instances(4.0, #Price 
                                                           image_id, 
                                                           count=1, 
                                                           type='one-time',
                                                           valid_until="{0}".format(deadline.isoformat()),
<<<<<<< HEAD
                                                           #availability_zone_group=None,
                                                           #key_name="klab-mesos.us-east-1",
                                                           user_data=userdata,
                                                           instance_type=instance_type,
=======
                                                           #availability_zone_group=None, 
                                                           key_name="klab-mesos.us-east-1", 
                                                           user_data=userdata, 
                                                           instance_type=instance_type, 
>>>>>>> 856f3c026f2bf7cae078da071f7353178bc5f27b
                                                           monitoring_enabled=False,
                                                           instance_profile_arn=role,
                                                           dry_run=DRY_RUN)


if __name__ == "__main__":
    mappings = load_mapping_csvs("ami_mapping.csv")

    app = bottle.default_app()
    try:
        app.config.load_config("production.conf")
    except Exception as e:
        logging.error("Exception {0} in load_config".format(e))
        exit(-1)
    cm.update_creds_from_metadata_server(app)

    #instances = ["m4.10xlarge", "c4.8xlarge", "m4.large", "m4.xlarge", "c4.xlarge" ]
#    instances = ["m4.10xlarge", "c4.8xlarge"] # "m4.large", "m4.xlarge", "c4.xlarge" ]
    instances = ["c4.8xlarge"] # "m4.large", "m4.xlarge", "c4.xlarge" ]

    for instance in instances :
        for m in mappings:
            print m["region_code"]
            cm.init(app, m["region_code"])
            print app.config["ec2.conn"]
            status = start_instance(app, m["ami"], instance)
            print "{0} {1} {2}".format(m["region_code"], instance, status)
<<<<<<< HEAD
            break;
=======
        # Break here to run only us-east-1
        break
>>>>>>> 856f3c026f2bf7cae078da071f7353178bc5f27b
