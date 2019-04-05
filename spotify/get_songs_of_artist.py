import spotipy
import spotipy.util as util
import csv
import pprint as pp


def get_albums(raw_albums):
    result = dict()
    for album in raw_albums:
        result[album['id']] = [album['artists'][0]['name'], album['name'], album['release_date'][:4]]
    # result['228Mzfzb0i3e43RmgPAHAM'] = ['Taco Hemingway', 'Flagey', '2018']
    # result['2FR4jyEN61L5p0uoHGQhkF'] = ['Taco Hemingway', 'Wosk', '2016']
    return result


def get_tracks(albums):
    columns = [
        'name',
        'artist',
        'album',
        'release_date',
        'spotify_id',
        'popularity'
    ]
    result = [columns]
    for id, album in albums.items():
        songs_from_album = sp.album_tracks(id)
        songs_from_album = songs_from_album['items']
        for item in songs_from_album:
            id = item['id']
            track = sp.track(id)
            result.append([
                track['name'],
                track['artists'][0]['name'],
                track['album']['name'],
                track['album']['release_date'],
                track['id'],
                track['popularity']
            ])
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
    ids = [x[4] for x in tracks]
    start = 0
    finish = start + 50
    while(start < len(ids)):
        audio_features = sp.audio_features(ids[start:finish])
        for track in audio_features:
            if track:
                data = [track[x] for x in columns]
                result.append(data)
        start = finish
        finish = start + 50
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
# todo: dict z nazwami potencjalnych artystów do analizy i ich spotify id
# artist_id = '7CJgLPEqiIRuneZSolpawQ'  # Taco Hemingway
artist_id = '6XyY86QOPPrYVGvF9ch6wz'  # Linkin Park
# artist_id = '3hN3iJMbbBmqBSAMx5veDa' #  Ultimo
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='060305157323499d95406a8fc72482bf',
                                   client_secret='bee088fdec1a4bf886cc125520508196',
                                   redirect_uri='http://localhost:8888/callback/')

if token:
    sp = spotipy.Spotify(auth=token)
    raw_albums = sp.artist_albums(artist_id=artist_id,
                                  album_type='album')
    raw_albums = raw_albums['items']
    albums = get_albums(raw_albums) # albums as a dict - key: id
    tracks = get_tracks(albums)
    features = get_audio_features(tracks)
    data = get_full_data(tracks, features)
    csv_file = 'linkin_park_tracks.csv'
    save_as_csv(csv_file, data)
else:
    print("Can't get token for", username)
