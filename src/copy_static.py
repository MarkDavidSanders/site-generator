# src/copy_static.py

'''
Recursive function that copies all the contents from "static" to "public" directory
First delete all the contents of the destination directory to ensure that the copy is clean.
Should copy all files and subdirectories, nested files, etc.

Logging functionality included for debugging purposes. I've commented it all out for now.
'''

import logging
import os
import shutil
import sys


def copy_static(src_dir, dest_dir):
    '''
    Deletes contents of destination directory ("public")
    and recursively copies contents from source directory ("static").

    ALL RELATIVE FILE PATHS ARE RELATIVE TO THE ROOT DIRECTORY ("site-generator").
    This script lives in site-generator/src/ but is called from site-generator root.
    '''

    # logging.basicConfig(filename='copy_static.log',
    #                     level=logging.INFO,
    #                     format='%(asctime)s - %(levelname)s - %(message)s')

    # build absolute paths
    root = os.path.abspath('.') # site-generator root directory
    abs_src_dir = os.path.join(root, src_dir)
    abs_dest_dir = os.path.join(root, dest_dir)

    # logging.info('Root directory: %s', root)
    # logging.info('Source path provided: %s', abs_src_dir)
    # logging.info('Destination path provided: %s', abs_dest_dir)

    # verify that source path exists and is in the right place
    if not os.path.exists(abs_src_dir) or root not in abs_src_dir:
        # logging.error(
        #     'Invalid source path provided. Path must be located within the site-generator root.')
        sys.exit(1)

    # delete contents of destination folder (if it exists and contains anything)
    if not os.path.exists(abs_dest_dir) or not os.listdir(abs_dest_dir):
    #     logging.info('Destination folder does not exist or is already empty')
        pass

    else:
        try:
            for item in os.listdir(abs_dest_dir):
                item_path = os.path.join(abs_dest_dir,item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    # logging.info('Recursively deleted %s/%s/', dest_dir, item)
                elif item != '.DS_Store':
                    os.remove(item_path)
            #         logging.info('Deleted %s/%s', dest_dir, item)
            # logging.info('Destination folder cleared')

        except Exception as e:
            # logging.error('Something went wrong while clearing destination folder: %s', e)
            print(f"!!! Something went wrong while clearing destination folder: {e}")
            sys.exit(1)

    # recursively copy src_dir files/subdirectories
    # create destination dir as needed
    if not os.path.exists(abs_dest_dir):
        os.mkdir(abs_dest_dir)

    # get list of src_dir contents and iterate
    src_contents = os.listdir(abs_src_dir)
    try:
        for src_item in src_contents:
            src_item_path = os.path.join(abs_src_dir, src_item)
            # if item is file, copy the file
            if os.path.isfile(src_item_path) and src_item != '.DS_Store':
                # logging.info('Copying %s', src_item)
                shutil.copy(src_item_path, abs_dest_dir)
            # if item is folder, call copy_static with it
            elif os.path.isdir(src_item_path):
                # logging.info('Recursively copying %s', src_item_path)
                dest_item_path = os.path.join(abs_dest_dir, src_item)
                copy_static(src_item_path, dest_item_path)
    except Exception as e:
    #     logging.error('Something went wrong while copying: %s', e)
        print(f"!!! Something went wrong while copying: {e}")
        sys.exit(1)

    # logging.info('%s contents successfully copied to %s', src_dir, dest_dir)
