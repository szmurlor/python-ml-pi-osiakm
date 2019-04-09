import spotipy
import csv
import spotipy.util as util


def get_data(artist_id):
    columns = [
        'name',
        'artist',
        'album',
        'release_date',
        'spotify_id',
        'popularity',
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
    data = [columns]
    albums = get_albums(artist_id)
    for album_id in albums:
        data += get_all_tracks(album_id)
    save_as_csv('paramore_tracks.csv', data)


def get_albums(artist_id):
    album_list = sp.artist_albums(artist_id=artist_id,
                                  album_type='album', limit=30)['items']
    for i, album in enumerate(album_list):
        print(i, album['name'])
    print('Which albums do you want to keep?')
    answer = list(map(int, input().split()))
    return [album_list[i]['id'] for i in answer]


def get_all_tracks(album_id):
    tracks = list()
    tracks_list = [item['id'] for item in sp.album_tracks(album_id=album_id)['items']]
    for id in tracks_list:
        tracks.append(get_track(id))
    audio_features = get_audio_features(tracks_list)
    return [tracks[i] + audio_features[i] for i in range(len(tracks))]
    return []


def get_track(track_id):
    track = sp.track(track_id=track_id)
    return [
        track['name'],
        track['artists'][0]['name'],
        track['album']['name'],
        track['album']['release_date'],
        track['id'],
        track['popularity']
    ]


def get_audio_features(ids):
    features = ['acousticness',
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
    result = list()
    audio_features = sp.audio_features(ids)
    for af in audio_features:
        result.append([af[feature] for feature in features])
    return result


def save_as_csv(data):
    with open(data[1][1], 'w', encoding='utf-8') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(data)


username = 'hardreamer'
scope = 'user-library-read playlist-read-private'
artist_id = '74XFHRwlV6OrjEM0A2NCMF'  # Paramore
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='060305157323499d95406a8fc72482bf',
                                   client_secret='bee088fdec1a4bf886cc125520508196',
                                   redirect_uri='http://localhost:8888/callback/')

if token:
    sp = spotipy.Spotify(auth=token)
    print('Artist?')
    query = input()
    results = sp.search(q=query,
                        type='artist')
    print('Do you mean:')
    for i, item in enumerate(results['artists']['items']):
        print('\t', i, item['name'])
    # get_data(artist_id)
