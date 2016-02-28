#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import numpy
data = np.loadtxt(open("aggregate.csv","r"),delimiter=", ", dtype=str)

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
                                    [a/b for a,b in zip(datapoints,data_avg)],
                                    linestyle='solid',
                                    marker=markers[ridx],
                                    markersize=5.0,
                                    color=colors[ridx],
                                    label=LABEL)

        plt.setp(omp1, alpha=0.6, antialiased=True, linewidth=3.0)


    #plt.yscale('log', basex=10)
    plt.xticks([x for x in datapoints], [x for x in datapoints])
    plt.xscale('log', basex=2)
    plt.legend(loc=2, ncol=10,  borderaxespad=2)
    plt.ylabel("Time to completion in seconds")
    plt.xlabel("Size of Transferred data (MB)")
    #plt.suptitle('afoooasdsad', fontsize=16)
    plt.show()


instance_types = ["m4.large", "m4.xlarge", "m4.10xlarge", "c4.xlarge", "c4.8xlarge"]
plotter_latency(results, instance_types[2])
#plotter_tiling()
exit()
