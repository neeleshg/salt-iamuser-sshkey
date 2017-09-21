{% for s_attri in pillar['users'] %}
{% for s_user in s_attri %}
{% if s_attri[s_user]['present'] %}

create iam user {{ s_user }}:
  iam_user.present:
    - name: {{ s_user }}

manage ssh public keys in iam {{ s_user }}:
  iam_sshkey.present:
    - name: {{ s_user }}
    - path: /home/{{ s_user }}/.ssh/id_rsa.pub

{% else %}

delete ssh public keys in iam for {{ s_user }}:
  iam_sshkey.absent:
    - name: {{ s_user }}

delete iam user {{ s_user }}:
  iam_user.absent:
    - name: {{ s_user }}

{% endif %}
{% endfor %}
{% endfor %}
