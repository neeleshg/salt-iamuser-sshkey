base:
  'G@role:gateway':
     - match: compound
     - users.sshd_config
     - users.create_lin_user
     - users.create_iam_user
