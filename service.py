from flask import Flask

import echonest
import json
import functools

app = Flask(__name__)

@app.route("/generate_playlist/<songs>")
@app.route("/generate_playlist/<songs>/<limit>")
@app.route("/generate_playlist/<songs>/<limit>/<pretty>")
def generate_playlist(songs, limit=10, pretty=None):
    limit = int(limit)
    song_ids = songs.split(",")

    if pretty == "pretty":
        formatter = functools.partial(
            json.dumps,
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
    else:
        formatter = json.dumps

    try:
        result = echonest.generate_songs(song_ids, limit)
    except echonest.EchoNestException as ex:
        return formatter({
            'status': {
                'success': False,
                'message': ex.message
            }})

    response = {
        'status': {
            'success': True,
            'message': 'Success'
        },
        'songs': result}

    return formatter(response)

@app.errorhandler(500)
def pageNotFound(error):
    return json.dumps({
            'status': {
                'success': False,
                'message': "Unexpected error '{}'".format(error.message)
            }})

if __name__ == "__main__":
    app.run()