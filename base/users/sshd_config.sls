/etc/ssh/sshd_config:
  file.managed:
    - source: salt://users/config/sshd_config.jinja
    - template: jinja
    - mode: 0644
    - user: root
    - group: root

sshd:
  service:
    - running
    - restart: True
    - watch:
      - file: /etc/ssh/sshd_config

/usr/local/bin/getkey.sh:
  file.managed:
    - source: salt://users/scripts/getkey.sh
    - mode: 0755
    - user: root
    - group: root


/usr/local/bin/getkey.py:
  file.managed:
    - source: salt://users/scripts/getkey.py
    - mode: 0755
    - user: root
    - group: root
