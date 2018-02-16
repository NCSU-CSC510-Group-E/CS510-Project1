import click

from prototype import main

@click.command()
@click.option('--training', default='input/', help='Path to your training documents.')

# Providing two "names" in one option creates a boolean parameter 
@click.option('--verbose/--no-verbose', default=False, help='Print extra debugging information.')

@click.option('--dictionary', default='save/dictionary.dict', help='The file to save your corpus dictionary to (for loading later)')

@click.option('--model', default='save/model', help='The file to save your model to (for loading later)')

@click.option('--test', default='input/test.txt', help='The file to predict once training is complete')


def analyze(training, test, dictionary, model, verbose):
    click.echo('Training on files in {}'.format( training ) )

    main(training, test, dictionary, model, verbose)

if __name__ == '__main__':
    analyze()
