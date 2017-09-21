'''
    This module is for Managing Users in IAM
    
    Auth: Neelesh Gurjar 
'''

import boto3
import os
import sys
import salt
import salt.exceptions

__virtualname__ = 'iam_user'

# Function to initialize AWS Session
def _session(keyid=None,key=None):
    global session
    session = boto3.Session(
        aws_access_key_id=keyid,
        aws_secret_access_key=key,
    )
    return session


def _finduser(user_name):
    client = session.client('iam')
    listuser=client.list_users()
    l1=[]
    for i in listuser['Users']:
	l1.append(i['UserName'])
    if user_name in l1:
	return True
    else:
	return False 

def _findgroup(group_name):
    client = session.client('iam')
    grouplist=client.list_groups()
    l1=[]
    for i in grouplist['Groups']:
        l1.append(i['GroupName'])
    if group_name in l1:
        return True
    else:
        return False

def _createuser(user_name):
    client = session.client('iam')
    response = client.create_user(
        UserName = user_name
    )
    return response

def _deleteuser(user_name):
    client = session.client('iam')
    if _finduser(user_name):
        client.delete_user(
            UserName = user_name
	)
    else:
	print "User Does Not Exists"
        return False


def present(name,keyid=None,key=None):
    ret = { 'name': name,
            'result': False,
            'comment': '',
            'changes': {},
           }
    _session(keyid=keyid,key=key)
    if _finduser(name):
        ret['comment'] = 'User Already Exists'
        ret['changes']['create'] = None
        ret['result'] = True
        return ret
    else:
        res1 = _createuser(name)
        ret['changes']['create'] = res1
        ret['result'] = True
        return ret

def absent(name,keyid=None,key=None):
    ret = { 'name': name,
            'result': False,
            'comment': '',
            'changes': {},
           }
    _session(keyid=keyid,key=key)
    if not _finduser(name):
        ret['comment'] = 'User Does not Exists'
        ret['changes']['delete'] = None
        ret['result'] = True
        return ret
    else:
        res1 = _deleteuser(name)
        ret['changes']['delete'] = name
        ret['result'] = True
        return ret
