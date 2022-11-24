API_TOKEN = "BAD_TOKEN"
NEED_SAVE_LOGS_TO_FILE = True

 #for locally rewrite settings add it to settings_local.py
try:
    from settings_local import *
except ModuleNotFoundError as err:
    pass

