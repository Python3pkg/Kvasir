# encoding: utf-8

__version__ = "1.0"

"""
##--------------------------------------#
## Kvasir
##
## (c) 2010-2014 Cisco Systems, Inc.
## (c) 2015 Kurt Grutzmacher
##
## Skaldship Nessus Module Library
##
## Author: Kurt Grutzmacher <grutz@jingojango.net>
##--------------------------------------#
"""

__all__ = ["hosts", "vulns", "plugins"]

from gluon import current


##-------------------------------------------------------------------------
def nessus_get_config():
    """
    Returns a dict of Nessus configuration settings based on yaml
    """

    nessus_config = current.globalenv['settings']['kvasir_config'].get('nessus') or {}
    config = {}
    config['ignored_plugins'] = nessus_config.get('ignored_plugins', [19506, 11219, 34277])
    config['servers'] = {}
    for server in nessus_config.get('servers'):
        for k,v in server.items():
            config['servers'][k] = {
                'url': v.get('url', 'http://localhost:8834/'),
                'user': v.get('user'),
                'password': v.get('password'),
                'access_key': v.get('access_key'),
                'secret_key': v.get('secret_key'),
                'verify_ssl': v.get('verify_ssl'),
                'proxies': v.get('proxies'),
                'version': v.get('version', 6)
            }

    return config

