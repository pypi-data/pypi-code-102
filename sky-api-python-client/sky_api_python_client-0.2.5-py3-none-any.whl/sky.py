import pandas as pd
import re
import pytz
import os
import pickle


from .utils import *
from logging import warn
from datetime import datetime


class Sky:

    def __init__(
        self, 
        api_key: Union[str, None] = None, 
        file_path: str = "sky_credentials.json", 
        token_path: Union[str, None]  = None
        ):
        """Blackbaud Sky API client 

        This class uses a :class:`authlib.integrations.requests_client.OAuth2Session` for 
        calls to the Blackbaud Sky API.
        
        """
        self.token = None
        self.client = None
        self.file_path = file_path

        # Seeing if the user saved the api key as an environment variable
        if os.getenv('BB_API_KEY'):
            self.api_key = os.getenv('BB_API_KEY')
        elif api_key:
            self.api_key = api_key
        else:
            warn("""
            A api key is needed to call the Blackbaud sky api. You can either initialize it when calling 
            the Sky class or you can save it in a environment variable called BB_API_KEY
            """)

        # Path to cached token
        if token_path:
            self.token_path = token_path
        elif os.getenv('BB_TOKEN_PATH'):
            self.token_path = os.getenv('BB_TOKEN_PATH')
        else:
            self.token_path = '.sky-token'


    @authorize
    def get(
        self,
        endpoint: str = "roles",
        params: Union[dict, None] = None,
        reference: str = 'school',
        raw_data: bool = False
        ) -> Union[dict, pd.DataFrame, dict, None]:
        """ Get request to the Sky API
        Args:
            params: Dictionary that defines parameters to be passed to 
            the api
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = GetRequest(
            self.client,
            url,
            self.request_header,
            params=params
        )

        data = apiCall.getData()
        self._saveToken(apiCall.updateToken(self.token))

        if raw_data:
            return data

        if not data.get('value'):
            return None
        df = pd.json_normalize(data['value'])

        while True:
            # Checking for another link
            if not data.get('next_link'):
                 return df
            # Saving the next link
            link = data['next_link']
            # Finding the endpoint value
            end = re.search('v[\\d]/', link).end(0)
            url = self._get_url(reference, link[end:])
            # Calling the api again
            data = GetRequest(
                self.client,
                url,
                self.request_header,
                params=params
            ).getData()
            # Typing the new data as a df and appending the data
            new_df = pd.json_normalize(data['value'])
            df = df.append(new_df)


    @authorize
    def post(
        self,
        data: dict,
        reference: str = 'school',
        endpoint: str = "users",
        ) -> dict:
        """Post request to the Sky API
        Args:
            data: Dictionary that defines the request data to be passed to 
            the api in order to create a new record
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = PostRequest(
            self.client,
            url,
            self.request_header,
            data=data
        )

        data = apiCall.getData()
        self._saveToken(apiCall.updateToken(self.token))
        return data


    @authorize
    def patch(
        self,
        reference: str = 'school',
        endpoint: str = "users",
        params: Union[dict, None] = None,
        body: Union[dict, None] = None,
        data: Union[dict, None] = None,
        **kwargs
        ) -> dict:
        """Patch requests to the Sky API
        Args:
            data: Dictionary that defines the request data to be passed to 
            the api in order to create a new record
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = PatchRequest(
            self.client,
            url,
            self.request_header,
            params=params,
            data=data
        )

        data = apiCall.getData(**kwargs)
        self._saveToken(apiCall.updateToken(self.token))
        return data


    @authorize
    def delete(
        self,
        reference: str = 'school',
        endpoint: str = "roles",
        params: Union[dict, None] = None,
        data: Union[dict, None] = None,
        **kwargs
        ) -> dict:
        """Delete requests to the sky API

        Args:
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference
            **kwargs: ... Honestly don't know yet. Never used this endpoint. Just 
            adding for testing

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = DeleteRequest(
            self.client,
            url,
            self.request_header,
            params = params,
            data=data
        )

        data = apiCall.getData(**kwargs)
        self._saveToken(apiCall.updateToken(self.token))
        return data


    def getUsers(
        self,
        role: str = 'student'
        ):
        """ Get a DataFrame of users from the Core database
        
        """
        users = self.get(
            endpoint = 'users/extended',
            params = {'base_role_ids':self.getRoleId(role)}
        )
        return users


    def getRoleId(
        self,
        role_name: str,
        base: bool = True
        ) -> int:
        """ Get the Blackbaud id of a role in the Core database

        Args:
            role_name: Name of a role in Core
            base: If True the base_role_id is returned, otherwise the role id 
            is returned

        Returns:
            The id of a given role
        """
        role_id = self.get('roles')
        role_id = role_id.loc[role_id.name == role_name.title()]
        if base:
            return role_id.base_role_id
        return role_id.id


    def get_levels(
        self,
        abbreviation: str =None, 
        name: str =None, 
        id: bool =False
        ) -> Union[pd.DataFrame, int]:
        """ Gets school level data from Core database

        Args:
            abbreviation: Abbreviation of a given school level in the Core db 
            name: Name of a given school level in the Core db 
            id: If True only the levels id will be returned

        Returns:
            Either a df of the school level(s) in the Core db or just the 
            given level's id
        """
        # Calling sky to get levels
        levels = self.get('levels')
        # Filtering
        if abbreviation:
            levels = levels.loc[(levels.abbreviation == abbreviation), ]
        elif name:
            levels = levels.loc[(levels.name == name), ]
        
        # Either returning levels df or just the id value of a particular school level
        if id:
            return levels['id']
        return levels


    def getSections(
        self,
        abbreviation: str =None, 
        name: str =None, 
        ) -> pd.DataFrame:
        """ Gets the sections in the users Core database

        Args:
            abbreviation: Abbreviation of a given school level in the Core db 
            to be passed into self.getLevels
            name: Name of a given school level in the Core db to be passed
             into self.getLevels
        
        Returns:
            Dataframe with data from sections in the Core Db
        """

        course_levels = self.get_levels(
            name=name,
            abbreviation=abbreviation,
            id=True
            )

        df = pd.DataFrame()

        # Looping over the course levels and passing in their value to the Sky API
        for index, value in course_levels.iteritems():
            # Appending data to the df
            df = df.append(self.get(
                endpoint = 'academics/sections',
                params = {'level_num':value}
            ))
        


        # Cleaning the teacher data for each section
        teacher_data = df.explode(
            'teachers'
        )['teachers'].apply(pd.Series).query(
            'head == True'
        ).add_prefix('teacher.').drop(
            'teacher.0', 
            axis=1
        )

        # Merging the section data with the teachers clena data
        df = df.merge(
            teacher_data,
            left_index=True,
            right_index=True
        ).reset_index(drop=True).drop(
            'teachers',
            axis=1
        )

        return df


    def getStudentEnrollments(
        self
        ) -> pd.DataFrame:
        """ Returns a DataFrame of all current student enrollments
        """
        sections = self.getSections()
        big_df = pd.DataFrame()
        for index, section_id in sections.id.iteritems():
            endpoint = f'academics/sections/{section_id}/students'
            roster = self.get(endpoint=endpoint)
            # Checking that a valid roster was returned
            if not isinstance(roster, pd.DataFrame):
                continue
            roster = roster.assign(section_id=section_id).rename(columns={'id':"userId"})
            big_df = big_df.append(roster)
        return big_df


    def getTerm(
        self,
        offeringType: str = "Academics", 
        name = False
        ) -> pd.DataFrame:
        """ Gets the active terms for the given offering type
        
        Args:
            offeringType: A string of a Core offering type
            name: If true just the name of the active terms wil be returned
        Returns:

        """
        params = {'offering_type':self.getOfferingId(offeringType)}

        data = self.get(
            'terms', 
            params=params
        )[
            [
                'id', 'level_description', 'description',
                'begin_date', 'end_date'
            ]
        ]
        
        data = data.query('id > 0').reset_index(drop=True)
        data['begin_date'] = pd.to_datetime(data['begin_date'])
        data['end_date'] = pd.to_datetime(data['end_date'])

        active_terms = self._isActive(data).rename(columns={
            "id":"term_id",
             'description':'term_name'
        })[['term_id', 'term_name', 'active']]
        
        if name:
            active_terms = active_terms.loc[
                active_terms['active'] == True, 
                'term_name'].drop_duplicates()

        return active_terms


    def getOfferingId(
        self,
        offeringType: str = "Academics"
        ) -> int:
        """ Gets the id of a Core offering type
        """
        data = self.get('offeringtypes')
        return data.loc[(data.description == offeringType), 'id'] .values[0]


    def getAdvancedList(
        self,
        list_id:int
        ) -> pd.DataFrame:
        """ Gets Advanced list from Core 

        Args:
            list_id: The sld of an advanced list in Core

        Returns:
            A pandas dataframe of the advanced list
        """
        # Calling api to get raw list data
        raw_list = self.get(endpoint=f'legacy/lists/{list_id}', raw_data=True)
        # Type casting the data to a dataframe
        data = pd.json_normalize(raw_list['rows'], 'columns').reset_index()
        return self._cleanAdvancedList(data)


    def _cleanAdvancedList(
        self,
        data: pd.DataFrame
        ) -> pd.DataFrame:
        """ Cleans data from the legacy/list Sky API endpoint
        Args:
            data: Data returned from calling the legacy/list Sky API endpoint 

        Returns:
            Pandas DataFrame with data from a Core Advanced List        
        """
        # Initializing empty array to store index data
        index = []
        # Number of columns in the data
        ncol = len(data.name.unique())
        # Initializing index value
        num = 0

        for i in range(len(data)):
            if (i % ncol) == 0:
                num += 1
            index.append(num)

        # Setting the index values
        data['index'] = index
        
        # Piviting the data wider
        data = data.pivot(index = "index", columns = "name", values = "value")
        return data


    def _isActive(
        self,
        data: pd.DataFrame
         ) -> pd.DataFrame:
        """ Takes 

        Args:
            data: pd.DataFrame with two datetime columns named
            'begin_date' & 'end_date' respectfully 

        Returns:
            Orginal DataFrame, but with a 'active' column that represents whether the current date 
            lies within the date range provided in the ['begin_date'. 'end_date'] columns.        
        """
        # Setting time zone
        utc=pytz.UTC
        today = utc.localize(datetime.now()) 
        data['active'] = [False for i in range(len(data))]
        # Checking which terms are active
        for index, row in data.iterrows():
            data.loc[index, 'active'] = (row['begin_date'] <= today <= row['end_date'])
        return data


    def _loadCachedToken(self) -> Union[None, OAuth2Token]:
        """Load Sky API token from cache"""
        # Loading token from binary file
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.token = pickle.load(token)          
        return self.token


    def _get_url(self, reference: str, endpoint: str) -> str:
        """Format api requests url

        Args:
            reference: 
            endpoint: 

        Returns:
            API url to call
        """
        return f'https://api.sky.blackbaud.com/{reference}/v1/{endpoint}'


    def _saveToken(
        self, 
        token: OAuth2Token
        ) -> None:
        """Save OAuth2Token for future use"""
        with open(self.token_path,  'wb') as f:
            pickle.dump(token, f)
        self.token = token


    @property
    def request_header(self):
        """API key to pass to Request header"""
        return {"Bb-Api-Subscription-Key": self.api_key}