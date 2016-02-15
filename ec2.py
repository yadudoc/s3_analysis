#!/usr/bin/env python

import boto
import boto.ec2

DRY_RUN=True

def start_instance(ami_id, instance_type):
    price_max = 4.00
    
    
    userdata = None
    with open(userdata_file, 'r') as data:
        userdata = data.read()

    print userdata
    
    spot_reqs   = conn.request_spot_instances(price,
                                              ami_id,
                                              count=count,
                                              instance_type=instance_type,
                                              type='one-time',
                                              key_name=Key_paid,
                                              user_data=userdata,
                                              dry_run=DRY_RUN)




if __name__ == "__main__":
    import launcher
    mappings = launcher.init()

    for m in mappings:
        start_instance(m["ami"], m["region_code"])
