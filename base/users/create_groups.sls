{% for s_group in pillar.get('groups', '') %}

{{ s_group }}:
  group:
    - present

{% endfor %}
