## performance_monitor.py
###### DESCRIPTION ######
## Python Script Timer
######
#
# 
#
#
###### IMPORTS ######
import time
###### GLOBAL VARIABLES ######

###### FUNCTIONS ######

def time_start():
    return time.perf_counter()

def time_stop():
    return time.perf_counter()

def timeelapsed(starttime, endtime):
    return time.strftime('%H hours, %M minutes, %S seconds', time.gmtime((endtime - starttime))) 

###### STANDALONE ######

def main(): ...

if __name__ == '__main__': main()