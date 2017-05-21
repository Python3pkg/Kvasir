#!/usr/bin/env python
# encoding: utf-8

__version__ = "1.0"

"""
##--------------------------------------#
## Kvasir
##
## (c) 2010-2014 Cisco Systems, Inc.
## (c) 2015 Kurt Grutzmacher
##
## Create/Change password users for Kvasir
##
## Run from a shell using web2py:
##
##   ./web2py.py -R applications/$appname/private/user.py -S $appname -M -A -u username -p password
##
## Author: Kurt Grutzmacher <grutz@jingojango.net>
##--------------------------------------#
"""

import sys
import getpass
from optparse import OptionParser, OptionGroup

##--------------------------------------------------------------------

optparser = OptionParser(version=__version__)

optparser.add_option("-u", "--user", dest="user",
    action="store", default=None, help="Username")
optparser.add_option("-p", "--password", dest="password",
    action="store", default=None, help="Password")
optparser.add_option("-P", "--prompt", dest="prompt",
    action="store_true", default=False, help="Prompt for password")
optparser.add_option("-n", "--nochange", dest="nochange",
    action="store_true", default=False, help="Do not change the user information")
optparser.add_option("-f", "--force", dest="forcechange",
    action="store_true", default=False, help="Force the change of user information without prompt")
optparser.add_option("-F", "--first", dest="first",
    action="store", default="Kvasir", help="First name")
optparser.add_option("-L", "--last", dest="last",
    action="store", default="User", help="Last name")
optparser.add_option("-E", "--email", dest="email",
    action="store", default="nobody@example.com", help="E-mail Addresss")

(options, params) = optparser.parse_args()

print("\n\nKvasir User Add/Modify Management\n")
if not options.user:
    user = input("Username: ")
else:
    user = options.user

if not user:
    sys.exit("No username provided\n")

# see if the user exists first
user_row = db(db.auth_user.username == user).select().first()
if user_row:
    # user exists, update password
    if options.nochange:
        sys.exit("Not changing user...\n")
    if not options.forcechange:
        ask_update = input("User exists, update password? [y/N]: ")
        if ask_update not in ['Y', 'y'] :
            sys.exit("Ok, leaving user as-is...\n")

if not options.password or options.prompt:
    password = getpass.getpass("Password: ")
else:
    password = options.password

if not password or password == '':
    sys.exit("Password cannot be blank\n")

if user_row:
    # user exists, update password
    print(("Updating password for {0}...".format(user)))
    user_row.update(password=password)
    db.commit()

else:
    # new user
    print(("Adding {0} to Kvasir user database...".format(user)))
    ret = db.auth_user.validate_and_insert(
        username=user,
        password=password,
        first_name=options.first,
        last_name=options.last,
        email=options.email,
        registration_id=options.email
    )
    if not ret.id:
        print(("[!] Error inserting user: {0}".format(ret.errors)))

    db.commit()
