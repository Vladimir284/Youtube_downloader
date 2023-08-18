# YouTube playlist downloader

## Instalation

Create virtual enviroment
`python3 -m venv venv`

Install packages
`pip install -r requirements.txt`

## Usage

`python3 playlist_downloader.py [youtube/playlist] [option] [arg] playlist_url`

### Options and arguments

- -h : print this help message and exit
- -i : print information about playlist and exit
- --dir=[name]           : set directory for output videos (implicitly current working directory)
- --playlist : set script download on youtube playlist
- --resolution=[int+p]   : specify quality (pixels) in which should be playlist downloaded (max. quality implicitly)
- --format=[audio/video] : specify format in which should be playlist downloaded (implicitly mp3)
- --help                 : print this help message and exit
- --version              : view version of script and exit
- --youtube : set script to download youtube video

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