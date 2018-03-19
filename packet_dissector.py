#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import sys
import argparse
from binascii import a2b_hex
from datetime import datetime

try:
    from pypacket_dissector import dissector as dis
except:
    import dissector as dis

def read_file(filename, verbose=False, debug=False):
    with open(filename) as f:
        data = f.buffer.read()
    #
    if verbose:
        print(dis.dissector.dump_byte(data))
    #
    ret3 = dis.dissector(data)
    print(dis.dump_pretty(ret3))

def read_stdin(filename, **kwargs):
    delimiter = kwargs.get("delimiter", b"")
    show_sep = kwargs.get("show_sep", True)
    verbose = kwargs.get("verbose", False)
    debug = kwargs.get("debug", False)
    #
    dlm = [ bytes([i]) for i in delimiter ]
    dlm_end = len(dlm) - 1
    while True:
        dlm_pos = 0
        data = bytearray()
        while True:
            b = sys.stdin.buffer.read(1)
            if dlm[dlm_pos] == b:
                if dlm_pos == dlm_end:
                    data = data[:-dlm_end]
                    break
                else:
                    dlm_pos += 1
                    data += b
                continue
            #
            dlm_pos = 0
            data += b
        #
        if verbose:
            print(dis.dump_byte(data))
        if show_sep:
            print("----", str(datetime.now()))
        ret = dis.dissector(data)
        print(dis.dump_pretty(ret))

def parse_args():
    p = argparse.ArgumentParser(description="a packet dissector.", epilog="")
    p.add_argument("target", metavar="TARGET", type=str,
                   help="""specify a filename containing
                   packet data.  '-' allows the stdin as the input.""")
    p.add_argument("--delimiter", action="store", dest="_delimiter",
                   default=dis.DELIMITER,
                   help='''specify a delimiter to read a series of data from the
                   stdin. e.g. {:s}'''.format(dis.DELIMITER))
    p.add_argument("--noshow-sep", action="store_false", dest="show_sep",
                   help="disable to show the separator.")
    p.add_argument("-v", action="store_true", dest="f_verbose",
                   help="enable verbose mode.")
    p.add_argument("-d", action="store_true", dest="f_debug",
                   help="enable debug mode.")

    args = p.parse_args()
    args.delimiter = a2b_hex(args._delimiter)
    return args

'''
main
'''
opt = parse_args()
if opt.target == "-":
    read_stdin(opt.target, delimiter=opt.delimiter, show_sep=opt.show_sep,
               verbose=opt.f_verbose, debug=opt.f_debug)
else:
    read_file(opt.target, verbose=opt.f_verbose, debug=opt.f_debug)
