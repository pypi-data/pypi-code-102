# vim: expandtab sw=4 ts=4 sts=4:
#
# Copyright © 2003 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of python-gammu <https://wammu.eu/python-gammu/>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
"""
Some static data.

@var Connections: List of connection types.
@var MemoryValueTypes: Types of memory entry values.
@var CalendarTypes: Types of calendar entries.
@var CalendarValueTypes: Types of calendar entry values.
@var TodoPriorities: Todo priorities.
@var TodoValueTypes: Types of todo entry values.
@var InternationalPrefixes: List of known internaltional prefixes.
"""

from gammu import ErrorNumbers, Errors

Connections = [
    "at",
    "at19200",
    "at115200",
    "fbus",
    "dlr3",
    "dku2",
    "dku5",
    "fbuspl2303",
    "mbus",
    "irdaphonet",
    "irdaat",
    "irdaobex",
    "irdagnapbus",
    "bluerffbus",
    "bluefbus",
    "bluerfphonet",
    "bluephonet",
    "blueat",
    "bluerfat",
    "blueobex",
    "bluerfobex",
    "fbusblue",
    "fbusirda",
    "phonetblue",
    "bluerfgnapbus",
]

MemoryValueTypes = [
    "Number_General",
    "Number_Mobile",
    "Number_Work",
    "Number_Fax",
    "Number_Home",
    "Number_Pager",
    "Number_Other",
    "Text_Note",
    "Text_Postal",
    "Text_WorkPostal",
    "Text_Email",
    "Text_Email2",
    "Text_URL",
    "Date",
    "Caller_Group",
    "Text_Name",
    "Text_LastName",
    "Text_FirstName",
    "Text_Company",
    "Text_JobTitle",
    "Category",
    "Private",
    "Text_StreetAddress",
    "Text_City",
    "Text_State",
    "Text_Zip",
    "Text_Country",
    "Text_WorkStreetAddress",
    "Text_WorkCity",
    "Text_WorkState",
    "Text_WorkZip",
    "Text_WorkCountry",
    "Text_Custom1",
    "Text_Custom2",
    "Text_Custom3",
    "Text_Custom4",
    "RingtoneID",
    "PictureID",
    "Text_UserID",
    "CallLength",
    "Text_LUID",
    "LastModified",
    "Text_NickName",
    "Text_FormalName",
    "PushToTalkID",
    "Photo",
    "Number_Mobile_Home",
    "Number_Mobile_Work",
    "Text_SecondName",
    "Text_VOIP",
    "Text_SIP",
    "Text_DTMF",
    "Number_Video",
    "Text_SWIS",
    "Text_WVID",
    "Text_NamePrefix",
    "Text_NameSuffix",
]

CalendarTypes = [
    "REMINDER",
    "CALL",
    "MEETING",
    "BIRTHDAY",
    "MEMO",
    "TRAVEL",
    "VACATION",
    "T_ATHL",
    "T_BALL",
    "T_CYCL",
    "T_BUDO",
    "T_DANC",
    "T_EXTR",
    "T_FOOT",
    "T_GOLF",
    "T_GYM",
    "T_HORS",
    "T_HOCK",
    "T_RACE",
    "T_RUGB",
    "T_SAIL",
    "T_STRE",
    "T_SWIM",
    "T_TENN",
    "T_TRAV",
    "T_WINT",
    "ALARM",
    "DAILY_ALARM",
    "SHOPPING",
]

CalendarValueTypes = [
    "START_DATETIME",
    "END_DATETIME",
    "TONE_ALARM_DATETIME",
    "SILENT_ALARM_DATETIME",
    "RECURRANCE",
    "TEXT",
    "DESCRIPTION",
    "LOCATION",
    "PHONE",
    "PRIVATE",
    "CONTACTID",
    "REPEAT_DAYOFWEEK",
    "REPEAT_DAY",
    "REPEAT_WEEKOFMONTH",
    "REPEAT_MONTH",
    "REPEAT_FREQUENCY",
    "REPEAT_STARTDATE",
    "REPEAT_STOPDATE",
    "LUID",
    "LAST_MODIFIED",
]

TodoPriorities = [
    "High",
    "Medium",
    "Low",
    "None",
]

TodoValueTypes = [
    "END_DATETIME",
    "START_DATETIME",
    "COMPLETED_DATETIME",
    "COMPLETED",
    "ALARM_DATETIME",
    "SILENT_ALARM_DATETIME",
    "TEXT",
    "DESCRIPTION",
    "LOCATION",
    "LUID",
    "PRIVATE",
    "CATEGORY",
    "CONTACTID",
    "PHONE",
    "LAST_MODIFIED",
]

