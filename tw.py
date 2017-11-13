#! /usr/bin/env python2

import codecs
import pickle
import os
import sys
import twitter

def main():
    try:
        consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
        consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
        access_token_key = os.environ["TWITTER_ACCESS_TOKEN_KEY"]
        access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    except KeyError as e:
        print "Looks like your Twitter credentials aren't in your environment."
        print e
        return 1

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    update_following(api)
    update_followers(api)
    update_list(api, "parodies", "ptfen")
    update_list(api, "ratio-killers", "ptfen")
    update_list(api, "goodfollas", "ptfen")
    update_list(api, "watch-don-t-follow1", "ptfen")
    update_list(api, "irl", "ptfen")
    update_list(api, "tier-1-twitter", "ptfen")

    return 0

def update_list(api, list_name, user_name):
    listmembers = api.GetListMembers(slug=list_name,
                                     owner_screen_name=user_name,
                                     skip_status=True,
                                     include_entities=False)
    print "List {} - {}".format(list_name, len(listmembers))
    with codecs.open("{}.txt".format(list_name), "w", "utf-8") as f:
        for user in listmembers:
            f.write(format_user(user))

def update_following(api):
    following = api.GetFriends(skip_status=True, include_user_entities=False)
    print "Following", len(following)
    with codecs.open("following.txt", "w", "utf-8") as f:
        for user in following:
            f.write(format_user(user))

def update_followers(api):
    followers = api.GetFollowers(skip_status=True, include_user_entities=False)
    print "Followers", len(followers)
    with codecs.open("followers.txt", "w", "utf-8") as f:
        for user in followers:
            f.write(format_user(user))

def format_user(user_obj):
    return u"{uid} || {name} || {screen_name}\n".format(
                uid=user_obj.id,
                name=user_obj.name,
                screen_name=user_obj.screen_name,
            )


if __name__ == "__main__":
    sys.exit(main())

