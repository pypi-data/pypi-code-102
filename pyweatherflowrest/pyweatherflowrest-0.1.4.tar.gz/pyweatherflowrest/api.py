"""WeatherFlow Data Wrapper."""
from __future__ import annotations

import aiohttp
from aiohttp import client_exceptions
import logging
from typing import Optional

from pyweatherflowrest.const import (
    DEVICE_TYPE_AIR,
    DEVICE_TYPE_HUB,
    DEVICE_TYPE_SKY,
    DEVICE_TYPE_TEMPEST,
    UNIT_TYPE_METRIC,
    VALID_UNIT_TYPES,
    WEATHERFLOW_DEVICE_BASE_URL,
    WEATHERFLOW_FORECAST_BASE_URL,
    WEATHERFLOW_OBSERVATION_BASE_URL,
    WEATHERFLOW_STATIONS_BASE_URL,
)
from pyweatherflowrest.data import (
    ObservationDescription,
    StationDescription,
    ForecastDescription,
    ForecastDailyDescription,
    ForecastHourlyDescription,
)
from pyweatherflowrest.exceptions import  Invalid,  BadRequest, WrongStationID, NotAuthorized
from pyweatherflowrest.helpers import Conversions, Calculations

_LOGGER = logging.getLogger(__name__)

class WeatherFlowApiClient:

    req: aiohttp.ClientSession

    def __init__ (
        self,
        station_id: int,
        api_token: str,
        units: Optional[str] = UNIT_TYPE_METRIC,
        homeassistant: Optional(bool) = True,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.station_id = station_id
        self.api_token = api_token
        self.units = units
        self.homeassistant = homeassistant

        if self.units not in VALID_UNIT_TYPES:
            self.units = UNIT_TYPE_METRIC

        if session is None:
            session = aiohttp.ClientSession()
        self.req = session
        self.cnv = Conversions(self.units, self.homeassistant)
        self.calc = Calculations()

        self._station_data: StationDescription = None
        self._observation_data: ObservationDescription = None
        self._device_id = None
        self._is_metric = self.units is UNIT_TYPE_METRIC

    @property
    def station_data(self) -> StationDescription:
        """Returns Station Data."""
        return self._station_data

    @property
    def device_url(self) -> str:
        """Rest Url for device data."""
        return f"{WEATHERFLOW_DEVICE_BASE_URL}{self._device_id}?token={self.api_token}"

    @property
    def observation_url(self) -> str:
        """Rest Url for observation data."""
        return f"{WEATHERFLOW_OBSERVATION_BASE_URL}{self.station_id}?token={self.api_token}"

    @property
    def forecast_url(self) -> str:
        """Rest Url for forecast Data."""
        return f"{WEATHERFLOW_FORECAST_BASE_URL}{self.station_id}&token={self.api_token}"

    @property
    def station_url(self) -> str:
        """Base Rest Url for station Data"""
        return f"{WEATHERFLOW_STATIONS_BASE_URL}{self.station_id}?token={self.api_token}"

    async def initialize(self) -> None:
        """Initialize data tables."""

        data = await self._api_request(self.station_url)

        if data is not None:
            if data["status"]["status_code"] == 404:
                raise WrongStationID(f"Station ID {self.station_id} does not exist") from None
            if data["status"]["status_code"] == 401:
                raise NotAuthorized(f"Token {self.api_token} is invalid") from None
            if data["stations"] == []:
                raise Invalid(f"The data returned from Station ID {self.station_id} is invalid") from None

            station = data["stations"][0]
            entity_data = StationDescription(
                key=self.station_id,
                name=station["name"],
                public_name=station["public_name"],
                latitude=station["latitude"],
                longitude=station["longitude"],
                timezone=station["timezone"],
                elevation=station["station_meta"]["elevation"],
            )
            for device in station["devices"]:
                if device["device_type"] == "HB":
                    entity_data.hub_device_id = device["device_id"]
                    entity_data.hub_device_type=DEVICE_TYPE_HUB
                    entity_data.hub_hardware_revision = device["hardware_revision"]
                    entity_data.hub_firmware_revision = device["firmware_revision"]
                    entity_data.hub_serial_number = device["serial_number"]
                if device["device_type"] == "ST":
                    entity_data.tempest_device_id = device["device_id"]
                    entity_data.tempest_device_type=DEVICE_TYPE_TEMPEST
                    entity_data.tempest_hardware_revision = device["hardware_revision"]
                    entity_data.tempest_firmware_revision = device["firmware_revision"]
                    entity_data.tempest_serial_number = device["serial_number"]
                    entity_data.is_tempest = True
                if device["device_type"] == "AR":
                    entity_data.air_device_id = device["device_id"]
                    entity_data.air_device_type=DEVICE_TYPE_AIR
                    entity_data.air_hardware_revision = device["hardware_revision"]
                    entity_data.air_firmware_revision = device["firmware_revision"]
                    entity_data.air_serial_number = device["serial_number"]
                if device["device_type"] == "SK":
                    entity_data.sky_device_id = device["device_id"]
                    entity_data.sky_device_type=DEVICE_TYPE_SKY
                    entity_data.sky_hardware_revision = device["hardware_revision"]
                    entity_data.sky_firmware_revision = device["firmware_revision"]
                    entity_data.sky_serial_number = device["serial_number"]

            self._station_data = entity_data


    async def _read_device_data(self) -> None:
        """Update observation data."""

        if self._station_data.is_tempest:
            self._device_id = self._station_data.tempest_device_id
            voltage_index = 16
            data = await self._api_request(self.device_url)
            if data is not None:
                device = data["obs"][0]
                self._observation_data.voltage_tempest = device[voltage_index]
                self._observation_data.battery_tempest = self.calc.battery_percent(self._station_data.is_tempest, device[voltage_index])
        else:
            self._device_id = self._station_data.air_device_id
            voltage_index = 6
            data = await self._api_request(self.device_url)
            if data is not None:
                device = data["obs"][0]
                self._observation_data.voltage_air = device[voltage_index]
                self._observation_data.battery_air = self.calc.battery_percent(self._station_data.is_tempest, device[voltage_index])

            self._device_id = self._station_data.sky_device_id
            voltage_index = 8
            data = await self._api_request(self.device_url)
            if data is not None:
                device = data["obs"][0]
                self._observation_data.voltage_sky = device[voltage_index]
                self._observation_data.battery_sky = self.calc.battery_percent(self._station_data.is_tempest, device[voltage_index])

    async def update_observations(self) -> None:
        """Update observation data."""
        if self._station_data is None:
            return

        data = await self._api_request(self.observation_url)
        if data is not None:
            obervations = data['obs'][0]
            visibility = self.calc.visibility(
                self._station_data.elevation,
                obervations["air_temperature"],
                obervations["relative_humidity"],
                obervations["dew_point"]
            )
            entity_data = ObservationDescription(
                key=self.station_id,
                utc_time=self.cnv.utc_from_timestamp(obervations["timestamp"]),
                air_temperature=self.cnv.temperature(obervations["air_temperature"]),
                barometric_pressure=self.cnv.pressure(obervations["barometric_pressure"]),
                station_pressure=self.cnv.pressure(obervations["station_pressure"]),
                sea_level_pressure=self.cnv.pressure(obervations["sea_level_pressure"]),
                relative_humidity=obervations["relative_humidity"],
                precip=self.cnv.rain(obervations["precip"]),
                precip_rate=self.cnv.rain_rate(obervations["precip"]),
                precip_accum_last_1hr=self.cnv.rain(obervations["precip_accum_last_1hr"]),
                precip_accum_local_day=self.cnv.rain(obervations["precip_accum_local_day"]),
                precip_accum_local_yesterday=self.cnv.rain(obervations["precip_accum_local_yesterday"]),
                precip_minutes_local_day=obervations["precip_minutes_local_day"],
                precip_minutes_local_yesterday=obervations["precip_minutes_local_yesterday"],
                wind_avg=self.cnv.windspeed(obervations["wind_avg"]),
                wind_direction=obervations["wind_direction"],
                wind_gust=self.cnv.windspeed(obervations["wind_gust"]),
                wind_lull=self.cnv.windspeed(obervations["wind_lull"]),
                solar_radiation=obervations["solar_radiation"],
                uv=obervations["uv"],
                brightness=obervations["brightness"],
                lightning_strike_last_epoch=self.cnv.utc_from_timestamp(obervations["lightning_strike_last_epoch"]),
                lightning_strike_last_distance=self.cnv.distance(obervations["lightning_strike_last_distance"]),
                lightning_strike_count=obervations["lightning_strike_count"],
                lightning_strike_count_last_1hr=obervations["lightning_strike_count_last_1hr"],
                lightning_strike_count_last_3hr=obervations["lightning_strike_count_last_3hr"],
                feels_like=self.cnv.temperature(obervations["feels_like"]),
                heat_index=self.cnv.temperature(obervations["heat_index"]),
                wind_chill=self.cnv.temperature(obervations["wind_chill"]),
                dew_point=self.cnv.temperature(obervations["dew_point"]),
                wet_bulb_temperature=self.cnv.temperature(obervations["wet_bulb_temperature"]),
                delta_t=obervations["delta_t"],
                air_density=obervations["air_density"],
                pressure_trend=obervations["pressure_trend"],
                is_raining=self.calc.is_raining(obervations["precip"]),
                is_freezing=self.calc.is_freezing(obervations["air_temperature"]),
                visibility=self.cnv.distance(visibility),
                absolute_humidity=self.calc.absolute_humidity(obervations["air_temperature"], obervations["relative_humidity"]),
                beaufort=self.calc.beaufort(obervations["wind_avg"]),
            )
            self._observation_data = entity_data
            await self._read_device_data()

            return entity_data

        return None


    async def update_forecast(self) -> None:
        """Update forecast data."""
        if self._station_data is None:
            return

        data = await self._api_request(self.forecast_url)
        if data is not None:
            current = data['current_conditions']
            entity_data = ForecastDescription(
                key=self.station_id,
                utc_time=self.cnv.utc_from_timestamp(current["time"]),
                conditions=current["conditions"],
                icon=current["icon"],
                air_temperature=self.cnv.temperature(current["air_temperature"]),
                station_pressure=self.cnv.pressure(current["station_pressure"]),
                sea_level_pressure=self.cnv.pressure(current["sea_level_pressure"]),
                pressure_trend=current["pressure_trend"],
                relative_humidity=current["relative_humidity"],
                wind_avg=self.cnv.windspeed(current["wind_avg"], self.homeassistant),
                wind_direction=current["wind_direction"],
                wind_direction_cardinal=current["wind_direction_cardinal"],
                wind_gust=self.cnv.windspeed(current["wind_gust"], self.homeassistant),
                solar_radiation=current["solar_radiation"],
                uv=current["uv"],
                brightness=current["brightness"],
                feels_like=self.cnv.temperature(current["feels_like"]),
                dew_point=self.cnv.temperature(current["dew_point"]),
                wet_bulb_temperature=self.cnv.temperature(current["wet_bulb_temperature"]),
                delta_t=current["delta_t"],
                air_density=self.cnv.density(current["air_density"]),
                lightning_strike_count_last_1hr=current["lightning_strike_count_last_1hr"],
                lightning_strike_count_last_3hr=current["lightning_strike_count_last_3hr"],
                lightning_strike_last_distance=current["lightning_strike_last_distance"],
                lightning_strike_last_distance_msg=current["lightning_strike_last_distance_msg"],
                lightning_strike_last_epoch=self.cnv.utc_from_timestamp(current["lightning_strike_last_epoch"]),
                precip_accum_local_day=self.cnv.rain(current["precip_accum_local_day"]),
                precip_accum_local_yesterday=self.cnv.rain(current["precip_accum_local_yesterday"]),
                precip_minutes_local_day=current["precip_minutes_local_day"],
                precip_minutes_local_yesterday=current["precip_minutes_local_yesterday"],
            )

            forecast_daily = data["forecast"]["daily"]

            entity_data.temp_high_today = forecast_daily[0]["air_temp_high"]          
            entity_data.temp_low_today = forecast_daily[0]["air_temp_low"]          

            for item in forecast_daily:
                calc_values = self.calc.day_forecast_extras(item, data["forecast"]["hourly"])
                day_item = ForecastDailyDescription(
                    utc_time = self.cnv.utc_from_timestamp(item["day_start_local"]),
                    conditions = item["conditions"],
                    icon=item["icon"],
                    sunrise=item["sunrise"],
                    sunset=item["sunset"],
                    air_temp_high=self.cnv.temperature(item["air_temp_high"]),
                    air_temp_low=self.cnv.temperature(item["air_temp_low"]),
                    precip=self.cnv.rain(calc_values["precip"]),
                    precip_probability=item["precip_probability"],
                    precip_icon=item["precip_icon"],
                    precip_type=item["precip_type"],
                    wind_avg=self.cnv.windspeed(calc_values["wind_avg"], self.homeassistant),
                    wind_direction=calc_values["wind_direction"],
                )
                entity_data.forecast_daily.append(day_item)

            forecast_hourly = data["forecast"]["hourly"]            
            for item in forecast_hourly:
                hour_item = ForecastHourlyDescription(
                    utc_time = self.cnv.utc_from_timestamp(item["time"]),
                    conditions = item["conditions"],
                    icon=item["icon"],
                    air_temperature=self.cnv.temperature(item["air_temperature"]),
                    sea_level_pressure=self.cnv.pressure(item["sea_level_pressure"]),
                    relative_humidity=item["relative_humidity"],
                    precip=self.cnv.rain(item["precip"]),
                    precip_probability=item["precip_probability"],
                    wind_avg=self.cnv.windspeed(item["wind_avg"], self.homeassistant),
                    wind_direction=item["wind_direction"],
                    wind_direction_cardinal=item["wind_direction_cardinal"],
                    wind_gust=self.cnv.windspeed(item["wind_gust"], self.homeassistant),
                    uv=item["uv"],
                    feels_like=self.cnv.temperature(item["feels_like"]),
                )
                entity_data.forecast_hourly.append(hour_item)
            
            return entity_data

        return None

    async def load_unit_system(self) -> None:
        """Returns unit of meassurement based on unit system"""
        density_unit = "kg/m^3" if self._is_metric else "lb/ft^3"
        distance_unit = "km" if self._is_metric else "mi"
        length_unit = "m/s" if self._is_metric else "mi/h"
        length_km_unit = "km/h" if self._is_metric else "mi/h"
        pressure_unit = "hPa" if self._is_metric else "inHg"
        precip_unit = "mm" if self._is_metric else "in"

        units_list = {
            "none": None,
            "density": density_unit,
            "distance": distance_unit,
            "length": length_unit,
            "length_km": length_km_unit,
            "pressure": pressure_unit,
            "precipitation": precip_unit,
            "precipitation_rate": f"{precip_unit}/h",
        }

        return units_list

    async def _api_request(
        self,
        url: str
        ) -> None:
        """Get data from WeatherFlow API."""

        try:
            async with self.req.get(url) as resp:
                data = await resp.json()
                return data

        except client_exceptions.ClientError as err:
            raise BadRequest(f"Error requesting data from WeatherFlow: {err}") from None