InternationalPrefixes = [
    "+1",
    "+20",
    "+210",
    "+211",
    "+212",
    "+213",
    "+214",
    "+215",
    "+216",
    "+217",
    "+218",
    "+219",
    "+220",
    "+221",
    "+222",
    "+223",
    "+224",
    "+225",
    "+226",
    "+227",
    "+228",
    "+229",
    "+230",
    "+231",
    "+232",
    "+233",
    "+234",
    "+235",
    "+236",
    "+237",
    "+238",
    "+239",
    "+240",
    "+241",
    "+242",
    "+243",
    "+244",
    "+245",
    "+246",
    "+247",
    "+248",
    "+249",
    "+250",
    "+251",
    "+252",
    "+253",
    "+254",
    "+255",
    "+256",
    "+257",
    "+258",
    "+259",
    "+260",
    "+261",
    "+262",
    "+263",
    "+264",
    "+265",
    "+266",
    "+267",
    "+268",
    "+269",
    "+27",
    "+28",
    "+290",
    "+291",
    "+292",
    "+293",
    "+294",
    "+295",
    "+296",
    "+297",
    "+298",
    "+299",
    "+30",
    "+31",
    "+32",
    "+33",
    "+34",
    "+350",
    "+351",
    "+352",
    "+353",
    "+354",
    "+355",
    "+356",
    "+357",
    "+358",
    "+359",
    "+36",
    "+370",
    "+371",
    "+372",
    "+373",
    "+374",
    "+375",
    "+376",
    "+377",
    "+378",
    "+379",
    "+380",
    "+381",
    "+382",
    "+383",
    "+384",
    "+385",
    "+386",
    "+387",
    "+388",
    "+389",
    "+39",
    "+40",
    "+41",
    "+420",
    "+421",
    "+422",
    "+423",
    "+424",
    "+425",
    "+426",
    "+427",
    "+428",
    "+429",
    "+43",
    "+44",
    "+45",
    "+46",
    "+47",
    "+48",
    "+49",
    "+500",
    "+501",
    "+502",
    "+503",
    "+504",
    "+505",
    "+506",
    "+507",
    "+508",
    "+509",
    "+51",
    "+52",
    "+53",
    "+54",
    "+55",
    "+56",
    "+57",
    "+58",
    "+590",
    "+591",
    "+592",
    "+593",
    "+594",
    "+595",
    "+596",
    "+597",
    "+598",
    "+599",
    "+60",
    "+61",
    "+62",
    "+63",
    "+64",
    "+65",
    "+66",
    "+670",
    "+671",
    "+672",
    "+673",
    "+674",
    "+675",
    "+676",
    "+677",
    "+678",
    "+679",
    "+680",
    "+681",
    "+682",
    "+683",
    "+684",
    "+685",
    "+686",
    "+687",
    "+688",
    "+689",
    "+690",
    "+691",
    "+692",
    "+693",
    "+694",
    "+695",
    "+696",
    "+697",
    "+698",
    "+699",
    "+7",
    "+800",
    "+801",
    "+802",
    "+803",
    "+804",
    "+805",
    "+806",
    "+807",
    "+808",
    "+809",
    "+81",
    "+82",
    "+83",
    "+84",
    "+850",
    "+851",
    "+852",
    "+853",
    "+854",
    "+855",
    "+856",
    "+857",
    "+858",
    "+859",
    "+86",
    "+870",
    "+871",
    "+872",
    "+873",
    "+874",
    "+875",
    "+876",
    "+877",
    "+878",
    "+879",
    "+880",
    "+881",
    "+882",
    "+883",
    "+884",
    "+885",
    "+886",
    "+887",
    "+888",
    "+889",
    "+89",
    "+90",
    "+91",
    "+92",
    "+93",
    "+94",
    "+95",
    "+960",
    "+961",
    "+962",
    "+963",
    "+964",
    "+965",
    "+966",
    "+967",
    "+968",
    "+969",
    "+970",
    "+971",
    "+972",
    "+973",
    "+974",
    "+975",
    "+976",
    "+977",
    "+978",
    "+979",
    "+98",
    "+990",
    "+991",
    "+992",
    "+993",
    "+994",
    "+995",
    "+996",
    "+997",
    "+998",
    "+999",
]

__all__ = [
    "Errors",
    "ErrorNumbers",
    "Connections",
    "MemoryValueTypes",
    "CalendarTypes",
    "CalendarValueTypes",
    "TodoPriorities",
    "TodoValueTypes",
    "InternationalPrefixes",
]
