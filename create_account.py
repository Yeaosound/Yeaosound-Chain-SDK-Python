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
parse = argparse.ArgumentParser(prog="Yeaosound Chain Create Account.", description="Create account on Yeaosound Chain.")
parse.add_argument("-u", "--username", help="Username", required=True,type=str)
parse.add_argument("-p", "--publickey", help="Public address cid", required=True,type=str)
parse.add_argument("-k", "--privatekey", help="Private Key cid", required=True,type=str)
parse.add_argument("-r", "--role", help="User Role:1 is user,2 is node,3 is admin", default=1,type=int)
#parse.add_argument("--new-publickey", help="new account public key", required=True)
#parse.add_argument("--new-privatekey", help="new account private key", required=True)
parse.add_argument("-t","--tax", help="Tax", default=0, type=int)
arg = parse.parse_args()
c = configloader.config()

os.environ['TZ'] = c.getkey("timezone")
time.tzset()

publickey = rsa.PublicKey.load_pkcs1(tools.load_from_ipfs(arg.publickey))
privatekey = rsa.PrivateKey.load_pkcs1(tools.load_from_ipfs(arg.privatekey))
try:
    if rsa.verify(arg.username.encode("utf-8"),rsa.sign(arg.username.encode('utf-8'), privatekey, 'SHA-1'),publickey) != "SHA-1":
        print("Key is not paired.")
        sys.exit(1)
except rsa.VerificationError:
    print("Key is not paired.")
    sys.exit(1)
#new_publickey = rsa.PublicKey.load_pkcs1(tools.load_from_ipfs(arg.new_publickey))
#new_privatekey = rsa.PrivateKey.load_pkcs1(tools.load_from_ipfs(arg.new_privatekey))
new_keys = rsa.newkeys(2048)
new_publickey = new_keys[0]
new_privatekey = new_keys[1]
try:
    if rsa.verify(arg.username.encode("utf-8"),rsa.sign(arg.username.encode('utf-8'), new_privatekey, 'SHA-1'),new_publickey) != "SHA-1":
        print("new Key is not paired.")
        sys.exit(1)
except rsa.VerificationError:
    print("new Key is not paired.")
    sys.exit(1)
new_publickey_cid = tools.write_to_ipfs(str(new_publickey.save_pkcs1(),'utf-8'),cid_version=1)
new_privatekey_cid = tools.write_to_ipfs(str(new_privatekey.save_pkcs1(),'utf-8'),cid_version=0)
msg = str(base64.b64encode(json.dumps({"username":arg.username,"publickey":new_publickey_cid,"role":arg.role}).encode()),'utf-8')
transfer = {
    "from": arg.publickey,
    "to": new_publickey_cid,
    "type":"NewAccount",
    "timestamp":int(time.time()),
    "tax":int(arg.tax),
    "value":0,
    "content":{
        "cipher":None,
        "msg":msg
    }
}
signed_transfer = rsa_sign.sign_trade(transfer,arg.privatekey)
json_transfer = json.dumps(signed_transfer)

r = requests.post(c.getkey("ysc_gateway_url")+"/api/v1/createuser",data={"data":str(base64.b64encode(json_transfer.encode()),'utf-8')})
output = r.json()
if output["status"] == False:
    print("Create Account Failed: "+output["msg"])
else:
    print("Create Account Success.")
    print("New Account:")
    print("Account Address: "+new_publickey_cid)
    print("Private Key: "+new_privatekey_cid)