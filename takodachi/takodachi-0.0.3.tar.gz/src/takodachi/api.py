"""For using YouTube Data API"""

from sys import stderr

from apiclient.discovery import build

APIKEY = "AIzaSyA5ul3TH3p3vaS8zomiA5TCq39SKqDP8B4"

PLAYLIST_ID = {
        'INA' : 'UUMwGHR0BTZuLsmjY_NT5Pwg',
        'CALLIOPE' : 'UUL_qhgtOy0dy1Agp8vkySQg',
        'GURA' : 'UUoSrY_IQQVpmIRZ9Xf-y93g',
        'KIARA' : 'UUHsx4Hqa-1ORjQTh9TYDhww',
        'AMELIA' : 'UUyl1z3jo3XHR1riLFKG5UAg',
        'LUNA' : 'UUa9Y57gfeY0Zro_noHRVrnw',
        'AYAME' : 'UU7fk0CB07ly8oSl0aqKkqFg',
        'SUBARU' : 'UUvzGlP9oQwU--Y0r9id_jnA',
        'CHOCO' : 'UU1suqwovbL1kzsoaZgFZLKg',
        'SHION' : 'UUXTpFs_3PqI41qX2d9tL2Rw',
        'AQUA' : 'UU1opHUrw8rvnsadT-iGp7Cg',
        'SANA' : 'UUsUj0dszADCGbF3gNrQEuSQ',
        'FAUNA' : 'UUO_aKKYxn4tvrqPjcTzZ6EQ',
        'KRONII' : 'UUmbs8T6MWqUHP1tIQvSgKrg',
        'MUMEI' : 'UU3n5uGu18FoCy23ggWWp8tA',
        'BAELZ' : 'UUgmPnx-EEeOrZSg5Tiw7ZRQ',
        'IRYS' : 'UU8rcEBzJSleTkf_-agPM20g',
        'BOTAN' : 'UUUKD-uaobj9jiqB-VXt71mA',
        'POLKA' : 'UUK9V2B22uJYu3N7eR_BT9QA',
        'NENE' : 'UUAWSyEs_Io8MtpY3m-zqILA',
        'LAMY' : 'UUFKOVgVbGmX65RxO3EtH3iw',
        }




def chid2playlistid(chid):
    assert len(chid) == 24
    chid_list = list(chid)
    assert chid_list[1] == 'C'
    chid_list[1] = 'U'
    playlistid = ''.join(chid_list)
    return playlistid




def get_video_list_from_playlist(playlist_id, max_results=5):
    
    video_id_list = []
    video_title_list = []
    
    youtube = build("youtube","v3",developerKey=APIKEY)

    playlistitems_list_request = youtube.playlistItems().list(
        playlistId=playlist_id, part='id,snippet', maxResults=max_results)

    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()

        for playlist_item in playlistitems_list_response["items"]:
            title = playlist_item["snippet"]["title"]
            video_title_list.append(title)
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
            video_id_list.append(video_id)

        playlistitems_list_request = youtube.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)

    youtube.close()
    
    return video_id_list, video_title_list





def get_chid_from_vid(vid):
    
    chid = None
    
    with build("youtube","v3",developerKey=APIKEY) as youtube:
        v_info_req = youtube.videos().list(part='snippet',id=vid)

        while v_info_req:
            v_info_res = v_info_req.execute()
            v_info_req = youtube.videos().list_next(v_info_req,v_info_res)

            for v_info in v_info_res['items']:
                chid_get = v_info.get('snippet')['channelId']
                if chid is None: chid = chid_get
                else: raise Exception("Multiple ChannelId Detected")
    
    return chid



def get_ch_info(chid,part='snippet,statistics'):

    ch_info_got = None

    with build("youtube","v3",developerKey=APIKEY) as youtube:
        ch_info_req = youtube.channels().list(part=part,id=chid)
        while ch_info_req:
            ch_info_res = ch_info_req.execute()
            if len(ch_info_res['items']) > 1:
                print("More than one `ch_info` found:\n", 
                        ch_info_res['items'], file=stderr)
            for ch_info in ch_info_res['items']:
                ch_info_got = ch_info
            ch_info_req = youtube.channels().list_next(ch_info_req,ch_info_res)

    return ch_info_got



def get_chinfo(chid, part):

    ch_info_res_items = None

    with build("youtube","v3",developerKey=APIKEY) as youtube:
        ch_info_req = youtube.channels().list(part=part,id=chid)
        while ch_info_req:
            ch_info_res = ch_info_req.execute()
            ch_info_res_items = ch_info_res['items']
            ch_info_req = youtube.channels().list_next(ch_info_req,ch_info_res)

    return ch_info_res_items




def get_vinfo(vid, part='snippet'):

    v_info_res_items = None
    
    with build("youtube","v3",developerKey=APIKEY) as youtube:
        v_info_req = youtube.videos().list(part=part,id=vid)

        while v_info_req:
            v_info_res = v_info_req.execute()
            v_info_req = youtube.videos().list_next(v_info_req,v_info_res)     
            v_info_res_items = v_info_res['items']

    return v_info_res_items




