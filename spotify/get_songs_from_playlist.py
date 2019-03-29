import spotipy
import spotipy.util as util
import csv


def show_tracks(raw_tracks):
    for i, item in enumerate(raw_tracks['items']):
        track = item['track']
        print("   %d %32.32s %s %s" % (i, track['artists'][0]['name'], track['name'], track['id']))


def get_tracks(raw_tracks):
    columns = ['artist_name',
               'track_name',
               'spotify_id']
    result = [columns]
    for i, item in enumerate(raw_tracks['items']):
        track = item['track']
        result.append([track['artists'][0]['name'], track['name'], track['id']])
    return result


def get_audio_features(tracks):
    columns = ['acousticness',
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
               'valence']
    result = [columns]
    ids = [x[2] for x in tracks]
    audio_features = sp.audio_features(ids)
    for track in audio_features:
        if track:
            data = [track[x] for x in columns]
            result.append(data)
    return result


def get_full_data(list_of_tracks, list_of_features):
    return [
        list_of_tracks[i] + list_of_features[i] for i in range(len(list_of_tracks))
    ]


def save_as_csv(csv_file, data):
    with open(csv_file, 'w', encoding='utf-8') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(data)


username = 'hardreamer'
scope = 'user-library-read playlist-read-private'
playlist_id = '53lUactAuesW5PVC8Hpo3c?si=Lyye34xiTVmW1c-JDWIs2g'
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='060305157323499d95406a8fc72482bf',
                                   client_secret='bee088fdec1a4bf886cc125520508196',
                                   redirect_uri='http://localhost:8888/callback/')

if token:
    sp = spotipy.Spotify(auth=token)
    sourcePlaylist = sp.user_playlist(username,
                                      playlist_id)

    raw_tracks = sourcePlaylist["tracks"]
    tracks = get_tracks(raw_tracks)
    features = get_audio_features(tracks)
    fd = get_full_data(tracks, features)
    csv_file = 'spotify_playlist.csv'
    save_as_csv(csv_file, fd)
else:
    print("Can't get token for", username)
