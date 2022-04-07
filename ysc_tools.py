from .tools import genuuid,calc_md5,write_to_ipfs,load_from_ipfs
from .tools import setipfs as set_ipfs
import json
import os
import time
import requests
import rsa
from .rsa_sign import sign_trade,verify_trade,verify_key_pair
import base64



class ysc:
    def __init__(self,publickey,privatekey,ysc_gateway_url):
        self.address = publickey
        self.ysc_gateway_url = ysc_gateway_url
        self.publickey = rsa.PublicKey.load_pkcs1(load_from_ipfs(publickey))
        self.privatekey = rsa.PrivateKey.load_pkcs1(load_from_ipfs(privatekey))
        if verify_key_pair(self.publickey,self.privatekey) != True:
            raise rsa.VerificationError()
        r = self.getuserinfo()

    @staticmethod
    def setipfs(api,gateway):
        set_ipfs(api,gateway)

    @staticmethod
    def settimezone(timezone):
        os.environ['TZ'] = timezone
        time.tzset()

    def getuserinfo(self):
        url = self.ysc_gateway_url + "/api/v1/getuserinfo"
        data = {"uid":self.address}
        r = requests.post(url,data=data)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        self.username = ret["username"]
        self.account_data = ret["account_data"]
        self.balance = ret["balance"]
        self.role = ret["role"]
        self.balance = ret["balance"]
        return ret
    
    def getbalance(self):
        url = self.ysc_gateway_url + "/api/v1/getbalance"
        data = {"uid":self.address}
        r = requests.post(url,data=data)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        self.balance = ret["balance"]
        return ret["balance"]
        
    def getheadblock(self):
        url = self.ysc_gateway_url + "/api/v1/getheadblock"
        r = requests.get(url)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret
    
    def getblock(self,cid):
        url = self.ysc_gateway_url + "/api/v1/getblock"
        r = requests.get(url,data={"cid":cid})
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def gettrade(self,cid,offset):
        url = self.ysc_gateway_url + "/api/v1/gettrade"
        r = requests.post(url,data={"cid":cid,"offset":offset})
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def getusertrade(self,depth=20):
        url = self.ysc_gateway_url + "/api/v1/getusertrade"
        r = requests.post(url,data={"uid":self.address,"depth":depth})
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def createdeal(self,to,value,content={"cipher":None,"msg":"Transfer"},tax=0,strict_waiting = False):
        transfer = {
            "from": self.address,
            "to": to,
            "type":"Send",
            "timestamp":int(time.time()),
            "tax":int(abs(tax)),
            "value":int(value),
            "content":content
        }
        if self.balance < transfer["value"] + transfer["tax"] and self.role not in [0]:
            raise Exception("Insufficient Balance")
        if transfer["value"] < 0 and self.role not in [0,4]:
            raise Exception("value can't be negative")
        signed_transfer = sign_trade(transfer,self.privatekey)
        json_transfer = json.dumps(signed_transfer)

        r = requests.post(self.ysc_gateway_url+"/api/v1/createdeal",data={"data":str(base64.b64encode(json_transfer.encode()),'utf-8')})
        output = r.json()
        if output["status"] == False:
            raise Exception("Create Deal Failed: "+output["msg"])
        else:
            return output

    def createuser(self,rsa_bits=4096,role=1,username=None,tax=0,strict_waiting = False):
        if username is None:
            username = genuuid()
        newkeys = rsa.newkeys(rsa_bits,poolsize=max(1,os.cpu_count()-1))
        publickey = newkeys[0]
        privatekey = newkeys[1]
        if verify_key_pair(publickey,privatekey) != True:
            raise rsa.VerificationError()
        new_publickey_cid = write_to_ipfs(str(publickey.save_pkcs1(),'utf-8'),cid_version=1)
        new_privatekey_cid = write_to_ipfs(str(privatekey.save_pkcs1(),'utf-8'),cid_version=0)
        msg = str(base64.b64encode(json.dumps({"username":username,"publickey":new_publickey_cid,"role":role}).encode()),'utf-8')
        transfer = {
            "from": self.address,
            "to": new_publickey_cid,
            "type":"NewAccount",
            "timestamp":int(time.time()),
            "tax":int(abs(tax)),
            "value":0,
            "content":{
                "cipher":None,
                "msg":msg
            }
        }
        signed_transfer = sign_trade(transfer,self.privatekey)
        json_transfer = json.dumps(signed_transfer)

        r = requests.post(self.ysc_gateway_url+"/api/v1/createuser",data={"data":str(base64.b64encode(json_transfer.encode()),'utf-8')})
        output = r.json()
        if output["status"] == False:
            raise Exception("Create Account Failed: "+output["msg"])
        else:
            return {
                "publickey":new_publickey_cid,
                "privatekey":new_privatekey_cid,
                "username":username
            }     
