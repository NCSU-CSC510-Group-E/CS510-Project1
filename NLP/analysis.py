import click

@click.command()
@click.option('--training', default='input/', help='Path to your training documents.')

def analyze(training):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo('Training on files in {}'.format( training ) )

if __name__ == '__main__':
    analyze()
