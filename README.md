# python_snippits
### Randomized assortment of helpful python snippits


### Python Library Reference
#### Pandas
_Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language._
>Installation:
>
>       pip install pandas
>
>Import/Usage:
>
>       import pandas as pd
>
>[Link to Documentation](https://pandas.pydata.org/docs/reference/index.html#api)

#### PySimpleGUI
_Python GUI For Humans - Transforms tkinter, Qt, Remi, WxPython into portable people-friendly Pythonic interfaces_
>Installation:
>
>       pip install pysimplegui
>
>Import/Usage:
>
>       import PySimpleGUI as sg
>
>[Link to Documentation](https://pysimplegui.readthedocs.io/en/latest/call%20reference/)

#### Lovely Logger
_A logger library which builds on, combines, and simplifies various logging features of Python 3_
>Installation:
>       pip install lovely-logger
>
>Import/Usage:
>
>       import lovely_logger as log
>
>       log.init('./my_log_file.log')
>
>       log.debug('here are the in-scope variables right now: %s', dir())
>       log.info('%s v1.2 HAS STARTED', __file__)
>       log.warning('here is a warning message')
>       log.error('generally you would use error for handled exceptions which prevent further execution')
>       log.critical('generally you would use critical for uncaught exceptions')
>
>[Link to Documentation](https://github.com/tier2tickets/lovely-logger)

#### Alive Progressbar
_A new kind of Progress Bar, with real-time throughput, ETA, and very cool animations!_
>Installation:
>
>       pip install alive-progress
>
>Import/Usage:
>
>       from alive_progress.styles import showtime  # Use showtime() to create a demo
>       from alive_progress import alive_bar        # Regular import
>       from alive_progress import alive_it         # Auto iterating import
>
>[Link to Documentation](https://github.com/rsalmei/alive-progress)

#### Selenium (python)
_The selenium package is used to automate web browser interaction from Python._
>Installation:
>
>       pip install selenium
>
>>Webdrivers:\
>>[Chrome: https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)\
>>[Firefox: https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)\
>>[Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)\
>>[Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)
>
>Import/Usage:
>
>>      from selenium import webdriver
>>      from selenium.webdriver.common.by import By
>>      from selenium.webdriver.common.keys import Keys
>>      from selenium.webdriver.support.ui import WebDriverWait
>>      from selenium.webdriver.support import expected_conditions as EC
>>      from selenium.webdriver.chrome.service import Service
>>      from selenium.webdriver.chrome.options import Options
>>      from selenium.webdriver.support.ui import Select
>
>[Link to Documentation](https://selenium-python.readthedocs.io/)