import sys
import time
from subprocess import Popen, PIPE
from threading import Thread, Condition
from queue import Queue
import jieba
import logging
jieba.setLogLevel(logging.INFO)

time_interval = 0.37

fast_show_letters = set([' ', '#'])

def slow_show(text, interval=time_interval):
    for letters in jieba.cut(text):
        print(letters, end = "")
        sys.stdout.flush()
        sleep_time = interval
        if letters in fast_show_letters:
            sleep_time = interval / 3
        time.sleep(sleep_time)

def stdout_reader(pipe, queue):
    try:
        with pipe:
            for char in iter(lambda: pipe.read(1), b''):
                queue.put(("output", 0, char))
    finally:
        queue.put(None)

global_cond = Condition()
input_cond = Condition()

def CondNotify(cond):
    time.sleep(time_interval / 4)
    cond.acquire()
    cond.notify()
    cond.release()


def CondWait(cond):
    cond.acquire()
    cond.wait()
    cond.release()


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
                        CondNotify(global_cond)
                    else:
                        # do nothing
                        pass
                    word += maybe_prompt
                elif char == b'.':
                    maybe_prompt = pipe.read(2)
                    if maybe_prompt == b'':
                        break
                    elif maybe_prompt == b'..':
                        CondNotify(global_cond)
                    else:
                        # do nothing
                        pass
                    word += maybe_prompt
                queue.put(("output", 0, word))
    finally:
        queue.put(None)

def output(queue):
    for data_type, display_interval, line in iter(queue.get, None):
        if data_type == "input":
            slow_show(line.decode(), display_interval)
            CondNotify(input_cond)
        elif data_type == "output":
            print(line.decode(), end="")
            sys.stdout.flush()
        else:
            raise NotImplementedError

# using option -c "import sys" to disable verbose
process = Popen(['python3', '-i', '-c', "import sys"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
queue = Queue()
stdout_thread = Thread(target=stdout_reader, args=[process.stdout, queue])
stderr_thread = Thread(target=stderr_reader, args=[process.stderr, queue])
display_thread = Thread(target=output, args=[queue])
stdout_thread.start()
stderr_thread.start()
display_thread.start()

def Interpret(expr, interval=time_interval):
    expr = expr.encode()
    queue.put(("input", interval, expr))
    CondWait(input_cond)
    process.stdin.write(expr)
    process.stdin.flush()
    CondWait(global_cond)

time.sleep(time_interval * 2)

for line in sys.stdin:
    Interpret(line)

Interpret("# Thanks for watching. Produced by https://github.com/Oneflow-Inc/oneflow\n", 0.1)
Interpret("\n")

process.stdin.close()
process.terminate()
stdout_thread.join()
stderr_thread.join()
display_thread.join()
print("")
