# HideIntoPNG
[![Build Status](https://travis-ci.org/HugoJH/HideIntoPNG.svg?branch=master)](https://travis-ci.org/HugoJH/HideIntoPNG)


## Toy Project to hide a payload inside PNG

This project aims to embed any file within a PNG containerfile.
The following is a example of the PNG Structure
![PNG file structure](http://stegosploit.info/images/png_file2.png "PNG file structure")

What HideIntoPNG does is insert two new chunks before the 'IEND Chunk' called meTa and teMa:
  * **Meta** contains the files filename (though it could contain any class of metadata, hence the name meTa).
  * **teMa** contains the file data itself.
Both meTa and teMa chunks are encrypted using pycrypto package. Moreover, click package has been used to provide an easy-to-use command line interface.

## Usage Examples

* If we want to get the bytes of the png container with the payload file embedded to pipe it to other \*nix commands:
```bash
hip hide /path/to/png/container.png /path/to/payload/file.txt <Password> | other-tool
```
or if you want to save it to a file (you can do it with the command `hideToFile` though)
```bash
hip hide /path/to/png/container.png /path/to/payload/file.txt <Password> > containerWithPayload.png
```

* As said before, If you want to save the png container with the payload embedded to a file you can use:
```bash
hip hideToFile /path/to/png/container.png /path/to/payload/file.txt <Password> > containerWithPayload.png
```

* On the other hand, if we want to extract the payload from a PNG container:
```bash
hip extract /path/to/png/container.png <Password>
```
In this case, the output is json formatted with two fields corresponding with the **Meta** and **teMa**.
For ease-of-use purposes in mind, the fields were branded filename and data respectively. Keep in mind that the 'data'
field was Base64 encoded to facilitate the piping to other tools and thus a decoding is necessary before saving it again to its original file format. The following could be done:
```bash
hip extract /path/to/png/container.png <Password> | jq -r '.data' | base64 --decode > file.ext
```
* As with the hiding function we can do likewise and straight save it to a file
```bash
hip extractToFile /path/to/png/container.png <Password> <outputFolder>
```
If the outputfolder argument if omitted the file will be saved in a `results` folder in the current path.


