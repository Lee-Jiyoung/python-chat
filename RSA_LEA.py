import ast
import LEA
import os,datetime,secrets
from random import random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_PEM_key():
    module_length = 2048
    private_key = RSA.generate(module_length)
    public_key = private_key.publickey().export_key("DER")
    return private_key,public_key

def generate_lea_key():
    lea_key = secrets.token_bytes(32)
    return lea_key

def encrython_rsa(lea_key,public_key):
    public_key = RSA.import_key(public_key)
    encrypto = PKCS1_OAEP.new(public_key)
    encrypted = encrypto.encrypt(lea_key)
    return encrypted

def decythion_rsa(private_key,lea_key):
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(ast.literal_eval(str(lea_key)))
    return decrypted

def encryption_LEA(pt, lea_key):
    leaECB = LEA.ECB(LEA.ENCRYPT_MODE,lea_key,True)
    ct = leaECB.update(pt)
    ct += leaECB.final()
    return ct

def decryption_LEA(ct,lea_key):
    leaECB = LEA.ECB(LEA.DECRYPT_MODE,lea_key,True)
    pt = leaECB.update(ct)
    pt+=leaECB.final()
    pt = pt.decode()
    return pt


        