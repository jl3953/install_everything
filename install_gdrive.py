import sys
import utils


def install_gdrive():
    utils.call("wget https://docs.google.com/uc?id=0B3X9GlR6EmbnWksyTEtCM0VfaFE&export=download /root/gdrive")
    utils.call("chmod +x /root/gdrive")
    utils.call("install /root/gdrive /usr/local/bin/gdrive")


def authenticate_gdrive():
    utils.call("gdrive list")


def main():
    install_gdrive()
    authenticate_gdrive()

    return 0


if __name__ == "__main__":
    sys.exit(main())

