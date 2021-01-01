import hashlib
import requests
import time
import threading
import asyncio
import queue
from multiprocessing import Process, Pool
from bs4 import BeautifulSoup


class sha_thread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while self.queue.qsize() > 0:
            data = self.queue.get()
            #a = sha(data)
            print(sha(data))


def sha(data):
    for i1 in range(0x21, 0x7F):
        for i2 in range(0x21, 0x7F):
            for i3 in range(0x21, 0x7F):
                for i4 in range(0x21, 0x7F):
                    for i5 in range(0x21, 0x7F):
                        testans = chr(i1)+chr(i2) + \
                            chr(i3)+chr(i4)+chr(i5)+data
                        ans = chr(i1)+chr(i2)+chr(i3)+chr(i4)+chr(i5)
                        shafunc = hashlib.sha256()
                        shafunc.update(testans.encode("utf-8"))
                        hexnum = shafunc.hexdigest()
                        hexnum2 = int(hexnum, 16) >> 236
                        if(hexnum2 == 0):
                            return testans


class web_thread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while self.queue.qsize() > 0:
            data = self.queue.get()
            #a = web(data)
            print(web(data))


def web(data):
    resp = requests.get(data)
    tem = BeautifulSoup(resp.text, "html.parser")
    need = str(tem.find("title"))
    need2 = need.split(">")
    ans = need2[1].split("<")
    return ans[0]


async def sha_corou(data):
    flag = 0
    for i1 in range(0x21, 0x7F):
        if(flag):
            break
        for i2 in range(0x21, 0x7F):
            if(flag):
                break
            for i3 in range(0x21, 0x7F):
                if(flag):
                    break
                for i4 in range(0x21, 0x7F):
                    if(flag):
                        break
                    for i5 in range(0x21, 0x7F):
                        if(flag):
                            break
                        testans = chr(i1)+chr(i2)+chr(i3)+chr(i4)+chr(i5)+data
                        ans = chr(i1)+chr(i2)+chr(i3)+chr(i4)+chr(i5)
                        shafunc = hashlib.sha256()
                        shafunc.update(testans.encode("utf-8"))
                        hexnum = shafunc.hexdigest()
                        hexnum2 = int(hexnum, 16) >> 236
                        if(hexnum2 == 0):
                            print(testans)
                            flag = 1


async def web_corou(data):
    resp = requests.get(data)
    tem = BeautifulSoup(resp.text, "html.parser")
    need = str(tem.find("title"))
    need2 = need.split(">")
    ans = need2[1].split("<")
    await asyncio.sleep(6)
    print(ans[0])


async def main1(Input, times):
    task = []
    for i in range(times):
        task.append(asyncio.create_task(sha_corou(Input[i])))
    for i in range(times):
        await task[i]


async def main2(Input, times):
    task = []
    for i in range(times):
        task.append(asyncio.create_task(web_corou(Input[i])))
    for i in range(times):
        await task[i]


if __name__ == "__main__":
    f = open('task1_sample.txt', 'r')
    #f = open('task2_sample.txt', 'r')
    comp = f.read()
    comp_list = comp.split("\n")
    case = int(comp_list[0])
    way = int(comp_list[1].split(" ")[0])
    if(way == 1 or way == 2):
        num = int(comp_list[1].split(" ")[1])
    times = int(comp_list[2])
    Input_list = []
    Input = queue.Queue()
    for i in range(times):
        temin = comp_list[i+3]
        Input_list.append(temin)
        Input.put(temin)

    tstart = time.time()
    if(case == 1):  # find sha256()
        if(way == 1):  # do by multithreading
            threads = []
            for i in range(num):
                threads.append(sha_thread(Input))
            for i in range(num):
                threads[i].start()
            for i in range(num):
                threads[i].join()
        elif(way == 2):  # do by multiprocessing
            with Pool(num) as pool:
                P = pool.map(sha, Input_list)
            for itr in P:
                print(itr)
        else:  # do by coroutine
            asyncio.run(main1(Input_list, times))

    else:  # find the title
        if(way == 1):  # do by multithreading
            threads = []
            for i in range(num):
                threads.append(web_thread(Input))
            for i in range(num):
                threads[i].start()
            for i in range(num):
                threads[i].join()
        elif(way == 2):  # do by multiprocessing
            with Pool(num) as pool:
                P = pool.map(web, Input_list)
            for itr in P:
                print(itr)
        else:  # do by coroutine
            asyncio.run(main2(Input_list, times))

    tend = time.time()
    print(tend-tstart)
