#! /usr/bin/env python2

import argparse
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

    ap = argparse.ArgumentParser()
    ap.add_argument("--add-to", type=str, metavar="LIST_SLUG",
        help="""Add the users listed on stdin to this list""")
    ap.add_argument("--remove-from", type=str, metavar="LIST_SLUG",
        help="""Remove the users listed on stdin from this list""")
    args = ap.parse_args()

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)


    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    user_list = [
        map(unicode.strip, line.split("||"))
        for line in sys.stdin]

    if args.remove_from:
        print "Removing users from {l}:".format(l=args.remove_from)
        for user_id, display_name, user_handle in user_list:
            print u"{d} (@{h} | {u})".format(
                d=display_name,
                h=user_handle,
                u=user_id)
        uid_list = [int(user_record[0]) for user_record in user_list]
        remove_users_from_list(api, uid_list, args.remove_from, "ptfen")

    if args.add_to:
        print "Adding users to {l}:".format(l=args.add_to)
        for user_id, display_name, user_handle in user_list:
            print u"{d} (@{h} | {u})".format(
                d=display_name,
                h=user_handle,
                u=user_id)
        uid_list = [int(user_record[0]) for user_record in user_list]
        add_users_to_list(api, uid_list, args.add_to, "ptfen")



def remove_users_from_list(api, uid_list, list_name, user_name):
    api.DestroyListsMember(slug=list_name,
                          owner_screen_name=user_name,
                          user_id=uid_list)
    update_list(api, list_name, user_name)

def add_users_to_list(api, uid_list, list_name, user_name):
    api.CreateListsMember(slug=list_name,
                          owner_screen_name=user_name,
                          user_id=uid_list)
    update_list(api, list_name, user_name)



def update_all():
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

