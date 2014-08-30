#!/usr/bin/env python2

from argparse import ArgumentParser
from threading import Thread as Process
from Queue import Queue
from itertools import islice

_MAX_QUEUE_SIZE = 10000


def write_multithread(iterator, write_func, path_fmt, n=8):
    """Write items to multiple files.

    """
    item_queue = Queue(maxsize=_MAX_QUEUE_SIZE)
    load_proc = Process(target=_load_to_queue,
                        args=(iterator, item_queue))
    write_procs = []
    write_handles = []
    for i in range(n):
        outpath = path_fmt % i
        handle = open(outpath, 'w')
        write_handles.append(handle)
        write_procs.append(Process(target=_write_from_queue,
                                   args=(write_func, item_queue, handle)))
    load_proc.start()
    for proc in write_procs:
        proc.start()
    load_proc.join()
    for proc, handle in zip(write_procs, write_handles):
        proc.join()
        handle.close()


def _load_to_queue(iterator, queue):
    """Put items from iterator into queue.

    """
    for item in iterator:
        queue.put(item, block=True, timeout=None)
    queue.put(None)


def _write_from_queue(write_func, queue, handle):
    """Write items from the queue.

    """
    while True:
        item = queue.get()
        if item is None:
            queue.put(item)
            break
        write_func(item, handle)


def grouper(iterable, n):
    it = iter(iterable)
    while True:
        chunk = list(islice(it, n))
        if not chunk:
            return
        yield chunk


def get_default_argument_parser():
    parser = ArgumentParser(add_help=False)
    return parser


class Options():
    """Base class for various commandline, option interfaces."""
    def __init__(self):
        self.parser = ArgumentParser(add_help=False)

    def get_parser(self):
        return self.parser

    def process_args(self, args):
        return args


class SeqStreamOptions():
    """Base class for tools which both take and produce sequence files."""

    _DEFAULT_IN_FMT = 'fasta'
    _DEFAULT_OUT_FMT = 'fasta'

    def __init__(self):
        super(SeqStreamOptions, self).__init__()
        self.parser.add_argument('-o', '--output', nargs='?', default=None,
                                 help=("The path of the output files. "
                                       "If no path given, goes to STDOUT."))
        self.parser.add_argument('input', nargs='*', default=None,
                                 help=("The paths of the input files. "
                                       "If no path given, reads from STDIN."))
        self.parser.add_argument('--in-format',
                                 default=SeqStreamOptions._DEFAULT_IN_FMT,
                                 help=(""))


def main():
    def test_writer(item, handle):
        handle.write("%d\n" % item)

    write_multithread(range(100000), test_writer, "test%d.out", n=2)

if __name__ == "__main__":
    main()
