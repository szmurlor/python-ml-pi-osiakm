import spotipy
import csv
import spotipy.util as util


def get_data(artist_id):
    data = [track_data + audio_features_names]
    albums = get_albums(artist_id)
    for album_id in albums:
        data += get_album_tracks(album_id)
    save_as_csv(data)
    print('oki')


def get_albums(artist_id):
    album_list = sp.artist_albums(artist_id=artist_id,
                                  album_type='album',
                                  limit=30)['items']
    for i, album in enumerate(album_list):
        print(i, album['name'])
    print('Which albums do you want to keep?')
    answer = list(map(int, input('Index(es): ').split()))
    return [album_list[i]['id'] for i in answer]


def get_track_ids(album_id):
    return [item['id'] for item in sp.album_tracks(album_id=album_id)['items']]


def get_album_tracks(album_id):
    tracks = list()
    track_ids = get_track_ids(album_id)
    for id in track_ids:
        tracks.append(get_track(id))
    features = get_audio_features(track_ids)
    return [tracks[i] + features[i] for i in range(len(tracks))]


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


def get_audio_features(track_ids):
    result = list()
    list_of_audio_features = sp.audio_features(track_ids)
    for feature in list_of_audio_features:
        result.append([feature[name] for name in audio_features_names])
    return result


def save_as_csv(data):
    with open(get_filename(data[1][1]), 'w', encoding='utf-8') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(data)


def get_filename(artist):
    return 'data/' + artist.lower().replace(' ', '_') + '.csv'


username = 'hardreamer'
scope = 'user-library-read playlist-read-private'
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='060305157323499d95406a8fc72482bf',
                                   client_secret='bee088fdec1a4bf886cc125520508196',
                                   redirect_uri='http://localhost:8888/callback/')
track_data = [
        'name',
        'artist',
        'album',
        'release_date',
        'spotify_id',
        'popularity']

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
    print('Who are you looking for?')
    query = input()
    results = sp.search(q=query,
                        type='artist')['artists']['items']
    print('Do you mean:')
    for i, item in enumerate(results):
        print('\t', i, item['name'])
    my_artist_id = results[int(input('Index? '))]['id']
    get_data(my_artist_id)
