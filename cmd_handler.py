
import threading, time

class CmdHandler (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):

        while(True):
            vel = int(input("Enter target velocity (-1 to quit): "))

            if vel == -1:
                break



if __name__ == "__main__":
    cmdHandler = CmdHandler()
    cmdHandler.start()
    cmdHandler.join()
