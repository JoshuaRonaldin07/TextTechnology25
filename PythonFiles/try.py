import pandas as pd
import matplotlib
import requests
import matplotlib.pyplot as plt
API_URL = "https://dracor.org/api/v1/"
# to get the info we extend the API URL by the parameter "info"
# save "info" parameter in variable
INFO_EXTENSION = "info"

# add extension to the base URL
api_info_url = API_URL + INFO_EXTENSION

# perform get request
r = requests.get(api_info_url)
r.text
# read response as JSON
parsed_response = r.json()
parsed_response
print(f"The current version of the Dracor-API is {parsed_response['version']}.")
# save "corpora" parameter in variable
CORPORA_EXT_PLAIN = "corpora"
# add parameter to base URL to get information about the DraCor corpora 
api_corpora_url = API_URL + CORPORA_EXT_PLAIN
print(f"URL for getting the list of corpora: {api_corpora_url}\n")

# perform API request
# parse response with .json
corpus_list = requests.get(api_corpora_url).json()

#save corpus abbreviations in a list for later checking 
corpus_abbreviations = []

# iterate through corpus list and print information
for corpus_description in corpus_list:
    name = corpus_description["name"]
    print(f'{name}: {corpus_description["title"]}')
    corpus_abbreviations.append(name)
    # save metrics parameter in variable
    
METRICS_PARAM_EXT = "?include=metrics"

# add parameter to URL to get more information about the corpora 
api_corpora_metrics_urls = api_corpora_url + METRICS_PARAM_EXT
print(f"URL for getting the list of corpora with metrics included: {api_corpora_metrics_urls}\n")

# perform API request
corpora_metrics = requests.get(api_corpora_metrics_urls).json()

# iterate through corpus list and print information
# add the number of plays to the print statement which is retrieved from the corpus metrics
print("Abbreviation: Corpus Name (Number of plays)")
for corpus in corpora_metrics:
    abbreviation = corpus['name']
    num_of_plays = corpus['metrics']['plays']
    print(f"{abbreviation}: {corpus['title']} ({str(num_of_plays)})")
    
for i in range(10):
    # get corpusname with user input
    # save corpusname in variable
    corpusname = str(input("Please choose a corpusname from the list above. Enter the abbreviation: "))
    if corpusname not in corpus_abbreviations:
        print("The abbreviation you selected is not in the list. Please enter the abbreviation again.")
    else:
        print("Success!")
        break
else:
    corpusname = "shake"
    # save corpora parameter (with slash) and metadata parameter in variables

CORPORA_EXT = "corpora/"
METADAT_EXT = "/metadata"

# build URL
corpus_metadata_path = API_URL + CORPORA_EXT + corpusname + METADAT_EXT
print(f"URL for getting the metadata of a specific corpus: {corpus_metadata_path}\n")
print("Attempting to download metadata CSV...")

# perform request
from io import StringIO
response = requests.get(corpus_metadata_path, headers={"accept": "text/csv"})
metadata_df = pd.read_csv(StringIO(response.text))

# display first five lines of the retrieved metadata 
metadata_df.head()
# print column names available in meta data 
metadata_df.columns
# 1. Get number of characters of each play and plot the normalized year
metadata_df.plot(x="yearNormalized", y="size", kind="scatter")
# 2. Plot length of play in words by the normalized year
metadata_df.plot(x="yearNormalized", y="wordCountText", kind="scatter", )
# 3. Sort plays by wordcount, show first 5 entries
metadata_by_length = metadata_df.sort_values(by="wordCountText", axis=0, ascending=False)

# get the first five entries 
metadata_by_length[0:5]
# 4. Get number of plays between 1800 and 1900 
num_of_plays = len(metadata_df[(metadata_df["yearNormalized"] > 1800) & (metadata_df["yearNormalized"] < 1900)])
print(f"Number of plays in the selected time period: {num_of_plays}")
# 5. Calculate percentage of tokens in stage directions in relation to all tokens 
# save the calculated percentages in a new column
stage_percentage = metadata_df["wordCountStage"] / metadata_df["wordCountText"]
metadata_df["wordCountStagePercentage"] = stage_percentage
metadata_df.plot(x="yearNormalized", y="wordCountStagePercentage", kind="scatter")
# 6. Display the relation of female speaker over time
speakers_total = metadata_df["numOfSpeakers"]
metadata_df["numOfSpeakersFemalePercentage"] = metadata_df["numOfSpeakersFemale"] / speakers_total
metadata_df.plot(x="yearNormalized", y="numOfSpeakersFemalePercentage", kind="scatter")


PLAY_EXT="/plays/"
# save column name in which the play names are stored in a variable 
PLAY_KEY = "name"
for i in range(10):
    # get play name with user input
    # save play name in variable
    play_name = str(input("Please choose a text from the corpus you have chosen. Enter the text name: "))
    if play_name not in metadata_df[PLAY_KEY].values:
        print("The name you selected is not in the list. Please enter the name again.")
    else:
        print("Success!")
        break
else:
    play_name = "strindberg-gillets-hemlighet"
# build URL
play_path = API_URL + CORPORA_EXT + corpusname + PLAY_EXT + play_name
print(f"URL for getting information of a specific play: {play_path}\n")

# perform request
play_info = requests.get(play_path).json()

# extract character names
character_names = [entry["name"] for entry in play_info["characters"]]
print("Character list")
print(character_names)

# API call for getting a specific play is saved in the variable `play_path`
# This is it consists of 
print(API_URL)
print(CORPORA_EXT)
print(corpusname)
print(PLAY_EXT)
print(play_name)
print(f"Combined the URL looks like this: {play_path}")

# We can add something to the URL like this:
# (just replace anything-you-want-to-add with the keyword of your choice)
# add your chosen parameter to the path to the play you selected
character_url = play_path + "/anything-you-want-to-add"

# perform request
character_info = requests.get(character_url)
if character_info.status_code != 200:
    print(f"It looks like your URL is not valid. Status code is: {character_info.status_code}")
else:
    print("Success! Here is the output:")
    print(character_info.json())
    plt.show()