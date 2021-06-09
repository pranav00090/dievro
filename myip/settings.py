"""
Settings file - contains settings loaded from environment

Copyright::

    +===================================================+
    |                 © 2021 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        IP Address Information Tool                |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+


"""
import logging
import warnings
from pathlib import Path
from os import getenv as env

import dotenv
from privex.helpers import empty, empty_if, env_bool, env_int, env_csv, DictObject
from privex.helpers import settings as pvx_settings

try:
    from rich.logging import RichHandler
except Exception as rxe:
    warnings.warn(f"Failed to import rich.logging.RichHandler. Reason: {type(rxe)} - {rxe!s}", ImportWarning)
    RichHandler = None

dotenv.load_dotenv()

cf = DictObject()
APP_DIR = Path(__file__).parent.expanduser().resolve()
TEMPLATES_DIR = APP_DIR / 'templates'
BASE_DIR = APP_DIR.parent

#######################################
#
# General configuration
#
#######################################
cf['DEBUG'] = DEBUG = env_bool('DEBUG', True if env('FLASK_ENV') == 'development' else False)

HOST = cf['HOST'] = env('HOST', '127.0.0.1')
PORT = cf['PORT'] = env_int('PORT', 5111)

cf['API_ONLY'] = env_bool('API_ONLY', False)
"""If set to ``True``, will always return JSON, never HTML pages."""

USE_IP_HEADER = cf['USE_IP_HEADER'] = env_bool('USE_IP_HEADER', True)
"""If set to False, will obtain the IP from request.remote_addr instead of the header set in IP_HEADER"""
IP_HEADER = cf['IP_HEADER'] = env('IP_HEADER', 'X-REAL-IP')
"""The name of the header that will be passed to Flask containing the IP address of the user"""

USE_FAKE_IPS = env_bool('USE_FAKE_IPS', DEBUG)
FAKE_V4 = empty_if(env('FAKE_V4', '185.130.44.140' if USE_FAKE_IPS else ''), None)
FAKE_V6 = empty_if(env('FAKE_V6', '2a07:e01:123::456' if USE_FAKE_IPS else ''), None)

MAX_ADDRESSES = env_int('MAX_ADDRESSES', 20)

MAIN_HOST = env('MAIN_HOST', 'myip.privex.io')

# To be able to detect both a user's IPv4 and IPv6 addresses, you must have two subdomains
# with the ipv4 subdomain having only an A record, and the ipv6 subdomain with only an AAAA.
V6_HOST = cf['V6_HOST'] = env('V6_HOST', 'ipv6.myip.privex.io')
V4_HOST = cf['V4_HOST'] = env('V4_HOST', 'ipv4.myip.privex.io')

pvx_settings.GEOIP_DIR = GEOIP_PATH = Path(env('GEOIP_PATH', '/usr/local/var/GeoIP')).expanduser().resolve()
"""An absolute path to the GeoIP2 folder containing mmdb files to use for IP lookups (NO ENDING SLASH)"""
cf['GEOIP_PREFIX'] = GEOIP_PREFIX = env('GEOIP_PREFIX', 'GeoLite2-')
"""The prefix for the GeoIP2 files, generally either 'GeoIP2-' for paid, or 'GeoLite2-' for the free edition"""

pvx_settings.GEOASN_NAME = GEOASN_NAME = f"{GEOIP_PREFIX}ASN.mmdb"
pvx_settings.GEOCITY_NAME = GEOCITY_NAME = f"{GEOIP_PREFIX}City.mmdb"
pvx_settings.GEOCOUNTRY_NAME = GEOCOUNTRY_NAME = f"{GEOIP_PREFIX}Country.mmdb"
pvx_settings.GEOASN = GEOIP_PATH / GEOASN_NAME
pvx_settings.GEOCITY = GEOIP_PATH / GEOCITY_NAME
pvx_settings.GEOCOUNTRY = GEOIP_PATH / GEOCOUNTRY_NAME

cf['GEOIP_CACHE_SEC'] = GEOIP_CACHE_SEC = int(env('GEOIP_CACHE_SEC', 600))
"""Amount of seconds to cache GeoIP data in Redis for. Default is 600 seconds (10 minutes)"""

REDIS_HOST = env('REDIS_HOST', 'localhost')
REDIS_PORT = int(env('REDIS_PORT', 6379))

#######################################
#
# Logging configuration
#
#######################################
# Log to console with LOG_LEVEL, as well as output logs >=info / >=warning to respective files
# with automatic daily log rotation (up to 14 days of logs)
# Due to the amount of output from logging.DEBUG, we only log INFO and higher to a file.
# Valid environment log levels (from least to most severe) are:
# DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL

USE_RICH_LOGGING = env_bool('USE_RICH_LOGGING', True)
RICH_TRACEBACKS = env_bool('RICH_TRACEBACKS', True)

if RichHandler is None: USE_RICH_LOGGING = False

LOG_LEVEL = str(env('LOG_LEVEL', 'DEBUG' if DEBUG else 'WARNING')).upper()
LOG_LEVEL = logging.getLevelName(LOG_LEVEL)
LOG_DIR = Path(env('LOG_DIR', 'logs')).expanduser()
LOG_DIR = BASE_DIR / str(LOG_DIR) if not LOG_DIR.is_absolute() else LOG_DIR.resolve()

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

DBG_LOG, ERR_LOG = str(LOG_DIR / 'debug.log'), str(LOG_DIR / 'error.log')