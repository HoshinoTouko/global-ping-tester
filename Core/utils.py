import platform


def get_os():
    return platform.system()


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"
