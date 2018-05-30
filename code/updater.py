import time
def updater(*args):
    now = time.time()
    ts = time.strftime('%H:%M:%S',time.localtime(now))
    print("Update at",ts)
    for arg in args:
        print(arg)
    print()
    return
