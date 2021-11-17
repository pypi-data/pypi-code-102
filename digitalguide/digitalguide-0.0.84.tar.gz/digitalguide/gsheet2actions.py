import yaml
from openpyxl import load_workbook
import collections
import pickle
import os
from typing import DefaultDict, List
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime

from collections import defaultdict

import re


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def sheed_id2excel(service, sheet_id, excel_file):
    byteData = service.files().export_media(
        fileId=sheet_id,
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ).execute()

    with open(excel_file, "wb") as f:
        f.write(byteData)


def readActions(format_inhalt_list):
    actions = []
    for format, inhalt in format_inhalt_list:
        actions.append(readAction(format, inhalt))

    return actions


def readAction(format, inhalt):
    action = {}

    if format == "Textnachricht":
        action["type"] = "message"
        action["text"] = inhalt

    elif format == "Audionachricht":
        action["type"] = "audio"
        regex = r"Datei: (?P<file>.*)\nAnzeigename: (?P<name>.*)\nPerformer: (?P<performer>.*)"

        match = re.search(regex, inhalt)
        if match:
            action["file"] = "assets/" + match.group('file')
            action["title"] = match.group('name')
            action["performer"] = match.group('performer')
        else:
            action["file"] = "assets/platzhalter.mp3"
            action["title"] = inhalt
            action["performer"] = "🤖"

    elif format == "Foto":
        action["type"] = "photo"
        regex = r"Datei: (?P<file>.*)\nAnzeigename: (?P<name>.*)"

        match = re.search(regex, inhalt)
        if match:
            action["file"] = "assets/" + match.group('file')
            action["caption"] = match.group('name')
        else:
            action["file"] = "assets/platzhalter.png"
            action["caption"] = inhalt

    elif format == "GPS":
        action["type"] = "venue"

        action["longitude"] = re.search(
            r"L: (?P<long>.*)", inhalt).group('long')
        action["latitude"] = re.search(r"B: (?P<lat>.*)", inhalt).group('lat')
        action["title"] = re.search(
            r"Anzeigename: (?P<name>.*)", inhalt).group('name')
        action["address"] = re.search(
            r"Adresse: (?P<address>.*)", inhalt).group('address')

    elif format == "Video":
        action["type"] = "video"
        regex = r"Datei: (?P<file>.*)\nAnzeigename: (?P<caption>.*)"

        match = re.search(regex, inhalt)
        if match:
            action["file"] = "assets/" + match.group('file')
            action["caption"] = match.group('caption')

    elif format == "Sticker":
        regex = r"ID: (?P<id>.*)$"

        match = re.search(regex, inhalt)
        action["type"] = "sticker"
        if match:
            action["id"] = match.group('id')
        else:
            print("Die angegebenen Informationen im Feld ({}) stimmen nicht mit dem angegebenen Format ({}) überein.".format(
                inhalt, format))
    elif format == "Kontextspeicherung":
        action["type"] = "function"
        action["func"] = "save_to_context"
        action["key"] = "name"
    elif format == "Return":
        action["type"] = "return"
        action["state"] = inhalt
    elif format == "Formel":
        action["type"] = "function"
        action["func"] = re.search(
            r"function: (?P<function>.*)", inhalt).group('function')
        for line in inhalt.split("\n")[1:]:
            if len(line.split(": "))==2:
                argument, value = line.split(": ")
                action[argument] = value

    else:
        print("Das angegebene Format ({}) ist nicht bekannt".format(format))

    return action

def readTriggers(format_inhalt_list, action):
    triggers = []
    for format, inhalt in format_inhalt_list:
        if format == "Liste":
            trigger_dict = {}
            trigger_dict["handler"] = "CommandHandler"
            trigger_dict["command"] = inhalt
            trigger_dict["action"] = action
            triggers.append(trigger_dict)
            trigger_dict = {}
            trigger_dict["handler"] = "MessageHandler"
            trigger_dict["filter"] = "regex"
            trigger_dict["action"] = action
            if inhalt == "Weiter":
                trigger_dict["regex"] = "WEITER_PATTERN"
            elif inhalt == "Ja":
                trigger_dict["regex"] = "JA_PATTERN"
            elif inhalt == "Wohin":
                trigger_dict["regex"] = "WOHIN_PATTERN"
            elif inhalt == "Nein":
                trigger_dict["regex"] = "NEIN_PATTERN"
            else:
                trigger_dict["regex"] = inhalt
                print("List {} ist nicht bekannt!".format(inhalt))
            triggers.append(trigger_dict)
        if format == "Freitext":
            trigger_dict = {}
            trigger_dict["handler"] = "MessageHandler"
            trigger_dict["filter"] = "text"
            trigger_dict["action"] = action
            triggers.append(trigger_dict)
        if format == "Foto":
            trigger_dict = {}
            trigger_dict["handler"] = "MessageHandler"
            trigger_dict["filter"] = "photo"
            trigger_dict["action"] = action
            triggers.append(trigger_dict)
        if format == "Regex":
            trigger_dict = {}
            trigger_dict["handler"] = "MessageHandler"
            trigger_dict["filter"] = "regex"
            trigger_dict["regex"] = inhalt
            trigger_dict["action"] = action
            triggers.append(trigger_dict)
    return triggers

