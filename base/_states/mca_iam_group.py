import boto3
import os
import sys
import salt
import salt.exceptions

__virtualname__ = 'mca_iam_group'

# Function to initialize AWS Session
def _session(keyid=None,key=None):
    global session
    session = boto3.Session(
        aws_access_key_id=keyid,
        aws_secret_access_key=key,
    )
    return session


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

def _creategroup(group_name):
    client = session.client('iam')
    response = client.create_group(
        GroupName = group_name
    )
    return response

def _deletegroup(group_name):
    client = session.client('iam')
    if _findgroup(group_name):
        client.delete_group(
            GroupName = group_name
	)
    else:
	print "Group does not exists"
        return False


def present(name,keyid=None,key=None):
    ret = { 'name': name,
            'result': False,
            'comment': '',
            'changes': {},
           }
    _session(keyid=keyid,key=key)
    if _findgroup(name):
        ret['comment'] = 'Group Already Exists'
        ret['changes']['create'] = None
        ret['result'] = True
        return ret
    else:
        res1 = _creategroup(name)
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
    if not _findgroup(name):
        ret['comment'] = 'Group Does not Exists'
        ret['changes']['delete'] = None
        ret['result'] = True
        return ret
    else:
        res1 = _deletegroup(name)
        ret['changes']['delete'] = name
        ret['result'] = True
        return ret
