import requests
import sys
import os
import json
import rsa
import base64
import argparse
import tools
import time
import rsa_sign
import configloader
parse = argparse.ArgumentParser(prog="Yeaosound Chain Create Deals.", description="Create deals on Yeaosound Chain.")
parse.add_argument("-p", "--publickey", help="Public address cid", required=True,type=str)
parse.add_argument("-k", "--privatekey", help="Private Key cid", required=True,type=str)
parse.add_argument("-d", "--destination", help="Destination", required=True,type=str)
parse.add_argument("-v", "--value", help="Value", required=True,type=int)
parse.add_argument("-t","--tax", help="Tax", default=0, type=int)
parse.add_argument("-m","--message", help="Message", default="Transfer", type=str)
arg = parse.parse_args()
c = configloader.config()

os.environ['TZ'] = c.getkey("timezone")
time.tzset()

publickey = rsa.PublicKey.load_pkcs1(tools.load_from_ipfs(arg.publickey))
privatekey = rsa.PrivateKey.load_pkcs1(tools.load_from_ipfs(arg.privatekey))
try:
    if rsa.verify(arg.destination.encode(),rsa.sign(arg.destination.encode(), privatekey, 'SHA-1'),publickey) != "SHA-1":
        print("Key is not paired.")
        sys.exit(1)
except rsa.VerificationError:
    print("Key is not paired.")
    sys.exit(1)

transfer = {
    "from": arg.publickey,
    "to": arg.destination,
    "type":"Send",
    "timestamp":int(time.time()),
    "tax":int(arg.tax),
    "value":arg.value,
    "content":{
        "cipher":None,
        "msg":arg.message
    }
}
signed_transfer = rsa_sign.sign_trade(transfer,arg.privatekey)
json_transfer = json.dumps(signed_transfer)

r = requests.post(c.getkey("ysc_gateway_url")+"/api/v1/createdeal",data={"data":str(base64.b64encode(json_transfer.encode()),'utf-8')})
output = r.json()
if output["status"] == False:
    print("Create deal Failed: "+output["msg"])
else:
    print("Create deal Success.")
