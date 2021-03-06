import yaml
import json
import os
import sys
from datetime import datetime
import importlib
from typing import Sequence

import click
from rich.console import Console
from jinja2 import Environment, PackageLoader, select_autoescape
from git import Repo

from appleseed.context import AppleseedContext

repo = Repo(os.getcwd())


@click.group()
def cli():
    pass


@cli.command('list')
def list_templates():
    console = Console()

    base_template_path = os.path.join(os.path.dirname(__file__), 'templates')

    for d in os.listdir(base_template_path):
        with open(os.path.join(base_template_path, d, 'appleseed.yaml'),
                  'r') as f:
            template_info = yaml.load(f, Loader=yaml.FullLoader)
        console.print(template_info['name'], template_info['version'])


@cli.command()
@click.argument('name')
@click.option('--template-branch', default='appleseed')
@click.option('--appleseed-spec', default='.appleseed.json')
@click.option('--verbose', '-v', is_flag=True)
def apply(name, template_branch, appleseed_spec, verbose):
    console = Console()

    base_template_path = os.path.join(os.path.dirname(__file__), 'templates')

    with open(os.path.join(base_template_path, name, 'appleseed.yaml'),
              'r') as f:
        template_manifest = yaml.load(f, Loader=yaml.FullLoader)

    spec = importlib.util.spec_from_file_location(
        'test', os.path.join(base_template_path, name, 'apply.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    params = {}
    if os.path.exists(appleseed_spec):
        with open(appleseed_spec, 'r') as f:
            params = json.load(f)

    for param in template_manifest.get('parameters', []):
        if param['name'] in params:
            continue

        if param['type'] == 'str':
            params[param['name']] = input(param['name'] + ': ')

        elif param['type'] == 'file' and param['format'] == 'yaml':
            file_name = input(param['name'] + ': ')
            with open(file_name, 'r') as f:
                params[param['name']] = list(
                    yaml.load_all(f, Loader=yaml.FullLoader))

    prev_branch = repo.active_branch.name

    if template_branch not in repo.heads:
        repo.git.checkout('--orphan', template_branch)
    else:
        repo.git.checkout(template_branch)

    context = AppleseedContext(console=console, parameters=params)
    module.apply(context)

    if verbose:
        for file in context.files_written:
            console.print(f"Updated file '{file}'")

    with open('.appleseed.json', 'w') as f:
        f.write(json.dumps(params, indent=2, sort_keys=True))

    if len(repo.index.diff(None)) > 0:
        repo.git.add('.')
        repo.git.commit('-a', '-m', 'Apply appleseed')
        repo.git.checkout(prev_branch)
        repo.git.merge(template_branch)
    else:
        repo.git.checkout(prev_branch)


if __name__ == '__main__':
    cli()