## config.py
###### DESCRIPTION ######
## Settings/config file reader/writer
######
#
# Basic Json file Reader/Writer
#
###### IMPORTS ######
import json, os, sys
###### GLOBAL VARIABLES ######
None
###### CLASSES ######
class Config_File():
    """Config_File gets and sets values from the config file using a set of helper functions.
    """
    def __init__(self):
        self.__key = ''
        self.__value = ''
        self.__configfile = 'config.json'
        
    ## Getter-Setters
    
    @property
    def key(self):
        return self.__key
    
    @property
    def value(self):
        return self.__value
    
    @key.setter
    def key(self, key):
        self.__key = key
    
    @value.setter
    def value(self, value):
        self.__value = value
        
    def read_config(self):
        """read_config Reads the config file in its entirety.

        Returns:
            dict: config dict containing the key: value pairs.
        """
        doexist = os.path.exists(self.__configfile)
        if not doexist:
            with open(self.__configfile, 'w') as f:
                pass  # empty file
        try:
            with open(self.__configfile, 'r') as f:
                config = json.load(f)
        except:
            config = {}
            print(f"No config file found : {sys.exc_info()[0]}")
        return config
    
    def read_value(self, key=None):
        """read_value reads a single value from the json file when provided a key

        Args:
            key (str, optional): Key to look for in the config file. Defaults to None. 
            

        Returns:
            str: value returned from given key
        """
        try:
            with open(self.__configfile, 'r') as f:
                config = json.load(f)
        except:
            config = {}
        # return config[key]
        if key:
            self.__value = config[key]
        else:
            self.__value = config[self.__key]
        return self.__value
    
    def modify_value(self, key=None, value=None):
        '''
        docstring
        '''
        
        try: # Try statement in the case we are creating it for the first time
            with open(self.__configfile, 'r') as f:
                config = json.load(f)
        except: # Fail to a blank dict
            config = {}
        # edit the data
        if key and value:
            config[key] = value
        elif key:
            config[key] = self.__value
        elif value:
            config[self.__key] = value
        else:
            config[self.__key] = self.__value

        # write it back to the file
        with open(self.__configfile, 'w') as f:
            json.dump(config, f)
        ## Clean out variables
        self.__key = ''
        self.__value = ''
            
###### TEST FUNCTIONS ######
key='Test_key'
    
def test_1(): # Modifying values
    config = Config_File()
    config.modify_value(key=key,value="Test_key_value")
    
def test_2(): # Reading values
    config = Config_File()
    # Can use either ( config.key = 'test' ) OR ( value = config.read_value(key='test') )
    value = config.read_value(key=key)
    print(key, value)

def test_3(): # Reading all values
    config = Config_File()
    all_values = config.read_config() # reads all values from the config file to a dict
    print(f"All Values: {all_values}")
    print(key, all_values[key])


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()