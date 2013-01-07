from julian.discourse.api.exceptions import InvalidParams
from julian.discourse.api.exceptions import  MissingParams

class Model(dict):
    
    def __init__(self, **kwargs):
        params  = set(kwargs.keys())

        missing = self.REQUIRED_FIELDS.difference(params)
        extra   = params.difference(self.REQUIRED_FIELDS|self.OPTIONAL_FIELDS)
        
        if missing:
            raise MissingParams( "The following parameters are missing: " + ", ".join(list(missing)))
        if extra:
            raise InvalidParams( "The following parameters are invalid/unrecognized: " + ", ".join(list(extra)))
        
        for key, val in kwargs.items():
            setattr( self, key, val)
        
    def to_dict(self):
        return self.__dict__