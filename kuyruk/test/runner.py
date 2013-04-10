import os
import sys
import subprocess
from time import time, sleep
from threading import Thread
from Queue import Queue, Empty
from subprocess import PIPE, STDOUT


class Popen(subprocess.Popen):
    """Adapted from: http://stackoverflow.com/a/4896288/242451"""

    def __init__(self, *args):
        super(Popen, self).__init__(
            args, stdout=PIPE, stderr=STDOUT,
            bufsize=1, close_fds=True)
        self.queue = Queue()
        self.reader = Thread(target=self.enqueue_output)
        self.reader.daemon = True
        self.reader.start()

    def enqueue_output(self):
        for line in iter(self.stdout.readline, b''):
            self.queue.put(line)
        self.stdout.close()

    def expect(self, s, timeout=10):
        start = time()
        try:
            while 1:
                passed = time() - start
                line = self.queue.get(timeout=timeout - passed)
                if s in line:
                    return line
        except Empty:
            raise Exception('Expected %r but not found' % s)

    def expect_exit(self, exit_code):
        self.wait()
        if self.returncode != exit_code:
            raise Exception('Expected exit(%i) but received exit(%i)' %
                            (exit_code, self.returncode))


class Unbuffered(object):
    """http://stackoverflow.com/a/107717/242451"""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def run_test_program():
    sys.stdout = Unbuffered(sys.stdout)
    print 'immediate'
    sleep(1)
    print 'after 1 second'
    sleep(3)
    print 'after 3 seconds'
    print 'bye'
    sys.exit(2)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_test_program()
    else:
        k = Popen(
            sys.executable,
            os.path.abspath(__file__),
            'test')
        print k.expect('imm', 2)
        print k.expect('1 sec', 1.1)
        print k.expect('seconds', 3.1)
        try:
            print k.expect('oh no', 1)
        except Exception:
            print 'raised exception'
        k.expect_exit(2)
