'''Extract files by type

Command line usage:
$ python order_files.py source_folder destination_folder

'''

import os
import sys
from shutil import copy2


def check_dest(destination_folder):
    """Creates the destination folder in case it doesn't exists
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    else:
        if not os.path.isdir(destination_folder):
            raise ValueError("File {} Found. Error".format(destination_folder))


def gen_folder(dest_folder, files_type):
    """Creates the folder for a filetype in the destination folder
    """
    future_path = os.path.join(dest_folder, files_type)

    if os.path.exists(future_path):
        if os.path.isdir(future_path):
            return future_path
        else:
            raise ValueError("{} Found. Error".format(future_path))
    else:
        os.makedirs(future_path)
        return future_path


def copy_file(org, dst):
    if os.path.exists(dst):
        copy_file(org, dst+"(1)")
    else:
        copy2(org, dst)


def order_files(src_f, dest_f):
    """ Scan the folder and save the files in the corresponding directory
    """
    if not os.path.isabs(src_f):
        src_f = os.path.realpath(src_f)

    if not os.path.isabs(dest_f):
        dest_f = os.path.realpath(dest_f)

    folder_list = os.listdir(src_f)

    for element in folder_list:
        if os.path.isdir(os.path.join(src_f, element)):
            order_files(os.path.join(src_f, element), dest_f)

        else:
            extension = os.path.splitext(element)[1]

            if extension != '':
                if extension[0] == '.':
                    extension = extension[1:]
                dest_path = gen_folder(dest_f, extension)
                copy_file(os.path.join(src_f, element),
                          os.path.join(dest_path, element))
                print("Copied " + os.path.join(dest_path, element))
            else:
                dest_path = gen_folder(dest_f, "OTHERS")
                copy_file(os.path.join(src_f, element),
                          os.path.join(dest_path, element))
                print("Copied " + os.path.join(dest_path, element))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        source_folder = sys.argv[1]
        destination_folder = sys.argv[2]

        if not os.path.isdir(source_folder):
            raise ValueError("Incorrect source folder")

        check_dest(destination_folder)
        order_files(source_folder, destination_folder)

    else:
        print(__doc__)
