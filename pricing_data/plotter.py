#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import numpy
import datetime
from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import pickle

def load_pricing_data(datafile):
    data = np.loadtxt(open(datafile,"r"),delimiter="\t", dtype=str)
    return data

line_types = ['-mo', '-co', '-rd', '-y^', '-b.', '-k*', '-b*', '-go', '-md', '--r*', '-b.', '-y^']

def plot_price_history (history, instance_type, title):
    figure         = plt.figure()

    availability_zones = set([x[1] for x in history])

    print availability_zones

    idx = 0
    for region_name in availability_zones:
        reg_hist   = [ x for x in history if x[1] == region_name and x[2] == instance_type]
        print "Len {0}in{1} {2} ".format(instance_type, region_name, len(reg_hist))
        line       = plt.plot([dateutil.parser.parse(x[5]) for x in reg_hist ],
                              [x[4]    for x in reg_hist ],  line_types[idx],  label=region_name)
        plt.setp(line, alpha=0.6, antialiased=True, linewidth=2.0)
        idx += 1

    plt.legend(loc=2, ncol=10,  borderaxespad=2)
    plt.ylabel("Price")
    plt.xlabel("Time")
    plt.yscale('log', basex=2)
    plt.title(title)
    plt.show()


def load_data(datafile):
    data = np.loadtxt(open(datafile,"r"),delimiter=" ", dtype=str)

    results = {}
    for item in data:
        insttype      = item[0]
        region        = item[1]
        transfer_type = item[2]
        data_size     = int(item[3])
        ttime         = item[4].strip('s').split('m')
        ttc           = (float(ttime[0])*60) + float(ttime[1])

        if region not in results:
            results[region] = {}

        if insttype not in results[region]:
            results[region][insttype] = {}

        if transfer_type not in results[region][insttype]:
            results[region][insttype][transfer_type] = {}

        if data_size not in results[region][insttype][transfer_type]:
            results[region][insttype][transfer_type][data_size] = []

        results[region][insttype][transfer_type][data_size].append(ttc)


        print results["ap-northeast-1c"]["m4.10xlarge"]["download"][1024]

        for region in results:
            for instype in results[region]:
                for ttype in results[region][instype]:
                    for size in results[region][instype][ttype]:
                        _min = min(results[region][instype][ttype][size])
                        _max = max(results[region][instype][ttype][size])
                        _avg = numpy.mean(results[region][instype][ttype][size])
                        _std = numpy.std(results[region][instype][ttype][size])
                #print "{0}, {1}, {2}, {3}, {4}, {5}, {6}".format(region, instype, ttype, size, _min, _max, _avg)
    return results
#print results


def plotter_latency (results, instype):

    figure         = plt.figure()

    datapoints     = [1, 4, 16, 64, 256, 1024]

    colors  = ['g', 'r', 'b', 'k', 'c']
    markers = ['^', 'x', 'o', 'h', '+']

    for ridx, region in enumerate(results):
        if instype not in results[region]:
            continue

        data_min = [0 for i in datapoints]
        data_max = [0 for i in datapoints]
        data_avg = [0 for i in datapoints]
        data_std = [0 for i in datapoints]

        for idx, size in enumerate(datapoints):
            data_min[idx] = min(results[region][instype]["download"][size])
            data_max[idx] = max(results[region][instype]["download"][size])
            data_avg[idx] = numpy.mean(results[region][instype]["download"][size])
            data_std[idx] = numpy.std(results[region][instype]["download"][size])

        print region
        print results[region][instype]["download"][1024]
        print datapoints, len(datapoints)
        print data_avg, len(data_avg)

        LABEL          = "{0} {1} {2}".format(region, instype, "Download")
        '''
        omp1           =  plt.plot(datapoints,
                                   [a/b for a,b in zip(datapoints,data_avg)],
        colors[ridx],  label=LABEL)
        '''
        omp1           =  plt.plot(datapoints,
                                   #data_avg,
                                   [8*(a/b) for a,b in zip(datapoints,data_min)],
                                   linestyle='solid',
                                   marker=markers[ridx],
                                   markersize=5.0,
                                   color=colors[ridx],
                                   label=LABEL)

        plt.setp(omp1, alpha=0.6, antialiased=True, linewidth=3.0)


    #plt.yscale('log', basex=10)
    plt.xticks([x for x in datapoints], [x for x in datapoints])
    #plt.xscale('log', basex=2)
    #plt.yscale('log', basex=2)
    plt.legend(loc=2, ncol=10,  borderaxespad=2)
    plt.ylabel("Time to completion in seconds")
    plt.xlabel("Bandwidth in Mbps")
    #plt.suptitle('afoooasdsad', fontsize=16)
    plt.show()

