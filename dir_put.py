# Code borrowed from Thorsten Simons (sw@snomis.de)
#
# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014-2016 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import sys
from os.path import normpath
from pprint import pprint
import hcpsdk

# HCP Connection details - you'll need to adopt this to your environment!
# -- primary HCP
P_FQDN = 'ns01.code1.hcpvm-dr.gssdallas.com'
P_USER = 'admin'
P_PASS = 'P@ssword'
P_PORT = 443
# -- file to be used for the test (read-only)
P_FILE = normpath('file02.txt')
# -- debug mode
P_DEBUG = True

if __name__ == '__main__':
    # end sample block 10
    # start sample block 15
    if P_DEBUG:
        import logging
        logging.basicConfig(level=logging.DEBUG,
                            style='{', format='{levelname:>5s} {msg}')
        # noinspection PyShadowingBuiltins
        print = pprint = logging.info
    # end sample block 15
    # noinspection PyUnboundLocalVariable
    print('running *simple_primary_only.py*')

    # start sample block 17
    # Setup an authorization object:
    auth = hcpsdk.NativeAuthorization(P_USER, P_PASS)
    print('*I_NATIVE* authorization initialized')
    print('')
    # end sample block 17

    # start sample block 20
    # Setup an HCP Target object:
    try:
        t = hcpsdk.Target(P_FQDN, auth, port=P_PORT)
    except hcpsdk.HcpsdkError as e:
        sys.exit('init of *Target* failed - {}'.format(e))
    else:
        print('Target *t* was initialized with IP addresses: {}'
              .format(t.addresses))
    # end sample block 20

    # start sample block 30
    # Setup a Connection object:
    try:
        c = hcpsdk.Connection(t)
    except hcpsdk.HcpsdkError as e:
        sys.exit('init of *Target* failed - {}'.format(e))
    else:
        print('Connection *c* uses IP address: {}'.format(c.address))
        print('')
        # end sample block 30


        path='code1'

        for filename in os.listdir(path):
            P_FILE=os.path.join(path, filename)

            # start sample block 40
            # Ingest an object:
            try:
                with open(P_FILE, 'r') as infile:
                    r = c.PUT('/rest/'+P_FILE,
                              body=infile,
                              params={'index': 'true', 'shred': 'true'})
            except hcpsdk.HcpsdkTimeoutError as e:
                sys.exit('PUT timed out - {}'.format(e))
            except hcpsdk.HcpsdkError as e:
                sys.exit('PUT failed - {}'.format(e))
            except OSError as e:
                sys.exit('failure on {} - {}'.format(P_FILE, e))
            else:
                if c.response_status == 201:
                    print('PUT Request was successful')
                    print('used IP address: {}'.format(c.address))
                    print('hash = {}'.format(c.getheader('X-HCP-Hash')))
                    print('connect time:     {:0.12f} seconds'
                          .format(c.connect_time))
                    print('Request duration: {:0.12f} seconds'
                          .format(c.service_time2))
                    print('')
                else:
                    sys.exit('PUT failed - {}-{}'.format(c.response_status,
                                                         c.response_reason))
            # end sample block 40

    # start sample block 70
    # Close the Connection:
    finally:
        # noinspection PyUnboundLocalVariable
        c.close()
        # end sample block 70
