import os
import sys
import time
import jieba
import logging
jieba.setLogLevel(logging.INFO)

time_interval = 0.333

def slow_show(text, interval=time_interval):
    for letters in jieba.cut(text):
        print(letters, end = "")
        sys.stdout.flush()
        time.sleep(interval)

for line in sys.stdin:
    print("[code_film@oneflow ]$", end=" ")
    slow_show(line)
    os.system(line)