def foo(data):

    availability_zones = set([x[1] for x in data[0:50] ])
    instance_types     = set([x[2] for x in data[::20] ])

    print instance_types
    print availability_zones
    updated = []
    for az in availability_zones:
        for it in instance_types:
            r = [ x for x in data if x[1] == az and x[2] == it ][::-1]
            print "{0} {1} = {2}/{3}".format(az, it, len(r), len(data))
            s = dateutil.parser.parse(r[0][5])
            s = s - relativedelta(minutes=s.minute, seconds=s.second) + relativedelta(hours=1)
            e = dateutil.parser.parse(r[-1][5])

            current = s
            temp    = None

            index = 0
            for x in r:
                index += 1
                tstamp =  dateutil.parser.parse(x[5])
                #print "tstamp < current : {0} < {1}".format(tstamp, current)
                if tstamp < current:
                    temp = x
                else:
                    temp[5] = current
                    updated.append(list(temp))
                    temp = x
                    current = current + relativedelta(hours=1)

    return updated

pickle_file = "data_by_hour.pickle"
pickle_file2= "earliest_date.pickle"

def pickle_to_file(fname, obj):
    with open(fname, 'wb') as handle:
        pickle.dump(obj, handle)

def pickle_load_from_file(fname):
    with open(fname, 'rb') as handle:
        return pickle.load(handle)

def process_all_data(datafiles):

    all_data = []
    first_dates = []
    for data in datafiles:
        results = load_pricing_data(data)
        data_by_hour = foo(results)
        first_dates.append(data_by_hour[0][5])
        print first_dates
        all_data.extend(data_by_hour)

    earliest = sorted(first_dates, key=lambda x: dateutil.parser.parse(x))[0]
    pickle_to_file(pickle_file,  all_data)
    pickle_to_file(pickle_file2, earliest)
    return all_data

def load_all_data():
    return pickle_load_from_file(pickle_file), pickle_load_from_file(pickle_file2)


def plot_price_per_instance (history, availability_zones, title):
    figure         = plt.figure()

    print availability_zones
    idx = 0
    for az in availability_zones:
        line       = plt.plot([dateutil.parser.parse(x[5]) for x in history[az] ],
                              [x[4]                        for x in history[az] ],
                              line_types[idx],
                              label=az)
        plt.setp(line, alpha=0.6, antialiased=True, linewidth=2.0)
        idx += 1

    plt.legend(loc=2, ncol=10,  borderaxespad=2)
    plt.ylabel("Price")
    plt.xlabel("Time")
    plt.yscale('log', basex=2)
    plt.title(title)
    plt.show()


if __name__ == "__main__" :

    instance_types = ["m4.large", "m4.xlarge", "m4.10xlarge", "c4.xlarge", "c4.8xlarge"]
    datafiles = ["us-east-1.data", "ap-northeast-1.data", "us-west-2.data"]

    #process_all_data(datafiles)
    print "Loading data..."
    all_data, earliest = load_all_data()
    print "Done loading data"

    ############################################################################################
    # Get Availability zones
    ############################################################################################
    azs = set([x[1] for x in all_data])
    print "Availability zones : ", azs


    ############################################################################################
    # Process instance wise data
    ############################################################################################
    for i in instance_types:
        print "Instance type : ", i
        instance_data = [ x for x in all_data if x[2] == i ]
        az_data = {}
        for az in azs:
            t = [ x for x in instance_data if x[1] == az ]
            if t :
                az_data[az] = t
                print "Data for instance : {0} in {1} : {2}".format(i, az, len(az_data[az]))
            else:
                print "No data available for instance : {0}".format(i)

        if az_data.keys():
            earliest = sorted([az_data[k][0][5] for k in az_data ], key=lambda x: dateutil.parser.parse(x))[0]
            latest   = sorted([az_data[k][-1][5] for k in az_data ], key=lambda x: dateutil.parser.parse(x))[-1]
            plot_price_per_instance(az_data, azs, i)
            price_at_stamp = {}
            for az in az_data.keys():
                for row in az_data[az]:
                    if row[5] not in price_at_stamp:
                        price_at_stamp[row[5]] = {}
                    price_at_stamp[row[5]][az] = float(row[4])

            print "[PRICEDATA], tstamp, instance, ",
            for az in az_data.keys():
                print "{0},".format(az),
            print

            for t in sorted(price_at_stamp.keys(), key=lambda x: dateutil.parser.parse(x)):
                print "[PRICEDATA], {0}, {1}, ".format(t, i),
                #z = min(price_at_stamp[t], key=lambda x: price_at_stamp[t][x])
                #print "[Best_Price] Time:{0} Instance_type:{1} AZ:{2} Price:{3}".format(t, i, z, price_at_stamp[t][z])
                for az in az_data.keys():
                    print "{0}, ".format(price_at_stamp[t].get(az, None)),
                print



    #for instance in instance_types:
    #    plot_price_history(data_by_hour, instance, "{0} - {1}".format(data, instance))

    #print set([ x[1] for x in all_data[::50]])
    #print set([ x[2] for x in all_data[::50]])

    #for i in r[0:10]:
    #    d = dateutil.parser.parse(i[5])
    #    print "{0} {1}".format(d, i[1])

