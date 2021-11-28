import yaml
import json
import os
import sys

import click
from rich.console import Console
from jinja2 import Environment, PackageLoader, select_autoescape
from git import Repo

env = Environment(loader=PackageLoader("appleseed"),
                  extensions=['jinja2_strcase.StrcaseExtension'],
                  autoescape=select_autoescape())

repo = Repo(os.getcwd())


@click.group()
def cli():
    pass


@cli.group()
def apply():
    pass


@apply.command()
@click.argument('output', type=click.File('w'))
def hello_world(output):
    console = Console()

    template = env.get_template("HelloWorld.py")
    output.write(template.render(message="Goodbye, World!!!!!"))


@apply.command()
@click.argument('spec', type=click.File('r'))
@click.option('--template-branch', default='appleseed')
def repos(spec, template_branch):
    console = Console()

    resources = list(yaml.load_all(spec, Loader=yaml.FullLoader))

    template = env.get_template("repo.py")

    prev_branch = repo.active_branch.name
    if template_branch not in repo.heads:
        repo.git.checkout('--orphan', template_branch)
    else:
        repo.git.checkout(template_branch)

    try:
        os.mkdir('repos')
    except OSError as error:
        pass

    for resource in resources:
        with open('./repos/' + resource['plural'] + ".py", 'w') as output:
            output.write(template.render(resource=resource))

    data = {'resources': resources, 'command': ' '.join(sys.argv)}
    with open('.repos.spec.json', 'w') as f:
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