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
@click.argument('passPhrase')
def hideToFile(container, payload, output, passPhrase):
	output.write(hidePayloadAndGetBytes(ContainerFilePath, payloadFilePath, passPhrase))


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
@click.argument('outputFolder')
@click.argument('passPhrase')
def extractToFile(container, passPhrase, outputFolder=join(getcwd() + "results/")):
	_prepareExtractionFolder(outputFolder)
	payload = extractPayloadDataAndMetadataDict(container, passPhrase)

	with open(join(outputFolder, payload['filename']), "wb") as outputFD:
		outputFD.write(payload['data'])

def _prepareExtractionFolder(outputPath):
	if not os.path.exists(os.path.dirname(outputPath)):
		os.makedirs(os.path.dirname(outputPath))

if __name__ == "__main__":
	main()
