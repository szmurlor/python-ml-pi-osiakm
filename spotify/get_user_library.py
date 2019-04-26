import spotipy
import csv
import spotipy.util as util


def get_data(limit, offset):
    raw_data = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
    data = [[item['added_at'],
             item['track']['id'],
             item['track']['name'],
             item['track']['artists'][0]['name']] for item in raw_data
    ]
    audio = get_audio_features([item[1] for item in data])
    return [data[x] + audio[x] for x in range(len(data))]


def get_audio_features(track_ids):
    result = list()
    list_of_audio_features = sp.audio_features(track_ids)
    for feature in list_of_audio_features:
        result.append([feature[name] for name in audio_features_names])
    return result


def save_as_csv(data):
    with open('data/my_data.csv', 'w', encoding='utf-8') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(data)


username = 'hardreamer'
scope = 'user-library-read playlist-read-private'
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='060305157323499d95406a8fc72482bf',
                                   client_secret='bee088fdec1a4bf886cc125520508196',
                                   redirect_uri='http://localhost:8888/callback/')

audio_features_names = [
        'acousticness',
        'danceability',
        'duration_ms',
        'energy',
        'instrumentalness',
        'key',
        'liveness',
        'loudness',
        'mode',
        'speechiness',
        'tempo',
        'valence'
    ]

if token:
    sp = spotipy.Spotify(auth=token)
    result = [[
        'added_at',
        'id',
        'name',
        'artist',
        'acousticness',
        'danceability',
        'duration_ms',
        'energy',
        'instrumentalness',
        'key',
        'liveness',
        'loudness',
        'mode',
        'speechiness',
        'tempo',
        'valence'
    ]]
    for i in range(0, 650, 50):
        result += get_data(50, i)

    save_as_csv(result)
