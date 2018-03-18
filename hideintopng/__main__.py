from os import getcwd, makedirs
from os.path import join, exists, dirname, basename
from json import dumps
from base64 import b64encode
import click
from .hideintopng import HideIntoPNG

@click.group()
def main():
	pass

@main.command()
@click.argument('container', type=click.File('rb'))
@click.argument('payload', type=click.File('rb'))
@click.argument('passPhrase')
def hide(container, payload, passphrase):
	hip = HideIntoPNG()
	contentBytes = b''
	contentBytes = hip.hide(containerData=container.read(),
                            payloadMetaData=basename(payload.name).encode("utf-8"),
					        payloadData=payload.read(),
					        passPhrase=passphrase)
	return click.echo(contentBytes)

@main.command()
@click.argument('container', type=click.File('rb'))
@click.argument('payload', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.argument('passphrase')
def hideToFile(container, payload, output, passphrase):
	hip = HideIntoPNG()
	contentBytes = b''
	contentBytes = hip.hide(containerData=container.read(),
                            payloadMetaData=basename(payload.name).encode("utf-8"),
					        payloadData=payload.read(),
					        passPhrase=passphrase)

	output.write(contentBytes)


@main.command()
@click.argument('container', type=click.File('rb'))
@click.argument('passPhrase')
def extract(container, passphrase):
	hip = HideIntoPNG()
	payloadDict = {}
	payloadDict = hip.extract(containerWithPayloadData=container.read(),
			                  passPhrase=passphrase)
	payloadDict['filename'] = payloadDict['filename'].decode('utf-8')
	payloadDict['data'] = b64encode(payloadDict['data']).decode('utf-8')
	return click.echo(dumps(payloadDict))

@main.command()
@click.argument('container', type=click.File('rb'))
@click.argument('passphrase')
@click.argument('outputfolder', default=join(getcwd(), "results/"))
def extractToFile(container, passphrase, outputfolder):
	_prepareExtractionFolder(outputfolder)
	hip = HideIntoPNG()
	payloadDict = {}
	payloadDict = hip.extract(containerWithPayloadData=container.read(),
			                  passPhrase=passphrase)

	with open(join(outputfolder, payloadDict['filename'].decode('utf-8')), "wb") as outputFD:
		outputFD.write(payloadDict['data'])

def _prepareExtractionFolder(outputPath):
	if not exists(dirname(outputPath)):
		makedirs(dirname(outputPath))

if __name__ == "__main__":
	main()
