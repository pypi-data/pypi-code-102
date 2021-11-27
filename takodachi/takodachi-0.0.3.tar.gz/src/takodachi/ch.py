"""Channels"""

ch_group_branches = [
    "JP","JP","JP","JP","JP","JP","JP","JP","ID","EN"
]

ch_group_names = [
    "Hololive-JP-0",
    "Hololive-JP-1",
    "Hololive-JP-2",
    "Hololive-Gamers",
    "Hololive-JP-3",
    "Hololive-JP-4",
    "Hololive-JP-5",
    "Holostars",
    "Hololive-ID",
    "Hololive-EN",
]


chid_to_name = \
[{'UCp6993wxpyDPHUpavwDFqgg': 'Tokino Sora',
  'UC0TXe_LYZ4scaW2XMyi5_kw': 'AZKi',
  'UCDqI2jOz0weumE8s7paEk6g': 'Roboco san',
  'UC-hM6YJuNYVAmUWxeIr9FeA': 'Sakura Miko',
  'UC5CwaMl1eIgY8h02uZw7u8A': 'Hoshimachi Suisei'},
 {'UCdn5BQ06XqgXoAxIhbqw5Rg': 'Shirakami Fubuki',
  'UCQ0UDLQCjY0rmuxCDE38FGg': 'Natsuiro Matsuri',
  'UCD8HOxPs4Xvsm8H0ZxXGiBw': 'Yozora Mel',
  'UC1CfXB_kRs3C-zaeTG3oGyg': 'Akai Haato',
  'UCFTLzh12_nrtzqBPsTCqenA': 'Aki Rosenthal'},
 {'UC1opHUrw8rvnsadT-iGp7Cg': 'Minato Aqua',
  'UC1suqwovbL1kzsoaZgFZLKg': 'Yuzuki Choco',
  'UC7fk0CB07ly8oSl0aqKkqFg': 'Nakiri Ayame',
  'UCXTpFs_3PqI41qX2d9tL2Rw': 'Murasaki Shion',
  'UCvzGlP9oQwU--Y0r9id_jnA': 'Oozora Subaru'},
 {'UCp-5t9SrOQwXMU7iIjQfARg': 'Ookami Mio',
  'UCvaTdHTWBGv3MKj3KVqJVCw': 'Nekomata Okayu',
  'UChAnqc_AY5_I3Px5dig3X1Q': 'Inugami Korone'},
 {'UCvInZx9h3jC2JzsIzoOebWg': 'Shiranui Flare',
  'UCdyqAaZDKHXg4Ahi7VENThQ': 'Shirogane Noel',
  'UCCzUftO8KOVkV4wQG1vkUvg': 'Houshou Marine',
  'UC1DCedRgGHBdm81E1llLhOQ': 'Usada Pekora',
  'UCl_gCybOJRIgOXw6Qb4qJzQ': 'Uruha Rushia'},
 {'UCZlDXzGoo7d44bwdNObFacg': 'Kiryu Coco (OG)',
  'UCqm3BQLlJfvkTsX_hvm0UmA': 'Tsunomaki Watame',
  'UC1uv2Oq6kNxgATlCiez59hw': 'Tokoyami Towa',
  'UCa9Y57gfeY0Zro_noHRVrnw': 'Himemori Luna'},
 {'UCFKOVgVbGmX65RxO3EtH3iw': 'Yukihana Lamy',
  'UCAWSyEs_Io8MtpY3m-zqILA': 'Momosuzu Nene',
  'UCUKD-uaobj9jiqB-VXt71mA': 'Shishiro Botan',
  'UCK9V2B22uJYu3N7eR_BT9QA': 'Omaru Polka'},
 {'UC6t3-_N8A6ME1JShZHHqOMw': 'Hanasaki Miyabi',
  'UCZgOv3YDEs-ZnZWDYVwJdmA': 'Kanade Izuru',
  'UCKeAhJvy8zgXWbh9duVjIaQ': 'Arurandeisu',
  'UC9mf_ZVpouoILRY9NUIaK-w': 'Rikka',
  'UCNVEsYbiZjH5QLmGeSgTSzg': 'Astel Leda',
  'UCGNI4MENvnsymYjKiZwv9eg': 'Kishido Temma',
  'UCANDOlYTJT7N5jlRC3zfzVA': 'Yukoku Roberu',
  'UChSvpZYRPh0FvG4SJGSga3g': 'Kageyama Shien',
  'UCwL7dgTxKo8Y4RFIKWaf8gA': 'Aragami Oga'},
 {'UCOyYb1c43VlX9rc_lT6NKQw': 'Ayunda Risu',
  'UCP0BspO_AMEe3aQqqpo89Dg': 'Moona Hoshinova',
  'UCAoy6rzhSf4ydcYjJw3WoVg': 'Airani Iofifteen',
  'UCYz_5n-uDuChHtLo7My1HnQ': 'Kureiji Ollie',
  'UC727SQYUvx5pDDGQpTICNWg': 'Anya Melfissa',
  'UChgTyjG-pdNvxxhdsXfHQ5Q': 'Pavolia Reine'},
 {'UCL_qhgtOy0dy1Agp8vkySQg': 'Mori Calliope',
  'UCHsx4Hqa-1ORjQTh9TYDhww': 'Takanashi Kiara',
  'UCMwGHR0BTZuLsmjY_NT5Pwg': "Ninomae Ina'nis",
  'UCoSrY_IQQVpmIRZ9Xf-y93g': 'Gawr Gura',
  'UCyl1z3jo3XHR1riLFKG5UAg': 'Watson Amelia',
  'UC8rcEBzJSleTkf_-agPM20g': 'IRyS',
  'UCsUj0dszADCGbF3gNrQEuSQ': 'Tsukumo Sana',
  'UCO_aKKYxn4tvrqPjcTzZ6EQ': 'Ceres Fauna',
  'UCmbs8T6MWqUHP1tIQvSgKrg': 'Ouro Kronii',
  'UC3n5uGu18FoCy23ggWWp8tA': 'Nanashi Mumei',
  'UCgmPnx-EEeOrZSg5Tiw7ZRQ': 'Hakos Baelz'}]

def get_chid_to_talent_info():
    chid_to_talent_info = {}
    for j, chids in enumerate(chid_to_name):
        ch_group_name = ch_group_names[j]
        ch_group_branch = ch_group_branches[j]
        for chid in chids.keys():
            talent_info = {
                'name':chids[chid], 
                'branch':ch_group_branch, 
                'group':ch_group_name
            }
            chid_to_talent_info[chid] = talent_info
    return chid_to_talent_info
