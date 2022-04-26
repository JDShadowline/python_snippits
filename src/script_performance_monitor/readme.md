# Python script time logging
_Performance monitor for script timing_

>Usage:
>       
>       import performance_monitor as pf
>       import time
>
>       start = pf.time_start()
>       *Code to run*
>       time.sleep(30) ## Timer for testing
>       stop = pf.time_stop()
>
>       time_elapsed = pf.time_elapsed(start,stop)
>       print(time_elapsed)
>
>Returns:
>
>>```0 hours, 0 minutes, 30 seconds```
>