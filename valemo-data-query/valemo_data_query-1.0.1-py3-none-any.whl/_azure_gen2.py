from azure.storage.filedatalake import DataLakeServiceClient
import pandas as pd
import numpy as np 
import warnings
import io
import parquet


class azure_datalake_gen2 : 
    
    __aggregation_level_list = ["ALL","NONE","project","year","month"]

    def __init__(self,credentials_dictionnary:dict, basepath:str, extension_file=".csv") : 
        """
        Modèle de requete du datalake gen 2. 

        Parametres : 
        
            - credentials_dictionnary [dict] : 
                Dictionnaire contenant les informations d'identification
                du datalake.
                
                keys : 
                    - 'account' : 
                        Nom du datalake ; 

                    - 'key' : 
                        Mot de passe de connexion ; 

            - basepath [str] : 
                Chemin de base de recherche des partitions ; 
                
            - extension_file [str] : 
                Extension de fichier à rechercher dans l'arborescence ; 
        """
        
        if 'key' not in credentials_dictionnary : 
            raise ValueError("'key' non renseigné dans le dictionnaire d'identification.")
        if 'account' not in credentials_dictionnary : 
            raise ValueError("'account' non renseigné dans le dictionnaire d'identification.")

        self.__storage_account_name = credentials_dictionnary["account"]
        self.__storage_account_key = credentials_dictionnary["key"]
        self.__basepath = basepath

        self.__extension_file = extension_file

        self.__projectListFilter = None
        self.__yearListFilter = None
        self.__monthListFilter = None
        self.__dayListFilter = None

        self.__files_dataframe = None

        self.__dataframe_dictionnary = None
        
        self.__selected_columns = None
        self.__transform_function = None
        self.__arg_transform_function = None
        self.__kwarg_transform_function = None


        ##Initialisation de la connexion
        self.__initialize_storage_account()



    def  __initialize_storage_account(self):
    
        try:  
            self.__account_url="{}://{}.dfs.core.windows.net".format("https", self.__storage_account_name)
            self.__service_client = DataLakeServiceClient(account_url=self.__account_url, credential=self.__storage_account_key)
            self.__file_system_client = self.__service_client.get_file_system_client(file_system="data")
        
        except Exception as e:
            print(e)
    

    def filter_partitionProject(self,projectList:list):
        """
        Filtrage des partitions si comportent les niveaux project=X pour X contenus dans la liste [projectList]
        d'objets "strings. Exemple pour filtrer les projets "BAM" et "BAV" : projectList = ["BAM","BAV"].

        Parametres : 

            - projectList [list<string>] : 
                Noms des projets à filtrer ;

        Returns : 
            None 
        """
        self.__projectListFilter = projectList

    def filter_partitionYear(self,yearList:list):
        """
        Filtrage des partitions si comportent les niveaux year=X pour X contenus dans la liste [yearList]
        d'objets "strings". Exemple pour filtrer les années "2021" et "2022" : yearList = ["2021","2022"].

        Parametres : 

            - yearList [list<string>] :
                Noms des années à filtrer ;

        """
        self.__yearListFilter = yearList

    def filter_partitionMonth(self,monthList:list):
        """
        Filtrage des partitions si comportent les niveaux month=X pour X contenus dans la liste [monthList]
        d'objets "strings". Exemple pour filtrer les mois "09" et "10" : monthList = ["09","10"].

        Parametres : 

            - monthList [list<string>] : 
                Noms des mois à filtrer ;

        """
        self.__monthListFilter = monthList

    # def filter_partitionDay(self,dayList:list):
    #     self.__dayListFilter = 
    
    def select_columns(self,columns:list,return_copy=False):
        """
        Sélectionne les colonnes précisée dans la liste columns. 
        
        Parametres : 
        
            - columns [list<string>] : 
                Liste des colonnes à sélectionner.
                
            - return_copy [bool] option (False) : 
                Si True, une copie est renvoyée sans modifier les données 
                de l'objet. Utilisable seulement de manière différée. 
                
                
        Si les fichiers sont déjà lus, la sélection remplace les données. Sinon 
        la sélection est dynamique lors de la lecture (meilleures performances).
        
        """
        copy_df = None
        if len(columns)>=1:
            self.__selected_columns = columns
            
            
            if self.__dataframe_dictionnary is not None : 
                if return_copy : 
                    copy_df = {}
                for key in self.__dataframe_dictionnary : 
                    df = self.__dataframe_dictionnary[key].copy()
                    col = self.__apply_select_columns(df)
                    if return_copy : 
                        copy_df[key] = df[col]
                    else : 
                        self.__dataframe_dictionnary[key] = df[col]
        return copy_df
                
                
    def __apply_select_columns(self,df:pd.DataFrame):
        df_col = df.columns
        col = [col_k for col_k in self.__selected_columns \
                    if col_k in df_col]
        
        if col == [] : 
            warnings.warn("Select operation not applied because selected columns aren't in dataframe.")
            return df_col
        else : 
            return col
            
    def dataframe_transformation(self,function:callable,
                                      return_copy=False,
                                      args=(),
                                      **kwargs,):
        """
        Applique une transformation des données basée sur une fonction de 
        l'utilisateur. 
        
        Parametres : 
        
            - function [callable] : 
                Fonction de d'utilisateur avec pour argument un dataframe. La 
                fonction s'applique sur les fichiers à la lecture (dynamique),
                ou sur les dataframes d'aggrégation après la lecture. La 
                fonction doit retourner un dataframe qui remplace l'ancien.
            
            - return_copy [bool] option (False) : 
                Si True, une copie est renvoyée sans modifier les données 
                de l'objet. Utilisable seulement de manière différée. 
            
            - args : arguments positionés à passer à la fonction utilisateur. 
            
            - kwargs : arguments par mot-clefs à passer à la fonction. 
        
        Si les fichiers sont déjà lus, l'opération remplace les données.
            
        """
        copy_df = None
        self.__transform_function = function
        self.__arg_transform_function = args
        self.__kwarg_transform_function = kwargs
        if self.__dataframe_dictionnary is not None : 
            if return_copy : 
                copy_df = {}
                
            for key in self.__dataframe_dictionnary : 
                df = self.__dataframe_dictionnary[key].copy()
                transformed_df = self.__apply_dataframe_transformation(df)
                if return_copy : 
                    copy_df[key] = transformed_df
                else :
                    self.__dataframe_dictionnary[key] = transformed_df
        return copy_df
    
    def __apply_dataframe_transformation(self,df):
        df = self.__transform_function(df, 
                                *self.__arg_transform_function, 
                                **self.__kwarg_transform_function)
        return df
        
                    
    def apply_user_partition_filter(self,filter_serie,how="direct",reset_index=True):
        """
        Applique un filtrage sur le dataframe des partitions retourné par la méthode "get_file_partition_df".
        Le filtrage des partitions est basé sur un tableau numpy ou une serie pandas contenant des booléens. 

        Parametres : 

            - filter_serie [numpy.ndarray<bool> or pandas.Series<bool>] : 
                Résultat booléen de la condition de filtrage. 
            
            - how [str] option ('direct') : 
                Méthode utilisée. Si "direct" la méthode slicing des tables numpy et 
                pandas est utilisée (table[filtre]). Si "join", alors le filtre doit
                être une série dont les indexes jointent les indexes de la table de 
                partition originale. 
            
            - reset_index [bool] option (True) : 
                Réinitialise les indexes du dataframe de partition.

        Exemple : 

            # query_model : objet de datalake_query_model
            file_df = query_model.get_partition_files_df
            partition_filter = query_model["partition"].str.contains("project=BAM")
            query_model.apply_user_partition_filter(partition_filter)


        """
        filter_type = type(filter_serie)
        if not( filter_type == pd.Series or filter_type == np.ndarray) : 
            raise ValueError("filter_serie must be a Numpy ndarray or pandas Serie")


        nfilter = filter_serie.shape[0]
        dtype_filter = filter_serie.dtype

        partition_size = self.__files_dataframe.shape[0]

        if (nfilter!=partition_size) : 
            raise ValueError("filter_serie shape doesn't match with partition structure dataframe. Must be (%i,%i) shape."%(partition_size,1))

        if dtype_filter != bool : 
            raise ValueError("filter_serie must be <bool> data type.")
        
        error = False
        if how == "direct" :
            try : 
                filtered_data_frame = self.__files_dataframe[filter_serie]
            except Exception as e :
                error = True
                raise Warning("Filtering not applied because of error : \n",e) 
        elif how == "join" : 
            if filter_type != pd.Series : 
                raise ValueError("For 'join' filtering method you must specified filter_serie as Pandas Serie object.")
            else : 
                try : 
                    filter_serie_copy = filter_serie.rename("user_filter")
                    filtered_data_frame = self.__files_dataframe.join(filter_serie_copy)
                    filtered_data_frame = filtered_data_frame.loc[filtered_data_frame["user_filter"]].\
                                                              drop(columns="user_filter")
                except Exception as e : 
                    error = True
                    raise Warning("Filtering not applied because of error : \n",e) 
        
        if not(error) : 
            if reset_index : 
                filtered_data_frame = filtered_data_frame.reset_index(drop=True)
            self.__files_dataframe = filtered_data_frame.copy()
        return 





    def __partition_reader(self,currentpath,filepath_list,verbose=False) : 
        if verbose : 
            print("     * current directory : ",currentpath)
        paths = self.__file_system_client.get_paths(path=currentpath,recursive=False)
        for path_obj in paths : 
            path_str = path_obj.name
            subdir = path_str.replace(currentpath,'').strip("/")
            
            recursive_read = False
            if subdir.endswith(self.__extension_file) : 
                filepath_list.append(path_str)
            
            elif path_obj.is_directory : 
                recursive_read = self.__partition_filter(subdir)
            
            if recursive_read :
                filepath_list = self.__partition_reader(path_str,filepath_list,verbose=verbose)

        return filepath_list


    def __partition_filter(self,subdir:str):
        recursive_read = True
        if (self.__projectListFilter is not None) and ("project=" in subdir)  : 
            recursive_read =  (subdir.replace("project=","") in self.__projectListFilter) 

        if (self.__yearListFilter is not None) and ("year=" in subdir)  : 
            recursive_read =  (subdir.replace("year=","") in self.__yearListFilter) 

        if (self.__monthListFilter is not None) and ("month=" in subdir)  : 
            recursive_read =  (subdir.replace("month=","") in self.__monthListFilter) 

        if (self.__dayListFilter is not None) and ("day=" in subdir)  : 
            recursive_read =  (subdir.replace("day=","") in self.__dayListFilter) 

        return recursive_read


    

    def read_csv_partition(self,verbose=True):
        """
        Recherche et formation de l'arborescence des fichiers csv présents dans la partition désignée et 
        répondant aux filtres de partitions définis. 

        Parametres : 

            - verbose [bool] option (True) : 
                Print l'évolution de la recherche ;

        """

        self.__extension_file = ".csv"
        self.__read_file_partition(verbose=verbose)
        

    def read_parquet_partition(self,verbose=True):
        """
        Recherche et formation de l'arborescence des fichiers parquets présents dans la partition désignée et 
        répondant aux filtres de partitions définis. 

        Parametres : 

            - verbose [bool] option (True) : 
                Print l'évolution de la recherche ;

        """

        self.__extension_file = ".parquet"
        self.__read_file_partition(verbose=verbose)



    def __read_file_partition(self,verbose=True) :

        filepath_list = []
        filepath_list = self.__partition_reader(self.__basepath,filepath_list,verbose=verbose)
        if len(filepath_list) == 0 : 
            self.__files_dataframe = None 
            return None 

        self.__files_dataframe = pd.DataFrame(filepath_list,columns=["filepath"])

        self.__files_dataframe[['partition',
                                    "filename"]] = self.__files_dataframe["filepath"].\
                                                        str.replace(self.__basepath,"").\
                                                        str.rsplit("/",n=1,expand=True)
        
        
        for s in ["project","year","month","day"] :
            sprefixe = s+"="  
            self.__files_dataframe.loc[:,s] = ''
            filter_s_in_partitions = self.__files_dataframe['partition'].str.contains(s)
            if filter_s_in_partitions.any() : 

                self.__files_dataframe.loc[filter_s_in_partitions,s] = \
                                                sprefixe +\
                                                self.__files_dataframe.loc[filter_s_in_partitions,
                                                                                'partition'].\
                                                str.split(s+"=",expand=True)[1].\
                                                str.split("/",expand=True)[0]
        
        
        
        
    def __concatenate_aggregation(self,aggregation_level):
            
        err_agg_level = True
        if isinstance(aggregation_level,list) : 
            if np.all([s in self.__aggregation_level_list for s in aggregation_level]) : 
                err_agg_level = False
                aggregation_list = aggregation_level.copy()
        elif isinstance(aggregation_level,str) : 
            if aggregation_level in self.__aggregation_level_list : 
                err_agg_level = False
                aggregation_list = [aggregation_level]
        if err_agg_level : 
            raise ValueError("Aggregation_level non valide : " +\
                        ",".join(self.__aggregation_level_list))

        aggregation_item = pd.Series(np.full(self.__files_dataframe.shape[0],'',dtype=str))

        for agg_level in aggregation_list : 
            if agg_level in self.__files_dataframe.columns : 
                aggregation_item.loc[:] = aggregation_item.loc[:] + "_" + self.__files_dataframe[agg_level].astype(str)
            elif agg_level == 'ALL' : 
                aggregation_item.loc[:] = "dataset"
            elif agg_level == 'NONE' : 
                aggregation_item.loc[:] = self.__files_dataframe["partition"].str.replace( r"\/" ,"_", regex=True)
            else : 
                aggregation_item.loc[:] = "dataset"
        return aggregation_item

    def __csv_reader(self,fileclient,delimiter,header,encoding):
        fileobject = io.BytesIO(fileclient.download_file().readall())
        dataframe = pd.read_csv(fileobject,sep=delimiter,header=header,encoding=encoding).\
                        dropna(how='all')
        return dataframe
        
    
    
    def __parquet_reader(self,fileclient):
        fileobject = io.BytesIO(fileclient.download_file().readall())
        filegenerator = parquet.DictReader(fileobject)
        dataframe = pd.DataFrame(filegenerator).\
                        dropna(how='all')
        return dataframe
        
        

    def concatenate_pandas(self,aggregation_level='ALL',delimiter=',',
                header="infer",verbose=True,convert_dtypes=False,
                encoding='utf-8',keep_partition_col=False,partition_col_prefixe="part."):
        """
        Lecture des fichiers présents dans l'arborescence puis concaténation
        sous un ou plusieurs dataframes pandas.

        Parametres : 

            - aggregation_level [str or list<str>] option ('ALL') :
                Défini un niveau d'aggrégation des dataframes. 
                Si 'ALL' tout est réuni sous un seul df. 
                Si 'month' l'aggréation est effectué sur le niveau
                'month=X' de la partition du fichier. 
                Possible d'avoir des niveaux multiples. 
                Si ["month","year"] partition par année et mois. 

            - delimiter [str] option (",") : 
                caractère de délimitation des colonnes du csv du
                datalake (seulement pour fichiers csv). 

            - header (seulement pour fichiers csv) 
                VOIR description pandas.read_csv : 
                int, list of int, default ‘infer’
                Row number(s) to use as the column names, 
                and the start of the data. Default behavior 
                is to infer the column names: if no names are 
                passed the behavior is identical to header=0 
                and column names are inferred from the first 
                line of the file, if column names are passed 
                explicitly then the behavior is identical to 
                header=None. Explicitly pass header=0 to be 
                able to replace existing names. The header can be
                a list of integers that specify row locations 
                for a multi-index on the columns e.g. [0,1,3]. 
                Intervening rows that are not specified will be 
                skipped (e.g. 2 in this example is skipped). 
                Note that this parameter ignores commented
                lines and empty lines if skip_blank_lines=True, 
                so header=0 denotes the first line 
                of data rather than the first line of the file.

            - convert_dtypes [bool] option (False) : 
                Appelle la fonction convert_dtypes de pandas. 

            - encoding [str] option ("utf-8") : 
                Encodage des fichiers csv du datalake (seulement pour fichiers csv). 

            - verbose [bool] option (True) : 
                Print l'évolution de la lecture et de l'aggrégation.

            - keep_partition_col [bool] option (False) : 
                Garde les colonnes définies par le chemin de la partition ; 
            
            - partition_col_prefixe [str] option (".part") : 
                Ajoute un préfixe aux colonnes ajoutées si keep_partition_col = True ;

        """
        if self.__files_dataframe is None : 
            self.__read_file_partition(verbose=verbose)
        if self.__files_dataframe.shape[0] == 0 : 
            raise ValueError("Empty partition. No file to read.")
            return 
        
        if self.__extension_file == ".parquet" :
            warnings.warn("Parquet reader not able to handle timestamp and datetime dtype.")
            
        aggregation_serie = self.__concatenate_aggregation(aggregation_level)
        
        listdf_dictionnary = {c : []  for c in aggregation_serie.unique()}
        print("READING PARTITIONS ... ")
        partitions_columns = self.__files_dataframe.columns
        for k,row in self.__files_dataframe.iterrows() : 
            if verbose : print("     * reading ", row["partition"] )
            filepath = row["filepath"]

            fileclient = self.__file_system_client.get_file_client(filepath)
            
            ## ------------ READ
            if self.__extension_file == ".csv" : 
                dataframe = self.__csv_reader(fileclient,delimiter,header,encoding)

            if self.__extension_file == ".parquet" : 
                dataframe = self.__parquet_reader(fileclient)
            

            ## ------------ TRANSFORM
            if (self.__selected_columns is not None)  : 
                col = self.__apply_select_columns(dataframe)
                dataframe = dataframe[col]
            
            if self.__transform_function is not None : 
                dataframe = self.__apply_dataframe_transformation(dataframe)
            
            if convert_dtypes : 
                dataframe = dataframe.convert_dtypes()

            ## ------------ AJOUT COLONNE PARTITION
            if keep_partition_col : 
                for col_partition in partitions_columns : 
                    dataframe.loc[:,partition_col_prefixe + col_partition] = \
                            row[col_partition]




            groupk = aggregation_serie.loc[k]
            listdf_dictionnary[groupk].append(dataframe)
        
        dataframe_dictionnary = {c : []  for c in aggregation_serie.unique()}
        notnull_partition = []
        print("CONCAT DATASET ... ")
        for ck in listdf_dictionnary : 
            listdf_k = listdf_dictionnary[ck]
            if verbose : print("Concatenated aggregation : ",ck)
            if len(listdf_k) > 0 : 
                notnull_partition.append(ck)
                df_k = pd.concat(listdf_k,sort=False,ignore_index=True)
                dataframe_dictionnary[ck] = df_k
                print("     * size : ",df_k.shape)
        self.__dataframe_dictionnary = {ck:dataframe_dictionnary[ck] for ck in notnull_partition}

            
    def write_concatenated_dataset_csv(self,local_path:str,
                    file_prefixe = "",
                    index=False,
                    encoding='utf-8',
                    delimiter=','):
        """
        Ecriture des fichiers lus avec la méthode concatenate_pandas au format csv.

        Parametres : 
            - local_path [str] : 
                Chemin d'écriture des fichiers.

            - delimiter [str] option (",") : 
                Caractère de délimitation des colonnes du csv local. 

            - encoding [str] option ("utf-8") : 
                Encodage des fichiers csv locaux. 

            - index [bool] option (False) : 
                Ecrire les index du dataframe dans le csv local. 

        """

        local_path = local_path.replace("\\","/")
        if not(local_path.endswith("/")) :
            local_path = local_path +"/" 
        if self.__dataframe_dictionnary is None : 
            print("No dataset to write.")
        else : 
            for ck in self.__dataframe_dictionnary : 
                self.__dataframe_dictionnary[ck].to_csv(local_path+file_prefixe+ck+".csv",
                            index=index,
                            encoding=encoding,
                            sep=delimiter)


    @property
    def get_file_partition_df(self):
        """
        Return : 

            - dataframe : 
                Arborescence des fichiers correspondant à la
                partition de base et au format de fichier recherché.
        """
        return self.__files_dataframe


    @property
    def get_concatenated_dataframes(self):
        """
        Return : 

            - dict<dataframe> or None : 
                Dictionnaire contenant les différentes aggrégations des partitions ouvertes. 
                None si vide. 
        """
        return self.__dataframe_dictionnary




                               
                            
        
