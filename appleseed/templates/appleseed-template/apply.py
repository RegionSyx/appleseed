import os
import yaml

from appleseed.cli import AppleseedContext
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),
                  extensions=['jinja2_strcase.StrcaseExtension'],
                  autoescape=select_autoescape())


def apply(context: AppleseedContext):
    name = context.parameters['template_name']
    author = context.parameters['author']

    yaml_template = env.get_template('appleseed.yaml.jinja')
    apply_template = env.get_template('apply.py.jinja')

    data = {'template_name': name, 'author': author}
    context.write_file(['appleseed.yaml'], yaml_template.render(**data))

    context.write_file(['apply.py'], apply_template.render())