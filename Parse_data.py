import json
import sys
import collections

# if len(sys.argv) > 1:
#     line_generator = open(sys.argv[1])
# else:
#     line_generator = sys.stdin
# for line in line_generator:
#     ### analyze line ###


def parse_and_insert(tweet):
    #parsed tweet
    if tweet.get('is_quote_status') and 'quoted_status' in tweet:
        #Insert quoted status
        parse_and_insert(tweet.get('quoted_status'))
    parsed_tweet = {'created_at': tweet.get('created_at')}
    parsed_tweet.update({'tweet_id': tweet.get('id')})
    parsed_tweet.update({'tweet_text': tweet.get('text')})
    parsed_tweet.update({'tweet_source': tweet.get('source')})
    parsed_tweet.update({'in_reply_to_status_id': tweet.get('in_reply_to_status_id')})
    parsed_tweet.update({'in_reply_to_user_id': tweet.get('in_reply_to_user_id')})
    parsed_tweet.update({'in_reply_to_screen_name': tweet.get('in_reply_to_screen_name')})
    parsed_tweet.update({'tweet_coordinates': tweet.get('coordinates')})
    #check if is_quoted_status is true but no quoted_status object is present
    parsed_tweet.update({'quoted_status_id': tweet.get('quoted_status_id',0)})
    parsed_tweet.update({'retweet_count': tweet.get('retweet_count',0)})
    parsed_tweet.update({'favorite_count': tweet.get('favorite_count',0)})
    parsed_tweet.update({'timestamp_ms': tweet.get('timestamp_ms',"0")})
    #Users Object
    user_info = tweet.get('user')
    parsed_tweet.update({'user_id': user_info.get('id')})
    parsed_tweet.update({'user_name': user_info.get('name')})
    parsed_tweet.update({'user_screen_name': user_info.get('screen_name')})
    parsed_tweet.update({'user_verified': user_info.get('verified',"false")})
    parsed_tweet.update({'user_description': user_info.get('description')})
    parsed_tweet.update({'user_followers_count': user_info.get('followers_count',0)})
    parsed_tweet.update({'user_friends_count': user_info.get('friends_count',0)})
    parsed_tweet.update({'user_location': user_info.get('location',"")})
    #Places Object
    place_info = tweet.get('place')
    if place_info != None:
        parsed_tweet.update({'place_country': place_info.get('country',"")})
        parsed_tweet.update({'place_full_name': place_info.get('full_name',"")})
        parsed_tweet.update({'place_type': place_info.get('place_type',"")})
        parsed_tweet.update({'place_coordinates': place_info.get('bounding_box',[]).get('coordinates',[])})
    else:
        parsed_tweet.update({'place_country': ""})
        parsed_tweet.update({'place_full_name': ""})
        parsed_tweet.update({'place_type': ""})
        parsed_tweet.update({'place_coordinates': []})
    #Entities Object
    entities = tweet.get('entities')
    hash_tags = []
    for item in entities.get('hashtags'):
        hash_tags.append(item.get('text'))
    parsed_tweet.update({'hash_tags': hash_tags})
    user_mentions = []
    for item in entities.get('user_mentions'):
        user_mentions.append(item.get('screen_name'))
    parsed_tweet.update({'user_mentions': user_mentions})
    #sorting accourding to key fields in dictonary
    od_parsed_tweet = collections.OrderedDict(sorted(parsed_tweet.items()))

    print(json.dumps(od_parsed_tweet, indent=4)) # pretty-print
    #f.write(json.dumps(od_parsed_tweet))
    return;


with open('test_sample.json', 'r') as f:
    # read tweets line by line
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        parse_and_insert(tweet)
    # try:
    #     actor_id_string = line_object["actor"]["id"]
    #     actor_id = int( actor_id_string.split(":")[2] )
    #     language_code = line_object["twitter_lang"]
    # except KeyError, e:
    #     actor_id = -1
    #     language_code = "Null"

#coordinates - Coordinates object
#place - Places object
#quoted_status - Tweet object
#entities - Entities object
