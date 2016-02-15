#!/bin/bash


BUCKET="s3://klab-s3-analysis/"

instance_id=$(curl http://169.254.169.254/latest/meta-data/instance-id)
instance_type=$(curl http://169.254.169.254/latest/meta-data/instance-type)
az=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone)

LOG="$instance_id.log"

get_instance_specific

run_upload(){
    filename="./upload_data_$1M"
    dd if=/tmp/data_source -of=$filename bs=1M count=$1
    time aws s3 cp --region us-east-1 $filename s3://klab- $1  | tee test_result_$1
    real_time=$(grep "real" test_result_$1 | awk '{print $2}')
    echo "$1, $2" >> $2
}

shuf -i 1-165600 > /tmp/data_source


for t in 1 4 16 #64 256 1024
do
    run_upload $t log &> s3_test.logs
done

for t in 1 4 16 #64 256 1024
do
    run_download $t log &> s3_test.logs
done



