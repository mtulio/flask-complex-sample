import time

class Tasks():

    def run_sleep15(*args, **kwargs):
        print("Task #run_sleep15 started!")
        print(repr(args))
        print(repr(kwargs))

        time.sleep(15)
        print("Task #run_sleep15 is done!")
        return True


    def run_sleep30(*args, **kwargs):
        print("Task #run_sleep30 started with args: ")
        print(repr(args))
        print(repr(kwargs))

        time.sleep(5)
        print("Task #run_sleep30 is done!")
        return True
