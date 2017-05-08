import datetime
import time

STR_FORMAT="{:%S%f}"
while (True):
    A=float(STR_FORMAT.format(datetime.datetime.today()))
    B=float(STR_FORMAT.format(datetime.datetime.today()))
    time.sleep(1)
    print(1-(A/B))
