from dataclasses import dataclass

@dataclass
class {{resource.name | to_camel}}:
    {%- for attr in resource.attributes %}
    {{attr.name}}: {{attr.type}}
    {%- endfor %}


class {{resource.name | to_camel}}Repo:

    def __init__(self, conn):
        self.conn = conn

    def get(self, id : int) -> {{resource.name | to_camel}}:
        raise NotImplementedError()

    def upsert(self, *{{resource.plural}} : list[{{resource.plural | to_camel}}]) -> list[{{resource.plural | to_camel}}]:
        raise NotImplementedError()

    def find(self) -> list[{{resource.plural | to_camel}}]:
        raise NotImplementedError()

    def delete(self, id : int) -> {{resource.name | to_camel}}:
        raise NotImplementedError()