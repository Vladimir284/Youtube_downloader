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
import src.constants as constants
import src.my_logger as my_logger


@my_logger.debug_log
def print_help():
    """
    Print help message of script
    """
    print("usage \n "
          "python3 playlist_downloader.py [youtube/playlist] [option] [arg] url\n"
          "--- Options and arguments ---\n"
          "-h\t\t\t : print this help message and exit\n"
          "-i\t\t\t : print information about playlist and exit\n"
          "--dir=[name]\t\t : set directory for output videos (implicitly current working directory)\n"
          "--playlist\t\t : set script download on youtube playlist\n"
          "--resolution=[int+p]\t : specify quality (pixels) in which should be playlist downloaded (max. quality "
          "implicitly)\n"
          "--format=[audio/video]\t : specify format in which should be playlist downloaded (implicitly mp3 )\n"
          "--help\t\t\t : print this help message and exit\n"
          "--version\t\t : view version of script and exit\n"
          "--youtube\t\t : set script to download youtube video")


@my_logger.debug_log
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
        my_logger.logger.error("Url error")
        sys.exit(constants.URL_ERROR)
    except requests.exceptions.ConnectionError:
        my_logger.logger.error("No internet connection")
        sys.exit(constants.URL_ERROR)

    return not ("Video unavailable" in request.text)


@my_logger.debug_log
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
    my_logger.logger.info("Parsing arguments...")

    url = None
    options = None

    # Check if url was passed as argument
    if "https://" in str(argv[len(argv) - 1]):
        url = argv[len(argv) - 1]
        arguments = argv[1:(len(argv) - 1)]
    else:
        arguments = argv[1:]

    try:
        options, arguments = getopt.getopt(arguments, shortopts=constants.SHORT_OPTIONS,
                                           longopts=constants.LONG_OPTIONS)
    except getopt.GetoptError as err:
        my_logger.logger.error("Argument error: {}".format(err.msg))
        sys.exit(constants.INVALID_ARGUMENT_ERROR)

    if len(arguments) != 0:
        my_logger.logger.error("Argument error, Invalid arguments : {}".format(str(arguments)))
        sys.exit(constants.INVALID_ARGUMENT_ERROR)

    check_arguments(options, url)

    return tuple((options, url))


@my_logger.debug_log
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
    my_logger.logger.info("Checking arguments...")

    # Store used arguments for check and hint
    used_options = set()

    for opt, arg in options:

        argument = (opt, arg)
        used_options.add(argument)

        # Check url
        if url is not None:
            if not video_exists(url):
                my_logger.logger.error("Video does not exist or no internet connection")
                sys.exit(constants.NO_VIDEO_ERROR)

        # This is basically switch case through known options
        if opt == "--playlist" or opt == "--youtube" and len(arg) == 0:
            pass
        elif opt == "-h" or opt == "-d" or opt == "-s" or opt == "-i" and len(arg) == 0:
            pass
        elif opt == "--help" or opt == "--version" and len(arg) == 0:
            pass
        elif opt == "--resolution" and isinstance(arg, str):

            # This construction was set here only because pyCharm has problem with not in statement
            if arg in constants.KNOWN_RESOLUTIONS:
                pass
            else:
                my_logger.logger.error("Invalid number in argument --resolution: {}".format(arg))
                sys.exit(constants.NO_VIDEO_ERROR)

        elif opt == "--dir" and isinstance(arg, str):
            if not os.path.isdir(arg):
                my_logger.logger.error("Non existent directory: {}".format(arg))
                sys.exit(constants.NON_EXISTING_DIRECTORY_ERROR)
        elif opt == "--format" and isinstance(arg, str):
            if not (arg == "audio" or arg == "video"):
                my_logger.logger.error("Invalid value of format: {}".format(arg))
                sys.exit(constants.INVALID_ARGUMENT_ERROR)
        else:
            my_logger.logger.error("Invalid argument: {}".format(opt))
            sys.exit(constants.INVALID_ARGUMENT_ERROR)

    # Warnings
    for option in used_options:
        if "--resolution" == option[0]:
            if ("--format", "audio") in used_options:
                my_logger.logger.warning("Used --resolution while format was set on video, no videos will be exported")


@my_logger.debug_log
def execute(options: tuple, url: str):
    """
    Execute script with entered options

    Parameters
    ----------
    url : str
        Url of video or playlist
    options : tuple
        Options in format like return from getopt.getopt
    """
    my_logger.logger.info("Executing script...")

    # Options that don't need any other arguments
    if ("--help", "") in options or ("-h", "") in options:
        print_help()
        sys.exit(0)

    elif ("--version", "") in options:
        print(constants.VERSION)
        sys.exit(0)

        # Mandatory arguments
    if not (("--playlist", "") in options or ("--youtube", "") in options):
        my_logger.logger.error("No mandatory argument [playlist/youtube]")
        sys.exit(constants.INVALID_ARGUMENT_ERROR)

    # Check if video exists
    if url is not None:
        if not video_exists(url):
            my_logger.logger.error("Video does not exist or no internet connection")
            sys.exit(constants.NO_VIDEO_ERROR)
    else:
        my_logger.logger.error("No url passed as argument")
        sys.exit(constants.URL_ERROR)

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
            sys.exit(0)

        download_all(playlist, output_dir, resolution, only_audio, only_video)
    elif ("--youtube", "") in options:
        youtube = pytube.YouTube(url)

        if ("-i", "") in options:
            print_youtube_info(youtube)
            sys.exit(0)

        download(youtube, output_dir, resolution, only_audio, only_video)


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


@my_logger.debug_log
def print_youtube_info(youtube: pytube.YouTube):
    """
    Print information about YouTube object

    Parameters
    ----------
    youtube : pytube.Youtube
        Youtube object we want to print info about
    """
    print(youtube.title)
    print("\tLength:\t\t" + view_length_pretty(youtube.length))
    print("\tResolution:\t" + view_resolutions_pretty(youtube.streams.filter(progressive=True).first()) + "\n")


@my_logger.debug_log
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


@my_logger.debug_log
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


@my_logger.debug_log
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


@my_logger.debug_log
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
        my_logger.logger.error("Video does not exist")
        sys.exit(constants.NO_VIDEO_ERROR)

    video_to_download.download(skip_existing=True, output_path=output_dir)
