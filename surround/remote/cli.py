import os
from pathlib import Path

from . import base
from . import local

__author__ = 'Akshat Bajaj'
__date__ = '2019/02/26'

BASE_REMOTE = base.BaseRemote()
LOCAL = local.Local()

def is_surround_project():
    """Whether inside surround project root directory
    Check for the .surround folder
    """
    file_ = Path(".surround/config.yaml")
    if file_.exists():
        return True
    else:
        return False

def parse_remote_args(parsed_args):
    remote_name = parsed_args.name
    remote_path = parsed_args.path
    global_ = parsed_args.glob
    add = parsed_args.add
    verify = parsed_args.verify
    if add:
        if global_:
            # Make directory if not exists
            home = str(Path.home())
            os.makedirs(os.path.dirname(home + "/.surround/config.yaml"), exist_ok=True)
            if remote_name and remote_path:
                BASE_REMOTE.write_config("remote", home + "/.surround/config.yaml", remote_name, remote_path)
            else:
                print("Supply remote name and path")
        else:
            if is_surround_project():
                if remote_name and remote_path:
                    BASE_REMOTE.write_config("remote", ".surround/config.yaml", remote_name, remote_path)
                else:
                    print("Supply remote name and path")
            else:
                print("Not a surround project")
                print("Goto project root directory")
    else:
        if global_:
            remotes = BASE_REMOTE.read_all_from_global_config("remote")
            if remotes:
                for key, value in remotes.items():
                    if key:
                        if verify:
                            print(key + ": " + value)
                        else:
                            print(key)
            else:
                print("No global remote")
        else:
            if is_surround_project():
                remotes = BASE_REMOTE.read_all_from_local_config("remote")
                if remotes:
                    for key, value in remotes.items():
                        if key:
                            if verify:
                                print(key + ": " + value)
                            else:
                                print(key)
                else:
                    print("No local remote")
            else:
                print("Not a surround project")
                print("Goto project root directory")

def parse_add_args(parsed_args):
    if is_surround_project():
        remote = parsed_args.remote
        file_to_add = parsed_args.file
        message = LOCAL.add(remote, file_to_add)
        print(message)
    else:
        print("Not a surround project")
        print("Goto project root directory")

def parse_pull_args(parsed_args):
    if is_surround_project():
        remote = BASE_REMOTE.read_from_config("remote", parsed_args.remote)
        if remote:
            file_ = parsed_args.file
            message = LOCAL.pull(parsed_args.remote, file_)
            print(message)
        else:
            print("Supply remote to pull from")
    else:
        print("Not a surround project")
        print("Goto project root directory")

def parse_push_args(parsed_args):
    if is_surround_project():
        remote = BASE_REMOTE.read_from_config("remote", parsed_args.remote)
        if remote:
            file_ = parsed_args.file
            message = LOCAL.push(parsed_args.remote, file_)
            print(message)
        else:
            print("Supply remote to push to")
    else:
        print("Not a surround project")
        print("Goto project root directory")
