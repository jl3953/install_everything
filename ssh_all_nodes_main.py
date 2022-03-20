import argparse
import shlex
import subprocess
import sys

import utils


def install_everything():
    cmd = ("git clone https://github.com/jl3953/install_everything /root/"
           "; python3 /root/install_everything/main.py")
    return subprocess.Popen(shlex.split(cmd))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num_nodes", type=int, help="number of nodes")
    args = parser.parse_args()

    clone_cmd = ("git clone https://github.com/jl3953/install_everything "
                 "/root/install_everything")
    pull_cmd = "cd /root/install_everything && git pull origin master "
    run_cmd = "python3 /root/install_everything/main.py "

    processes = []
    for i in range(args.num_nodes):

        # configure ssh
        utils.call("ssh-keyscan node-{} >> /root/.ssh/known_hosts".format(i))

        # identify host
        host = "node-{}".format(i)

        # try to git clone install_everything
        try:
            utils.call_remote(host, clone_cmd)
        except BaseException:
            print("install_everything repo already exists on {}".format(host))
            utils.call_remote(host, pull_cmd)

        # run install_everything
        cmd = "ssh {0} '{1}'".format(host, run_cmd)
        if i == 0:
            driver_node_run_cmd = "{0} --smdbrpc --clone_test_scripts".format(
                run_cmd)
            cmd = "ssh {0} '{1}'".format(host, driver_node_run_cmd)
        elif i == 11:
            cicada_node_run_cmd = "{0} --cicada".format(run_cmd)
            cmd = "ssh {0} '{1}'".format(host, cicada_node_run_cmd)
        print(cmd)
        processes.append(subprocess.Popen(shlex.split(cmd)))

    # wait for processes to finish
    for p in processes:
        p.wait()

    return 0


if __name__ == "__main__":
    sys.exit(main())
