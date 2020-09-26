import sys
import time
from subprocess import Popen, PIPE
from threading import Thread, Condition
from queue import Queue
import jieba
import logging
jieba.setLogLevel(logging.INFO)

time_interval = 0.333

def slow_show(text, interval=time_interval):
    for letters in jieba.cut(text):
        print(letters, end = "")
        sys.stdout.flush()
        time.sleep(interval)

def stdout_reader(pipe, queue):
    try:
        with pipe:
            for line in iter(lambda: pipe.readline(), b''):
                queue.put(("output", line))
    finally:
        queue.put(None)

global_cond = Condition()

def stderr_reader(pipe, queue):
    try:
        with pipe:
            for char in iter(lambda: pipe.read(1), b''):
                word = char
                if char == b'>':
                    maybe_prompt = pipe.read(2)
                    if maybe_prompt == b'':
                        break
                    elif maybe_prompt == b'>>':
                        time.sleep(time_interval)
                        global_cond.acquire()
                        global_cond.notify()
                        global_cond.release()
                    else:
                        # do nothing
                        pass
                    word += maybe_prompt
                elif char == b'.':
                    maybe_prompt = pipe.read(2)
                    if maybe_prompt == b'':
                        break
                    elif maybe_prompt == b'..':
                        time.sleep(time_interval)
                        global_cond.acquire()
                        global_cond.notify()
                        global_cond.release()
                    else:
                        # do nothing
                        pass
                    word += maybe_prompt
                queue.put(("output", word))
    finally:
        queue.put(None)

def output(queue):
    terminal_flag = False
    for data_type, line in iter(queue.get, None):
        if data_type == "input":
            slow_show(line.decode())
        elif data_type == "output":
            #if terminal_flag == False:
            print(line.decode(), end="")
        elif data_type == "halt":
            terminal_flag = True
        else:
            raise NotImplementedError

process = Popen(['python3', '-i'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
queue = Queue()
stdout_thread = Thread(target=stdout_reader, args=[process.stdout, queue])
stderr_thread = Thread(target=stderr_reader, args=[process.stderr, queue])
display_thread = Thread(target=output, args=[queue])
stdout_thread.start()
stderr_thread.start()
display_thread.start()

def Interpret(expr):
    expr = expr.encode()
    queue.put(("input", expr))
    process.stdin.write(expr)
    process.stdin.flush()
    global_cond.acquire()
    global_cond.wait()
    global_cond.release()
    time.sleep(time_interval)

time.sleep(time_interval * 2)

for line in sys.stdin:
    Interpret(line)

queue.put(("halt", True))

process.stdin.close()
process.terminate()
stdout_thread.join()
stderr_thread.join()
display_thread.join()
process.wait(timeout=time_interval)

slow_show("# Thanks for watching\n", interval=0.1)
time.sleep(time_interval * 10)
