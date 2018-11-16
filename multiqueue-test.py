import time
import random
import os
from multiprocessing import Process


def workkeri(workker):
    while True:
        satunnaisuus = random.randint(1, 5)
        print("workker-name" , workker, "os-pid ", os.getpid(), proc)
        time.sleep(satunnaisuus)


if __name__ == '__main__':

    procs = []
    jobit = ["stor1", "stor2", "stor3", "stor4", "stor5"]
    for jobi in jobit:
        luku = jobi
        workker = "thread-" + luku
        proc = Process(target=workkeri, args=(workker,))
        procs.append(proc)
        proc.start()

    while True:

        time.sleep(5)
        print(procs)

        for duuni in  range(len(procs)):
            print(duuni)

            if procs[duuni].is_alive() is True:
                print(duuni, "Elossa", procs[duuni].is_alive())

            if procs[duuni].is_alive() is not True:
                print("Ei elossa", procs[duuni].is_alive())
                time.sleep(1)
                print("Start new workker")
                workker = "thread-" + jobit[duuni]
                procs.remove(procs[duuni])
                proc = Process(target=workkeri, args=(workker,))
                procs.append(proc)
                proc.start()

        time.sleep(1)
