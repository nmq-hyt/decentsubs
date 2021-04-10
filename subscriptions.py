from googleapiclient.discovery import build
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
import io
import re
import argparse
import json
import os

# parse_cl = argparse.ArgumentParser()
# parse_cl.add_argument("-scid", help = "Set the channel ID to operate on. Must be set at least once.", default = None)
# parse_cl.add_argument("-ssf", help = "Set a target file to write the settings of the tool to.")
# parse_cl.add_argument("-recent", help = "Returns n recent videos from a channel. Requries a valid channel ID.")
# parse_cl.add_argument("-subs", help = "Harvests subscriptions of a user, and turns them into a dictionary value")
# parse_cl.add_argument("-vfw", help = "Returns recently video uploads from the user's set of channels, the watchlist")
# parse_cl.add_argument("-watchlist", help = "Updates a watchlist of channels to watch. Accepts a series of channel IDs as a series of strings", action= append)
# args = parse_cl.parse_args()



def get_oauth_permission():
    # start a flow, a class which begins the OAuth process, using the locally stored oauth secrets, with a scope to just read/write from a youtube channel
    # user verification is done by redirection to a URL, which provides an access code - the docs vaguely hint that 
    # this method may be taken down in future...
    subs_flow = InstalledAppFlow.from_client_secrets_file("oauth_secrets.json", scopes=["https://www.googleapis.com/auth/youtube.readonly"], redirect_uri= "urn:ietf:wg:oauth:2.0:oob")
    # get credentials as described above, this will print a link to console which the user retrieves a validation code 
    creds = subs_flow.run_console()
    # now i build the actual service itself, subs
    subs = build('youtube', 'v3', developerKey="AIzaSyBz-zhx-we-PyUjbpbaGcwWXDco2_Q0vjA", credentials = creds)
    return subs


def get_user_subs():
    # nptoken, or next page token
    # we use it to  cull the entirety of a user's subscriptions to harvest to json, by repeatedly calling the api, and changing the nptoken each time
    subs_resource_request = permission.subscriptions().list(part = "snippet", mine=True, order="unread", maxResults = 50)
    subs_resource = subs_resource_request.execute()
    new_list = [];
    list_iter = iter(subs_resource['items']);
    for element in list_iter:
        new_list.append(element);
    nptoken = subs_resource['nextPageToken']
    while(('nextPageToken' in subs_resource) == True):
        try:
            subs_resource_request = permission.subscriptions().list(pageToken = nptoken, part = "snippet",  mine=True,order="unread", maxResults = 50)
            subs_resource = subs_resource_request.execute()
            list_iter = iter(subs_resource['items']);
            for element in list_iter:
                new_list.append(element);
            nptoken = subs_resource['nextPageToken']
        except KeyError:
            pass
    # this is a list type object
    return new_list;
     # the very last iteration will have no further 'nextPageToken' key:value pair, which will raise a KeyError, so we just pass out of the function
     # suprisingly this last part took very little time to figure out, but the nptoken loop did
     # i should stop programming after midnight


def harvest_videos_per_channel(loci):

    loci = loci.values();
    for element in loci:
        bequest = permission.playlistItems().list(part="snippet,contentDetails",playlistId = element );
        bequest = bequest.execute();
        # print video title
        print(bequest['items'][0]['snippet']['title']);
        # https://www.youtube.com/watch?v=vidIdent
        # is the video url
        # TODO: construct channel name (loci.keys()) : video name string
        # TODO: construct youtube url string with above prefix

        #print video identity
        print(bequest['items'][0]['snippet']['resourceId']['videoId']);

        print(bequest['items'][0]['snippet'].keys());

def build_uploaded_playlist(list):

    # channels begin with UC in their identifier
    # playlists which are the channels uploaded playlist begin with UU (and are otherwise identical to their channel identifier)
    dict = {} ;
    for k,v in list.items():
        g = v.replace('C','U',1);
        dict[k] = g;
    return dict;


def build_title_id_dict (list):
    new_dict = {};
    for element in list:
        new_dict[element['snippet']['title']] = element['snippet']['resourceId']['channelId'];
    # construct list of snipped/channelId , snippet/title
    return new_dict;


permission = get_oauth_permission();
los= get_user_subs();
loci= build_title_id_dict(los);
loup = build_uploaded_playlist(loci);
louv = harvest_videos_per_channel(loup);
print(louv);
