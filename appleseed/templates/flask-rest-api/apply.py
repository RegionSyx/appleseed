import os
from appleseed.cli import AppleseedContext
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),
                  extensions=['jinja2_strcase.StrcaseExtension'],
                  autoescape=select_autoescape())


def apply(context: AppleseedContext):
    resources = context.parameters['resources_spec']
    package_name = context.parameters['package_name']

    repo_template = env.get_template("repo.py.jinja")
    models_template = env.get_template("models.py.jinja")

    for resource in resources:
        context.write_file(
            [package_name, 'repos', resource['plural'] + '.py'],
            repo_template.render(package_name=package_name, resource=resource),
        )

    context.write_file(
        [package_name, 'models.py'],
        models_template.render(package_name=package_name, resources=resources),
    )

    context.write_file(['requirements.txt'], 'sqlalchemy')
