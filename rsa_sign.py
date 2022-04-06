import logging
from typing import Dict
import rsa
import base64
import json
import requests
import tools

def sign_trade(trade:Dict,cid,sign_method:str="SHA-1")->Dict:
    """
    Sign a trade with an rsa private key cid
    """
    if type(cid) is str:
        rawkey = tools.load_from_ipfs(cid)
        privkey = rsa.PrivateKey.load_pkcs1(rawkey)
    else:
        privkey = cid
    sorted_trade = dict(sorted(trade.items(), key=lambda x: x[0],reverse=False))
    encoded_trade = json.dumps(sorted_trade)
    sign = rsa.sign(encoded_trade.encode(), privkey, sign_method)
    trade["sign"] = {"data":base64.b64encode(sign).decode(),"method":sign_method}
    return trade

def verify_trade(trade:Dict,cid:str)->bool:
    """
    Verify a trade with an account cid
    """
    rawkey = tools.load_from_ipfs(cid)
    try:
        pubkey = rsa.PublicKey.load_pkcs1(rawkey)
    except ValueError:
        return False
    sign_message = trade["sign"]["data"]
    sign_method = trade["sign"]["method"]
    del trade["sign"]
    sorted_trade = dict(sorted(trade.items(), key=lambda x: x[0],reverse=False))
    encoded_trade = json.dumps(sorted_trade)
    try:
        if rsa.verify(encoded_trade.encode(), base64.b64decode(sign_message.encode()), pubkey) == sign_method:
            return True
        else:
            return False
    except rsa.VerificationError:
        return False


def verify_key_pair(publickey,privatekey)->bool:
    try:
        if type(publickey) is str:
            publickey = rsa.PublicKey.load_pkcs1(tools.load_from_ipfs(publickey))
        if type(privatekey) is str:
            privatekey = rsa.PrivateKey.load_pkcs1(tools.load_from_ipfs(privatekey))
        text = tools.genuuid()
        try:
            if rsa.verify(text.encode(),rsa.sign(text.encode(), privatekey, 'SHA-1'),publickey) != "SHA-1":
                logging.error("verify_key_pair failed. the key is not valid")
                return False
        except rsa.VerificationError:
            logging.error("verify_key_pair failed. the key is not valid")
            return False
        return True
    except:
        import traceback
        logging.error(traceback.format_exc())
        return False

        