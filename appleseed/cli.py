import yaml
import json
import os
import sys
from datetime import datetime

import click
from rich.console import Console
from jinja2 import Environment, PackageLoader, select_autoescape
from git import Repo

env = Environment(loader=PackageLoader("appleseed"),
                  extensions=['jinja2_strcase.StrcaseExtension'],
                  autoescape=select_autoescape())

repo = Repo(os.getcwd())


def _write_header(f):
    header = env.get_template('header.py.jinja').render(
        now=datetime.now().isoformat())
    f.write(header + '\n')


@click.group()
def cli():
    pass


@cli.command()
@click.option('--resources-path')
@click.option('--package-name')
@click.option('--template-branch', default='appleseed')
@click.option('--appleseed-spec', default='.appleseed.json')
def apply(template_branch, appleseed_spec, resources_path, package_name):
    console = Console()

    if os.path.exists(appleseed_spec):
        with open(appleseed_spec, 'r') as f:
            params = json.loads(f.read())
    else:
        params = {}

    if resources_path:
        pass
    elif params.get('resources_path'):
        resources_path = params['resources_path']
    else:
        raise ArgumentError("--resources-path must be given")

    if package_name:
        pass
    elif params.get('package_name'):
        package_name = params['package_name']
    else:
        raise ArgumentError("--package-name must be given")

    with open(resources_path, 'r') as f:
        resources = list(yaml.load_all(f, Loader=yaml.FullLoader))

    repo_template = env.get_template("repo.py.jinja")
    models_template = env.get_template("models.py.jinja")

    prev_branch = repo.active_branch.name
    if template_branch not in repo.heads:
        repo.git.checkout('--orphan', template_branch)
    else:
        repo.git.checkout(template_branch)

    try:
        os.mkdir(package_name)
    except OSError as error:
        pass

    try:
        os.mkdir(package_name + '/repos')
    except OSError as error:
        pass

    for resource in resources:
        with open(package_name + '/repos/' + resource['plural'] + ".py",
                  'w') as output:
            _write_header(output)
            output.write(repo_template.render(resource=resource))

    with open(package_name + '/models.py', 'w') as output:
        _write_header(output)
        output.write(models_template.render(resources=resources))

    with open('./requirements.txt', 'w') as output:
        for r in ['sqlalchemy']:
            output.write(r + '\n')

    data = {
        'resources_path': resources_path,
        'package_name': package_name,
        'command': ' '.join(sys.argv)
    }
    with open('.appleseed.json', 'w') as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))

    if len(repo.index.diff(None)) > 0:
        repo.git.add('.')
        repo.git.commit('-a', '-m', 'Apply appleseed')
        repo.git.checkout(prev_branch)
        repo.git.merge(template_branch)
    else:
        repo.git.checkout(prev_branch)


if __name__ == '__main__':
    cli()