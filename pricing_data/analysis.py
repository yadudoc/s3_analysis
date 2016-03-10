#!/usr/bin/env python
import csv

def get_data(filename, headers=None, delimiter='|'):
    try :
        f = open(filename, 'rb')
        if headers == "implicit":
            headers = f.readline().split(delimiter)
            f.next()
            reader = csv.DictReader(f, delimiter=delimiter, fieldnames=headers)

        elif type(headers) is list :
            reader = csv.DictReader(f, delimiter=delimiter, fieldnames=headers)

        else:
            reader = csv.DictReader(f, delimiter=delimiter)

    except Exception, e:
        print "[ERROR]Caught exception in opening the file:{0}".format(filename)
        print "[ERROR]Reason : {0}".format(e)
        exit(-1)
    return reader


# Data size in GB
def pricing_fn_stupid(row, azs, data_size):
    myrow = row
    #print azs
    for az in azs:
        if row[az] != 'None':
            if az.startswith('us-east') :
                myrow[az] = float(row[az])
            else:
                myrow[az] = float(row[az])
    return myrow


# Data size in GB
# Considers the region to region cost of data transfer
def pricing_fn_simple(row, azs, data_size):
    myrow = row
    for az in azs:
        if row[az] != 'None':
            if az.startswith('us-east') :
                myrow[az] = float(row[az])
            else:
                myrow[az] = float(row[az]) + data_size*0.02
    return myrow

BWu = 1
BWd = 1
# Data size in GB
# Considers the region to region transfer cost and
# Partial hour cost
def pricing_fn_partial(row, azs, data_size):
    myrow = row
    for az in azs:
        if row[az] != 'None':
            if az.startswith('us-east') :
                myrow[az] = float(row[az]) + ((data_size/BWu)+(data_size/BWd))*float(row[az])
            else:
                myrow[az] = float(row[az]) + ((data_size/BWu)+(data_size/BWd))*float(row[az]) + data_size*0.02
    return myrow



# Choose 1az each from US-east-1
# Choose from any az in us-east
# Choose from any az
def single_zone_strategy(data, azs, az, func, data_transfer_volume):
    total_price     = 0
    hours_available = 0
    hours_total     = 0
    for x in data:
        x_adj = func(x, azs, data_transfer_volume)
        if x_adj[az] != 'None':
            total_price += float(x_adj[az])
            hours_available += 1
        hours_total += 1

    return (total_price, hours_available, hours_total)

# Choose from any az in us-east
def single_region_strategy(data, azs, az, func, data_transfer_volume):
    total_price     = 0
    hours_available = 0
    hours_total     = 0
    my_azs = [ x for x in azs if x.startswith(az) ]

    mix = {}
    for x in data:
        x_adj = func(x, azs, data_transfer_volume)
        price  = min([x_adj[az] for az in my_azs])
        min_az = [ az for az in my_azs if x_adj[az] == price ][0]

        #print [x_adj[az] for az in my_azs], price
        if x_adj[min_az] != 'None':
            total_price += float(price)
            mix[min_az] = mix.get(min_az,0) + 1
            hours_available += 1
        hours_total += 1

    return (total_price, hours_available, hours_total, mix)

# Choose from any az in us-east
def multi_region_strategy(data, azs, az, func, data_transfer_volume):
    total_price     = 0
    hours_available = 0
    hours_total     = 0
    my_azs = azs

    mix = {}
    for x in data:
        x_adj = func(x, azs, data_transfer_volume)
        price  = min([x_adj[az] for az in my_azs])
        min_az = [ az for az in my_azs if x_adj[az] == price ][0]

        #print [x_adj[az] for az in my_azs], price
        if x_adj[az] != 'None':
            total_price += float(price)
            mix[min_az] = mix.get(min_az,0) + 1
            hours_available += 1
        hours_total += 1

    return (total_price, hours_available, hours_total, mix)


def strategies(azs, data, data_transfer_volume, pricing_method):

    for az in [x for x in azs if x.startswith('us-east')]:
        (tp, ha, ht) = single_zone_strategy(data, azs, az, pricing_method, data_transfer_volume)
        print "{4}|{0} : Totalprice:{1} hours:{2}/{3} ".format(az, tp, ha, ht, pricing_method.__name__)

    (tp, ha, ht, mix) = single_region_strategy(data, azs, 'us-east', pricing_method, data_transfer_volume)
    print "{5}|{0} : Totalprice:{1} hours:{2}/{3} mix:{4}".format("single_region", tp, ha, ht, mix, pricing_method.__name__)

    (tp, ha, ht, mix) = multi_region_strategy(data, azs, 'us-east', pricing_method, data_transfer_volume)
    print "{5}|{0} : Totalprice:{1} hours:{2}/{3} mix:{4} ".format("multi_region", tp, ha, ht, mix, pricing_method.__name__)

    return


if __name__ == "__main__" :

    data = list(get_data("price_data", headers="implicit", delimiter=','))
    azs = open("price_data", 'r').readline().split(',')[3:-1]

    instance_types = list(set([ x['instance'] for x in data]))

    for instance in instance_types:
    #for instance in ["m4.10xlarge"]:
        print "{0} {1} {0}".format("="*40, instance)
        idata = [x for x in data if x['instance'] == instance]

        for func in [pricing_fn_stupid, pricing_fn_simple, pricing_fn_partial]:
        #for func in [pricing_fn_simple]:
            strategies(azs, idata, 1, func)
            print "-"*90
