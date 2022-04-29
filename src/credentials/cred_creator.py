#Cred_creator_gui.py
###### DESCRIPTION ######
## Creates a credential file. Now with a GUI!
######
#
#
#
#
###### IMPORTS ######
from cryptography.fernet import Fernet
import re
import ctypes
import time
import os
import sys
import PySimpleGUI as sg 
import asyncio, threading
  
class Credentials():
    """Credentials creates a set of single user credentials for the services labeled below.
    """  
    def __init__(self):
        self.__services = {1:'Test', 2:'WinAir', 3:'MyBoeingFleet'}
        self.__service = ""
        self.__username = ""
        self.__key = ""
        self.__password = ""
        self.__key_file = '.key' #extension only?
        self.__time_of_exp = -1
  
#----------------------------------------
# Getter setter for attributes
#----------------------------------------

    @property
    def services(self):
        return f'Available services: {self.__services}'
    
    
    def get_service_key(self, value):
        for k, v in self.__services.items():
            if value.lower() == v.lower():
                return k

    @property
    def service(self):
        return self.__service
    
    @service.setter
    def service(self,service):
        # selections = f'{self.__services}'
        while (service == ''):
            service = sg.popup_get_text('Enter number of the service, blank is not accepted:')
            # service = eg.enterbox(msg='Enter number of the service, blank is not accepted:')
        self.__service = self.__services.get(service).lower()
   
    @property
    def username(self):
        return self.__username
  
    @username.setter
    def username(self,username):
        while (username == ''):
            username = sg.popup_get_text('Enter username, blank is not accepted:')
            # username = eg.enterbox(msg='Enter a proper User name, blank is not accepted:')
        self.__username = username
  
    @property
    def password(self):
        return self.__password
  
    @password.setter
    def password(self,password):
        while (password == ''):
            # password = eg.enterbox(msg='Enter a proper password, blank is not accepted:')
            password = sg.popup_get_text('Enter a proper password, blank is not accepted:', password_char="*")
        if len(password) < 8:
            sg.popup_notify('Security Reminder: \nPassword should be at least 8 characters long with mixed case and numbers for better security.')
            # eg.msgbox(msg='Your password is less than 8 characters long. You should really consider a stronger password')
        self.__key = Fernet.generate_key()
        f = Fernet(self.__key)
        self.__password = f.encrypt(password.encode()).decode()
        del f
  
    @property
    def expiry_time(self):
        return self.__time_of_exp
  
    @expiry_time.setter
    def expiry_time(self,exp_time):
        if(exp_time >= 2):
            self.__time_of_exp = exp_time
  
  
    def create_cred(self):
        """
        This function is responsible for encrypting the password and create  key file for
        storing the key and create a credential file with user name and password
        """
        
        key_mod = f'service_key_{self.__service}{self.__key_file}'
        cred_filename = f'service_cred_{self.__service}.ini'
  
        with open(cred_filename,'w') as file_in:
            file_in.write(f"#Credential file:\nService={self.service}\nUsername={self.__username}\nPassword={self.__password}\nExpiry={self.__time_of_exp}\n")
            file_in.write("++"*20)
  
  
        #If there exists an older key file, This will remove it.
        if(os.path.exists(key_mod)):
            os.remove(key_mod)
  
        #Open the Key.key file and place the key in it.
        #The key file is hidden.
        try:
  
            os_type = sys.platform
            if (os_type == 'linux'):
                key_mod = '.' + key_mod
  
            with open(key_mod,'w') as key_in:
                key_in.write(self.__key.decode())
                #Hidding the key file.
                #The below code snippet finds out which current os the script is running on and does the task base on it.
                if(os_type == 'win32'):
                    ctypes.windll.kernel32.SetFileAttributesW(key_mod, 2)
                else:
                    pass
  
        except PermissionError:
            os.remove(key_mod)
            print("A Permission error occurred.\n Please re run the script")
            sys.exit()
  
        self.__service = ""
        self.__username = ""
        self.__password = ""
        self.__key = ""
        self.__key_file
  
  
def main():

  
    # Creating an object for Credentials class
    creds = Credentials()
  
    #Accepting credentials
    # print(creds.services)
    creds.service = 2  #int(eg.enterbox(msg=f"Enter service number:\n{creds.services}"))
    creds.username = sg.popup_get_text('Enter username:')
    # eg.enterbox(msg="Enter User Name:")
    creds.password = sg.popup_get_text("Enter password:", password_char="*")
    # eg.passwordbox(msg="Enter Password:")
    # print("Enter the epiry time for key file in minutes, [default:Will never expire]")
    creds.expiry_time = '-1' #int(eg.enterbox(msg="Enter the expiry time for key file in minutes: [default:Will never expire]") or '-1')
  
    #calling the Credit
    creds.create_cred()
    print("**"*20)
    print("Cred file created successfully at {}"
    .format(time.ctime()))
  
    # if not(creds.expiry_time == -1):
    #     key_mod = f'key_00{self.__service}{self.__key_file}'
    #     cred_filename = f'CredFile-{self.__service}.ini'
    #     import cred_expire
    #     cred_expire(key_mod,cred_filename)
        
        # os.startfile('cred_expire.py')
  
  
    print("**"*20)
  
if __name__ == "__main__":
    main()