
import threading, time
import _thread
import sys



class CmdHandler (threading.Thread):
    def __init__(self, lock, defaultValue):
        threading.Thread.__init__(self)
        self.lock = lock
        self.value = 0.0
        self.defaultValue = defaultValue
        self.quit = False


    def SetValue(self, value):
        self.lock.acquire()
        self.value = value
        self.lock.release()

    def GetValue(self):
        v = 0.0
        self.lock.acquire()
        v = self.value
        self.value = self.defaultValue
        self.lock.release()

        return v
    def run(self):
        global quit
        while(self.quit == False):
            try:
                print("Enter target velocity (-1.0 to quit):", end=" ")
                vel = float(input())
                self.SetValue(vel)
            except:
                print("press a float value")




if __name__ == "__main__":
    lock=_thread.allocate_lock()
    cmdHandler = CmdHandler(lock)
    cmdHandler.start()

    while(quit == False):
        val = 0

        lock.acquire()

        val = cmdHandler.value
        lock.release()

        if (val != 0):
            print("value is: %d" % val)

        time.sleep(0.5)

    cmdHandler.join()
