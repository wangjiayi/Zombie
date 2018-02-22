import time


class Zombie:
    def __init__(self):
        self.fhLog = open("logs/ZombieLog", "a+")
        self.fhLog.write("====================\n")
        self.fhLog.write(str(time.time()) + " new zombie is created\n")
        self.running()

    def running(self):
        i = 0
        while True:
            time.sleep(1)
            self.fhLog.write(str(time.time()) + " running " + str(i) + "\n")
            i += 1


Zombie()
