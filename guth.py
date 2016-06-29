#!/usr/bin/env python
# -*- coding: utf-8 -*-
#____________________________________________________________
#
#  Copyright 2016 bjarneh@ifi.uio.no. All rights reserved. 
#  Use of this source code is governed by a BSD-style 
#  license that can be found in the LICENSE file. 
#
#____________________________________________________________
#
# Dependencies: 
#   https://github.com/tadeck/onetimepass
#   https://github.com/jaraco/keyring
#
"""
 guth.py - google authenticator time based token

 usage: guth.py - [OPTIONS]

 options:
     -h --help     :  print this menu and exit
     -v --version  :  print version and exit
     -s --secret   :  specify secret to use (!!)
     -i --interval :  sec interval (default: 30)
     -l --length   :  token length (default: 6)
     -r --report   :  print keyring secret (!!)
     -d --delete   :  delete secret from keyring
"""

import sys
import time
import getopt
import keyring
import onetimepass

# Globals

__version__  = 1.0
__author__   = 'bjarneh@ifi.uio.nö́'
__license__  = 'BSD'

# They keyring library requires a 'service_name' and a 'user_name'
# although it just seems to create it's own label based on these,
# but the names chosen here make sense I guess, this will be the
# resulting label when viewed:
#
#    Password for 'guth.py' on 'localhost'
#
# which should be understandable by someone owning the keyring?


USER     = 'guth.py'    # These are choosen almost at random, see above
SERVICE  = 'localhost'  # These are choosen almost at random, see above 
INTERVAL = 30           # We default to 30 seconds
TOKENLEN = 6            # We default to a 6 digit token
SECRET   = None         # This should be store in keyring


def niceopt(argv, short_opts, long_opts):
    """ Allow long options which start with a single '-' sign"""
    for i, e in enumerate(argv):
        for opt in long_opts:
            if( e.startswith("-" + opt) or
              ( e.startswith("-" + opt[:-1]) and opt[-1] == "=") ):
                argv[i] = "-" + e
    return getopt.gnu_getopt(argv, short_opts, long_opts)


def pass_loop(interval, secret, tok_len):
    """ 
    Print google authenticator time-based-token once every interval,
    based on the given secret and token length
    """
    cnt = long(time.time()) % interval
    sin = str(interval)
    siz = len(sin)
    fmt = "  code: %0"+str(tok_len)+"d [%0"+ str(siz) +"d/"+ sin +"]\r"
    pw  = None
    while True:
        if cnt == 0 or pw is None:
            pw = onetimepass.get_totp(secret, token_length=tok_len,
                                      interval_length=interval)
        sys.stdout.write(fmt % (pw, cnt) )
        sys.stdout.flush()
        time.sleep(1)
        cnt = ((cnt + 1) % interval)


def delete_secret_from_keyring():
    """ Remove my current secret stored for guth.py"""
    global SERVICE, USER
    return keyring.delete_password(SERVICE, USER)


def get_secret_from_keyring():
    """ Return users secret from keyring"""
    global SERVICE, USER
    return keyring.get_password(SERVICE, USER)


def get_secret_from_keyring_or_user():
    """ Try to find secret in keyring, or ask user for it """
    global SERVICE, USER
    secret = get_secret_from_keyring()
    if not secret:
        while not secret:
            secret = raw_input(" Type in secret (q to exit): ")
            if not secret or secret == 'q':
                raise SystemExit(0)
            else:
                keyring.set_password(SERVICE, USER, secret)
    return secret


def main(argv=sys.argv):
    """ Entry point, parse arguments start loop or give error feedback """

    global SECRET, INTERVAL, TOKENLEN

    try:

        (opts, args) = niceopt(argv[1:], "hvrdi:s:l:",
                               ['help', 'version','report','delete',
                                'secret=','interval=', 'length='])

        for o, a in opts:
            if o in ('-h', '--help'):
                print( __doc__ );
                raise SystemExit(0)
            if o in ('-v', '--version'):
                print( "%s - %s" % (argv[0], __version__));
                raise SystemExit(0)
            if o in ('-r', '--report'):
                print( "%s" % ( get_secret_from_keyring() ));
                raise SystemExit(0)
            if o in ('-d', '--delete'):
                delete_secret_from_keyring()
                raise SystemExit(0)
            if o in ('-i', '--interval'):
                INTERVAL = int(a)
            if o in ('-l', '--length'):
                TOKENLEN = int(a)
            if o in ('-s', '--secret'):
                SECRET = a

        if not SECRET:
            SECRET = get_secret_from_keyring_or_user()

        if not SECRET:
            raise SystemExit( "No secret?" )

        pass_loop(INTERVAL, SECRET, TOKENLEN)

        raise SystemExit( 0 )

    except SystemExit, inst:
        if inst.code != 0:
            raise inst
    except KeyboardInterrupt, inst:
        sys.stdout.write("\r" + " "*80 +"\r")
    except Exception, inst:
        raise SystemExit( "[ERROR] %s\n" % inst )
    return 0


if __name__ == '__main__':
    sys.exit( main() )
