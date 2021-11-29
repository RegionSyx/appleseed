import sqlalchemy as sa


{% for resource in resources -%}
{{resource.plural | to_snake}} = sa.Table(metadata, 
    {%- for attr in resource.attributes%}
    {{attr.name}}=
    {%- if attr.type == 'int' -%}
        sa.Integer()
    {%- elif attr.type == 'string' -%}
        sa.Text()
    {%- endif -%},
    {%- endfor %}
    created_at=sa.DateTime(),
    updated_at=sa.DateTime(),
)


{% endfor %}