def excel2dict(sheet, interaktion_spalte, poi_spalte, aktion_spalte, format_spalte, inhalt_spalte, max_row):

    excel_dict = defaultdict(
        lambda: defaultdict(
                list
            )
        )
    previous_interaktion=""
    previous_pio=""
    previous_aktion=""

    for row in sheet.iter_rows(min_row=2, max_row=max_row):
        if row[interaktion_spalte].value == None:
            interaktion = previous_interaktion
        else:
            interaktion = row[interaktion_spalte].value
            previous_interaktion = interaktion

        if row[poi_spalte].value == None:
            poi = previous_pio
        else:
            poi = row[poi_spalte].value
            previous_pio = poi

        if row[aktion_spalte].value == None:
            aktion = previous_aktion
        else:
            aktion = row[aktion_spalte].value
            previous_aktion = aktion

        if row[format_spalte].value == None:
            ValueError("Empty Field in {}".format(row[format_spalte]))
        else:
            format = row[format_spalte].value

        if row[inhalt_spalte].value == None:
            ValueError("Empty Field in {}".format(row[inhalt_spalte]))
        else:
            inhalt = row[inhalt_spalte].value

        excel_dict[(poi, interaktion)][aktion].append((format, inhalt))
    
    return excel_dict


def create_states_anctions(excel_dict):
    actions = defaultdict(list)
    states = defaultdict(list)
    for poi_interaction, interaktion_dict in excel_dict.items():
        poi, interaction = poi_interaction
    
        if "Next" in interaktion_dict.keys():
            weiter_dict = dict((x, y) for x, y in interaktion_dict["Next"])
            print(weiter_dict)
            weiter_action = "{}_{}".format(weiter_dict["POI"], weiter_dict["Aktion"])

        if interaction == "Aktion":
            print(interaktion_dict)
            actions["{}".format(poi)] = readActions(
                interaktion_dict["Aktion"])

        elif interaction == "Datenabfrage":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])
            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])

            states["{}_FRAGE".format(poi.upper())] = readTriggers(interaktion_dict["Typ"], weiter_action) \
                                                + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]

        elif interaction == "Weg":
            actions["{}_weg".format(poi)] = readActions(interaktion_dict["Weg"] \
                                            + [("Return", "{}_WEG".format(poi.upper()))])

            actions["{}_navigation".format(poi)] = readActions(
                interaktion_dict["Navigation"])
            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])

            states["{}_WEG".format(poi.upper())] = readTriggers(interaktion_dict["trigger_navigation"], "{}_navigation".format(poi)) \
                                                + readTriggers(interaktion_dict["trigger_weiter"], weiter_action) \
                                                + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]

        elif interaction == "Quizfrage":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])
            
            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])

            for aktion, aktion_list in interaktion_dict.items():
                if aktion.startswith("antwort_"):
                    actions["{}_{}".format(poi, aktion)] = readActions(aktion_list) \
                                                        + readActions(interaktion_dict["Aufloesung"]) \
                                                        + readActions([("Return", "{}_AUFLOESUNG".format(poi.upper()))])

                elif aktion.startswith("trigger_"):
                    states["{}_FRAGE".format(poi.upper())] += readTriggers(aktion_list, "{}_{}".format(poi, aktion.replace("trigger_", "antwort_")))

            states["{}_AUFLOESUNG".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction == "Schätzfrage":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])
            
            actions["{}_aufloesung".format(poi)] = readActions(interaktion_dict["Aufloesung"]) \
                                                + readActions([("Return", "{}_AUFLOESUNG".format(poi.upper()))])

            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])

            print(interaktion_dict["Typ"])
            if interaktion_dict["Typ"][0][0] == "Jahreszahl":
                states["{}_FRAGE".format(poi.upper())] = (readTriggers([("Regex", "^(\d{1,4})$")], "{}_aufloesung".format(poi))) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]

            elif interaktion_dict["Typ"][0][0] == "Prozentzahl":
                states["{}_FRAGE".format(poi.upper())] = (readTriggers([("Regex", "(\d{1,2}),? ?(\d{,2})")], "{}_aufloesung".format(poi))) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]

            elif interaktion_dict["Typ"][0][0] == "Römische Jahreszahl":
                states["{}_FRAGE".format(poi.upper())] = (readTriggers([("Regex", "^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")], "{}_aufloesung".format(poi))) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]
            
            else:
                print("Der Schätzfragentyp {} ist nicht bekannt!".format(interaktion_dict["Typ"][0][0]))

            states["{}_AUFLOESUNG".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction == "Listenfrage":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])

            
            answer_id_name_list = []
            for aktion, aktion_list in interaktion_dict.items():
                if aktion.startswith("antwort_"):
                    actions["{}_{}".format(poi, aktion)] = readActions([("Formel", "function: check_in_context\nkey: {}\nvalue: {}\ndoppelte_antwort: {}\n".format(poi, aktion.replace("antwort_", ""), interaktion_dict["doppelte Antwort"][0][1]))])\
                                                        + readActions([("Formel", "function: append_to_context\nkey: {}\nvalue: {}".format(poi, aktion.replace("antwort_", "")))])\
                                                        + readActions(aktion_list) \
                                                        + readActions(interaktion_dict["richtig Antwort"])

                elif aktion.startswith("trigger_"):
                    states["{}_FRAGE".format(poi.upper())] += readTriggers(aktion_list, "{}_{}".format(poi, aktion.replace("trigger_", "antwort_")))

                elif aktion.startswith("name_"):
                    answer_id_name_list.append([aktion.replace("name_", ""), aktion_list[0][1]])


            actions["{}_aufloesung".format(poi)] = [{"type": "function", "func": "eval_list", "answer_id_name_list": answer_id_name_list, "poi": poi, "response_text": interaktion_dict["response_text"][0][1]}]\
                                                + readActions(interaktion_dict["Aufloesung"]) \
                                                + readActions([("Return", "{}_AUFLOESUNG".format(poi.upper()))])

            actions["{}_falsche_antwort".format(poi)] = readActions(interaktion_dict["falsch Antwort"])

            states["{}_FRAGE".format(poi.upper())] += readTriggers([("Liste", "Weiter")], "{}_aufloesung".format(poi))\
                                                    + [{"handler": "TypeHandler", "type": "Update", "action": "{}_falsche_antwort".format(poi)}]

            states["{}_AUFLOESUNG".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]
        elif interaction == "Beteiligungsfrage":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])
            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])

            actions["{}_aufloesung".format(poi)] = readActions(interaktion_dict["Aufloesung"]+ [("Return", "{}_AUFLOESUNG".format(poi.upper()))])

            states["{}_FRAGE".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                    + readTriggers([("Liste", "Nein")], weiter_action) \
                                                    + readTriggers(interaktion_dict["Typ"], "{}_aufloesung".format(poi)) \
                                                    + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]

            weiter_dict = dict((x, y) for x, y in interaktion_dict["Next"])
            weiter_action = "{}_{}".format(weiter_dict["POI"], weiter_dict["Aktion"])

            states["{}_AUFLOESUNG".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction == "GIF Generator":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])

            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])

            actions["{}_aufloesung".format(poi)] = readActions(interaktion_dict["Aufloesung"])

            states["{}_FRAGE".format(poi.upper())] = readTriggers([("Foto","")], "{}_aufloesung".format(poi)) \
                                                    + readTriggers([("Liste", "Weiter")], weiter_action) \
                                                    + readTriggers([("Liste", "Nein")], weiter_action) \
                                                    + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]

        elif interaction == "Infostrecke":
            actions["{}_info".format(poi)] = readActions(
                interaktion_dict["Info"]+ [("Return", "{}_INFO".format(poi.upper()))])
            
            states["{}_INFO".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        elif interaction == "Assoziationskette":
            actions["{}_frage".format(poi)] = readActions(
                interaktion_dict["Frage"]+ [("Return", "{}_FRAGE".format(poi.upper()))])
            actions["{}_loop".format(poi)] = readActions(
                interaktion_dict["Loop"])
            states["{}_FRAGE".format(poi.upper())] = readTriggers([("Liste", "Weiter")], "{}_aufloesung".format(poi)) \
                                                    + readTriggers([("Freitext", "")], "{}_loop".format(poi)) \
                                                    + [{"handler": "TypeHandler", "type": "Update", "action": "{}_tipp".format(poi)}]
            actions["{}_tipp".format(poi)] = readActions(interaktion_dict["Tipp"])
            actions["{}_aufloesung".format(poi)] = readActions(interaktion_dict["Aufloesung"]+  [("Return", "{}_AUFLOESUNG".format(poi.upper()))])

            states["{}_AUFLOESUNG".format(poi.upper())] = readTriggers([("Liste", "Weiter")], weiter_action) \
                                                        + [{"handler": "TypeHandler", "type": "Update", "action": "weiter_tipp"}]

        else:
            print("Der Interaktionstyp {} ist nicht bekannt!".format(interaction))

    states["NONE"]=[]
    return states, actions