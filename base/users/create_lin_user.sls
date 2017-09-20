include:
  - .create_groups
#  - .def_user
#  - .sshd_config
#  - .add_sudo
 
{% for attribute in pillar['users'] %}
{% for s_user in attribute %}
{% if attribute[s_user]['present'] %}

{{ s_user }}:
  user:
    - present
    - home: /home/{{ s_user }}
    - shell: /bin/bash
    - maxdays: 99999
    - optional_groups:
{% for s_group in attribute[s_user]['groups'] %}
      - {{ g }}
{% endfor %}
    - require:
{% for g in attribute[s_user]['groups'] %}
      - group: {{ g }}
{% endfor %}

create_pub_{{ s_user }}:
  cmd:
    - run
    - name: cat /dev/zero | ssh-keygen -q -N ""
    - shell: /bin/bash
    - user: {{ s_user }}
    - unless: stat /home/{{ s_user }}/.ssh/id_rsa

{% else %}

{{ s_user }}:
  user:
    - absent
    - purge: True
    - force: True

/etc/ssh/keys/{{ s_user }}_authorized_keys:
  file:
    - absent

{% endif %}
{% endfor %}
{% endfor %}
