import click

from prototype import main

@click.command()
@click.option('--training', default='input/', help='Path to your training documents.')

# Providing two "names" in one option creates a boolean parameter 
@click.option('--verbose/--no-verbose', default=False, help='Print extra debugging information.')

def analyze(training, verbose):
    click.echo('Training on files in {}'.format( training ) )

    main(training, verbose)

if __name__ == '__main__':
    analyze()
