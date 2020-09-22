from googleapiclient.discovery import build
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
import io
import queue
import re
# start a flow, a class which begins the OAuth process, using the locally stored oauth secrets, with a scope to just read/write from my youtube channel
# user verification is done by redirection to a URL, which provides an access code - the docs vaguely hint that 
# this method may be taken down in future...
subs_flow = InstalledAppFlow.from_client_secrets_file("oauth_secrets.json", scopes=["https://www.googleapis.com/auth/youtube"], redirect_uri= "urn:ietf:wg:oauth:2.0:oob")
# get credentials as described above, this will print a link to console which the user retrieves a validation code 
creds = subs_flow.run_console()
## now i build the actual service itself, subs
# note developer key is left blank here as it depend on each user
subs = build('youtube', 'v3', developerKey=, credentials = creds)
##specify that i want a list of my subscriptions, which is accessible if 
##i authed everything correctly, and do it in chronological order
#
##open our target file
#dump = open('/home/nmq-hyt/projects/python/subs/dummy', 'w+')


def get_subs_as_JSON(target):
    try:
        assert(isinstance(target,io.TextIOBase) == True)
    except AssertionError:
        print("Target file is not a file!")
    except FileNotFoundError:
        print("File does not exist!")

    # nptoken, or next page token
    # we use it to  cull the entirety of my subscriptions to harvest to json, by repeatedly calling the api, and changing the nptoken each time
    #subs_resource is a dict
    subs_resource_request = subs.subscriptions().list(part = "contentDetails,snippet", mine=True, order="unread", maxResults = 50)
    subs_resource = subs_resource_request.execute()
    texdump.write(str(subs_resource['items']))
    nptoken = subs_resource['nextPageToken']
    # we make repeated calls to the api here, cycling through each new page token we're given
    # to retrieve all 300 ish subscription nodes
    while(('nextPageToken' in subs_resource) == True):
        try:
            subs_resource_request = subs.subscriptions().list(pageToken = nptoken, part = "contentDetails,snippet", mine=True, order="unread", maxResults = 50)
            subs_resource = subs_resource_request.execute()
            texdump.write(str(subs_resource['items']))
            nptoken = subs_resource['nextPageToken']
        except KeyError:
            pass
     # the very last iteration will have no further 'nextPageToken' key:value pair, which will raise a KeyError, so we just pass out of the function


#Need to consider e and i matching functions
# makes sense to me: if we  get a true on e or i, we're in the right area, so we should do the seek in the file,
# and call handle_string
#

subs = open ("/home/nmq-hyt/projects/python/subs/dummy", 'r')
text = subs.read(None)

def subs_filter(some_input):

    back_stack = []
    channel_titles = []
    channel_IDs = []
    input_length = len(some_inpu)

    for i in range(input_length):
        back_stack.append(some_input[i])
   back_stack =  back_stack.reverse()
    
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
    return lambda truth_value : True if (resource_start.match[i:i+2]) else False
    
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
        
    for i in range(input_length):
        if (parsing_table["match_start"](some_input[i]):
            increment(i,1)
            if (parsing_table["match_tchar"](some_input[i]):
                increment(i,1)
                if (parsing_table["match_ichar"](some_input[i]):
                    parsing_table["handle_title"](some_input[i])
            elif (parsing_table["match_rchar"](some_input[i]):
                increment(i,1)
                if (parsing_table["match_echar"](some_input[i]):
                    increment(i,1)
                    parsing_table["handle_resource"](some_input[i])
        else:
           continue
   
    #build a dictionary of values
    my_dict = {}
    for i in len(channel_IDs)
        my_dict.update{channel_titles[i]:channel_IDs[i]}



    
get_subs_as_JSON(dump)
filter_subs(text)
texdump.close()
