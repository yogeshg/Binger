import sys

from BingApi import BingApi
from ContentSummaryConstructor import ContentSummaryConstructor
from QProber import QProber



def main():
    #TO DO:
    #Get input from user(t_es, t_ec, hostname)
    #Check the users input
    host = "xxx.com"
    ts = 0.6
    tc = 100
    qp = QProber()
    qp.probe(host,ts, tc)
    root = qp.r
    construct = ContentSummaryConstructor(root, host)


if __name__ =='__main__' :
    main()