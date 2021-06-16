import subprocess
import sys


import utils


def install_gdrive():
    utils.call("wget --output-document=/root/gdrive https://docs.google.com/uc?id=0B3X9GlR6EmbnWksyTEtCM0VfaFE&export=download")
    utils.call("chmod +x /root/gdrive")
    utils.call("install /root/gdrive /usr/local/bin/gdrive")
    utils.call("install /root/install_everything/gdrive_upload.sh /usr/local/bin/gdrive_upload")


def main():
    install_gdrive()

    return 0


if __name__ == "__main__":
    sys.exit(main())

