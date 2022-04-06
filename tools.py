# Tools of Yeaosound-Chain

import importlib
import os
import sys
import time
import json
import subprocess
import logging
import configloader
import requests
import rsa
import uuid
c = configloader.config()

def genuuid()->str:
    """
    Generate an uuid.
    """
    ouid = uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))
    okey = str(ouid)
    return okey

def calc_md5(string:str)->str:
    """
    Calculate the md5 of the string.
    """
    import hashlib
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val

def write_to_ipfs(string:str,cid_version=0)->str:
    """
    Write the string to ipfs and return its CID.
    """
    ret = requests.post(url=c.getkey("ipfs_api")+"/api/v0/add?pin=true&cid-version="+str(cid_version),files={'file':string})
    cid = ret.json()["Hash"]
    return cid

def load_from_ipfs(cid:str)->str:
    """
    Load the content of the cid from ipfs.
    """
    res = requests.get(url=c.getkey("ipfs_gateway")+"/ipfs/"+cid,timeout=60)
    
    return res.text

