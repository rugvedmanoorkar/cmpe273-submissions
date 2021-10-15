from flask import Flask, abort, jsonify, redirect, request


app = Flask(__name__)


def bad_request(message):
   
    response = jsonify({'message': message})
    response.status_code = 400
    return response

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/users', methods=['POST'])
def set_users():
    if not request.json:
        return bad_request('Provide URL in JSON Format')

    if 'name' and 'email' not in request.json:
        return bad_request('Name and Email not found . Provide in json')
    
    name = request.json['name']
    email = request.json['email']

    if len(list(users)) == 0:
        temp_id = 100
    else:
        temp_id = list(users)[-1] + 1
    
    print(temp_id, " Temp Id")
    id = temp_id
    res ={
        "id": temp_id,
        "name" : name,
        "email" : email,
        "tweets" : [], 
        "followers" : []
    }

    # tr
    # pen_id = list(dict)[-1]
    users[id] = res
    print(users)
    return jsonify({'response': res}), 201

@app.route('/users/<id>/followers/<fid>', methods=['PATCH'])
def patch_followers(id, fid):
    print(id)

    follow = users[int(id)] 
    follow_list = follow["followers"]
    follow_list.append(fid)
    print(follow["followers"])
    users[int(id)]["followers"]= follow_list
    return jsonify({'response': users}), 201

@app.route('/users/<user_id>/tweets', methods=['POST'])
def set_tweets(user_id):
    tweet_list = users[int(user_id)]["tweets"]
    print(tweet_list)
    tweet = request.json['tweet']
    print(tweet)
    tres = {
        "tweet_id" : 1,
        "tweet" : tweet
    }
    tweet_list.append(tres)
    users[int(user_id)]["tweets"]= tweet_list
    return jsonify({'response': users}), 201

@app.route('/<user_id>', methods=['GET'])
def get_user_details(user_id):
    res = users[int(user_id)]
    return jsonify({'response': res}), 201

@app.route('/<user_id>/timeline', methods=['GET'])
def get_timeline(user_id):
    res ={}
    for user in users:
        print (users[user]["id"])
        print(users[int(user_id)]["id"])
        if users[user]["id"] == users[int(user_id)]["id"]:
            print(users[user]["id"])
            res = {
                "user_id" : users[user]["id"],
                "tweet" : users[user]["tweets"]
            }
    return jsonify({'response': res}), 201

users = {}
timeline = {}
if __name__ == '__main__':
    app.run(debug=True)