import requests
import json

def get_lyrics_mean(artist : str) -> float:
    '''The function returns the average/mean number of words in artist song'''
    recordings = get_recordings(artist)
    titles = get_titles(recordings)
    lyrics_count_list = []
    for title in titles:
        response = fetch_lyrics_data(artist,title)
        if response.status_code == 200:
            lyrics_data_obj = json.loads(response.content)
            lyrics_str = lyrics_data_obj['lyrics']
            word_count = get_word_count(lyrics_str)
            lyrics_count_list.append(word_count)
    print(lyrics_count_list)
    if len(lyrics_count_list)> 0:
        return (sum(lyrics_count_list) / len(lyrics_count_list))
    else:
        return 0

def get_recordings(artist : str) -> list:
    ''' The function is extracting and returning list of recordings for the artist provided'''
    response = fetch_recordings_data(artist)
    recording_data_obj = json.loads(response.content)
    return recording_data_obj['recordings']

def get_titles(recordings : list) -> list:
    ''' The function is extracting and returning list of song titles from the list of recordings provided'''
    title_list =[]
    for recording in recordings:
        title_list.append(recording['title'])
    print(title_list)
    return title_list

def get_word_count(lyrics : str) -> int:
    '''The function returns the word count for the lyrics provided'''
    word_list = lyrics.split()
    return len(word_list)

# Utility methods to fetch data from Web service
def fetch_recordings_data(artist : str,offset='0',limit='10') -> str:
    '''Fetch the recordings data for a particular artist in JSON format'''
    url = 'https://musicbrainz.org/ws/2/recording?query=artist:'+artist+'&limit='+limit+'&offset='+offset
    header = {"Accept": "application/json"}
    return requests.get(url,verify=False,headers=header)

def fetch_lyrics_data(artist : str , title : str) -> str:
    '''Fetch the lyrics data for a particular artist and a given song title in JSON format'''
    url = 'https://api.lyrics.ovh/v1/'+artist+'/'+title
    return requests.get(url,verify=False)

artist = input('Enter the artist name : ')
mean_val = get_lyrics_mean(artist)
print('Mean value of lyrics word count for artist',artist,'is', mean_val) 
