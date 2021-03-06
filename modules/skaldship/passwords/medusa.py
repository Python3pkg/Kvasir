# encoding: utf-8

__version__ = "1.0"

"""
##--------------------------------------#
## Kvasir
##
## (c) 2010-2014 Cisco Systems, Inc.
##
## Medusa password functions
##
## Author: Kurt Grutzmacher <grutz@jingojango.net>
##--------------------------------------#
"""

from skaldship.passwords.utils import lookup_hash
from skaldship.log import log
import logging


##-------------------------------------------------------------------------
def process_medusa(line):
    """
    Process a medusa line and return a dictionary

    :param line: A line from a medusa output file
    :returns dict: A dictionary based upon the content
    { 'ip'  : ip address
      'port': port info - can be port # or module name
      'user': username,
      'pass': password,
      'hash': ntlm hash if smbnt hash used
      'msg' : status message
    }

    >>> process_medusa("# Medusa v.2.0a_rc1 (2012-12-06 10:44:10)")
    {}
    >>> process_medusa("ACCOUNT FOUND: [smbnt] Host: 10.89.172.23 User: spauser Password: password [SUCCESS]")
    {'ip': '10.89.172.23', 'error': False, 'user': 'spauser', 'pass': 'password', 'msg': '[SUCCESS]', 'type': 'cleartext', 'port': '[smbnt]'}
    >>> process_medusa("ACCOUNT FOUND: [smbnt] Host: 10.89.172.24 User: spauser Password: AAD3B435B51404EEAAD3B435B51404EE:31D6CFE0D16AE931B73C59D7E0C089C0::: [SUCCESS]")
    {'ip': '10.89.172.23', 'port': 'smbnt', 'user': 'spauser', 'password': '', 'hash': 'AAD3B435B51404EEAAD3B435B51404EE:31D6CFE0D16AE931B73C59D7E0C089C0', 'msg': '[SUCCESS]'}
    """
    retval = {}

    try:
        data = line.split()
    except Exception, e:
        log("Error processing medusa line: %s -- %s" % (e, line), logging.ERROR)
        return retval

    if " ".join(data[:2]) == "ACCOUNT FOUND:":
        retval['port'] = data[2]
        retval['ip'] = data[4]
        retval['user'] = data[6]

        if retval['user'] == "Password:":
            # no username provided, adjust the field modulator cap'n
            retval['user'] = None
            retval['pass'] = data[7]
            retavl['msg'] = " ".join(data[9:])
        elif data[7] == "Password:" and data[8][0] == '[':
            # so this will break if the password starts with "[" however there's no
            # better way I can think of to detect a blank password w/o regex. Other
            # ideas are welcome! data[8] will be the response message which could be
            # [SUCCESS] or [ERROR ...] or something else..
            retval['pass'] = ""
            retval['msg'] = " ".join(data[8:])
        else:
            # Standard password and message location
            retval['pass'] = data[8]
            retval['msg'] = " ".join(data[9:])

        if len(retval['pass']) == 68 and retval['pass'][65:68] == ":::":
            # we have an ntlm hash cap'n
            retval['hash'] = ":".join(retval['pass'].split(':')[:2])
            retval['pass'] = lookup_hash(retval['hash'])
            retval['type'] = 'smb'
        else:
            retval['type'] = 'cleartext'

        if retval['msg'].startswith("[SUCCESS"):
            retval['error'] = False
        else:
            retval['error'] = True

    return retval


##-------------------------------------------------------------------------
def _doctest():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _doctest()
                   
