"""Helper Class for Weatherflow Rest module."""
from __future__ import annotations

import datetime
import logging
import math
import pytz

from pyweatherflowrest.const import UNIT_TYPE_METRIC

UTC = pytz.utc

_LOGGER = logging.getLogger(__name__)

class Conversions:
    """Converts values from metric."""
    def __init__(self, units: str, homeassistant: bool) -> None:
        self.units = units
        self.homeassistant = homeassistant

    def temperature(self, value) -> float:
        """Returns celcius to Fahrenheit."""
        if value is None or self.units == UNIT_TYPE_METRIC or self.homeassistant:
            return value
        return round(value * 1.8 + 32, 1)

    def pressure(self, value) -> float:
        """Returns inHg from mb/hPa."""
        if value is None or self.units == UNIT_TYPE_METRIC:
            return value
        return round(value * 0.029530, 1)

    def rain(self, value) -> float:
        """Converts rain units."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 2)
        return round(value * 0.03937007874, 2)

    def rain_rate(self, value) -> float:
        """Calculates Rain Rate."""
        if value is None:
            return None

        _rain_rate = value * 60

        return self.rain(_rain_rate)

    def density(self, value) -> float:
        """Converts air density."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.06243, 1)

    def distance(self, value) -> float:
        """Conerts km to mi."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value,1)

        return round(value * 0.6213688756, 1)
        
    def windspeed(self, value, wind_unit_kmh: bool = False) -> float:
        """Returns miles per hour from m/s."""
        if value is None:
            return value
        
        if self.units == UNIT_TYPE_METRIC:
            if wind_unit_kmh:
                return round(value * 3.6, 1)
            return round(value, 1)

        return round(value * 2.236936292, 1)

    def utc_from_timestamp(self, timestamp: int) -> datetime.datetime:
        """Return a UTC time from a timestamp."""
        return UTC.localize(datetime.datetime.utcfromtimestamp(timestamp))

class Calculations:
    """Calculate entity values."""

    def is_raining(self, rain):
        """Returns true if it is raining."""
        if rain is None:
            return None
            
        rain_rate = rain * 60
        return rain_rate > 0

    def is_freezing(self, temperature):
        """Returns true if temperature below 0."""
        if temperature is None:
            return None
            
        return temperature < 0

    def day_forecast_extras(self, day_data, hour_data) -> float:
        """Returns accumulated precip for the day."""
        _precip = 0
        _wind_avg =[]
        _wind_bearing=[]

        for item in hour_data:
            if item["local_day"] == day_data["day_num"]:
                _precip += item["precip"]
                _wind_avg.append(item["wind_avg"])
                _wind_bearing.append(item["wind_direction"])
        
        _sum_wind_avg = sum(_wind_avg) / len(_wind_avg)
        _sum_wind_bearing = sum(_wind_bearing) / len(_wind_bearing)

        return {"precip": round(_precip, 1), "wind_avg": round(_sum_wind_avg, 1), "wind_direction": int(_sum_wind_bearing)}

    def visibility(self, elevation, air_temperature, relative_humidity, dewpoint) -> float:
        """Returns the calculated visibility."""

        if elevation is None or air_temperature is None or relative_humidity is None or dewpoint is None:
            return None

        elevation_min = float(2)
        if elevation > 2:
            elevation_min = float(elevation)

        max_visibility = float(3.56972 * math.sqrt(elevation_min))
        percent_reduction_a = float((1.13 * abs(air_temperature - dewpoint) - 1.15) /10)
        if percent_reduction_a > 1:
            percent_reduction = float(1)
        elif percent_reduction_a < 0.025:
            percent_reduction = float(0.025)
        else:
            percent_reduction = percent_reduction_a
        
        visibility_km = float(max_visibility * percent_reduction)

        return visibility_km

    def absolute_humidity(self, air_temperature, relative_humidity) -> float:
        """Returns calculated absolute humidity."""

        if air_temperature is None or relative_humidity is None:
            return None

        temperature_kelvin = air_temperature + 273.16
        humidity = relative_humidity / 100
        abs_humidity = (1320.65 / temperature_kelvin) * humidity * (10 ** ((7.4475 * (temperature_kelvin - 273.14)) / (temperature_kelvin - 39.44)))

        return round(abs_humidity, 2)

    def battery_percent(self, is_tempest: bool, voltage: float) -> int:
        """Returns battery percentage from voltage."""

        if is_tempest is None or voltage is None:
            return None

        if is_tempest:
            if voltage > 2.80:
                bat_percent = 100
            elif voltage < 1.8:
                bat_percent = 0
            else:
                bat_percent = (voltage - 1.8) * 100
        else:
            if voltage > 3.50:
                bat_percent = 100
            elif voltage < 2.4:
                bat_percent = 0
            else:
                bat_percent = ((voltage - 2.4) / 1.1) * 100

        return int(bat_percent)

    def beaufort(self, wind_speed: float) -> int:
        """Returns Beaufort scale value from wind speed."""

        if wind_speed is None:
            return None

        if wind_speed > 32.7:
            bft_value = 12
        elif wind_speed >= 28.5:
            bft_value = 11
        elif wind_speed >= 24.5:
            bft_value = 10
        elif wind_speed >= 20.8:
            bft_value = 9
        elif wind_speed >= 17.2:
            bft_value = 8
        elif wind_speed >= 13.9:
            bft_value = 7
        elif wind_speed >= 10.8:
            bft_value = 6
        elif wind_speed >= 8.0:
            bft_value = 5
        elif wind_speed >= 5.5:
            bft_value = 4
        elif wind_speed >= 3.4:
            bft_value = 3
        elif wind_speed >= 1.6:
            bft_value = 2
        elif wind_speed >= 0.3:
            bft_value = 1
        else:
            bft_value = 0

        return bft_value
