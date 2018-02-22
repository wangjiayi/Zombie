import time


class BotMaster:
    ccList = []

    def __init__(self):
        self.fhCC = open("channel/CommunicationChannel", "w")
        self.fhLog = open("logs/BotMasterLog", "a+")
        self.fhLog.write("====================\n")
        self.start()
        self.running()

    def start(self):
        self.fhCC.write("start 3")
        self.fhCC.close()
        self.fhLog.write(str(time.time()) + " send message to start 3 zombies\n")

    def running(self):
        while True:
            time.sleep(4)
            self.fhCC = open("channel/communicationChannel", "r")
            lines = self.fhCC.readlines()
            down = 0
            for i in range(len(lines)):
                content = lines[i].split(' ')
                if content[0] == 'down':
                    down += 1
            if down != 0:
                self.fhLog.write(str(time.time()) + " got message, " + str(down) + " zombies down\n")
                self.fhCC = open("channel/communicationChannel", "w")
                self.fhCC.write("start " + str(down))
                self.fhLog.write(str(time.time()) + " send message to start " + str(down) + " zombies\n")
                self.fhCC.close()


BotMaster()
