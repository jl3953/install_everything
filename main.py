import sys
import utils


def install_cockroachdb_dependencies():
    # libncurses-dev
    utils.call("apt install libncurses5-dev")

    # golang
    utils.call("wget https://golang.org/dl/go1.15.8.linux-amd64.tar.gz")
    utils.call("tar -C /usr/local -xzf go1.15.8.linux-amd64.tar.gz")
    utils.call("echo 'export PATH=$PATH:/usr/local/go/bin' >> /root/.bashrc")

    # install nodejs v12 and yarn
    utils.call("apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates")
    utils.call("curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -")
    utils.call("apt -y install nodejs")
    utils.call("npm install --global yarn")

    # install bazel
    utils.call("apt install curl gnupg")
    utils.call("curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg")
    utils.call("mv bazel.gpg /etc/apt/trusted.gpg.d/")
    utils.call(
        "echo 'deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8' | sudo tee /etc/apt/sources.list.d/bazel.list")
    utils.call("sudo apt update -y && sudo apt install bazel -y")
    utils.call("sudo apt update -y && sudo apt full-upgrade -y")


def clone_cockroach_repo():
    utils.call("mkdir -p $(go env GOPATH)/src/github.com/cockroachdb")
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb;"
               "git clone https://github.com/jl3953/cockroach3.0 cockroach")


def build_cockroach_from_scratch():
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb/cockroach;"
               "git clean -fdx;"
               "make clean;"
               "make")


def change_cockroach_vendor_origin():
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb/cockroach/vendor;"
               "git remote rename origin upstream;"
               "git remote add origin https://github.com/jl3953/vendored2")


def install_cockroachdb():
    install_cockroachdb_dependencies()
    clone_cockroach_repo()
    build_cockroach_from_scratch()
    change_cockroach_vendor_origin()
    build_cockroach_from_scratch()


def setup_vimrc():
    utils.call("echo 'set nu' >> /root/.vimrc")
    utils.call("echo 'set autoindent' >> /root/.vimrc")
    utils.call("echo 'set tabstop=4 shiftwidth=4 expandtab' >> /root/.vimrc")


def main():
    utils.call("apt update")
    utils.call("apt upgrade -y")
    utils.call("apt install gnuplot-x11 -y")
    utils.call("apt install htop -y")
    utils.call("apt install feh -y")
    setup_vimrc()

    install_cockroachdb()

    return 0


if __name__ == '__main__':
    sys.exit(main())
