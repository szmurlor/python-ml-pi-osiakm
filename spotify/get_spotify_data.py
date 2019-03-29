import spotipy
import spotipy.util as util
import pprint as pp
import csv


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s %s" % (i, track['artists'][0]['name'], track['name'], track['id']))

def get_tracks(tracks):
    result = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        id = track['id']
        result.append([i, track['artists'][0]['name'], track['name'], track['id']])
    return result

def get_audio_features(list_of_tracks):
    result = []
    ids = [x[3] for x in list_of_tracks]
    audio_features = sp.audio_features(ids)
    for track in audio_features:
        result.append(track)
    return result

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
    print(sourcePlaylist['name'])
    print('total tracks: ', sourcePlaylist['tracks']['total'])

    tracks = sourcePlaylist["tracks"]
    show_tracks(tracks)
    l = get_tracks(tracks)
    # pp.pprint(l)
    csv_file = 'spotify_playlist.csv'
    with open(csv_file, 'w', encoding='utf-8') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(l)
    af = get_audio_features(l)
    pp.pprint(af)
else:
    print("Can't get token for", username)