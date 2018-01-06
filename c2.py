# client
# coding:utf-8  
  
import socket
import rsa

# load公钥和密钥
with open('public.pem') as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)

with open('private.pem') as privatefile:
    p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)

# 用公钥加密,用私钥签名认证
message = 'hello,server'
abstract = 'client'
crypto = rsa.encrypt(message, pubkey)
signaturec = rsa.sign(abstract, privkey, 'SHA-1')
# message = rsa.decrypt(crypto, privkey)
# print message
 
address = ('127.0.0.1', 13150)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect(address)    
data = s.recv(512)   
signatures= s.recv(512)
s.send(crypto)
s.send(signaturec)     
s.close() 

# print data

# 用私钥解密,用公钥验证签名
message = rsa.decrypt(data, privkey)
r = rsa.verify('server',signatures, pubkey)
print r
print  'server:',message