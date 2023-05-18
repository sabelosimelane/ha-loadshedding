import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_API_KEY

from .api import YourIntegrationAPI

DOMAIN = 'ha-loadshedding'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_API_KEY): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    """Set up the Your Integration component."""
    # Get API from configuration.yaml
    api_key = config[DOMAIN][CONF_API_KEY]

    session = async_get_clientsession(hass)
    hass.data[DOMAIN] = YourIntegrationAPI(api_key, session)

    # Load platforms...
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform('sensor', DOMAIN, {}, config)
    )

    return True
