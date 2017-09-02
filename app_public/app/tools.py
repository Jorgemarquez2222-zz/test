import json, string, random, logging
import datetime
import pytz
from typing import Dict, Any, Iterable

JsonType = Dict[str, Any]
logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


"""
    Displays an error on the Django logger
"""
def log_error(message):
    logger.error("[ERROR] " + str(message))

"""
    Displays a message on the Django logger
"""
def log_info(message):
    logger.info("[INFO] " + str(message))

"""
    Returns a random string made with lowercase chars and digits
"""
def get_random_string(length : int = 50) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

"""
    Converts a json api response to usable json
"""
def get_json_from_jsonresponse(jsonresponse) -> JsonType:
    l = jsonresponse.content
    l = l.decode("utf-8")
    l = json.loads(l)
    return l

"""
    Convers a unix timestamp in milliseconds to a datetime
    The timestamp is sent by the valueOf() function of moment.js
"""
def get_datetime_from_request(time):
    return datetime.datetime.fromtimestamp(int(time), tz=pytz.utc)


"""
    Filter values if a dictionnary
"""
def filter_dict_fields(dic : dict, fields : Iterable) -> dict:
    return {key: value for key, value in dic.items() if key in fields}

