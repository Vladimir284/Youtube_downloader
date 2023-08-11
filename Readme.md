# YouTube playlist downloader

## Instalation

Create virtual enviroment 
`python3 -m venv venv`

Install packages
`pip install -r requirements.txt`

## Usage

`python3 playlist_downloader.py [options] playlist_url`

### Options and arguments

- -d : print debug information\n" # Fixme how to enable debugging from beginning
- -h : print this help message and exit
- -i : print information about playlist and exit
- -s : turn off output messages and warnings\n" Fixme same here
- --dir=[name]           : set directory for output videos (implicitly current working directory)
- --resolution=[int+p]   : specify quality (pixels) in which should be playlist downloaded (max. quality implicitly)
- --format=[audio/video] : specify format in which should be playlist downloaded (implicitly mp3)
- --help                 : print this help message and exit
- --version              : view version of script and exit

## Error codes of playlist downloader

|         Error type          | Error code |
|:---------------------------:|:----------:|
|      Invalid argument       |     15     |
|          Url error          |     14     |
|   Non existent directory    |     13     |
|       Invalid format        |     12     |
| Invalid resolution of video |     11     |
|    Video does not exist     |     10     |
|        System error         |     9      |