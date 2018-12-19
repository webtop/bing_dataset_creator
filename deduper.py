"""
    This files purpose is to generate hashes from images, to look for duplicates
    and then remove them.
"""
import argparse
import os
import cv2

def dedupe():
    """Just because pylint says so"""
    args = get_args()
    remove = []
    hashes = []
    if os.path.isdir(args['folder']):
        for root, folder, image_files in os.walk(args['folder']):
            for image_file in image_files:
                image = cv2.imread("{}/{}".format(root, image_file))
                if image is None:
                    # Probably an encoding issue so mark for removal
                    remove.append(image_file)
                    continue

                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image_hash = dhash(image)

                if str(image_hash) not in hashes:
                    hashes.append(str(image_hash))
                else:
                    remove.append(image_file)

            if folder:
                folder = folder[0]

            if remove:
                for image_file in remove:
                    os.remove("{}/{}".format(root, image_file))

                print("Removed {} duplicate images from {}".format(len(remove), root))

            hashes = []
            remove = []
    else:
        print("Folder {} does not exist".format(args['folder']))

def dhash(image, hash_size=8):
    """Resize the image and generate a hash from it"""
    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    resized = cv2.resize(image, (hash_size + 1, hash_size))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash
    return sum([2 ** index for (index, value) in enumerate(diff.flatten()) if value])

def get_args():
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", required=True, help="name of the folder to dedupe")
    args = vars(parser.parse_args())

    return args

if __name__ == "__main__":
    dedupe()
