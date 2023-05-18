import requests
from homeassistant.helpers.entity import Entity
from . import DOMAIN

def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Your Integration sensor."""
    api_key = hass.data[DOMAIN]['api_key']
    async_add_entities([LoadSheddingService(api_key)], True)

class LoadSheddingService(Entity):
    def __init__(self, api_key):
        """Initialize the sensor."""
        self._api_key = api_key
        self._state = None
        self._name = None
        self._region = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {"region": self._region}

    async def async_update(self):
        """Fetch new state data for the sensor."""
        headers = {'Authorization': self._api_key}
        response = requests.get("https://developer.sepush.co.za/business/2.0/area?id=eskde-10-fourwaysext10cityofjohannesburggauteng&test=current", headers=headers)
        data = response.json()
        
        if data:
            self._name = data['info']['name']
            self._region = data['info']['region']

            # This assumes that "events" always has at least one entry. You may want to add some error checking here.
            event = data['events'][0]

            if event['note'] == 'Stage 2':
                self._state = 'Power Out'
            else:
                self._state = 'Power On'
