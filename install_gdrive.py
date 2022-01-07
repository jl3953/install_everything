import subprocess
import sys


import utils


def install_gdrive():
    utils.call("wget --output-document=/root/gdrive.tar.gz https://github.com/prasmussen/gdrive/releases/download/2.1.1/gdrive_2.1.1_linux_386.tar.gz")
    utils.call("cd /root; gunzip gdrive.tar.gz; tar -xvf gdrive.tar;")
    utils.call("chmod +x /root/gdrive")
    utils.call("cd /root/install_everything; git pull origin master")
    utils.call("install /root/gdrive /usr/local/bin/gdrive")
    utils.call("install /root/install_everything/gdrive_upload_file.sh /usr/local/bin/gdrive_upload_file")
    utils.call("install /root/install_everything/gdrive_upload_dir.sh /usr/local/bin/gdrive_upload_dir")


def main():
    install_gdrive()

    return 0


if __name__ == "__main__":
    sys.exit(main())

