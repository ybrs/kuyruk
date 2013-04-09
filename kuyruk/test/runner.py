import os
import sys
import subprocess
from time import time, sleep
from subprocess import PIPE, Popen
from threading  import Thread


class Kopen(Popen):
    
    def __init__(self, args, bufsize=0, executable=None, stdin=None,
                 stdout=None, stderr=None, preexec_fn=None, close_fds=False,
                 shell=False, cwd=None, env=None, universal_newlines=False,
                 startupinfo=None, creationflags=0):
        super(Kopen, self).__init__(args, bufsize, executable, stdin, stdout,
                                    stderr, preexec_fn, close_fds, shell, cwd,
                                    env, universal_newlines, startupinfo,
                                    creationflags)

    def expect(self, s):
        pass

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

p = Popen(['myprogram.exe'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

# ... do other things here

# read line without blocking
try:  line = q.get_nowait() # or q.get(timeout=.1)
except Empty:
    print('no output yet')
else: # got line
# ... do something with line





def start_process(name, cmd, first_line):
    print 'Starting %s...' % name
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(SERVER_STARTUP_WAIT_TIME)
    out = p.stdout.readline()
    print out
    assert first_line in out, p.stdout.read(-1)
    return p


def run_test_program():
    print 'immediate'
    print 'immediate'
    sleep(1)
    print 'after 1 second'
    sleep(10)


def _time(s=''):
    global start
    now = time()
    print s, now - start
    start = now

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_test_program()
    else:
        start = time()
        p = subprocess.Popen([
            sys.executable,
            os.path.abspath(__file__),
            'test',
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        _time('subprocess')
        # print p.stdout.readline()
        # _time('readline')
        while 1:
            print p.stdout.read(1)
            _time('read -1')
