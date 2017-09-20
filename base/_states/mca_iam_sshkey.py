import boto3
import os
import sys
import salt
import salt.exceptions
from datetime import date,datetime,timedelta

__virtualname__ = 'mca_iam_sshkey'

# Function to initialize AWS Session


def _session(keyid=None, key=None):
    global session
    session = boto3.Session(
        aws_access_key_id=keyid,
        aws_secret_access_key=key,
    )
    return session

def _read_file(path):
    """
    :param path:
    :return:
    """
    with open(path, 'r') as f:
	return f.read()

def _finduser(user_name):
    client = session.client('iam')
    listuser = client.list_users()
    l1 = []
    for i in listuser['Users']:
        l1.append(i['UserName'])
    if user_name in l1:
        return True
    else:
        return False


def _findkeyid(user_name):
    client = session.client('iam')
    keyforuser = client.list_ssh_public_keys(
        UserName=user_name)['SSHPublicKeys']
    if not keyforuser:
        return None
    else:
        keylist = client.list_ssh_public_keys(UserName=user_name)
        for i in keylist['SSHPublicKeys']:
            sshkeyid = i['SSHPublicKeyId']
    return sshkeyid


def _findsshpubkey(user_name):
    client = session.client('iam')
    if _finduser(user_name):
        sshkeyid = _findkeyid(user_name)
        if sshkeyid:
            keydet = client.get_ssh_public_key(
                UserName=user_name,
                SSHPublicKeyId=sshkeyid,
                Encoding='SSH'
            )
            sshpubkey = keydet['SSHPublicKey']['SSHPublicKeyBody']
            return sshpubkey
        else:
            print "SSH Key not found"
            return None
    else:
        print "User Not found"
        return None


def _uploadsshkey(user_name, path):
    client = session.client('iam')
    keycontent = _read_file(path)
    res = client.upload_ssh_public_key(
        UserName=user_name,
        SSHPublicKeyBody=keycontent
    )
    return res

def _comparesshkeys(user_name,path):
    client = session.client('iam')
    old_sshpubkey = _findsshpubkey(user_name)
    new_sshpubkey = _read_file(path)
    words=new_sshpubkey.split(" ")
    del words[2]
    new_sshpubkey_u=" ".join(words)
    if old_sshpubkey == new_sshpubkey_u:
        return True
    else:
        return False

def _deletesshkey(user_name,sshkeyid):
    client = session.client('iam')
    res = client.delete_ssh_public_key(
                UserName=user_name,
                SSHPublicKeyId=sshkeyid
          )
    return res

def _inactivesshkey(user_name,sshkeyid):
    client = session.client('iam')
    res = client.update_ssh_public_key(
            UserName=user_name,
            SSHPublicKeyId=sshkeyid,
            Status='Inactive'
         )


def _updatesshkey(user_name, path):
    client = session.client('iam')
    old_sshpubkey = _findsshpubkey(user_name)
    if old_sshpubkey:
        if not _comparesshkeys(user_name,path):
            old_sshkeyid = _findkeyid(user_name)
            _inactivesshkey(user_name,old_sshkeyid)
            _deletesshkey(user_name,old_sshkeyid)
            _uploadsshkey(user_name, path)
    else:
        _uploadsshkey(user_name, path)

def _getsshkeydate(user_name):
    client = session.client('iam')
    sshkeydet = client.list_ssh_public_keys(UserName = user_name)
    sshkeydate = sshkeydet['SSHPublicKeys'][0]['UploadDate']
    return sshkeydate.date(), user_name

def _comparekeydates(sshkey_date, duration):
    newdate = datetime.now() - timedelta(days=duration)
    if sshkey_date <= newdate.date():
        return True
    else:
        return False


def rotate(name, duration, keyid=None, key=None):
    ret = {'name': name,
           'result': False,
           'comment': '',
           'changes': {},
           }
    _session(keyid=keyid, key=key)
    a = _getsshkeydate(name)[0]
    b = _comparekeydates(a,duration)
    if b:
        ret['result'] = True
        return ret
    else:
        ret['result'] = False
        ret['comment'] = "No Change Required"
        return ret


def present(name, path, keyid=None, key=None):
    ret = {'name': name,
           'result': False,
           'comment': '',
           'changes': {},
           }
    _session(keyid=keyid, key=key)
    if _finduser(name):
        if not _findsshpubkey(name):
            res1 = _uploadsshkey(name, path)
            ret['comment'] = 'Uploaded SSH Public Key'
            ret['changes']['create'] = res1
            ret['result'] = True
            return ret
        else:
            if _comparesshkeys(name,path):
                ret['comment'] = 'SSH Public Key already exists'
                ret['result'] = True
                return ret
            else: 
                old_sshkeyid = _findkeyid(name)
                client = session.client('iam')
                res1 = _inactivesshkey(name,old_sshkeyid)
                res2 = _deletesshkey(name,old_sshkeyid)
                res3 = _uploadsshkey(name, path)
                ret['comment'] = 'Updated SSH Public Key'
                ret['changes']['delete'] = res2
                ret['changes']['create'] = res3
                ret['result'] = True
                return ret
    else:
        ret['comment'] = 'User Not Found'
        ret['result'] = False
        return ret

 
 
def absent(name, keyid=None, key=None):
    ret = {'name': name,
           'result': False,
           'comment': '',
           'changes': {},
           }
    _session(keyid=keyid, key=key)
    if _finduser(name):
        if not _findsshpubkey(name):
            ret['comment'] = 'SSH Key Does Not Exists '
            ret['result'] = True
            return ret
        else:
            sshkeyid = _findkeyid(name)
            res1 = _deletesshkey(name,sshkeyid)
            ret['comment'] = 'SSH Key Deleted '
            ret['changes']['delete'] = res1
            ret['result'] = True
            return ret
    else:
        ret['comment'] = 'User Not Found'
        ret['result'] = True
        return ret

