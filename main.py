import click
from rich.console import Console

@click.group()
def cli():
    pass

@cli.command()
def generate():
    console = Console()
    console.print("Generate")

if __name__ == '__main__':
    cli()