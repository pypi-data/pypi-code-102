"""
Defines generic sensor data and data for API-independent analysis
all timestamps are integers in microseconds unless otherwise stated
"""
import enum
from typing import List, Union, Dict, Optional, Tuple
from pathlib import Path
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.parquet as pq

import redvox.common.sensor_data_io as io
import redvox.common.date_time_utils as dtu
from redvox.common.io import FileSystemWriter as Fsw
from redvox.common import offset_model as om
from redvox.common.errors import RedVoxExceptions
from redvox.common.gap_and_pad_utils_wpa import calc_evenly_sampled_timestamps
from redvox.api1000.wrapped_redvox_packet.station_information import (
    NetworkType,
    PowerState,
    CellServiceState,
    WifiWakeLock,
    ScreenState,
)
from redvox.api1000.wrapped_redvox_packet.sensors.location import LocationProvider
from redvox.api1000.wrapped_redvox_packet.sensors.image import ImageCodec
from redvox.api1000.wrapped_redvox_packet.sensors.audio import AudioCodec

# columns that cannot be interpolated
NON_INTERPOLATED_COLUMNS = ["compressed_audio", "image"]
# columns that are not numeric but can be interpolated
NON_NUMERIC_COLUMNS = ["location_provider", "image_codec", "audio_codec", "network_type",
                       "power_state", "cell_service", "wifi_wake_lock", "screen_state"]


class SensorType(enum.Enum):
    """
    Enumeration of possible types of sensors to read data from
    """

    UNKNOWN_SENSOR = 0  # unknown sensor
    ACCELEROMETER = 1  # meters/second^2
    AMBIENT_TEMPERATURE = 2  # degrees Celsius
    AUDIO = 3  # normalized counts
    COMPRESSED_AUDIO = 4  # bytes (codec specific)
    GRAVITY = 5  # meters/second^2
    GYROSCOPE = 6  # radians/second
    IMAGE = 7  # bytes (codec specific)
    LIGHT = 8  # lux
    LINEAR_ACCELERATION = 9  # meters/second^2
    LOCATION = 10  # See standard
    MAGNETOMETER = 11  # microtesla
    ORIENTATION = 12  # radians
    PRESSURE = 13  # kilopascal
    PROXIMITY = 14  # on, off, cm
    RELATIVE_HUMIDITY = 15  # percentage
    ROTATION_VECTOR = 16  # Unitless
    INFRARED = 17  # this is proximity
    STATION_HEALTH = 18
    # Health sensors: battery charge and current level, phone internal temperature, network source and strength,
    # available RAM of the system, cell service status, amount of hard disk space left, power charging state
    # wifi lock state, cpu utilization, screen state, and screen brightness
    BEST_LOCATION = 19  # See standard

    @staticmethod
    def type_from_str(type_str: str) -> "SensorType":
        """
        converts a string to a sensor type

        :param type_str: string to convert
        :return: a sensor type, UNKNOWN_SENSOR is the default for invalid inputs
        """
        if (
                type_str.lower() == "audio"
                or type_str.lower() == "mic"
                or type_str.lower() == "microphone"
        ):
            return SensorType.AUDIO
        elif type_str.lower() == "accelerometer" or type_str.lower() == "accel":
            return SensorType.ACCELEROMETER
        elif type_str.lower() == "ambient_temperature":
            return SensorType.AMBIENT_TEMPERATURE
        elif type_str.lower() == "compressed_audio":
            return SensorType.COMPRESSED_AUDIO
        elif type_str.lower() == "gravity":
            return SensorType.GRAVITY
        elif type_str.lower() == "gyroscope" or type_str.lower() == "gyro":
            return SensorType.GYROSCOPE
        elif type_str.lower() == "image":
            return SensorType.IMAGE
        elif type_str.lower() == "light":
            return SensorType.LIGHT
        elif (
                type_str.lower() == "linear_acceleration"
                or type_str.lower() == "linear_accel"
        ):
            return SensorType.LINEAR_ACCELERATION
        elif type_str.lower() == "location" or type_str.lower() == "loc":
            return SensorType.LOCATION
        elif type_str.lower() == "best_location" or type_str.lower() == "best_loc":
            return SensorType.BEST_LOCATION
        elif type_str.lower() == "magnetometer" or type_str.lower() == "mag":
            return SensorType.MAGNETOMETER
        elif type_str.lower() == "orientation":
            return SensorType.ORIENTATION
        elif (
                type_str.lower() == "pressure"
                or type_str.lower() == "bar"
                or type_str.lower() == "barometer"
        ):
            return SensorType.PRESSURE
        elif type_str.lower() == "proximity" or type_str.lower() == "infrared":
            return SensorType.PROXIMITY
        elif type_str.lower() == "relative_humidity":
            return SensorType.RELATIVE_HUMIDITY
        elif type_str.lower() == "rotation_vector":
            return SensorType.ROTATION_VECTOR
        else:
            return SensorType.UNKNOWN_SENSOR


