import PySimpleGUI as sg
import db_calls as db
import datetime
from dateutil import parser

#import numpy as np
#import matplotlib.pyplot as plt

import time
from decimal import Decimal as dec

from cryptography.fernet import Fernet


#Encryption Utility: Use to encrypt and decrypt databases so they can be opened in a database browser.
#Set the database file, key location, and the mode. Run the file with caution.
#Always clear the db name and file name after use. Always set the if statement to False after use. 
#Failure to follow these guidelines could result in data loss. Thank you.

db_name = "Arthurs_Information_Emporium.fid" #WARNING: Delete the file name after you use this utility to avoid bricking your database. Do not encrypt twice.
filename = "Arthurs_Information_Emporium.fidkey" #Warning: Delete File Name. Don't Encrypt Twice.
save_location = "/home/joe/Documents/01_BurrillvilleRealizationGroup/001_Letters/Letter_Database/"
connection = db.create_connection(f"./{db_name}")
mode = "decrypt" 
if False: #Safer to leave this set to False (decrypt) unless you are encrypting. 
    mode = "encrypt"

#End Encryption Utility



def generate_filekey(db_name, save_location):
    key = Fernet.generate_key()
    if save_location[-1] != "/":
        save_location = save_location + "/"
    filename = f'{db_name}key'    
    file_address = f'{save_location}{db_name}key'
    with open(file_address, 'wb') as filekey:
        filekey.write(key)#-----------------------------------------------------------------------
    return key, filename



def encrypt_database(db_name, mode, filename, save_location):
    """Encrypts or decrypts a database file. 
    Mode is 'encypt' or 'decrypt'. 
    filekey=False will generate a new filekey.
    save_location=False will save to the Iceberg directory."""
    print(f"encrypt db_name {db_name}; mode: {mode}; filename: {filename}; save_location: {save_location}")
    if save_location == False:
        save_location = "./"
    if save_location[-1] != "/":
        save_location = save_location + "/"
    if filename == False and mode == "encrypt":
        filekey, filename = generate_filekey(db_name, save_location)
    elif filename== False and mode =="decrypt":
        return "Error: Attempted decryption without key.", ""
    if mode == "encrypt":
        with open(f'./{filename}','rb') as file:
            filekey = file.read()        
        #print('filekey generated')
        #print(filekey)
        fernet=Fernet(filekey)
        with open(f'./{db_name}','rb') as file:
            original_db = file.read()
        #print(original_db)
        encrypted_db = fernet.encrypt(original_db)
        with open(f'./{db_name}','wb') as encrypted_file:
            encrypted_file.write(encrypted_db)
        return filekey, filename
    elif mode == "decrypt":
        with open(f'./{filename}','rb') as file:
            filekey = file.read()  
        fernet=Fernet(filekey)
        with open(f'./{db_name}','rb') as file:
            original_db = file.read()
        print(filekey)
        encrypted_db = fernet.decrypt(original_db)
        with open(f'./{db_name}','wb') as encrypted_file:
            encrypted_file.write(encrypted_db)
        return filekey, filename
    else:
        return "Error: Mode not selected. (encrypt or decrypt)", ""
    
#filekey, filename = encrypt_database(db_name,"encrypt",filename,save_location)


#print(filekey, filename)


#ENCRYPT DECRYPT FILE:
filekey, filename = encrypt_database(db_name,mode,filename,save_location)
print(filekey, filename)

def int_to_shifted_binary(num, n):
  """Converts an integer to its binary representation and then shifts it right by n bits.

  Args:
    num: The integer to convert.
    n: The number of bits to shift right.

  Returns:
    A string representing the shifted binary number.
  """

  #binary = bin(num)[2:]  # Convert to binary, remove "0b" prefix
  #shifted_binary = "0" * n + binary  # Add n leading zeros for the shift
  #return shifted_binary[-len(binary):]  # Return the rightmost bits

  shifted_num = num >> n
  return bin(shifted_num)[2:]

# Example usage
#number = 42
#shift_amount = 3
#shifted_result = int_to_shifted_binary(number, shift_amount)
#print(f"The binary representation of {number} shifted right by {shift_amount} bits is: {shifted_result}")

#Instantiate a class for the session
if False: #Set to "if False:" to disable code block
    class new_session:
        def __init__(self):
            self.ledger_name = ""
            self.synchronized = "No"
            self.connection = False
            self.num = 1
            self.guitimer="Initializing"
            print(self.guitimer)
            self.db_name = ""
            self.filekey = ""
            self.filename = ""
            self.chart_of_accounts_display_content = []
            
            self.session_filekey, self.session_filename, self.session_save_location= db.encrypt_database("sessions.icbs","decrypt","sessions.icbskey",False,"sessions.icbs")
            session_log_connection = db.create_connection("sessions.icbs")
            self.session_log_connection = db.load_db_to_memory(session_log_connection)
            


            create_console_table = f"""CREATE TABLE tbl_Console_Log (Log_ID INTEGER NOT NULL"""
            
            lines = [   """, Console_Messages VARCHAR(9999) NOT NULL""", 
                        """, Created_Time VARCHAR(9999) NOT NULL""", 
                        """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                        """, PRIMARY KEY ("Log_ID" AUTOINCREMENT)"""
                    ]
            num_lines = len(lines)
            for p in range(num_lines):
                create_console_table = create_console_table + lines[p]
            create_console_table = create_console_table + """);"""


            created_table = db.create_tables(self.session_log_connection,create_console_table)
            print(f"{created_table}: tbl_Console_Log (scratch_new_session 121)")

            self.session_filekey, self.session_filename, self.session_save_location= db.encrypt_database("sessions.icbs","encrypt","sessions.icbskey",False,"sessions.icbs") #False
            print(self.session_filekey)

    icb_session = new_session()

    print(icb_session.guitimer)
#End IF False
