import platform
from getpass import getuser

user = getuser()

PHOTOS_DESTINATION="/home/%s/playground/images/" % user
VIDEOS_DESTINATION="/home/%s/playground/videos" % user

MEDIA_DIR = "/media"

# on Windows, set as destination directory My Pictures and My Videos
if platform.system() == "Windows":
    from win32com.shell import shell, shellcon
    PHOTOS_DESTINATION = shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, 0, 0)
    VIDEOS_DESTINATION = shell.SHGetFolderPath(0, shellcon.CSIDL_MYVIDEO, 0, 0)

    # TODO try to automatically select an external drive
    # for the moment do nothing
    MEDIA_DIR = "C:\\"

elif platform.system() == "Mac":
    PHOTOS_DESTINATION="/Users/%s" % user
    VIDEOS_DESTINATION="/Users/%s" % user

