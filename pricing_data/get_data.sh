#!/bin/bash



export AWS_DEFAULT_OUTPUT="text"
instance="c4.8xlarge"


for region in "us-east-1" "us-west-2" "ap-northeast-1" "eu-central-1"
do
    rm -f $region.data
    for instance in 'c4.8xlarge' 'c4.xlarge' 'm4.10xlarge' 'm4.large' 'm4.xlarge':
    do
	export AWS_DEFAULT_REGION=$region
	#echo "Region : ", $region
	aws ec2 --region $region \
	    describe-spot-price-history \
	    --start-time=2016-02-01T01:00:00 \
	    --instance-types $instance \
	    --filters Name="product-description",Values="Linux/UNIX" &>> $region.data
    done
done
