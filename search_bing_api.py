"""Search the Bing API service for required images and save to disk"""

# import the necessary packages
import argparse
import os
import requests
import cv2
import config

MAX_RESULTS = 250
GROUP_SIZE = 50
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

def main():
    """Just because PyLint says so"""

    args = get_args()

    headers = {"Ocp-Apim-Subscription-Key" : config.BING_API_KEY}
    params = {"q": args["query"], "offset": 0, "count": GROUP_SIZE}

    # make the search
    print("[INFO] searching Bing API for '{}'".format(args["query"]))
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()

    # grab the results from the search, including the total number of
    # estimated results returned by the Bing API
    results = search.json()
    est_num_results = min(results["totalEstimatedMatches"], MAX_RESULTS)
    print("[INFO] {} total results for '{}'".format(est_num_results, args["query"]))

    # initialize the total number of images downloaded thus far
    total = 0

    # loop over the estimated number of results in `GROUP_SIZE` groups
    for offset in range(0, est_num_results, GROUP_SIZE):
        # update the search parameters using the current offset, then
        # make the request to fetch the results
        print("[INFO] making request for group {}-{} of {}...".format(
            offset, offset + GROUP_SIZE, est_num_results))
        params["offset"] = offset
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()
        print("[INFO] saving images for group {}-{} of {}...".format(
            offset, offset + GROUP_SIZE, est_num_results))

        # loop over the results
        for result in results["value"]:
            # try to download the image
            try:
                path = get_image_and_save(result, args, total)

            # catch any errors that would not unable us to download the
            # image
            except (IOError, FileNotFoundError, requests.exceptions.RequestException,
                    requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as ex:
                print("[INFO] skipping: {} for {}".format(result["contentUrl"], ex))
                continue

            # try to load the image from disk
            image = cv2.imread(path)

            # if the image is `None` then we could not properly load the
            # image from disk (so it should be ignored)
            if image is None:
                print("[INFO] deleting: {}".format(path))
                os.remove(path)
                continue

            # update the counter
            total += 1

def get_image_and_save(result, args, total):
    """Make a request to the Bing API and save the resulting image"""

    # make a request to download the image
    print("[INFO] fetching: {}".format(result["contentUrl"]))
    req = requests.get(result["contentUrl"], timeout=30)

    # build the path to the output image
    ext = result["contentUrl"][result["contentUrl"].rfind("."):].lower()
    path = os.path.sep.join([args["output"], "{}{}".format(
        str(total).zfill(8), ext)]).rsplit('?')[0]

    # write the image to disk
    fpr = open(path, "wb")
    fpr.write(req.content)
    fpr.close()

    return path

def get_args():
    """construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", required=True, help="query to search Bing Image API for")
    parser.add_argument("-o", "--output", required=True, help="path to output directory of images")
    args = vars(parser.parse_args())

    return args

if __name__ == "__main__":
    main()
