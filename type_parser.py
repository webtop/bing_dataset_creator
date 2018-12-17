"""
    This file is responsible for reading ina  list of items in the input file, creating the
    necessary folder structure, and then calling the Bing image API script to fetch
    and save the related images
"""
import argparse
import os

ITEM_TYPE_FOLDER = "./datasets/input_files"
IMAGE_FOLDER = "./datasets/images"

def type_parser_main():
    """Just because pylint says so"""
    args = get_args()
    set_path = "{}/{}".format(IMAGE_FOLDER, args['name'].lower().replace(" ", "_"))
    if os.path.isdir(set_path):
        msg = """Folder {} already exists in datasets. Please remove or specify a different name"""
        print(msg.format(set_path))
        exit(1)

    os.mkdir(set_path)
    input_file = "{}/{}".format(ITEM_TYPE_FOLDER, args['input'])

    if os.path.isfile(input_file):
        control_list = list(open(input_file, 'r'))
        for item in control_list:
            item = item.rstrip("\r\n").lower().replace(" ", "_")
            item_path = "{}/{}".format(set_path, item)

            try:
                print("Creating folder {}...".format(item_path))
                os.mkdir(item_path)
            except OSError as ex:
                print("Failed to create folder {} due to {}".format(item_path, ex))
                continue

            try:
                print("Running image search for {}...".format(item))

                # Be sure to use the original args value here, not the cleaned version
                query_string = '--query "{} {}"'.format(item, args['name'])
                output_string = '--output {}'.format(item_path)
                exec_string = "python search_bing_api.py {} {}".format(query_string, output_string)
                os.system(exec_string)
            except OSError as ex:
                print("Failed to fetch images for {} due to {}".format(item, ex))

def get_args():
    """construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help="name of the image subject")
    parser.add_argument("-i", "--input", required=True, help="name of the input file")
    args = vars(parser.parse_args())

    return args

if __name__ == "__main__":
    type_parser_main()
