VERSION = "playlist_downloader.py v1.0.0 (c) 2023 - by Vladimir Meciar"
LOG_FORMAT = '%(asctime)s (%(funcName)s) [%(levelname)s]: %(message)s'
DEBUG = True

INVALID_ARGUMENT_ERROR = 15
URL_ERROR = 14
NON_EXISTING_DIRECTORY_ERROR = 13
FORMAT_ERROR = 12
RESOLUTION_ERROR = 11
NO_VIDEO_ERROR = 10
SYSTEM_ERROR = 9

KNOWN_RESOLUTIONS = {"144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"}

LONG_OPTIONS = {"dir=", "resolution=", "format=", "help", "version", "playlist", "youtube"}
SHORT_OPTIONS = "dhis"