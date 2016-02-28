#!/bin/bash


apt-get -y update
apt-get -y install python-pip git
apt-get -y install awscli

BUCKET="s3://klab-s3-analysis/"

instance_id=$(curl http://169.254.169.254/latest/meta-data/instance-id)
instance_type=$(curl http://169.254.169.254/latest/meta-data/instance-type)
az=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone)
REPEAT=6

LOG="$instance_id.log"

run_upload()
{
    filename="./upload_data_$1M"
    dd if=/dev/zero of=$filename bs=1M count=$1
    { time aws s3 cp --region us-east-1 $filename s3://klab-s3-analysis/$instance_id/ ;} &> test_result_$1
    real_time=$(grep "real" test_result_$1 | awk '{print $2}')
    echo "$instance_type, $az, upload, $1, $real_time" >> $2
    rm -f test_result_$1 $filename
}

run_download()
{
    filename="upload_data_$1M"
    { time aws s3 cp --region us-east-1 s3://klab-s3-analysis/$instance_id/$filename . ;} &> test_result_$1
    real_time=$(grep "real" test_result_$1 | awk '{print $2}')
    echo "$instance_type, $az, download, $1, $real_time" >> $2
    rm -f test_result_$1 $filename
}

#shuf -i 1-165600 > /tmp/data_source

#rm -f $LOG

for t in 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192
do
    for repeat in $(seq 1 1 $REPEAT)
    do
	#echo $repeat $t
	echo "Uploading $t [$repeat]"
	run_upload $t $LOG
    done
done

for t in 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192
do
    for repeat in $(seq 1 1 $REPEAT)
    do
	echo "Downloadin $t [$repeat]"
	run_download $t $LOG
    done
done

aws s3 cp --region us-east-1 $LOG s3://klab-s3-analysis/$instance_id/
aws ec2 terminate-instances --instance-ids $instance_id
shutdown now
