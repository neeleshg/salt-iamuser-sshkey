{% for attribute in pillar['users'] %}
{% for s_user in attribute %}
{% if attribute[s_user]['present'] %}

check_rotation_{{ s_user }}:
  iam_sshkey.rotate:
    - name: {{ s_user }}
    - duration: 1


create_pub_{{ s_user }}:
  cmd:
    - run
    - name: cat /dev/null|echo -e  'y'|ssh-keygen -q -t rsa -N "" -f ~/.ssh/id_rsa
    - shell: /bin/bash
    - user: {{ s_user }}
    - watch:
      -  iam_sshkey.rotate: check_rotation_{{ s_user }}

manage ssh public keys in iam {{ s_user }}:
  iam_sshkey.present:
    - name: {{ s_user }}
    - path: /home/{{ s_user }}/.ssh/id_rsa.pub
    - onchanges:
      - cmd: create_pub_{{ s_user }}

{% endif %}
{% endfor %}
{% endfor %}
