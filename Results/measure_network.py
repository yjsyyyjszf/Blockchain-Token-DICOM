import pandas as pd
import os
import time
import statistics
from tcp_latency import measure_latency
import pandas as pd
import datetime
import psutil
import sys
import contextlib

processTime = []
latAPIBC = []
latSocketFile = []
latPeers = []
latOderer = []
latCouchs = []


@contextlib.contextmanager
def atomic_overwrite(filename):
    temp = filename + '~'
    with open(temp, "w") as f:
        yield f
    # this will only happen if no exception was raised
    os.rename(temp, filename)


if __name__ == "__main__":

    server_hostname = '10.62.9.185'

    print("Connecting to {0}".format(server_hostname))

    #pid = int(sys.argv[1])

    times = 0

    start = time.time()
    finish = 0
    fname = datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S")
    while finish <= 4:
        print('Read Latency ...')
        peers = []
        couch = []
        processTime.append(times)
        latAPIBC.append(measure_latency(server_hostname, port=3000)[0])
        latSocketFile.append(measure_latency(
            server_hostname, port=5001)[0])
        latOderer.append(measure_latency(server_hostname, port=7050)[0])
        peers.append(measure_latency(server_hostname, port=7051)[0])
        peers.append(measure_latency(server_hostname, port=8051)[0])
        peers.append(measure_latency(server_hostname, port=9051)[0])
        peers.append(measure_latency(server_hostname, port=10051)[0])
        peers.append(measure_latency(server_hostname, port=11051)[0])
        peers.append(measure_latency(server_hostname, port=12051)[0])
        peers.append(measure_latency(server_hostname, port=13051)[0])
        peers.append(measure_latency(server_hostname, port=14051)[0])
        peers.append(measure_latency(server_hostname, port=15051)[0])
        peers.append(measure_latency(server_hostname, port=16051)[0])
        peers = list(filter(None, peers))
        latPeers.append(statistics.mean(peers))
        couch.append(measure_latency(server_hostname, port=5984)[0])
        couch.append(measure_latency(server_hostname, port=6984)[0])
        couch.append(measure_latency(server_hostname, port=7984)[0])
        couch.append(measure_latency(server_hostname, port=8984)[0])
        couch.append(measure_latency(server_hostname, port=9984)[0])
        couch.append(measure_latency(server_hostname, port=10984)[0])
        couch.append(measure_latency(server_hostname, port=11984)[0])
        couch.append(measure_latency(server_hostname, port=12984)[0])
        couch.append(measure_latency(server_hostname, port=13984)[0])
        couch.append(measure_latency(server_hostname, port=14984)[0])
        couch = list(filter(None, couch))
        latCouchs.append(statistics.mean(couch))
        time.sleep(1)
        times += 1
        finish += int((time.time() - start)/3600)

        #print('Finished Mensure ...')
        table = pd.DataFrame()
        table.insert(0, "Time", processTime)
        table.insert(1, "Latency Socket", latSocketFile)
        table.insert(2, "Latency API Blockchain", latAPIBC)
        table.insert(3, "Latency Orderer", latOderer)
        table.insert(4, "Latency Peers", latPeers)
        table.insert(5, "Latency Couch", latCouchs)
        with atomic_overwrite('../Results/table_latency.csv') as f:
            table.to_csv(f, sep=';')
