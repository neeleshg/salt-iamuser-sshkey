#!/usr/bin/env python
import boto3
import os
import sys

def _findkeyid(user_name):
    iam_con = boto3.client('iam')
    keylist = iam_con.list_ssh_public_keys(UserName=user_name)
    for i in keylist['SSHPublicKeys']:
        sshkeyid=i['SSHPublicKeyId']
    return sshkeyid

def _findsshpubkey(user_name):
    sshpubkeyid=_findkeyid(user_name)
    iam_con = boto3.client('iam')
    keydet = iam_con.get_ssh_public_key(
        UserName = user_name,
        SSHPublicKeyId = sshpubkeyid,
        Encoding = 'SSH'
	)
    sshpubkey=keydet['SSHPublicKey']['SSHPublicKeyBody']
    print sshpubkey

user_name = sys.argv[1]
_findsshpubkey(user_name)
