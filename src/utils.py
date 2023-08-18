"""
Utils
-----

Modules for better and clear working with script
"""
import sys
import requests
import getopt
import os
import pytube

DEBUG = True
VERSION = "playlist_downloader.py v1.0.0 (c) 2023 - by Vladimir Meciar"

# Possible errors number
INVALID_ARGUMENT_ERROR = 15
URL_ERROR = 14
NON_EXISTING_DIRECTORY_ERROR = 13
FORMAT_ERROR = 12
RESOLUTION_ERROR = 11
NO_VIDEO_ERROR = 10
SYSTEM_ERROR = 9

# Known resolutions for check
KNOWN_RESOLUTIONS = {"144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"}

# Options of script
LONG_OPTIONS = ["dir=", "resolution=", "format=", "help", "version", "playlist", "youtube"]
SHORT_OPTIONS = "dhis"


def print_debug_important(pattern: str, message: str):
    """
    Print initial debug message if DEBUG is set on True

    Parameters
    ----------
    pattern : str
        Pattern to be printed multiple times in fornt of and after message
    message : str
        Message to be printed out
    """
    if DEBUG:
        # Print stripe for better distinguishing
        for i in range(20):
            print(pattern, end='')
        print("  " + message + "  ", end='')
        for i in range(20):
            print(pattern, end='')
        print("")


def print_debug(message: str):
    """
    Print formatted debug message

    Parameters
    ----------
    message : str
        Message to be printed out
    """
    if DEBUG:
        print("DEBUG: " + message)


def end(pattern: str, message: str):  # Function is used for not repeating patterns in code
    """
    Print debug message if needed and exit script

    Parameters
    ----------
    pattern : str
        Pattern to be printed multiple times in fornt of and after message
    message : str
        Message to be printed out
    """
    print_debug_important(pattern, message)
    sys.exit(0)


def warning(message: str):
    """
    Print formatted text as warning on stderr

    Parameters
    ----------
    message : str
        Message to be printed out
    """
    print("WARNING: " + message, file=sys.stderr)


def error(err_num: int, message: str = ""):
    """
    Print formatted text as error on stderr and exit with err_num

    Parameters
    ----------
    err_num : int
        Error number
    message : str
        Error message
    """
    print("ERROR: " + message, file=sys.stderr)
    sys.exit(err_num)


def video_exists(video_url: str) -> bool:
    """
    Check if passed url of video exists

    Parameters
    ----------
    video_url : str
        Url of vide
    Returns
    -------
        True if video exists, otherwise False

    """
    request = None
    try:
        request = requests.get(video_url)
    except requests.exceptions.MissingSchema:
        error(URL_ERROR, "Url error")
    except requests.exceptions.ConnectionError:
        error(URL_ERROR, "No internet connection")

    return not ("Video unavailable" in request.text)


def print_help():
    """
    Print help message of script
    """
    print("usage \n "
          "python3 playlist_downloader.py [youtube/playlist] [option] [arg] url\n"
          "--- Options and arguments ---\n"
          # "-d\t\t : print debug information\n" # Fixme how to enable debugging from beginning
          "-h\t\t\t : print this help message and exit\n"
          "-i\t\t\t : print information about playlist and exit\n"
          # "-s\t\t : turn off output messages and warnings\n" Fixme same here
          "--dir=[name]\t\t : set directory for output videos (implicitly current working directory)\n"
          "--playlist\t\t : set script download on youtube playlist\n"
          "--resolution=[int+p]\t : specify quality (pixels) in which should be playlist downloaded (max. quality "
          "implicitly)\n"
          "--format=[audio/video]\t : specify format in which should be playlist downloaded (implicitly mp3 )\n"
          "--help\t\t\t : print this help message and exit\n"
          "--version\t\t : view version of script and exit\n"
          "--youtube\t\t : set script to download youtube video")


def parse_arguments(argv: list) -> tuple:
    """
    Parse arguments and check if all passed arguments are in correct format

    Parameters
    ----------
    argv : list
        List of arguments returned by sys.argv

    Returns
    -------
        Tuple of url and options of argument
    """
    print_debug("Parsing arguments")

    url = None
    options = None

    # Check if url was passed as argument
    if "https://" in str(argv[len(argv) - 1]):
        url = argv[len(argv) - 1]
        arguments = argv[1:(len(argv) - 1)]
    else:
        arguments = argv[1:]

    try:
        options, arguments = getopt.getopt(arguments, shortopts=SHORT_OPTIONS, longopts=LONG_OPTIONS)
    except getopt.GetoptError as err:
        error(20, "Argument error " + err.msg)

    if len(arguments) != 0:
        error(20, "Argument error Invalid arguments" + str(arguments))

    print_debug("Parsing arguments OK")

    check_arguments(options, url)

    return tuple([url, options])


