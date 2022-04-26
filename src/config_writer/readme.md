# Python config file reader/wrtier
_JSON based config file reader and writer_

>Usage:
>       
>       import config
>       
>       key='Test_key'
>    
>       def test_1(): # Modifying values
>           config = Config_File()
>           config.modify_value(key=key,value="Test_key_value")
>    
>       def test_2(): # Reading values
>           config = Config_File()
>       # Can use either ( config.key = 'test' ) OR ( value = config.read_value(key='test') )
>           value = config.read_value(key=key)
>           print(key, value)
>   
>       def test_3(): # Reading all values
>           config = Config_File()
>           all_values = config.read_config() # reads all values from the config file to a dict
>           print(f"All Values: {all_values}")
>           print(key, all_values[key])
>
>    test_1()
>    test_2()
>    test_3()
>
>
>Returns:
>
>>Test_key Test_key_value
>>All Values: {'Test_key': 'Test_key_value'}
>>Test_key Test_key_value
>