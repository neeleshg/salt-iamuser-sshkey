# salt-iamuser-sshkey

Salt based User Management for Linux and AWS IAM.
SSH Keys will be stored in IAM.
Prerequisites:
- There should be 3 or 2  Linux EC2 instances:
  - Salt-master
  - Gateway
  - instance1
- On Gateway, Salt Grain "role" should be set to "gateway" in /etc/salt/grains
- Boto3 should be installed on all
- Gateway Machine will require read-write access to AWS IAM, to list, create, delete user, add, delete, update SSH-keys.

Workflow:
- Configure SSHD "/etc/sshd_config" to pull key from IAM and use for Authentication: AuthorizedKey Command
- User will be created on Gateway
- Generate SSH keypair on Gateway
- User will be created in IAM
- Upload SSH Public key in IAM
- All instances will use same public key for Authentication
- One Python script will actually pulls SSH public key from IAM.
- Same script is used in /etc/ssh/sshd_config as “AuthorizedKey Command”.


base/top.sls -> Top file for Users
base/users -> State files of Users
base/_states -> Salt State Modules for managing Users in IAM
base/users/scripts --> Scripts for getting Public Keys from SSH

Process:
- All States are under base/users directory. It should be coppied under file_roots
- Add content of base/top.sls to your top file.
- Copy files of pillar/base under your pillar_roots
- Copy content of pillar/base/top.sls to your pillar's top.sls
- Copy folder base/_states under your file_roots
- Execute -> salt '*' saltutil.sync_all

Add Groups in pillar/base/groups.sls:
	For Eg. I have added below information already. You can replace "family" with your Group Name.
	groups:
   	  - family

	SUDOERS:
          - '%family   ALL=(ALL)       NOPASSWD: ALL'

Add Users in pillar/base/users.sls:
	For eg. I have added below 2 users in it already. Replace "ganesh" & "neelesh" with your usernames
	Also change "family" to your groupname.
	users:
  	  - ganesh:
     	    present: True
     	    groups:
       	      - family

	  - neelesh:
            present: True
            groups:
              - family


- Copy folder base/_states under your file_roots
- Execute -> salt '*' saltutil.refresh_pillar

Note: To delete User, replace "True" to "False"

Apply States Manually on Gateway Machine -
	salt -G 'role: gateway' state.sls users.sshd_config
	salt -G 'role: gateway' state.sls users.create_groups
	salt -G 'role: gateway' state.sls users.create_lin_user
	salt -G 'role: gateway' state.sls users.create_iam_user

On Other Instance Apply just create_groups, sshd_config and create_lin_user
	salt 'instance1' state.sls create_groups
	salt 'instance1' state.sls sshd_config
	salt 'instance1' state.sls create_lin_user


Setup daily cron for Checking up key rotation:
	salt -G 'role: gateway' state.sls users.rotatekeys

 
