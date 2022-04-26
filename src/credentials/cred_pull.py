#Cred_pull.py
###### DESCRIPTION ######
## Retrieves a credential file.
######
#
#
#
#
###### IMPORTS ######
# from cryptography.fernet import Fernet
import os, time
import easygui as eg

###### FUNCTIONS ######
def get_credential(servicename):
    """get_credential Gathers credential information for the given service name. If any are found.

    Args:
        servicename (str): Name of the service to look up key for.

    Returns:
        str, tuple: username, password
    """    
    servicename = servicename.lower() # auto-convert it to lowercase
    key_file = f'service_key_{servicename}.key'
    cred_filename = f'service_cred_{servicename}.ini'
    
    key = ''
    create_loop = True
    while create_loop:
        if(os.path.exists(key_file) and os.path.exists(cred_filename)):
            print(f"Credential Exists for {servicename}")
            with open(key_file,'r') as key_in:
                key = key_in.read().encode()
            
            #If you want the Cred file to be of one
            # time use uncomment the below line
            #os.remove(key_file)
            
            f = Fernet(key)
            with open(cred_filename,'r') as cred_in:
                lines = cred_in.readlines()
                config = {}
                for line in lines:
                    tuples = line.rstrip('\n').split('=',1)
                    if tuples[0] in ('Username','Password'):
                        config[tuples[0]] = tuples[1]
                username = config['Username']
                passwd = f.decrypt(config['Password'].encode()).decode()
                # create_loop = False
                return username,passwd
            
        else:
            print(f"Nonexistant credential for {servicename}")
            choice = eg.boolbox(msg='No credential/key file pair found. Create new?', choices=['Yes','No'])
            if choice:
                print("Creating credential")
                from cred_creator import Credentials
                    # Creating an object for Credentials class
                creds = Credentials()
            
                #Accepting credentials
                creds.service = int(eg.enterbox(msg=f"Enter service number:\n{creds.services}", default=creds.get_service_key(servicename)))
                creds.username = eg.enterbox(msg="Enter User Name:")
                creds.password = eg.passwordbox(msg="Enter Password:")
                # print("Enter the epiry time for key file in minutes, [default:Will never expire]")
                creds.expiry_time = -1 #int(eg.enterbox(msg="Enter the epiry time for key file in minutes: [default:Will never expire]") or '-1')
            
                #calling the Credit
                creds.create_cred()
                print("**"*20)
                print(f"Cred file created successfully at {time.ctime()}")
                print("**"*20)
                continue
            else:
                break
                # create_loop = False
                
###### MAIN ######  
def main():
    service = eg.enterbox(msg="Please type service name", default="TEST")
    print(get_credential(service)) 
        

if __name__ == '__main__':
    main()