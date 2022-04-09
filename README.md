# Yeaosound Chain Python SDK

### Installation:

    Clone this Repositories and rename this folder to "ysc2"


<br/>

------------

<br/>

### Setup:


```python
from ysc2 import ysc
ysc.settimezone("Asia/Shanghai")
ysc.setipfs(api="http://127.0.0.1:5010",gateway="http://127.0.0.1:8080")
# Setting IPFS environment is required.
# Timezone should be the same as the server. If the time is wrong, the server would not accept deals.
```

<br/>

------------

<br/>

### Usage:

#### Login an new account:
```python
user = ysc(publickey="bafkreixxxxxxxxxxxxxxxxxx",privatekey="Qmxxxxxxxxxxxxxxxx",ysc_gateway_url="https://finance-v2.yeaosound.com")
```
<br/>

#### Get balance from local cache:
```python
user.balance
```
##### return balance(int):
```python
0
```

<br/>

#### Get balance from Chain:
```python
user.getbalance()
```
##### return balance(int):
```python
0
```

<br/>

#### Get account address:
```python
user.address
```

##### return address(str):
```python
'bafkreixxxxxxxxxxxxxxxxxx'
```

<br/>

#### Get role:
```python
user.role
```
##### return role(int):
```python
0
# 0:superadmin
# 1:user
# 2:node
# 3:admin
# 4:finance
```
<br/>

#### Get account data(for nextcloud and others):
```python
user.account_data
```

##### return account_data(str):

<br/>


#### load user info from chain:
```python
user.getuserinfo()
```

##### return user_info(dict):

```python
{
    'status': True,
    'username': "username",
    "account_data": "account_data",
    'balance': 0,
    "last_addr": "Qmxxxx|0",
    "first_addr": "Qmxxxx|0,
    "role": 0,
}
```

<br/>

#### Get Head Block:
```python
user.getheadblock()
```

##### return headblock cid and data(dict):
```python
{
    "status":True,
    "data": {
        "block": "Qmxxxx",
        "data": {
            # block details here
        }}
}
```

<br/>

#### Get Block:
```python
user.getblock(cid="Qmxxxx")
```

##### return block data(dict):
```python
{
    "status":True,
    "this_block": {
        # block details here
    }
}
```

<br/>

#### Get Transfer by cid and offset:
```python
user.gettrade(cid="Qmxxxx",offset=0)
```

##### return trade data(dict):
```python
{
    "status":True,
    "this_block": {
        # block details here, would be deprecated in future version.
    },
    "this_transfer": {
        # transfer details here
    }
}
```

#### Get history trades for user:
```python
user.getusertrade(depth=20) 
#if depth not set, default is 20.
```
##### return trade list(dict):
```python
{
    "status":True,
    "username": "username",
    "transfers": [
        {
            # transfer details here
        },
        {
            # transfer details here
        }
    ]
}
```

#### create deal:
```python
user.createdeal(to="bafkreixxxxxxxxxxxxxxxxxx",value=114514,content={"cipher":None,"msg":"Transfer"},tax=0,strict_waiting = False)
# to:address for receive
# value:int, the amount of coin to transfer
# content:dict, the content of deal, should be a dict, default is {"cipher":None,"msg":"Transfer"}
# tax:int, the tax of deal, should be a int, default is 0
# strict_waiting:bool, if set to True, the deal would be created and waiting for confirm, if set to False, the deal would be created and do not wait for it to be confirmed, default value is False
```
##### if strict_waiting is True, return deal cid(dict):
```python
{
    "status":True,
    "block_cid":"Qmxxxx|0"
}
```
##### else only return true and message(dict):
```python
{
    "status":True,
    "message":"success"
}
```

#### create user:
```python
user.createuser(rsa_bits=4096,role=1,username=None,tax=0,strict_waiting = False)
# rsa_bits:int, the bits of rsa key, default is 4096, the key would be generated automatically.
# role:int, the role of user, default is 1, 0:superadmin, 1:user, 2:node, 3:admin, 4:finance
# username:str, the username of user, default is None, if set to None, the username would be generated automatically.
# tax:int, the tax of deal, default is 0
# strict_waiting:bool, if set to True, the deal would be created and waiting for confirm, if set to False, the deal would be created and do not wait for it to be confirmed, default value is False
```
##### if strict_waiting is True, return deal cid, username and key pairs(dict):
```python
{
    "status":True,
    "block_cid":"Qmxxxx|0",
    "publickey":"bafkreixxxxxxxxxxxxxxxxxx",
    "privatekey":"Qmxxxxxxxxxxxxxxxx",
    "username":"username"
}
```
##### else only return true , message, username and key pairs(dict):
```python
{
    "status":True,
    "message":"success",
    "publickey":"bafkreixxxxxxxxxxxxxxxxxx",
    "privatekey":"Qmxxxxxxxxxxxxxxxx",
    "username":"username"
}
```


--------

# Enjoy Use