include:
  - .create_groups
 
{% for s_attri in pillar['users'] %}
{% for s_user in s_attri %}
{% if s_attri[s_user]['present'] %}

{{ s_user }}:
  user:
    - present
    - home: /home/{{ s_user }}
    - shell: /bin/bash
    - maxdays: 99999
    - optional_groups:
{% for s_group in s_attri[s_user]['groups'] %}
      - {{ s_group }}
{% endfor %}
    - require:
{% for s_group in s_attri[s_user]['groups'] %}
      - group: {{ s_group }}
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
