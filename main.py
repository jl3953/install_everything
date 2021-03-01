import sys
import utils


def install_cockroachdb_dependencies():
    # libncurses-dev
    utils.call("apt install libncurses5-dev -y")

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
    utils.call("apt install curl gnupg -y")
    utils.call("curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg")
    utils.call("mv bazel.gpg /etc/apt/trusted.gpg.d/")
    utils.call(
        "echo 'deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8' | sudo tee /etc/apt/sources.list.d/bazel.list")
    utils.call("sudo apt update -y && sudo apt install bazel -y")
    # utils.call("sudo apt update -y && sudo apt full-upgrade -y")

    utils.call("apt install cmake -y")


#    utils.call("source /root/.bashrc")


def clone_upstream_cockroach_repo():
    # original cockroachdb
    utils.call("mkdir -p $(go env GOPATH)/src/github.com/cockroachdb")
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb; "
               "git clone https://github.com/cockroachdb/cockroach; "
               "cd cockroach; "
               "git fetch origin staging-20.1.9; git checkout staging-20.1.9; "
               "git clean -fdx; make clean; make")
    utils.call("mv $(go env GOPATH)/src/github.com/cockroachdb/cockroach /root")


def clone_cockroach_repo():
    # utils.call("mkdir -p $(go env GOPATH)/src/github.com/cockroachdb")
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb;"
               "git clone https://github.com/jl3953/cockroach3.0 cockroach")


def build_cockroach_from_scratch():
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb/cockroach;"
               "git clean -fdx;"
               "make clean;"
               "make")


def change_cockroach_vendor_origin():
    utils.call("cd $(go env GOPATH)/src/github.com/cockroachdb/cockroach/vendor; "
               "git remote rename origin upstream; "
               "git remote add origin https://github.com/jl3953/vendored2; "
               "git fetch origin jacks_code_again; "
               "git checkout jacks_code_again; ")


def install_cockroachdb():
    install_cockroachdb_dependencies()
    clone_upstream_cockroach_repo()
    clone_cockroach_repo()
    build_cockroach_from_scratch()
    change_cockroach_vendor_origin()
    build_cockroach_from_scratch()


def setup_vimrc():
    utils.call("echo 'set nu' >> /root/.vimrc")
    utils.call("echo 'set autoindent' >> /root/.vimrc")
    utils.call("echo 'set tabstop=4 shiftwidth=4 expandtab' >> /root/.vimrc")


def install_grpc():
    utils.call("export MY_INSTALL_DIR=/root/.local; "
               "mkdir -p $MY_INSTALL_DIR")
    utils.call("apt install -y build-essential autoconf libtool pkg-config")
    utils.call("cd /root; "
               "git clone --recurse-submodules -b v1.35.0 https://github.com/grpc/grpc")
    utils.call("export MY_INSTALL_DIR=/root/.local; "
               'export PATH="$PATH:$MY_INSTALL_DIR/bin"; '
               "cd /root/grpc; "
               "mkdir -p cmake/build; pushd cmake/build; "
               "cmake -DgRPC_INSTALL=ON -DgRPC_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR ../..; "
               "make -j; "
               "make install")
    utils.call("export MY_INSTALL_DIR=/root/.local; "
               'export PATH="$PATH:$MY_INSTALL_DIR/bin"; '
               "echo 'PATH=$PATH:$MY_INSTALL_DIR/bin' >> /root/.bashrc; ")


def install_grpc_go():
    utils.call("export GO111MODULE=on; "
               "go get google.golang.org/protobuf/cmd/protoc-gen-go google.golang.org/grpc/cmd/protoc-gen-go-grpc; "
               'export PATH="$PATH:$(go env GOPATH)/bin"')
    utils.call("cd /root; "
               "git clone -b v1.35.0 https://github.com/grpc/grpc-go; ")


def install_smdbrpc_dependencies():
    # YOU BETTER HAVE INSTALLED GO AT THIS POINT
    utils.call("apt install -y protobuf-compiler")


def install_smdbrpc():
    utils.call("cd /root; "
               "git clone https://github.com/jl3953/smdbrpc; "
               "cd smdbrpc/protos; "
               "export GO111MODULE=on; "
               "go get google.golang.org/protobuf/cmd/protoc-gen-go google.golang.org/grpc/cmd/protoc-gen-go-grpc; "
               "export PATH=$PATH:$(go env GOPATH)/bin; "
               "protoc --go_out=../go/build/gen --go-grpc_out=../go/build/gen *.proto; ")


def install_cicada():
    utils.call("cd /root; "
               "git clone https://github.com/jl3953/cicada-engine; "
               "cd cicada-engine; "
               "mkdir -p build; cd build; "
               "export PATH=$PATH:/root/.local; "
               "cmake -DLTO=ON ..; "
               "make -j; cp ../src/mica/test/*.json .; "
               "../script/setup.sh 16384 16384; ")


def main():
    # # utils.call("apt update")
    # # #utils.call("apt upgrade -y")
    # # utils.call("apt install gnuplot-x11 -y")
    # # utils.call("apt install htop -y")
    # # utils.call("apt install feh -y")
    # # #setup_vimrc()
    # #
    # # install_cockroachdb()
    #
    # install_grpc()
    #install_grpc_go()

    #install_smdbrpc_dependencies()
    #install_smdbrpc()
    install_cicada()

    return 0


if __name__ == '__main__':
    sys.exit(main())
