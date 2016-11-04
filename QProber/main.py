#!/usr/bin/python

import sys

from QProber import QProber

import argparse

def main():
    try:
        api = sys.argv[1]
        ts = float(sys.argv[2])
        tc = int(sys.argv[3])
        host = sys.argv[4]
    except:
        print 'usage:\n\t'+sys.argv[0]+' <API> <t_es> <t_ec> <host>'
        sys.exit(1)
    qp = QProber(bingApiKey=api)
    qp.probe(host,ts, tc)
    qp.writeContentSummaries(host)

if __name__ =='__main__' :
    main()

