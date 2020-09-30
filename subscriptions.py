from googleapiclient.discovery import build
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import path
import io
import re
import argparse
import datetime
import tempfile

current_timestamp = datetime.date.today()

class channel_record:
    # A class designed to represent a record of a single channel's video uploads.
    def update_timestamp(channel_record):
        channel_record.timestamp = current_timestamp

    def __init__(self, ID, title):
        self.channel_ID = ID
        self.channel_title = title
        self.num_new_vids = 0
        self.list_of_videos = []
        self.timestamp = 0


parse_cl = argparse.ArgumentParser()
parse_cl.add_argument("-scid", help = "Set the channel ID to operate on. Must be set at least once." default = None)
parse_cl.add_argument("-ssf", help = "Set a target file to write the settings of the tool to.")
parse_cl.add_argument("-recent", help = "Returns n recent videos from a channel. Requries a valid channel ID.")
parse_cl.add_argument("-subs", help = "Harvests subscriptions of a user, and turns them into a dictionary value")
parse_cl.add_argument("-watchlist", help = "Updates a watchlist of channels to watch. Accepts a series of channel IDs as a series of strings")
args = parse_cl.parse_args()



def obtain_oauth_permission():
    # start a flow, a class which begins the OAuth process, using the locally stored oauth secrets, with a scope to just read/write from a youtube channel
    # user verification is done by redirection to a URL, which provides an access code - the docs vaguely hint that 
    # this method may be taken down in future...
    subs_flow = InstalledAppFlow.from_client_secrets_file("oauth_secrets.json", scopes=["https://www.googleapis.com/auth/youtube"], redirect_uri= "urn:ietf:wg:oauth:2.0:oob")
    # get credentials as described above, this will print a link to console which the user retrieves a validation code 
    creds = subs_flow.run_console()
    # now i build the actual service itself, subs
    subs = build('youtube', 'v3', developerKey=, credentials = creds)
    return subs



def get_subs_as_JSON(channel_ID):
    try:
        with tempfile.mkdtemp(suffix = "temp_dir", dir = pathlib.Path("~/decentsubs").expanduser() ) as work_dir
        with tempfile.mkstemp(prefix = "temp_work", dir = work_dir text = True) as workspace
        # check to make sure the function is receiving a text file when called
        assert((work_dir.exists() == True) and (workspace.exists() == True)
    except AssertionError:
        print("Failed to make tempfile!")

    # nptoken, or next page token
    # we use it to  cull the entirety of a user's subscriptions to harvest to json, by repeatedly calling the api, and changing the nptoken each time
    subs_resource_request = subs.subscriptions().list(part = "contentDetails,snippet", channelId = user_channel_ID, order="unread", maxResults = 50)
    subs_resource = subs_resource_request.execute()
    texdump.write(str(subs_resource['items']))
    nptoken = subs_resource['nextPageToken']
    while(('nextPageToken' in subs_resource) == True):
        try:
            subs_resource_request = subs.subscriptions().list(pageToken = nptoken, part = "contentDetails,snippet",  order="unread", maxResults = 50)
            subs_resource = subs_resource_request.execute()
            texdump.write(str(subs_resource['items']))
            nptoken = subs_resource['nextPageToken']
        except KeyError:
            pass
     # the very last iteration will have no further 'nextPageToken' key:value pair, which will raise a KeyError, so we just pass out of the function
     # suprisingly this last part took very little time to figure out, but the nptoken loop did
     # i should stop programming after midnight



def subs_filter(some_input):
    # whilst I  thought I had to write an entire parser,
    #  this function is more like a filter with some ideas i gleaned from reading about formal language theory
    # i.e. production rules, lookahead, using a stack and regex etc.



    # note to self: abstract these routines
    # inefficent 
    endchar = re.compile(r"," "|" r"}" )
    def match_terminal (i, truth_value = None):
        return lambda truth_value : True if (endchar.match(i)) else False 

    startchar = re.compile(r"'")
    def match_start (i, truth_value = None):
        return lambda truth_value : True if (startchar.match(i) else False

    tchar = re.compile(r"t")
    def match_tchar (i, truth_value = None):
        return lambda truth_value : True if (tchar.match(i) else False

    ichar = re.compile(r"i")
    def match_ichar (i, truth_value = None):
        return lambda truth_value : True if (ichar.match(i) else False

    rchar = re.compile(r"r")
    def match_rchar (i, truth_value = None):
    return lambda truth_value : True if (rchar.match(i)) else False
    
    echar = re.compile(r"e")
    def match_echar(i, truth_value= None):
    return lambda truth_value : True if (resource_start.match[i]) else False
    
    def increment (x,n):
    return lambda x,n : x + n 

    def handle_string_part(i,some_buffer):
        while (match_terminal(i) == False):
            some_buffer.write(some_input[i])
            increment(i,1)
        return (some_buffer.getvalue()) 

    def handle_title(i):
        increment(i,8)
        title_buffer = io.StringIO("")
        channel_titles.append(parsing_table["handle_string_part"](i, title_buffer))
        title_buffer.close()
        

    def handle_resource(i):
        increment(i,54)
        resource_buffer = io.StringIO("")
        channel_IDs.append(parsing_table["handle_string_part"](i,resource_buffer))
        resource_buffer.close()
        
    parsing_table = {
            "match_start" : match_start,
            "match_tchar" : match_tchar,
            "match_ichar" : match_ichar,
            "match_rchar" : match_rchar,
            "match_echar" : match_echar,
            "handle_title" : handle_title,
            "handle_resource" : handle_resource,
            "handle_string_part" : handle_string_part,
            }

    channel_titles = []
    channel_IDs = []
    input_length = len(some_input)
    input_str = str(some_input)

        
    for i in range(input_length):
        if (parsing_table["match_start"](some_input[i])):
            increment(i,1)
            if (parsing_table["match_tchar"](some_input[i])):
                increment(i,1)
                if (parsing_table["match_ichar"](some_input[i])):
                    parsing_table["handle_title"](some_input[i])
            elif (parsing_table["match_rchar"](some_input[i])):
                increment(i,1)
                if (parsing_table["match_echar"](some_input[i])):
                    increment(i,1)
                    parsing_table["handle_resource"](some_input[i])
        else:
           continue
   
    #build a dictionary of values
    my_dict = {}
    for i in len(channel_IDs)
        my_dict.update{channel_titles[i]:channel_IDs[i]}
    return my_dict


    
