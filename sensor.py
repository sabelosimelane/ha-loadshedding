import logging
import requests
import voluptuous as vol

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Custom Schedule'
CONF_ENDPOINT = 'https://developer.sepush.co.za/business/2.0/area?id=eskde-10-fourwaysext10cityofjohannesburggauteng&test=current'

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_key = config[CONF_API_KEY]
    name = config[CONF_NAME]

    add_entities([CustomScheduleSensor(api_key, name)])

class CustomScheduleSensor(Entity):
    def __init__(self, api_key, name):
        self._api_key = api_key
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        headers = {'Authorization': self._api_key}
        try:
            response = requests.get(CONF_ENDPOINT, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Here you would process the response and store the result in self._state
            self._state = 'Updated' # Placeholder line, replace with real processing

        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error getting data from the api: %s", ex)
            self._state = 'Error'
