import os
from .dev import settings as dev_settings

class Struct:
    '''
    Just to have property style access (obj.prop) instead of obj['prop']
    '''
    def __init__(self, **entries):
        self.__dict__.update(entries)

settings = dev_settings

if os.getenv("env") == "prod":
    from .prod import settings as prod_settings
    settings = prod_settings

settings = Struct(**settings)
