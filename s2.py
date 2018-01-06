# server
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
reply = 'hi,client'
abstract = 'server'
crypto = rsa.encrypt(reply, pubkey)
signatures = rsa.sign(abstract, privkey, 'SHA-1')
  
address = ('127.0.0.1', 13150)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
s.bind(address)  
s.listen(5)
print 'waiting for connection' 

conn, addr = s.accept()  
print 'got connected from',addr  
conn.send(crypto)  
conn.send(signatures)
ra = conn.recv(512)  
signaturec = conn.recv(512)

conn.close()  
s.close()


# 用私钥解密、用公钥验证签名
message = rsa.decrypt(ra, privkey)
r = rsa.verify('client',signaturec, pubkey)
print r
print  'client:',message