class SensorDataPa:
    """
    Generic SensorData class for API-independent analysis

    Properties:
        name: string, name of sensor.  REQUIRED

    Protected:
        _type: SensorType, enumerated type of sensor, default UNKNOWN_SENSOR

        _sample_rate_hz: float, sample rate in Hz of the sensor, default np.nan, usually 1/sample_interval_s

        _sample_interval_s: float, mean duration in seconds between samples, default np.nan, usually 1/sample_rate

        _sample_interval_std_s: float, standard deviation in seconds between samples, default np.nan

        _is_sample_rate_fixed: bool, True if sample rate is constant, default False

        _timestamps_altered: bool, True if timestamps in the sensor have been altered from their original values
        default False

        _use_offset_model: bool, if True, use an offset model to correct timestamps, otherwise use the best known
        offset.  default False

        _errors: RedVoxExceptions, class containing a list of all errors encountered by the sensor.

        _gaps: List of Tuples of floats, timestamps of data points on the edge of gaps, default empty list

        _fs_writer: FileSystemWriter, handles file system i/o parameters

        _data: pyarrow Table, used to store the data when it's not written to the disk.  default None
    """

    def __init__(
            self,
            sensor_name: str,
            sensor_data: Optional[pa.Table] = None,
            sensor_type: SensorType = SensorType.UNKNOWN_SENSOR,
            sample_rate_hz: float = np.nan,
            sample_interval_s: float = np.nan,
            sample_interval_std_s: float = np.nan,
            is_sample_rate_fixed: bool = False,
            are_timestamps_altered: bool = False,
            calculate_stats: bool = False,
            use_offset_model_for_correction: bool = False,
            save_data: bool = False,
            base_dir: str = ".",
            gaps: Optional[List[Tuple[float, float]]] = None,
            show_errors: bool = False
    ):
        """
        initialize the sensor data with params

        :param sensor_name: name of the sensor.  REQUIRED
        :param sensor_type: enumerated type of the sensor, default SensorType.UNKNOWN_SENSOR
        :param sensor_data: Optional pyarrow table with the timestamps and sensor data;
                            first column is always the timestamps,
                            the other columns are specific metadata and data channels in the sensor
                            default is None
        :param sample_rate_hz: sample rate in hz of the data
        :param sample_interval_s: sample interval in seconds of the data
        :param sample_interval_std_s: std dev of sample interval in seconds of the data
        :param is_sample_rate_fixed: if True, sample rate is constant for all data, default False
        :param are_timestamps_altered: if True, timestamps in the sensor have been altered from their
                                        original values, default False
        :param calculate_stats: if True, calculate sample_rate, sample_interval_s, and sample_interval_std_s
                                default False
        :param use_offset_model_for_correction: if True, use an offset model to correct timestamps, otherwise
                                                use the best known offset.  default False
        :param save_data: if True, save the data of the sensor to disk, otherwise use a temporary dir.  default False
        :param base_dir: directory to save pyarrow table, default "." (current dir).  internally uses a temporary
                            dir if not saving data
        :param gaps: Optional list of timestamp pairs of data points on the edge of gaps in the data.  anything between
                        the pairs of points exists to maintain sample rate and are not considered valid points.
                        Default None
        :param show_errors: if True, show any errors encountered.  Default False
        """
        self._errors: RedVoxExceptions = RedVoxExceptions("Sensor")
        self.name: str = sensor_name
        self._type: SensorType = sensor_type
        self._sample_rate_hz: float = sample_rate_hz
        self._sample_interval_s: float = sample_interval_s
        self._sample_interval_std_s: float = sample_interval_std_s
        self._is_sample_rate_fixed: bool = is_sample_rate_fixed
        self._timestamps_altered: bool = are_timestamps_altered
        self._use_offset_model: bool = use_offset_model_for_correction
        self._fs_writer = Fsw("", "parquet", base_dir, save_data)
        self._gaps: List[Tuple] = gaps if gaps else []
        self._data: Optional[pa.Table()] = None
        if sensor_data:
            if "timestamps" not in sensor_data.schema.names:
                self._errors.append('must have a column titled "timestamps"')
            elif sensor_data['timestamps'].length() > 0:
                self.set_file_name(f"{sensor_type.name}_{int(sensor_data['timestamps'][0].as_py())}")
                if calculate_stats:
                    self.organize_and_update_stats(sensor_data)
                elif sensor_data["timestamps"].length() > 1:
                    self.sort_by_data_timestamps(sensor_data)
                else:
                    self.write_pyarrow_table(sensor_data)
        else:
            self._errors.append('cannot be empty')
        if show_errors:
            self.print_errors()

    @staticmethod
    def from_dir(
            sensor_name: str,
            data_path: str,
            sensor_type: SensorType = SensorType.UNKNOWN_SENSOR,
            sample_rate_hz: float = np.nan,
            sample_interval_s: float = np.nan,
            sample_interval_std_s: float = np.nan,
            is_sample_rate_fixed: bool = False,
            are_timestamps_altered: bool = False,
            calculate_stats: bool = False,
            use_offset_model_for_correction: bool = False,
            save_data: bool = False) -> "SensorDataPa":
        """
        init but with a path to directory containing parquet file(s) instead of a table of data

        :param sensor_name: name of the sensor
        :param data_path: path to the directory containing the parquet files
        :param sensor_type: enumerated type of the sensor, default SensorType.UNKNOWN_SENSOR
        :param sample_rate_hz: sample rate in hz of the data, default np.nan
        :param sample_interval_s: sample interval in seconds of the data, default np.nan
        :param sample_interval_std_s: std dev of sample interval in seconds of the data, default np.nan
        :param is_sample_rate_fixed: if True, sample rate is constant for all data, default False
        :param are_timestamps_altered: if True, timestamps in the sensor have been altered from their
                                        original values, default False
        :param calculate_stats: if True, calculate sample_rate, sample_interval_s, and sample_interval_std_s
                                default False
        :param use_offset_model_for_correction: if True, use an offset model to correct timestamps, otherwise
                                                use the best known offset.  default False
        :param save_data: if True, save the data of the sensor to disk, otherwise use a temporary dir.  default False
        :return: SensorData object
        """
        result = SensorDataPa(sensor_name,
                              ds.dataset(data_path, format="parquet", exclude_invalid_files=True).to_table(),
                              sensor_type, sample_rate_hz, sample_interval_s, sample_interval_std_s,
                              is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                              use_offset_model_for_correction, save_data, data_path)
        result.set_file_name()
        return result

    @staticmethod
    def from_dict(
            sensor_name: str,
            sensor_data: Dict,
            sensor_type: SensorType = SensorType.UNKNOWN_SENSOR,
            sample_rate_hz: float = np.nan,
            sample_interval_s: float = np.nan,
            sample_interval_std_s: float = np.nan,
            is_sample_rate_fixed: bool = False,
            are_timestamps_altered: bool = False,
            calculate_stats: bool = False,
            use_offset_model_for_correction: bool = False,
            save_data: bool = False,
            arrow_dir: str = "",
    ) -> "SensorDataPa":
        """
        init but with a dictionary

        :param sensor_name: name of the sensor
        :param sensor_type: enumerated type of the sensor, default SensorType.UNKNOWN_SENSOR
        :param sensor_data: dict with the timestamps and sensor data; first column is always the timestamps,
                            the other columns are the data channels in the sensor
        :param sample_rate_hz: sample rate in hz of the data, default np.nan
        :param sample_interval_s: sample interval in seconds of the data, default np.nan
        :param sample_interval_std_s: std dev of sample interval in seconds of the data, default np.nan
        :param is_sample_rate_fixed: if True, sample rate is constant for all data, default False
        :param are_timestamps_altered: if True, timestamps in the sensor have been altered from their
                                        original values, default False
        :param calculate_stats: if True, calculate sample_rate, sample_interval_s, and sample_interval_std_s
                                default False
        :param use_offset_model_for_correction: if True, use an offset model to correct timestamps, otherwise
                                                use the best known offset.  default False
        :param save_data: if True, save the data of the sensor to disk, otherwise use a temporary dir.  default False
        :param arrow_dir: directory to save pyarrow table, default "" (current dir).  default temporary dir if not
                            saving data
        :return: SensorData object
        """
        return SensorDataPa(sensor_name, pa.Table.from_pydict(sensor_data), sensor_type, sample_rate_hz,
                            sample_interval_s, sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered,
                            calculate_stats, use_offset_model_for_correction, save_data, arrow_dir)

    def is_save_to_disk(self) -> bool:
        """
        :return: True if sensor will be saved to disk
        """
        return self._fs_writer.save_to_disk

    def set_save_to_disk(self, save: bool):
        """
        :param save: If True, save to disk
        """
        self._fs_writer.save_to_disk = save

    def set_file_name(self, new_file: Optional[str] = None):
        """
        set the pyarrow file name or use the default: {sensor_type}_{int(first_timestamp)}
        Do not give an extension

        :param new_file: optional file name to change to; default None (use default name)
        """
        self._fs_writer.file_name = new_file if new_file else f"{self._type.name}_{int(self.first_data_timestamp())}"

    def set_base_dir(self, new_dir: Optional[str] = None):
        """
        set the pyarrow directory or use the default: "." (current directory)

        :param new_dir: the directory to change to; default None (use current directory)
        """
        self._fs_writer.base_dir = new_dir if new_dir else "."

    def full_file_name(self) -> str:
        """
        :return: full name of parquet file containing the data
        """
        return self._fs_writer.full_name()

    def file_name(self) -> str:
        """
        :return: file name without extension
        """
        return self._fs_writer.file_name

    def base_dir(self) -> str:
        """
        :return: directory containing parquet files for the sensor
        """
        return self._fs_writer.save_dir()

    def full_path(self) -> str:
        """
        :return: the full path to the data file
        """
        return self._fs_writer.full_path()

    def fs_writer(self) -> Fsw:
        """
        :return: FileSystemWriter object
        """
        return self._fs_writer

    def pyarrow_ds(self, base_dir: Optional[str] = None) -> ds.Dataset:
        """
        :param base_dir: optional directory to use when loading the dataset.  if None, use self.base_dir()
        :return: the dataset stored in base_dir
        """
        if base_dir is None:
            base_dir = self.base_dir()
        return ds.dataset(base_dir, format="parquet", exclude_invalid_files=True)

    def pyarrow_table(self) -> pa.Table:
        """
        :return: the table defined by the dataset stored in self
        """
        return self._data if self._data else self.pyarrow_ds().to_table()

    def data_df(self) -> pd.DataFrame:
        """
        :return: the pandas dataframe defined by the dataset stored in self._arrow_dir
        """
        return self.pyarrow_table().to_pandas()

    def write_pyarrow_table(self, table: pa.Table):
        """
        saves the pyarrow table to disk or to memory.
        if writing to disk, uses a default filename: {sensor_type}_{first_timestamp}.parquet
        creates the directory if it doesn't exist and removes any existing parquet files

        :param table: the table to write
        """
        self._data = table
        # self._fs_writer.create_dir()
        # pq.write_table(table, self.full_path())

    def _actual_file_write_table(self):
        self._fs_writer.create_dir()
        pq.write_table(self._data, self.full_path())
        self._data = None

    def errors(self) -> RedVoxExceptions:
        """
        :return: errors of the sensor
        """
        return self._errors

    def gaps(self) -> List[Tuple]:
        """
        :return: start and end timestamps of gaps in data
        """
        return self._gaps

    def type(self) -> SensorType:
        """
        :return: type of sensor
        """
        return self._type

    def type_as_str(self) -> str:
        """
        gets the sensor type as a string

        :return: sensor type of the sensor as a string
        """
        return self._type.name

    def sample_rate_hz(self) -> float:
        """
        :return: sample rate in Hz
        """
        return self._sample_rate_hz

    def sample_interval_s(self) -> float:
        """
        :return: mean sample interval in seconds
        """
        return self._sample_interval_s

    def sample_interval_std_s(self) -> float:
        """
        :return: sample interval standard deviation in seconds
        """
        return self._sample_interval_std_s

    def is_sample_rate_fixed(self) -> bool:
        """
        :return: true if sample rate of sensor is constant
        """
        return self._is_sample_rate_fixed

    def is_timestamps_altered(self) -> bool:
        """
        :return: true if timestamps have been changed from original data values
        """
        return self._timestamps_altered

    def used_offset_model(self) -> bool:
        """
        :return: true if an offset model was used to perform timestamp corrections
        """
        return self._use_offset_model

    def sort_by_data_timestamps(self, ptable: pa.Table, ascending: bool = True):
        """
        sorts the data based on timestamps

        :param ptable: pyarrow table to sort
        :param ascending: if True, timestamps are sorted in ascending order, else sort by descending order
        """
        if ascending:
            order = "ascending"
        else:
            order = "descending"
        data = pc.take(ptable, pc.sort_indices(ptable, sort_keys=[("timestamps", order)]))
        # if not np.isnan(self.first_data_timestamp()) and self.first_data_timestamp() != data['timestamps'][0].as_py():
        #     os.remove(self.full_path())
        # self.set_file_name(f"{self._type.name}_{int(data['timestamps'][0].as_py())}")
        self.write_pyarrow_table(data)

    def organize_and_update_stats(self, ptable: pa.Table) -> "SensorDataPa":
        """
        sorts the data by timestamps, then if the sample rate is not fixed, recalculates the sample rate, interval,
            and interval std dev.  If there is only one value, sets the sample rate, interval, and interval std dev
            to np.nan.  Updates the SensorData object with the new values

        :param ptable: pyarrow table to update
        :return: updated version of self
        """
        self.sort_by_data_timestamps(ptable)
        if not self._is_sample_rate_fixed:
            if self.num_samples() > 1:
                timestamp_diffs = np.diff(self.data_timestamps())
                self._sample_interval_s = dtu.microseconds_to_seconds(
                    float(np.mean(timestamp_diffs))
                )
                self._sample_interval_std_s = dtu.microseconds_to_seconds(
                    float(np.std(timestamp_diffs))
                )
                self._sample_rate_hz = (
                    np.nan
                    if self.is_sample_interval_invalid()
                    else 1 / self._sample_interval_s
                )
            else:
                self._sample_interval_s = np.nan
                self._sample_interval_std_s = np.nan
                self._sample_rate_hz = np.nan
        return self

    def append_sensor(self, new_sensor: "SensorDataPa", recalculate_stats: bool = False) -> "SensorDataPa":
        """
        append the new data to the sensor, update the sensor's stats on demand if it doesn't have a fixed
            sample rate, then return the updated SensorData object

        :param new_sensor: sensor containing data to add to the calling sensor
        :param recalculate_stats: if True and the sensor does not have a fixed sample rate, sort the timestamps,
                                    recalculate the sample rate, interval, and interval std dev, default False
        :return: the updated SensorData object
        """
        _arrow: pa.Table = pa.concat_tables([self.pyarrow_table(), new_sensor.pyarrow_table()])
        if recalculate_stats and not self._is_sample_rate_fixed:
            self.organize_and_update_stats(_arrow)
        else:
            self.write_pyarrow_table(_arrow)
        return self

    def append_data(
            self, new_data: List[np.array], recalculate_stats: bool = False
    ) -> "SensorDataPa":
        """
        append the new data to the dataframe, update the sensor's stats on demand if it doesn't have a fixed
            sample rate, then return the updated SensorData object

        :param new_data: list of arrays containing data to add to the sensor's dataframe
        :param recalculate_stats: if True and the sensor does not have a fixed sample rate, sort the timestamps,
                                    recalculate the sample rate, interval, and interval std dev, default False
        :return: the updated SensorData object
        """
        _arrow = pa.concat_tables([self.pyarrow_table(),
                                   pa.Table.from_arrays(arrays=[pa.array(s) for s in new_data],
                                                        names=self.data_channels())])
        if recalculate_stats and not self._is_sample_rate_fixed:
            self.organize_and_update_stats(_arrow)
        else:
            self.write_pyarrow_table(_arrow)
        return self

    def is_sample_interval_invalid(self) -> bool:
        """
        :return: True if sample interval is np.nan or equal to 0.0
        """
        return np.isnan(self._sample_interval_s) or self._sample_interval_s == 0.0

    def data_timestamps(self) -> np.array:
        """
        :return: the timestamps as a numpy array or [np.nan] if none exist
        """
        if "timestamps" in self.pyarrow_table().schema.names:
            return self.pyarrow_table()["timestamps"].to_numpy()
        else:
            return np.array([np.nan])

    def unaltered_data_timestamps(self) -> np.array:
        """
        :return: the unaltered timestamps as a numpy array
        """
        if "unaltered_timestamps" in self.pyarrow_table().schema.names:
            return self.pyarrow_table()["unaltered_timestamps"].to_numpy()
        else:
            return np.array([np.nan])

    def first_data_timestamp(self) -> float:
        """
        :return: timestamp of the first data point or np.nan if no timestamps
        """
        return self.data_timestamps()[0]

    def last_data_timestamp(self) -> float:
        """
        :return: timestamp of the last data point or np.nan if no timestamps
        """
        return self.data_timestamps()[-1]

    def num_samples(self) -> int:
        """
        :return: the number of rows (samples) in the dataframe
        """
        if self.pyarrow_table():
            return self.pyarrow_table().num_rows
        return 0

    def samples(self) -> np.ndarray:
        """
        gets the non-timestamp samples of dataframe

        :return: the data values of the dataframe as a numpy ndarray
        """
        return self.data_df().iloc[:, 2:].T.to_numpy()

    def data_channels(self) -> List[str]:
        """
        :return: a list of the names of the columns (data channels) of the dataframe
        """
        return self.pyarrow_table().schema.names

    def get_data_channel(self, channel_name: str) -> Union[np.array, List[str]]:
        """
        gets the data channel specified, raises an error and lists valid fields if channel_name is not in the dataframe

        :param channel_name: the name of the channel to get data for
        :return: the data values of the channel as a numpy array or list of strings for enumerated channels
        """
        _arrow = self.pyarrow_table()
        if channel_name not in _arrow.schema.names:
            self._errors.append(f"WARNING: {channel_name} does not exist; try one of {_arrow.schema.names}")
            return []
        if channel_name == "location_provider":
            return [LocationProvider(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "image_codec":
            return [ImageCodec(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "audio_codec":
            return [AudioCodec(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "network_type":
            return [NetworkType(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "power_state":
            return [PowerState(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "cell_service":
            return [CellServiceState(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "wifi_wake_lock":
            return [WifiWakeLock(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "screen_state":
            return [ScreenState(c.as_py()).name for c in _arrow[channel_name]]
        return _arrow[channel_name].to_numpy()

    def _get_non_numeric_data_channel(self, channel_name: str) -> List[str]:
        """
        get_data_channel but specifically enumerated channels

        :param channel_name: the name of the channel to get data for
        :return: the data values of the channel as a list of strings
        """
        _arrow = self.pyarrow_table()
        if channel_name == "location_provider":
            return [LocationProvider(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "image_codec":
            return [ImageCodec(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "audio_codec":
            return [AudioCodec(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "network_type":
            return [NetworkType(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "power_state":
            return [PowerState(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "cell_service":
            return [CellServiceState(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "wifi_wake_lock":
            return [WifiWakeLock(c.as_py()).name for c in _arrow[channel_name]]
        elif channel_name == "screen_state":
            return [ScreenState(c.as_py()).name for c in _arrow[channel_name]]
        self._errors.append(f"WARNING: {channel_name} does not exist")
        return []

    def get_valid_data_channel_values(self, channel_name: str) -> np.array:
        """
        gets all non-nan values from the channel specified

        :param channel_name: the name of the channel to get data for
        :return: non-nan values of the channel as a numpy array
        """
        channel_data = self.get_data_channel(channel_name)
        return channel_data[~np.isnan(channel_data)]

    def _get_valid_non_numeric_data_channel_values(self, channel_name: str) -> List[str]:
        """
        NOT IMPLEMENTED
        return non-nan'd values; technically this evaluates an actual numeric channel first

        :param channel_name:
        :return:
        """
        pass

    def print_errors(self):
        """
        print all errors to screen
        """
        self._errors.print()

    def extend_errors(self, errors: RedVoxExceptions):
        """
        add errors to the SensorData's errors

        :param errors: errors to add
        """
        self._errors.extend_error(errors)

    def update_data_timestamps(self, offset_model: om.OffsetModel):
        """
        updates the timestamps of the data points

        :param offset_model: model used to update the timestamps
        """
        slope = dtu.seconds_to_microseconds(self._sample_interval_s) * (1 + offset_model.slope) \
            if self._use_offset_model else dtu.seconds_to_microseconds(self._sample_interval_s)
        if self._type == SensorType.AUDIO:
            # use the model to update the first timestamp or add the best offset (model's intercept value)
            timestamps = pa.array(
                calc_evenly_sampled_timestamps(
                    offset_model.update_time(self.first_data_timestamp(), self._use_offset_model),
                    self.num_samples(),
                    slope))
        else:
            timestamps = pa.array(offset_model.update_timestamps(self.data_timestamps(),
                                                                 self._use_offset_model))
        # old_name = self.full_path()
        self.write_pyarrow_table(self.pyarrow_table().set_column(0, "timestamps", timestamps))
        self.set_file_name()
        # os.rename(old_name, self.full_path())
        time_diffs = np.floor(np.diff(self.data_timestamps()))
        if len(time_diffs) > 1:
            self._sample_interval_s = dtu.microseconds_to_seconds(slope)
            if self._sample_interval_s > 0:
                self._sample_rate_hz = 1 / self._sample_interval_s
                self._sample_interval_std_s = dtu.microseconds_to_seconds(np.std(time_diffs))
        self._timestamps_altered = True

    def interpolate(self, interpolate_timestamp: float, first_point: int, second_point: int = 0,
                    copy: bool = True) -> pa.Table:
        """
        interpolates two points at the intercept value.  the two points must be consecutive in the dataframe.
        data channels that can't be interpolated are set to np.nan.

        :param interpolate_timestamp: timestamp to interpolate other values
        :param first_point: index of first point
        :param second_point: delta to second point, default 0 (same as first point)
        :param copy: if True, copies the values of the first point, default True
        :return: pyarrow Table of interpolated points
        """
        start_point = self.pyarrow_table().slice(first_point, 1).to_pydict()
        if not copy and second_point:
            i_p = {}
            end_point = self.pyarrow_table().slice(first_point + second_point, 1).to_pydict()
            first_closer = \
                np.abs(start_point[0] - interpolate_timestamp) \
                <= np.abs(end_point[0] - interpolate_timestamp)
            for col in self.pyarrow_table().schema.names:
                # process each column independently into new table object
                if col not in NON_INTERPOLATED_COLUMNS + NON_NUMERIC_COLUMNS:
                    numeric_diff = end_point[col] - start_point[col]
                    numeric_diff = \
                        (numeric_diff / numeric_diff["timestamps"]) * \
                        (interpolate_timestamp - start_point[col]) + start_point[col]
                    i_p[col] = numeric_diff
                elif col in NON_NUMERIC_COLUMNS:
                    if first_closer:
                        i_p[col] = start_point[col]
                    else:
                        i_p[col] = end_point[col]
        else:
            i_p = start_point
        i_p["timestamps"] = [interpolate_timestamp]
        return pa.Table.from_pydict(i_p)

    def as_dict(self) -> dict:
        """
        :return: sensor as dict
        """
        return {
            "name": self.name,
            "type": self._type.name,
            "num_samples": self.num_samples(),
            "sample_rate_hz": self._sample_rate_hz,
            "sample_interval_s": self._sample_interval_s,
            "sample_interval_std_s": self._sample_interval_std_s,
            "is_sample_rate_fixed": self._is_sample_rate_fixed,
            "timestamps_altered": self._timestamps_altered,
            "use_offset_model": self._use_offset_model,
            "gaps": self._gaps,
            "fs_writer": self._fs_writer.as_dict(),
            "errors": self._errors.as_dict()
        }

    def to_json(self) -> str:
        """
        :return: sensor as json string
        """
        return io.to_json(self)

    def to_json_file(self, file_name: Optional[str] = None) -> Path:
        """
        saves the sensor as json and data in the same directory.

        :param file_name: the optional base file name.  Do not include a file extension.
                            If None, a default file name is created using this format:
                            [sensor_type]_[first_timestamp].json
        :return: path to json file
        """
        if self._fs_writer.file_extension == "parquet":
            self._actual_file_write_table()
        return io.to_json_file(self, file_name)

    @staticmethod
    def from_json_file(file_dir: str, file_name: Optional[str] = None) -> "SensorDataPa":
        """
        convert contents of json file to SensorData

        :param file_dir: full path to containing directory for the file
        :param file_name: optional name of file and extension to load data from; if not specified, finds the first one
        :return: SensorData object
        """
        if file_name is None:
            file_name = io.get_json_file(file_dir)
            if file_name is None:
                result = SensorDataPa("Empty")
                result.append_error("File to load Sensor from not found.")
                return result
        json_data = io.from_json(os.path.join(file_dir, file_name))
        if "name" in json_data.keys():
            result = SensorDataPa.from_dir(json_data["name"], json_data["fs_writer"]["base_dir"],
                                           SensorType[json_data["type"]],
                                           json_data["sample_rate_hz"], json_data["sample_interval_s"],
                                           json_data["sample_interval_std_s"], json_data["is_sample_rate_fixed"],
                                           json_data["timestamps_altered"], False, json_data["use_offset_model"])
            result.set_errors(RedVoxExceptions.from_dict(json_data["errors"]))
            result.set_gaps(json_data["gaps"])
        else:
            result = SensorDataPa("Empty")
            result.append_error(f"Loading from {file_name} failed; Sensor missing name.")
        return result

    def class_from_type(self) -> "SensorDataPa":
        """
        Updates the class to be a specific type of sensor based on self._type

        :return: Self
        """
        if self._type == SensorType.AUDIO:
            self.__class__ = AudioSensor
        if self._type == SensorType.COMPRESSED_AUDIO:
            self.__class__ = CompressedAudioSensor
        if self._type == SensorType.IMAGE:
            self.__class__ = ImageSensor
        if self._type == SensorType.LOCATION:
            self.__class__ = LocationSensor
        if self._type == SensorType.BEST_LOCATION:
            self.__class__ = BestLocationSensor
        if self._type == SensorType.STATION_HEALTH:
            self.__class__ = StationHealthSensor
        if self._type == SensorType.LIGHT:
            self.__class__ = LightSensor
        if self._type == SensorType.PRESSURE:
            self.__class__ = PressureSensor
        if self._type == SensorType.PROXIMITY or self._type == SensorType.INFRARED:
            self.__class__ = ProximitySensor
        if self._type == SensorType.RELATIVE_HUMIDITY:
            self.__class__ = RelativeHumiditySensor
        if self._type == SensorType.AMBIENT_TEMPERATURE:
            self.__class__ = AmbientTemperatureSensor
        if self._type == SensorType.ACCELEROMETER:
            self.__class__ = AccelerometerSensor
        if self._type == SensorType.GYROSCOPE:
            self.__class__ = GyroscopeSensor
        if self._type == SensorType.MAGNETOMETER:
            self.__class__ = MagnetometerSensor
        if self._type == SensorType.ORIENTATION:
            self.__class__ = OrientationSensor
        if self._type == SensorType.GRAVITY:
            self.__class__ = GravitySensor
        if self._type == SensorType.LINEAR_ACCELERATION:
            self.__class__ = LinearAccelerationSensor
        if self._type == SensorType.ROTATION_VECTOR:
            self.__class__ = RotationVectorSensor
        return self

    def set_errors(self, errors: RedVoxExceptions):
        """
        sets the errors of the Sensor

        :param errors: errors to set
        """
        self._errors = errors

    def append_error(self, error: str):
        """
        add an error to the Sensor

        :param error: error to add
        """
        self._errors.append(error)

    def set_gaps(self, gaps: List[Tuple]):
        """
        sets the gaps of the Sensor

        :param gaps: gaps to set
        """
        self._gaps = gaps


class AudioSensor(SensorDataPa):
    """
    Audio specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.AUDIO, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_microphone_data(self) -> np.array:
        """
        :return: audio data as numpy array
        """
        return super().get_data_channel('microphone')

    def get_valid_microphone_data(self) -> np.array:
        """
        :return: non-nan audio data as numpy array
        """
        return super().get_valid_data_channel_values('microphone')


class CompressedAudioSensor(SensorDataPa):
    """
    Compressed audio specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.COMPRESSED_AUDIO, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_compressed_audio_data(self) -> np.array:
        """
        :return: compressed audio data as numpy array
        """
        return super().get_data_channel('compressed_audio')

    def get_valid_compressed_audio_data(self) -> np.array:
        """
        :return: non-nan compressed audio data as numpy array
        """
        return super().get_valid_data_channel_values('compressed_audio')

    def get_audio_codec_data(self) -> List[str]:
        """
        :return: audio codec as list of strings
        """
        return super()._get_non_numeric_data_channel('audio_codec')

    def _get_valid_audio_codec_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan audio codec as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('audio_codec')


class ImageSensor(SensorDataPa):
    """
    Image specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.IMAGE, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_image_data(self) -> np.array:
        """
        :return: image data as numpy array
        """
        return super().get_data_channel('image')

    def get_valid_image_data(self) -> np.array:
        """
        :return: non-nan image data as numpy array
        """
        return super().get_valid_data_channel_values('image')

    def get_image_codec_data(self) -> List[str]:
        """
        :return: image codec as list of strings
        """
        return super()._get_non_numeric_data_channel('image_codec')

    def get_valid_image_codec_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan image codec as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('image_codec')


class PressureSensor(SensorDataPa):
    """
    Pressure specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.PRESSURE, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_pressure_data(self) -> np.array:
        """
        :return: pressure data as numpy array
        """
        return super().get_data_channel('pressure')

    def get_valid_pressure_data(self) -> np.array:
        """
        :return: non-nan pressure data as numpy array
        """
        return super().get_valid_data_channel_values('pressure')


class LightSensor(SensorDataPa):
    """
    Light specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.LIGHT, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_light_data(self) -> np.array:
        """
        :return: light data as numpy array
        """
        return super().get_data_channel('light')

    def get_valid_light_data(self) -> np.array:
        """
        :return: non-nan light data as numpy array
        """
        return super().get_valid_data_channel_values('light')


class ProximitySensor(SensorDataPa):
    """
    Proximity specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.PROXIMITY, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_proximity_data(self) -> np.array:
        """
        :return: proximity data as numpy array
        """
        return super().get_data_channel('proximity')

    def get_valid_proximity_data(self) -> np.array:
        """
        :return: non-nan proximity data as numpy array
        """
        return super().get_valid_data_channel_values('proximity')


class AmbientTemperatureSensor(SensorDataPa):
    """
    Ambient temperature specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.AMBIENT_TEMPERATURE, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_ambient_temperature_data(self) -> np.array:
        """
        :return: ambient temperature data as numpy array
        """
        return super().get_data_channel('ambient_temperature')

    def get_valid_ambient_temperature_data(self) -> np.array:
        """
        :return: non-nan ambient temperature data as numpy array
        """
        return super().get_valid_data_channel_values('ambient_temperature')


class RelativeHumiditySensor(SensorDataPa):
    """
    Relative humidity specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.RELATIVE_HUMIDITY, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_relative_humidity_data(self) -> np.array:
        """
        :return: relative humidity data as numpy array
        """
        return super().get_data_channel('relative_humidity')

    def get_valid_relative_humidity_data(self) -> np.array:
        """
        :return: non-nan relative humidity data as numpy array
        """
        return super().get_valid_data_channel_values('relative_humidity')


class AccelerometerSensor(SensorDataPa):
    """
    Accelerometer specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.ACCELEROMETER, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_accelerometer_x_data(self) -> np.array:
        """
        :return: accelerometer x channel data as numpy array
        """
        return super().get_data_channel('accelerometer_x')

    def get_valid_accelerometer_x_data(self) -> np.array:
        """
        :return: non-nan accelerometer x channel data as numpy array
        """
        return super().get_valid_data_channel_values('accelerometer_x')

    def get_accelerometer_y_data(self) -> np.array:
        """
        :return: accelerometer y channel data as numpy array
        """
        return super().get_data_channel('accelerometer_y')

    def get_valid_accelerometer_y_data(self) -> np.array:
        """
        :return: non-nan accelerometer y channel data as numpy array
        """
        return super().get_valid_data_channel_values('accelerometer_y')

    def get_accelerometer_z_data(self) -> np.array:
        """
        :return: accelerometer z channel data as numpy array
        """
        return super().get_data_channel('accelerometer_z')

    def get_valid_accelerometer_z_data(self) -> np.array:
        """
        :return: non-nan accelerometer z channel data as numpy array
        """
        return super().get_valid_data_channel_values('accelerometer_z')


class MagnetometerSensor(SensorDataPa):
    """
    Magnetometer specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.MAGNETOMETER, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_magnetometer_x_data(self) -> np.array:
        """
        :return: magnetometer x channel data as numpy array
        """
        return super().get_data_channel('magnetometer_x')

    def get_valid_magnetometer_x_data(self) -> np.array:
        """
        :return: non-nan magnetometer x channel data as numpy array
        """
        return super().get_valid_data_channel_values('magnetometer_x')

    def get_magnetometer_y_data(self) -> np.array:
        """
        :return: magnetometer y channel data as numpy array
        """
        return super().get_data_channel('magnetometer_y')

    def get_valid_magnetometer_y_data(self) -> np.array:
        """
        :return: non-nan magnetometer y channel data as numpy array
        """
        return super().get_valid_data_channel_values('magnetometer_y')

    def get_magnetometer_z_data(self) -> np.array:
        """
        :return: magnetometer z channel data as numpy array
        """
        return super().get_data_channel('magnetometer_z')

    def get_valid_magnetometer_z_data(self) -> np.array:
        """
        :return: non-nan magnetometer z channel data as numpy array
        """
        return super().get_valid_data_channel_values('magnetometer_z')


class LinearAccelerationSensor(SensorDataPa):
    """
    Linear acceleration specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.LINEAR_ACCELERATION, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_linear_acceleration_x_data(self) -> np.array:
        """
        :return: linear acceleration x channel data as numpy array
        """
        return super().get_data_channel('linear_acceleration_x')

    def get_valid_linear_acceleration_x_data(self) -> np.array:
        """
        :return: non-nan linear acceleration x channel data as numpy array
        """
        return super().get_valid_data_channel_values('linear_acceleration_x')

    def get_linear_acceleration_y_data(self) -> np.array:
        """
        :return: linear acceleration y channel data as numpy array
        """
        return super().get_data_channel('linear_acceleration_y')

    def get_valid_linear_acceleration_y_data(self) -> np.array:
        """
        :return: non-nan linear acceleration y channel data as numpy array
        """
        return super().get_valid_data_channel_values('linear_acceleration_y')

    def get_linear_acceleration_z_data(self) -> np.array:
        """
        :return: linear acceleration z channel data as numpy array
        """
        return super().get_data_channel('linear_acceleration_z')

    def get_valid_linear_acceleration_z_data(self) -> np.array:
        """
        :return: non-nan linear acceleration z channel data as numpy array
        """
        return super().get_valid_data_channel_values('linear_acceleration_z')


class OrientationSensor(SensorDataPa):
    """
    Orientation specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.ORIENTATION, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_orientation_x_data(self) -> np.array:
        """
        :return: orientation x channel data as numpy array
        """
        return super().get_data_channel('orientation_x')

    def get_valid_orientation_x_data(self) -> np.array:
        """
        :return: non-nan orientation x channel data as numpy array
        """
        return super().get_valid_data_channel_values('orientation_x')

    def get_orientation_y_data(self) -> np.array:
        """
        :return: orientation y channel data as numpy array
        """
        return super().get_data_channel('orientation_y')

    def get_valid_orientation_y_data(self) -> np.array:
        """
        :return: non-nan orientation y channel data as numpy array
        """
        return super().get_valid_data_channel_values('orientation_y')

    def get_orientation_z_data(self) -> np.array:
        """
        :return: orientation z channel data as numpy array
        """
        return super().get_data_channel('orientation_z')

    def get_valid_orientation_z_data(self) -> np.array:
        """
        :return: non-nan orientation z channel data as numpy array
        """
        return super().get_valid_data_channel_values('orientation_z')


class RotationVectorSensor(SensorDataPa):
    """
    Rotation vector specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.ROTATION_VECTOR, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_rotation_vector_x_data(self) -> np.array:
        """
        :return: rotation vector x channel data as numpy array
        """
        return super().get_data_channel('rotation_vector_x')

    def get_valid_rotation_vector_x_data(self) -> np.array:
        """
        :return: non-nan rotation vector x channel data as numpy array
        """
        return super().get_valid_data_channel_values('rotation_vector_x')

    def get_rotation_vector_y_data(self) -> np.array:
        """
        :return: rotation vector y channel data as numpy array
        """
        return super().get_data_channel('rotation_vector_y')

    def get_valid_rotation_vector_y_data(self) -> np.array:
        """
        :return: non-nan rotation vector y channel data as numpy array
        """
        return super().get_valid_data_channel_values('rotation_vector_y')

    def get_rotation_vector_z_data(self) -> np.array:
        """
        :return: rotation vector z channel data as numpy array
        """
        return super().get_data_channel('rotation_vector_z')

    def get_valid_rotation_vector_z_data(self) -> np.array:
        """
        :return: non-nan rotation vector z channel data as numpy array
        """
        return super().get_valid_data_channel_values('rotation_vector_z')


class GyroscopeSensor(SensorDataPa):
    """
    Gyroscope specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.GYROSCOPE, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_gyroscope_x_data(self) -> np.array:
        """
        :return: gyroscope x channel data as numpy array
        """
        return super().get_data_channel('gyroscope_x')

    def get_valid_gyroscope_x_data(self) -> np.array:
        """
        :return: non-nan gyroscope x channel data as numpy array
        """
        return super().get_valid_data_channel_values('gyroscope_x')

    def get_gyroscope_y_data(self) -> np.array:
        """
        :return: gyroscope y channel data as numpy array
        """
        return super().get_data_channel('gyroscope_y')

    def get_valid_gyroscope_y_data(self) -> np.array:
        """
        :return: non-nan gyroscope y channel data as numpy array
        """
        return super().get_valid_data_channel_values('gyroscope_y')

    def get_gyroscope_z_data(self) -> np.array:
        """
        :return: gyroscope z channel data as numpy array
        """
        return super().get_data_channel('gyroscope_z')

    def get_valid_gyroscope_z_data(self) -> np.array:
        """
        :return: non-nan gyroscope z channel data as numpy array
        """
        return super().get_valid_data_channel_values('gyroscope_z')


class GravitySensor(SensorDataPa):
    """
    Gravity specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.GRAVITY, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_gravity_x_data(self) -> np.array:
        """
        :return: gravity x channel data as numpy array
        """
        return super().get_data_channel('gravity_x')

    def get_valid_gravity_x_data(self) -> np.array:
        """
        :return: non-nan gravity x channel data as numpy array
        """
        return super().get_valid_data_channel_values('gravity_x')

    def get_gravity_y_data(self) -> np.array:
        """
        :return: gravity y channel data as numpy array
        """
        return super().get_data_channel('gravity_y')

    def get_valid_gravity_y_data(self) -> np.array:
        """
        :return: non-nan gravity y channel data as numpy array
        """
        return super().get_valid_data_channel_values('gravity_y')

    def get_gravity_z_data(self) -> np.array:
        """
        :return: gravity z channel data as numpy array
        """
        return super().get_data_channel('gravity_z')

    def get_valid_gravity_z_data(self) -> np.array:
        """
        :return: non-nan gravity z channel data as numpy array
        """
        return super().get_valid_data_channel_values('gravity_z')


class LocationSensor(SensorDataPa):
    """
    Location specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.LOCATION, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_gps_timestamps_data(self) -> np.array:
        """
        :return: gps timestamps as numpy array
        """
        return super().get_data_channel('gps_timestamps')

    def get_valid_gps_timestamps_data(self) -> np.array:
        """
        :return: non-nan gps timestamps as numpy array
        """
        return super().get_valid_data_channel_values('gps_timestamps')

    def get_latitude_data(self) -> np.array:
        """
        :return: latitude data as numpy array
        """
        return super().get_data_channel('latitude')

    def get_valid_latitude_data(self) -> np.array:
        """
        :return: non-nan latitude data as numpy array
        """
        return super().get_valid_data_channel_values('latitude')

    def get_longitude_data(self) -> np.array:
        """
        :return: longitude data as numpy array
        """
        return super().get_data_channel('longitude')

    def get_valid_longitude_data(self) -> np.array:
        """
        :return: non-nan longitude data as numpy array
        """
        return super().get_valid_data_channel_values('longitude')

    def get_altitude_data(self) -> np.array:
        """
        :return: altitude data as numpy array
        """
        return super().get_data_channel('altitude')

    def get_valid_altitude_data(self) -> np.array:
        """
        :return: non-nan altitude data as numpy array
        """
        return super().get_valid_data_channel_values('altitude')

    def get_speed_data(self) -> np.array:
        """
        :return: speed data as numpy array
        """
        return super().get_data_channel('speed')

    def get_valid_speed_data(self) -> np.array:
        """
        :return: non-nan speed data as numpy array
        """
        return super().get_valid_data_channel_values('speed')

    def get_bearing_data(self) -> np.array:
        """
        :return: bearing data as numpy array
        """
        return super().get_data_channel('bearing')

    def get_valid_bearing_data(self) -> np.array:
        """
        :return: non-nan bearing data as numpy array
        """
        return super().get_valid_data_channel_values('bearing')

    def get_horizontal_accuracy_data(self) -> np.array:
        """
        :return: horizontal accuracy data as numpy array
        """
        return super().get_data_channel('horizontal_accuracy')

    def get_valid_horizontal_accuracy_data(self) -> np.array:
        """
        :return: non-nan horizontal accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('horizontal_accuracy')

    def get_vertical_accuracy_data(self) -> np.array:
        """
        :return: vertical accuracy data as numpy array
        """
        return super().get_data_channel('vertical_accuracy')

    def get_valid_vertical_accuracy_data(self) -> np.array:
        """
        :return: non-nan vertical accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('vertical_accuracy')

    def get_speed_accuracy_data(self) -> np.array:
        """
        :return: speed accuracy data as numpy array
        """
        return super().get_data_channel('speed_accuracy')

    def get_valid_speed_accuracy_data(self) -> np.array:
        """
        :return: non-nan speed accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('speed_accuracy')

    def get_bearing_accuracy_data(self) -> np.array:
        """
        :return: bearing accuracy data as numpy array
        """
        return super().get_data_channel('bearing_accuracy')

    def get_valid_bearing_accuracy_data(self) -> np.array:
        """
        :return: non-nan bearing accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('bearing_accuracy')

    def get_location_provider_data(self) -> List[str]:
        """
        :return: location provider data as list of strings
        """
        return super()._get_non_numeric_data_channel('location_provider')

    def get_valid_location_provider_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan location provider data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('location_provider')


class BestLocationSensor(SensorDataPa):
    """
    Best-location specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.BEST_LOCATION, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_gps_timestamps_data(self) -> np.array:
        """
        :return: gps timestamps as numpy array
        """
        return super().get_data_channel('gps_timestamps')

    def get_valid_gps_timestamps_data(self) -> np.array:
        """
        :return: non-nan gps timestamps as numpy array
        """
        return super().get_valid_data_channel_values('gps_timestamps')

    def get_latitude_data(self) -> np.array:
        """
        :return: latitude data as numpy array
        """
        return super().get_data_channel('latitude')

    def get_valid_latitude_data(self) -> np.array:
        """
        :return: non-nan latitude data as numpy array
        """
        return super().get_valid_data_channel_values('latitude')

    def get_longitude_data(self) -> np.array:
        """
        :return: longitude data as numpy array
        """
        return super().get_data_channel('longitude')

    def get_valid_longitude_data(self) -> np.array:
        """
        :return: non-nan longitude data as numpy array
        """
        return super().get_valid_data_channel_values('longitude')

    def get_altitude_data(self) -> np.array:
        """
        :return: altitude data as numpy array
        """
        return super().get_data_channel('altitude')

    def get_valid_altitude_data(self) -> np.array:
        """
        :return: non-nan altitude data as numpy array
        """
        return super().get_valid_data_channel_values('altitude')

    def get_speed_data(self) -> np.array:
        """
        :return: speed data as numpy array
        """
        return super().get_data_channel('speed')

    def get_valid_speed_data(self) -> np.array:
        """
        :return: non-nan speed data as numpy array
        """
        return super().get_valid_data_channel_values('speed')

    def get_bearing_data(self) -> np.array:
        """
        :return: bearing data as numpy array
        """
        return super().get_data_channel('bearing')

    def get_valid_bearing_data(self) -> np.array:
        """
        :return: non-nan bearing data as numpy array
        """
        return super().get_valid_data_channel_values('bearing')

    def get_horizontal_accuracy_data(self) -> np.array:
        """
        :return: horizontal accuracy data as numpy array
        """
        return super().get_data_channel('horizontal_accuracy')

    def get_valid_horizontal_accuracy_data(self) -> np.array:
        """
        :return: non-nan horizontal accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('horizontal_accuracy')

    def get_vertical_accuracy_data(self) -> np.array:
        """
        :return: vertical accuracy data as numpy array
        """
        return super().get_data_channel('vertical_accuracy')

    def get_valid_vertical_accuracy_data(self) -> np.array:
        """
        :return: non-nan vertical accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('vertical_accuracy')

    def get_speed_accuracy_data(self) -> np.array:
        """
        :return: speed accuracy data as numpy array
        """
        return super().get_data_channel('speed_accuracy')

    def get_valid_speed_accuracy_data(self) -> np.array:
        """
        :return: non-nan speed accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('speed_accuracy')

    def get_bearing_accuracy_data(self) -> np.array:
        """
        :return: bearing accuracy data as numpy array
        """
        return super().get_data_channel('bearing_accuracy')

    def get_valid_bearing_accuracy_data(self) -> np.array:
        """
        :return: non-nan bearing accuracy data as numpy array
        """
        return super().get_valid_data_channel_values('bearing_accuracy')

    def get_location_provider_data(self) -> List[str]:
        """
        :return: location provider data as list of strings
        """
        return super()._get_non_numeric_data_channel('location_provider')

    def get_valid_location_provider_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan location provider data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('location_provider')


class StationHealthSensor(SensorDataPa):
    """
    Station-health specific functions
    """
    def __init__(self, sensor_name: str,
                 sensor_data: Optional[pa.Table] = None,
                 sample_rate_hz: float = np.nan,
                 sample_interval_s: float = np.nan,
                 sample_interval_std_s: float = np.nan,
                 is_sample_rate_fixed: bool = False,
                 are_timestamps_altered: bool = False,
                 calculate_stats: bool = False,
                 use_offset_model_for_correction: bool = False,
                 save_data: bool = False,
                 base_dir: str = ".",
                 gaps: Optional[List[Tuple[float, float]]] = None,
                 show_errors: bool = False):
        super().__init__(sensor_name, sensor_data, SensorType.STATION_HEALTH, sample_rate_hz, sample_interval_s,
                         sample_interval_std_s, is_sample_rate_fixed, are_timestamps_altered, calculate_stats,
                         use_offset_model_for_correction, save_data, base_dir, gaps, show_errors)

    def get_battery_charge_remaining_data(self) -> np.array:
        """
        :return: battery charge remaining data as numpy array
        """
        return super().get_data_channel('battery_charge_remaining')

    def get_valid_battery_charge_remaining_data(self) -> np.array:
        """
        :return: non-nan battery charge remaining data as numpy array
        """
        return super().get_valid_data_channel_values('battery_charge_remaining')

    def get_battery_current_strength_data(self) -> np.array:
        """
        :return: battery current strength data as numpy array
        """
        return super().get_data_channel('battery_current_strength')

    def get_valid_battery_current_strength_data(self) -> np.array:
        """
        :return: non-nan battery current strength data as numpy array
        """
        return super().get_valid_data_channel_values('battery_current_strength')

    def get_internal_temp_c_data(self) -> np.array:
        """
        :return: internal temperature celsius data as numpy array
        """
        return super().get_data_channel('internal_temp_c')

    def get_valid_internal_temp_c_data(self) -> np.array:
        """
        :return: non-nan internal temperature celsius data as numpy array
        """
        return super().get_valid_data_channel_values('internal_temp_c')

    def get_network_type_data(self) -> List[str]:
        """
        :return: network type data as list of strings
        """
        return super()._get_non_numeric_data_channel('network_type')

    def get_valid_network_type_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan network type data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('network_type')

    def get_network_strength_data(self) -> np.array:
        """
        :return: network strength data as numpy array
        """
        return super().get_data_channel('network_strength')

    def get_valid_network_strength_data(self) -> np.array:
        """
        :return: non-nan network strength data as numpy array
        """
        return super().get_valid_data_channel_values('network_strength')

    def get_power_state_data(self) -> List[str]:
        """
        :return: power state data as list of strings
        """
        return super()._get_non_numeric_data_channel('power_state')

    def get_valid_power_state_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan power state data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('power_state')

    def get_avail_ram_data(self) -> np.array:
        """
        :return: available RAM data as numpy array
        """
        return super().get_data_channel('avail_ram')

    def get_valid_avail_ram_data(self) -> np.array:
        """
        :return: non-nan available RAM data as numpy array
        """
        return super().get_valid_data_channel_values('avail_ram')

    def get_avail_disk_data(self) -> np.array:
        """
        :return: available disk space data as numpy array
        """
        return super().get_data_channel('avail_disk')

    def get_valid_avail_disk_data(self) -> np.array:
        """
        :return: non-nan available disk space data as numpy array
        """
        return super().get_valid_data_channel_values('avail_disk')

    def get_cell_service_data(self) -> List[str]:
        """
        :return: cell service data as list of strings
        """
        return super()._get_non_numeric_data_channel('cell_service')

    def get_valid_cell_service_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan cell service data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('cell_service')

    def get_cpu_utilization_data(self) -> np.array:
        """
        :return: CPU utilization data as numpy array
        """
        return super().get_data_channel('cpu_utilization')

    def get_valid_cpu_utilization_data(self) -> np.array:
        """
        :return: non-nan CPU utilization data as numpy array
        """
        return super().get_valid_data_channel_values('cpu_utilization')

    def get_wifi_wake_lock_data(self) -> List[str]:
        """
        :return: wifi wake lock data as list of strings
        """
        return super()._get_non_numeric_data_channel('wifi_wake_lock')

    def get_valid_wifi_wake_lock_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan wifi wake lock data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('wifi_wake_lock')

    def get_screen_state_data(self) -> List[str]:
        """
        :return: screen state data as list of strings
        """
        return super()._get_non_numeric_data_channel('screen_state')

    def get_valid_screen_state_data(self) -> List[str]:
        """
        NOT IMPLEMENTED
        :return: non-nan screen state data as list of strings
        """
        pass
        # return super().get_valid_data_channel_values('screen_state')

    def get_screen_brightness_data(self) -> np.array:
        """
        :return: screen brightness data as numpy array
        """
        return super().get_data_channel('screen_brightness')

    def get_valid_screen_brightness_data(self) -> np.array:
        """
        :return: non-nan screen brightness data as numpy array
        """
        return super().get_valid_data_channel_values('screen_brightness')
