from hdsr_wis_config_reader.constants.idmappings.columns import IdMapColumnChoices
from hdsr_wis_config_reader.constants.idmappings.custom_dataframe import IdMappingDataframe
from hdsr_wis_config_reader.constants.idmappings.files import IdMapChoices
from hdsr_wis_config_reader.fews_utilities import FewsConfig
from hdsr_wis_config_reader.fews_utilities import xml_to_dict

import pandas as pd  # noqa pandas comes with geopandas


class IdMappingCollection:
    def __init__(self, fews_config: FewsConfig):
        self.fews_config = fews_config
        self._id_opvl_water = None
        self._id_opvl_water_hymos = None
        self._id_hdsr_nsc = None
        self._id_opvl_water_wq = None
        self._id_grondwater_caw = None
        self._id_all = None

    @property
    def idmap_opvl_water(self) -> IdMappingDataframe:
        if self._id_opvl_water is not None:
            return self._id_opvl_water
        self._id_opvl_water = self.get_idmap_df(idmap=IdMapChoices.idmap_opvl_water)
        return self._id_opvl_water

    @property
    def idmap_opvl_water_hymos(self) -> IdMappingDataframe:
        if self._id_opvl_water_hymos is not None:
            return self._id_opvl_water_hymos
        self._id_opvl_water_hymos = self.get_idmap_df(idmap=IdMapChoices.idmap_opvl_water_hymos)
        return self._id_opvl_water_hymos

    @property
    def idmap_hdsr_nsc(self) -> IdMappingDataframe:
        if self._id_hdsr_nsc is not None:
            return self._id_hdsr_nsc
        self._id_hdsr_nsc = self.get_idmap_df(idmap=IdMapChoices.idmap_hdsr_nsc)
        return self._id_hdsr_nsc

    @property
    def idmap_opvl_water_wq(self) -> IdMappingDataframe:
        if self._id_opvl_water_wq is not None:
            return self._id_opvl_water_wq
        self._id_opvl_water_wq = self.get_idmap_df(idmap=IdMapChoices.idmap_opvl_water_wq)
        return self._id_opvl_water_wq

    @property
    def idmap_grondwater_caw(self) -> IdMappingDataframe:
        if self._id_grondwater_caw is not None:
            return self._id_grondwater_caw
        self._id_grondwater_caw = self.get_idmap_df(idmap=IdMapChoices.idmap_grondwater_caw)
        return self._id_grondwater_caw

    @property
    def idmap_all(self) -> IdMappingDataframe:
        if self._id_all is not None:
            return self._id_all
        merged_df = IdMappingDataframe(
            columns=[
                IdMapColumnChoices.ex_loc.value,
                IdMapColumnChoices.ex_par.value,
                IdMapColumnChoices.int_loc.value,
                IdMapColumnChoices.int_par.value,
            ]
        )
        for idmap in IdMapChoices:
            idmap_df = getattr(self, idmap.name)
            assert isinstance(idmap_df, IdMappingDataframe)
            merged_df = pd.concat(objs=[merged_df, idmap_df], axis=0)
        self._id_all = merged_df
        return self._id_all

    @classmethod
    def add_column_histtag(cls, df: IdMappingDataframe) -> IdMappingDataframe:
        assert (IdMapColumnChoices.ex_loc.value and IdMapColumnChoices.ex_par.value) in df
        df["histtag"] = df[IdMapColumnChoices.ex_loc.value] + "_" + df[IdMapColumnChoices.ex_par.value]
        return df

    def get_idmap_df(self, idmap: IdMapChoices) -> IdMappingDataframe:
        assert isinstance(idmap, IdMapChoices)
        file_name = idmap.value
        file_path = self.fews_config.IdMapFiles[file_name]
        _dict = xml_to_dict(xml_filepath=file_path)
        _list_with_dicts = _dict["idMap"]["map"]
        # use a Dataframe that is extended with custom (filter) methods
        df = IdMappingDataframe(data=_list_with_dicts)
        assert sorted(df.columns) == [
            IdMapColumnChoices.ex_loc.value,
            IdMapColumnChoices.ex_par.value,
            IdMapColumnChoices.int_loc.value,
            IdMapColumnChoices.int_par.value,
        ]
        df["source"] = file_name
        df = self.add_column_histtag(df=df)
        return df