def check_arguments(options: list, url: str):
    """
    Check if passed arguments to script are in correct format

    Parameters
    ----------
    options : list
        List of tuples like in return getopt.getopt
    url : str
        Url of playlist or video
    """
    # Store used arguments for check and hint
    used_options = set()

    print_debug("Checking options and arguments")

    # Mandatory arguments
    if not (("--playlist", "") in options or ("--youtube", "") in options):
        error(INVALID_ARGUMENT_ERROR, "No mandatory argument [playlist/youtube]")

    for opt, arg in options:

        argument = (opt, arg)
        used_options.add(argument)

        # Check url
        if url is not None:
            if not video_exists(url):
                error(10, "Video does not exist or no internet connection")

        # This is basically switch case through known options
        if opt == "--playlist" or opt == "--youtube" and len(arg) == 0:
            pass
        elif opt == "-h" or opt == "-d" or opt == "-s" or opt == "-i" and len(arg) == 0:
            pass
        elif opt == "--help" or opt == "--version" and len(arg) == 0:
            pass
        elif opt == "--resolution" and isinstance(arg, str):

            # This construction was set here only because pyCharm has problem with not in statement
            if arg in KNOWN_RESOLUTIONS:
                pass
            else:
                error(10, "Invalid number in argument --resolution")

        elif opt == "--dir" and isinstance(arg, str):
            if not os.path.isdir(arg):
                error(15, "Non existent directory " + arg)
        elif opt == "--format" and isinstance(arg, str):
            if not (arg == "audio" or arg == "video"):
                error(15, "Invalid value of format " + arg)
        else:
            error(20, "Invalid argument " + opt)

    # Warnings
    for option in used_options:
        if "--resolution" == option[0]:
            if ("--format", "audio") in used_options:
                warning("Used --resolution while format was set on video, no videos will be exported")

    print_debug("Checking options and arguments OK")


def execute(url: str, options: tuple):
    """
    Execute script with entered options

    Parameters
    ----------
    url : str
        Url of video or playlist
    options : tuple
        Options in format like return from getopt.getopt
    """
    print_debug("Executing script")

    # Options that don't need any other arguments
    if ("--help", "") in options or ("-h", "") in options:
        print_help()
        end()
    elif ("--version", "") in options:
        print(VERSION)
        end()

    # Check if video exists
    if url is not None:
        if not video_exists(url):
            error(10, "Video does not exist or no internet connection")
    else:
        error(URL_ERROR, "No url passed as argument")

    only_audio = True
    only_video = False
    resolution = None
    output_dir = "."

    for opt, arg in options:
        if opt == "--dir":
            output_dir = arg
        if opt == "--resolution":
            resolution = arg
        if opt == "--format":
            if arg == "audio":
                pass
            if arg == "video":
                only_video = True
                only_audio = False

    if ("--playlist", "") in options:
        playlist = pytube.Playlist(url)

        if ("-i", "") in options:
            print_playlist_info(playlist)
            end()

        download_all(playlist, output_dir, resolution, only_audio, only_video)
    elif ("--youtube", "") in options:
        youtube = pytube.YouTube(url)

        if ("-i", "") in options:
            print_youtube_info(youtube)
            end()

        download(youtube, output_dir, resolution, only_audio, only_video)

    print_debug("Executing script OK")


def print_playlist_info(playlist: pytube.Playlist):
    """
    Print pretty playlist info

    Parameters
    ----------
    playlist : pytube.Playlist
        Playlist Object which inf we want o be shown
    """
    # Playlist info
    print(playlist.title)
    print(playlist.description)
    print(str(playlist.length) + "\n")

    # Each videos properties
    index = 0
    for video in playlist.videos:
        index += 1
        print(str(index) + ". ", end="")
        print_youtube_info(video)


def print_youtube_info(youtube: pytube.YouTube):
    """
    Print information about YouTube object

    Parameters
    ----------
    youtube : pytube.Youtube
        Youtube object we want to print infor about
    """
    print(youtube.title)
    print("\tLength:\t\t" + view_length_pretty(youtube.length))
    print("\tResolution:\t" + view_resolutions_pretty(youtube.streams.filter(progressive=True).first()) + "\n")


def view_length_pretty(length: int) -> str:
    """
    View passed length in nice format (Xh, Ym, Zs)
    Parameters
    ----------
    length : int
        Length in seconds

    Returns
    -------
    str

    """
    hours = length // 3600
    minutes = (length - hours * 3600) // 60
    seconds = (length - hours * 3600 - minutes * 60) % 60

    return str(hours) + "hr " + str(minutes) + "min " + str(seconds) + "sec "


def view_resolutions_pretty(streams: pytube.StreamQuery) -> str:  # Help function
    """
    View all videos resolution in pretty format
    Parameters
    ----------
    streams : pytube.StreamQuery
        Passed StreamQuery of YouTube object
    Returns
    -------
    str

    """
    list_of_resolution = []
    for stream in streams:
        list_of_resolution.append(stream.resolution)
    return str(list_of_resolution)


def download_all(playlist: pytube.Playlist, output_dir: str = ".", resolution: str = None, only_audio: bool = True,
                 only_video: bool = False):
    """
    Download all videos in YouTube playlist with entered parameters

    Parameters
    ----------
    playlist : pytube.Playlist
        Playlist object of Playlist
    output_dir : str
        Directory where all output will be stored
    resolution : str
        Resolution in which should be playlist downloaded
    only_audio : bool
        Flag if only audio should be downloaded
    only_video : bool
        Flag if only audio should be downloaded

    """
    print("Playlist:" + playlist.title)

    for video in playlist.videos:
        download(video, output_dir, resolution, only_audio, only_video)
    print("Done")


def download(youtube: pytube.YouTube, output_dir: str = ".", resolution: str = None, only_audio: bool = True,
             only_video: bool = False):
    """
    Download certain YouTube video

    Parameters
    ----------
    youtube : pytube.Youtube
        Youtube video object to be downloaded
    output_dir : str
        Directory where all output should be stored
    resolution : str
        Resolution in which the video should be downloaded
    only_audio : bool
        Flag if only audio should be downloaded
    only_video :
        Flag if only video should be downloaded
    """
    print("Downloading " + youtube.title)

    if resolution is None:
        resolution = youtube.streams.get_highest_resolution()

    video_to_download = youtube.streams.filter(res=resolution, only_video=only_video,
                                               only_audio=only_audio).first()
    if video_to_download is None:
        error(NO_VIDEO_ERROR, "Video does not exist")

    video_to_download.download(skip_existing=True, output_path=output_dir)

    print("Done")
