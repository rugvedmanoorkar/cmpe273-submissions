from base64 import b64encode
from hashlib import blake2b
import random
import re
from urllib.parse import urlparse
import datetime
from flask import Flask, abort, jsonify, redirect, request

app = Flask(__name__)


def url_valid(url):
    
    return re.match(regex_url, url) is not None


def shorten(url):
    
    hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    while hash in short_dict:
        url += str(random.randint(0, 9))
        hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    b64 = b64encode(hash.digest(), altchars=b'-_')
    return b64.decode('utf-8')


def bad_request(message):
   
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/shorten', methods=['POST'])
def url_short():

    if not request.json:
        return bad_request('Provide URL in JSON Format')

    if 'url' not in request.json:
        return bad_request('Key URL not found. Put long url in URL key.')

    url = request.json['url']

    if url[:4] != 'http':
        url = 'http://' + url

    if not url_valid(url):
        return bad_request('long url provided is not valid. ')

    shortened_url = shorten(url)
    res = {"link": shortened_url,
           "long_url": url,
           "link_clicks": [
               {
                   "clicks": "0",
                   "date": "string"
               }
           ],
           "units": "-1",
           "unit": "day",
           "unit_reference": str(datetime.datetime.now().isoformat())
           }
    short_dict[shortened_url] = res

    return jsonify({'shortened_url': res}), 201


@app.route('/shorten', methods=['GET'])
def shorten_url_get():

    return bad_request('Must use POST.')


@app.route('/<short_url>', methods=['GET'])
def get_shortened(short_url):

    if short_url not in short_dict:
        return bad_request('Unknown alias.')

    res = short_dict[short_url]
    url = res["long_url"]
    print(url, " Shortened")
    try:
        obj = res['link_clicks'][0]['clicks']

        clicks = int(obj)

        clicks += 1

        res['link_clicks'][0]['clicks'] = str(clicks)
    except KeyError:
        print("keyerror")
        obj = None
    print(res['link_clicks'][0]['clicks'])
    return redirect(url, code=302)


@app.route('/bitlinks', methods=['POST'])
def create_bitlinks():
    if not request.json:
        return bad_request('Url must be provided in json format.')

    if 'url' not in request.json:
        return bad_request('Url parameter not found.')

    url = request.json['url']

    if url[:4] != 'http':
        url = 'http://' + url

    if not url_valid(url):
        return bad_request('Provided url is not valid.')

    shortened_url = shorten(url)
    print(shortened_url)

    res = {"link": shortened_url,
           "long_url": url,
           "link_clicks": [
               {
                   "clicks": "0",
                   "date": "string"
               }
           ],
           "units": "day",
           "unit": "-1",
           "unit_reference": str(datetime.datetime.now().isoformat())
           }

    if 'domain' in request.json:
        res["domain"] = request.json['domain']

    if 'title' in request.json:
        res["title"] = request.json['title']

    if 'tags' in request.json:
        res["tags"] = request.json['tags']

    if 'deeplinks' in request.json:
        res["deeplinks"] = request.json['deeplinks']

    
    try:
        obj = request.json['deeplinks'][0]['app_id']
        print(obj)
        res['deeplinks'][0]['app_id'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['app_uri_path']
        print(obj)
        res['deeplinks'][0]['app_uri_path'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['install_url']
        print(obj)
        res['deeplinks'][0]['install_url'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['install_type']
        print(obj)
        res['deeplinks'][0]['install_type'] = obj
    except KeyError:
        obj = None

    # print(res)
    short_dict[shortened_url] = res
    print(short_dict, " Shortened")
    return jsonify({'shortened_url': res}), 201


@app.route('/bitlinks/<short_url>', methods=['POST'])
def update_bitlinks(short_url):
    if short_url not in short_dict:
        return bad_request('Unknown URL.')

    res = {}
    if 'references' in request.json:
        res["references"] = request.json['references']

    if 'link' in request.json:
        res["link"] = request.json['link']

    if 'id' in request.json:
        res["id"] = request.json['id']

    if 'title' in request.json:
        res["title"] = request.json['title']

    if 'title' in request.json:
        res["title"] = request.json['title']

    if 'archived' in request.json:
        res["archived"] = request.json['archived']

    if 'created_at' in request.json:
        res["created_at"] = request.json['created_at']

    if 'created_by' in request.json:
        res["created_by"] = request.json['created_by']

    if 'client_id' in request.json:
        res["client_id"] = request.json['client_id']

    if 'custom_bitlinks' in request.json:
        res["custom_bitlinks"] = request.json['custom_bitlinks']

    if 'tags' in request.json:
        res["tags"] = request.json['tags']

    if 'launchpad_ids' in request.json:
        res["launchpad_ids"] = request.json['launchpad_ids']

    if 'deeplinks' in request.json:
        res["deeplinks"] = request.json['deeplinks']

    if 'created_at' in request.json:
        res["created_at"] = request.json['created_at']

    if 'created_at' in request.json:
        res["created_at"] = request.json['created_at']

    try:
        obj = request.json['deeplinks'][0]['guid']
        print(obj)
        res['deeplinks'][0]['guid'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['bitlink']
        print(obj)
        res['deeplinks'][0]['bitlink'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['app_uri_path']
        print(obj)
        res['deeplinks'][0]['app_uri_path'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['install_url']
        print(obj)
        res['deeplinks'][0]['install_url'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['app_guid']
        print(obj)
        res['deeplinks'][0]['app_guid'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['os']
        print(obj)
        res['deeplinks'][0]['app_guid'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['install_type']
        print(obj)
        res['deeplinks'][0]['app_guid'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['created']
        print(obj)
        res['deeplinks'][0]['app_guid'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['modified']
        print(obj)
        res['deeplinks'][0]['modified'] = obj
    except KeyError:
        obj = None

    try:
        obj = request.json['deeplinks'][0]['brand_guid']
        print(obj)
        res['deeplinks'][0]['brand_guid'] = obj
    except KeyError:
        obj = None

    short_dict[short_url] = res
    return jsonify({'response': res}), 201


@app.route('/bitlinks/<short_url>', methods=['GET'])
def get_bitlinks(short_url):
    if short_url not in short_dict:
        return bad_request('Unknown url.')

    res = short_dict[short_url]
    print(short_dict, " Shortened")
    return jsonify({short_url: res}), 201


@app.route('/bitlinks/<short_url>/clicks', methods=['GET'])
def get_clicks(short_url):
    if short_url not in short_dict:
        return bad_request('Unknown url.')
    res = short_dict[short_url]
    try:
        obj = res['link_clicks']
        return jsonify({short_url: res['link_clicks']}), 201
    except KeyError:
        return bad_request('No Clicks data')

regex_url = re.compile(
    r'^(?:http)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
DIGEST_SIZE = 9  
short_dict = {}
clicks = {}
if __name__ == '__main__':
    app.run(debug=True)
