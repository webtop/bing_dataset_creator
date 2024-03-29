# Simple Machine Learning Dataset Creator
Creates a dataset of images based off a list of item types (i.e. cats).

Dataset can then be used in a Machine Learning training model

The topic is stored in a file in the ./datasets/input_files folder and passed into the main script as a command line argument.

Note: You will need to create your own config.py file to hold your API key for the Bing Cognitive Service

## Example
*python type_parser.py -n cat_breeds -i cat_breeds.txt*

where:
-    -n is the name of the topic to do an image search on
-    -i is the name of the file with the list of subtopics (breeds for animals)

## Workflow
- type_parser.py - is the runner which checks for errors and parses the command line args
- search_bing_api.py - uses the Bing API service based on your key from config, to find and download images
- deduper.py - removes any duplicate images it finds, based on hashing the file via OpenCV
- mover.py - splits the dataset into the training and testing folders

## To Do
- [ ] Create dummy config file
- [ ] Convert move.php to Python
