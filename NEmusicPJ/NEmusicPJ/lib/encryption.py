# -*-coding:utf-8-*-
import os
import re
import sys
import json
import base64
import binascii
import hashlib
import requests
from Crypto.Cipher import AES

class CommentCrawl(object):
    '''评论的API封装成一个类，直接传入评论的API，再调用函数get_song_comment()和get_album_comment()即可分别获取歌曲和专辑的评论信息
    '''

    def __init__(self,comment_url):
        self.comment_url = comment_url
        self.headers = {
            "Referer":"http://music.163.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3067.6 Safari/537.36",
        }

    def createSecretKey(self,size):
        '''生成长度为16的随机字符串作为密钥secKey
        '''
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    def AES_encrypt(self,text, secKey):
        '''进行AES加密
        '''
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def rsaEncrypt(self, text, pubKey, modulus):
        '''进行RSA加密
        '''
        text = text[::-1]
        rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def encrypted_request(self, text):
        '''将明文text进行两次AES加密获得密文encText,
        因为secKey是在客户端上生成的，所以还需要对其进行RSA加密再传给服务端。
        '''
        pubKey = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'

        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        encText = self.AES_encrypt(self.AES_encrypt(text, nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        return data
