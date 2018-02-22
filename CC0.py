import time, subprocess, os, re


class CC0:
    def __init__(self):
        self.fhLog = open("logs/CC0Log", "a+")
        self.fhLog.write("====================\n")
        self.fhLog.write(str(time.time()) + " CC0 is running\n")
        self.zombieList = [None, None, None]
        self.running()

    def running(self):
        time.sleep(1)
        while True:
            self.newZombies()
            self.checkZombies()
            time.sleep(1)

    def newZombies(self):
        fhCC = open("channel/CommunicationChannel", "r")
        lines = fhCC.readlines()
        needToStart = 0
        flag = False
        for i in range(len(lines)):
            content = lines[i].split(' ')
            if content[0] == 'start':
                needToStart = int(content[1])
                fhCC = open("channel/CommunicationChannel", "w")
                fhCC.write('')
                fhCC.close()
                self.fhLog.write(str(time.time()) + " need to start " + str(needToStart) + " new zombie\n")

        for i in range(len(self.zombieList)):
            if needToStart > 0 and (self.zombieList[i] is None or self.is_running(str(self.zombieList[i])) is False):
                flag = True
                self.zombieList[i] = subprocess.Popen(['python', 'Zombie.py']).pid
                needToStart -= 1
                self.fhLog.write(str(time.time()) + " starting new zombie " + str(i) + "\n")
        if flag:
            activeList = str(self.zombieList[0]) + " " + str(self.zombieList[1]) + " " + str(self.zombieList[2])
            fhCCC = open("channel/CCChannel", "w")
            fhCCC.write(activeList)
            fhCCC.close()
            self.fhLog.write(str(time.time()) + " tell other CC, the new zombies is " + activeList + "\n")

    def checkZombies(self):

        fhCCC = open("channel/CCChannel", "r")
        lines = fhCCC.readlines()
        if len(lines) is 0:
            return
        pids = lines[0].split(' ')

        down = 0
        for i in range(len(pids)):
            pid = pids[i]
            proc = self.is_running(pid)
            if proc is False:
                down += 1
        if down > 0:
            fhCC = open("channel/CommunicationChannel", "w")
            fhCC.write('down ' + str(down))
            fhCC.close()
            fhCCC = open("channel/CCChannel", "w")
            fhCCC.write('')
            fhCCC.close()
            self.fhLog.write(
                str(time.time()) + " CC0 cleared CC communication channel, send message to master, we have " + str(
                    down) + " zombies down\n")

    def is_running(self, process):

        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
        for x in s.stdout:

            if re.search(process, x):
                return True

        return False


CC0()
