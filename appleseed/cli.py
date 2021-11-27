import click
from rich.console import Console
from jinja2 import Environment, PackageLoader, select_autoescape

@click.group()
def cli():
    pass

@cli.command()
@click.argument('output', type=click.File('w'))
def generate(output):
    console = Console()

    env = Environment(
        loader=PackageLoader("appleseed"),
        autoescape=select_autoescape()
    )

    template = env.get_template("HelloWorld.py")
    output.write(template.render(message="Hello, World!"))

if __name__ == '__main__':
    cli()