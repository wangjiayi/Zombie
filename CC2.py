import time, subprocess, re


class CC2:
    def __init__(self):
        self.fhLog = open("logs/CC2Log", "a+")
        self.fhLog.write("====================\n")
        self.fhLog.write(str(time.time()) + " CC2 is running\n")
        self.zombieList = [None, None, None]
        self.running()

    def running(self):
        time.sleep(3)
        while True:
            self.checkZombies()
            time.sleep(1)

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
                str(time.time()) + " CC2 cleared CC communication channel, send message to master, we have " + str(
                    down) + " zombies down\n")

    def is_running(self, process):

        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
        for x in s.stdout:

            if re.search(process, x):
                return True

        return False


CC2()
