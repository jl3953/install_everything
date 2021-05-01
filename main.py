import sys
import utils


def install_cockroachdb_dependencies():
    # libncurses-dev
    utils.call("apt install libncurses5-dev -y")

    # golang
    utils.call("wget https://golang.org/dl/go1.15.8.linux-amd64.tar.gz")
    utils.call("tar -C /usr/local -xzf go1.15.8.linux-amd64.tar.gz")

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

    utils.call("apt install cmake -y")


def clone_upstream_cockroach_repo():
    # original cockroachdb
    utils.call("mkdir -p /root/go/src/github.com/cockroachdb")
    utils.call("cd /root/go/src/github.com/cockroachdb; "
               "git clone https://github.com/cockroachdb/cockroach; "
               "cd cockroach; "
               "export PATH=$PATH:/root/go/bin:/usr/local/go/bin; "
               "git fetch origin staging-20.1.9; git checkout staging-20.1.9; "
               "git clean -fdx; make clean; make")
    utils.call("mv /root/go/src/github.com/cockroachdb/cockroach /root")


def clone_cockroach_repo():
    utils.call("mkdir -p /root/go/src/github.com/cockroachdb")
    utils.call("cd /root/go/src/github.com/cockroachdb; "
               "git clone --recurse-submodules https://github.com/jl3953/cockroach3.0 cockroach")


def build_cockroach_from_scratch():
    utils.call("cd /root/go/src/github.com/cockroachdb/cockroach; "
               "export PATH=$PATH:/root/go/bin:/usr/local/go/bin; "
               "git clean -fdx; "
               "make clean; "
               "make")


def change_cockroach_vendor_origin():
    utils.call("cd /root/go/src/github.com/cockroachdb/cockroach/vendor; "
               "git remote rename origin upstream; "
               "git remote add origin https://github.com/jl3953/vendored2; "
               "git fetch origin jacks_code_again; "
               "git checkout jacks_code_again; ")


def install_cockroachdb():
    install_cockroachdb_dependencies()
    clone_upstream_cockroach_repo()
    try:
        clone_cockroach_repo()
    except BaseException:
        print("we'll be fine")
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
    utils.call("/root/grpc/test/distrib/cpp/run_distrib_test_cmake.sh ")


def setup_bashrc():
    utils.call("echo 'export PATH=$PATH:/root/.local/bin:/usr/local/go/bin:/root/go/bin:/root/.local' >> /root/.bashrc")


def install_grpc_go():
    utils.call("export GO111MODULE=on; "
               "go get google.golang.org/protobuf/cmd/protoc-gen-go google.golang.org/grpc/cmd/protoc-gen-go-grpc; "
               "export PATH=$PATH:/root/go/bin:/usr/local/go/bin; ")
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
               "export PATH=$PATH:/root/go/bin:/usr/local/go/bin:/root/.local/bin; "
               "/usr/local/go/bin/go get google.golang.org/protobuf/cmd/protoc-gen-go google.golang.org/grpc/cmd/protoc-gen-go-grpc; "
               "protoc --go_out=../go/build/gen --go-grpc_out=../go/build/gen *.proto; ")


def install_cicada_dependencies():
    utils.call("apt update")
    utils.call("apt install -y software-properties-common")
    utils.call("add-apt-repository -y ppa:ubuntu-toolchain-r/test")
    utils.call("apt update")

    utils.call("apt-get install -y build-essential cmake git libjemalloc-dev libnuma-dev")


def install_cicada():
    utils.call("cd /root; "
               "git clone https://github.com/jl3953/cicada-engine; "
               "cd cicada-engine; "
               "mkdir -p build; cd build; "
               "export PATH=$PATH:/root/.local:/root/.local/bin; "
               "cmake -DLTO=ON -DDEBUG=OFF ..; "
               "make -j; cp ../src/mica/test/*.json .; "
               "../script/setup.sh 16384 16384; ")


def main():
    utils.call("apt update")
    utils.call("apt install gnuplot-x11 -y")
    utils.call("apt install htop -y")
    utils.call("apt install feh -y")
    setup_vimrc()
    install_cockroachdb()

    install_grpc()
    install_grpc_go()

    #install_smdbrpc_dependencies()
    #install_smdbrpc()
    install_cicada_dependencies()
    install_cicada()
    setup_bashrc()

    utils.call("rm -rf /root/cockroach")

    return 0


if __name__ == '__main__':
    sys.exit(main())
