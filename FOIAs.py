import PySimpleGUI as sg
import db_calls as db
import datetime
from dateutil import parser
#import numpy as np
#import matplotlib.pyplot as plt
import time
from decimal import Decimal as dec
import tempfile
#import PIL
import shutil
import math

import string
import random


#img2pdf
import img2pdf
import subprocess
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from cryptography.fernet import Fernet

import os
import sys
sys.path.append('PATH')
from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageDraw2, ImageFont

#HOW TO PRINT
#import os
#
#os.startfile("C:/Users/TestFile.txt", "print")



#------------------------------------------Section 1 Date Information
#  _____          _________  ___  _____ ______   _______           ________             ________  ________  _________  _______      
# / __  \        |\___   ___\\  \|\   _ \  _   \|\  ___ \         |\   __  \           |\   ___ \|\   __  \|\___   ___\\  ___ \     
#|\/_|\  \       \|___ \  \_\ \  \ \  \\\__\ \  \ \   __/|        \ \  \|\  \  /\      \ \  \_|\ \ \  \|\  \|___ \  \_\ \   __/|    
#\|/ \ \  \           \ \  \ \ \  \ \  \\|__| \  \ \  \_|/__       \ \__     \/  \      \ \  \ \\ \ \   __  \   \ \  \ \ \  \_|/__  
#     \ \  \           \ \  \ \ \  \ \  \    \ \  \ \  \_|\ \       \|_/  __     /|      \ \  \_\\ \ \  \ \  \   \ \  \ \ \  \_|\ \ 
#      \ \__\           \ \__\ \ \__\ \__\    \ \__\ \_______\        /  /_|\   / /       \ \_______\ \__\ \__\   \ \__\ \ \_______\
#       \|__|            \|__|  \|__|\|__|     \|__|\|_______|       /_______   \/         \|_______|\|__|\|__|    \|__|  \|_______|
#                                                                    |_______|\__\                                                  
#                                                                            \|__|                                                  
                                                                                                                                   


sample_date = parser.parse('2023-04-02')

now= datetime.datetime.now()
current_date = now.strftime('%m/%d/%Y')
current_date_db = now.strftime('%Y/%m/%d')
current_year = now.year
week_past = now.date() - datetime.timedelta(6)

current_month = now.strftime('%Y/%m/01')

def get_current_time_info():
    """Returns the current time information in string format."""
    weekday = ''
    if datetime.datetime.now().weekday() == 0:
        weekday = "Monday"
    if datetime.datetime.now().weekday() == 1:
        weekday = "Tuesday"
    if datetime.datetime.now().weekday() == 2:
        weekday = "Wednesday"
    if datetime.datetime.now().weekday() == 3:
        weekday = "Thursday"
    if datetime.datetime.now().weekday() == 4:
        weekday = "Friday"
    if datetime.datetime.now().weekday() == 5:
        weekday = "Saturday"
    if datetime.datetime.now().weekday() == 6:
        weekday = "Sunday"


    time_info = time.tzname[time.daylight]

    current_time = f"""{weekday}, {datetime.datetime.now().month}/{datetime.datetime.now().day}/{datetime.datetime.now().year}  -  {format(datetime.datetime.now().hour,'02d')}:{format(datetime.datetime.now().minute,'02d')} {time_info}"""
    current_timestamp = f"""{weekday}, {datetime.datetime.now().month}/{datetime.datetime.now().day}/{datetime.datetime.now().year}  -  {format(datetime.datetime.now().hour, '02d')}:{format(datetime.datetime.now().minute,'02d')}:{format(datetime.datetime.now().second,'02d')} {time_info}"""
    return current_time, current_timestamp





#------------------------------------------Section 2 Load Initial Data

#  _______          ___  ________   ___  _________  ___  ________  ___       ___  ________  _______      
# /  ___  \        |\  \|\   ___  \|\  \|\___   ___\\  \|\   __  \|\  \     |\  \|\_____  \|\  ___ \     
#/__/|_/  /|       \ \  \ \  \\ \  \ \  \|___ \  \_\ \  \ \  \|\  \ \  \    \ \  \\|___/  /\ \   __/|    
#|__|//  / /        \ \  \ \  \\ \  \ \  \   \ \  \ \ \  \ \   __  \ \  \    \ \  \   /  / /\ \  \_|/__  
#    /  /_/__        \ \  \ \  \\ \  \ \  \   \ \  \ \ \  \ \  \ \  \ \  \____\ \  \ /  /_/__\ \  \_|\ \ 
#   |\________\       \ \__\ \__\\ \__\ \__\   \ \__\ \ \__\ \__\ \__\ \_______\ \__\\________\ \_______\
#    \|_______|        \|__|\|__| \|__|\|__|    \|__|  \|__|\|__|\|__|\|_______|\|__|\|_______|\|_______|
                                                                                                        
                                                                                                        
                                                                                                        






#Instantiate a class for the session
class new_session:
    def __init__(self):
        self.current_time_display = get_current_time_info()
        self.current_year = str(current_year)
        self.synchronized = "No"#
        self.connection = False#
        self.num = 1#
        self.guitimer="Initializing" ##
        #print(self.guitimer)
        self.db_name = ""#
        self.filekey = ""#
        self.filename = ""#
        self.save_location = False#
        self.window = False
        self.values = False
        self.current_date = f"{datetime.datetime.now().month}/{datetime.datetime.now().day}/{datetime.datetime.now().year}"
        self.organization_name = []
        self.organization_acronym = []
        self.organization_address = []
        self.manager_firstname = []
        self.manager_middlename = []
        self.manager_lastname = []
        self.manager_title = []
        self.manager_preferredname = []
        self.manager_fullname = []
        self.manager_title = []
        self.organization_phone = []
        self.organization_email = []
        self.organization_notes = []
        self.documents_location = "./Documents/"
        self.current_console_messages = [f"""Welcome to FOIA Cajones! Create or open a database to get started."""]
        self.session_filekey, self.session_filename, self.session_save_location= db.encrypt_database("sessions.fid","decrypt","sessions.fidkey",False,"sessions.fid")
        session_log_connection = db.create_connection("sessions.fid")
        self.session_log_connection = db.load_db_to_memory(session_log_connection)
        self.session_filekey, self.session_filename, self.session_save_location= db.encrypt_database("sessions.fid","encrypt","sessions.fidkey",False,"sessions.fid")
        self.requesters = []
        self.tab_key_list = [
            '-Dashboard_Tab-',#0
            '-View_Applications_Tab-',#1
            '-View_Analysis_Tab-',#2
            '-View_Letters_Tab-',#3
            '-View_Responses_Tab-',#4
            '-View_Forwarding_Tab-',#5
            '-Requesters_Time_Tab-',#6
            '-Timekeeping_Records_Tab-',#7
            '-Documentation_Tab-',#8
            '-About_Tab-',#9
            '-View_Properties_Tab-',#10
            '-Templates_Tab-',#11
            '-Applicants_Tab-',#12
            '-Responders_Tab-'#13
        ]
        
        #https://deepai.org/machine-learning-model/surreal-graphics-generator
        self.logo = "WalrusCarpenter_StarryNight.png"

        self.phone_types = ["Mobile","Home", "Office", "Work", "Other"]
        self.request_types = ["Supporting Desposition Request","Stenographic Notes","Audio","Video","Combined Media","Documents"]

        #Applications and FOIA Responses are scanned in as received.
        self.letter_types = ["Application","FOIA Request","FOIA Response","Forwarding","Management"]

        #print(self.session_filekey)
        self.this_requester = 1
        self.requester_photo = ""
        self.new_requester = 0
        self.new_letter = 0

        self.letter_image = ""
        self.letter_response_image = ""
        self.letter_response_forwarding_image = ""
        self.applicants =[]
        self.this_applicant = []
        self.responders = []
        self.this_responder = []
        self.this_letter = {"Application_ID":0,"Letter_ID":""} #Sets that there is no application associated with the letter by default
        self.this_letter_body = r""
        self.letter_saved = False
        self.display_letters = []
        self.this_letter_id = ""

        #Applications
        self.this_application = {"Application_ID":0,"Documents": [], "Requests": []}
        self.this_application_id = 0
        self.new_application_id = 0
        self.display_applications = []



        #Templates
        self.display_templates = []
        self.new_template_number = 0
        self.this_template = 0
        self.template_names = []


        self.database_loaded = False

    def console_log(self, message, current_console_messages):#
        """Posts a message to the console and logs it in the database.."""
        self.current_time_display = get_current_time_info()
        this_message = f"""Console ({self.current_time_display[1]}): {message}"""
        full_message = f"""{this_message}"""
        for i in range(len(current_console_messages)):
            full_message = full_message + f"""\n{current_console_messages[i]}"""
        
        self.window["-Console_Log-"].update(full_message)
        current_console_messages = [this_message] + current_console_messages           

        

        insert_log_entry_query = f"""INSERT INTO tbl_Console_Log (Console_Messages, Created_Time, Edited_Time)
            VALUES(("{this_message}"),("{self.current_time_display[1]}"),("{self.current_time_display[1]}"));
        """
        created_session_entry = db.execute_query(self.session_log_connection,insert_log_entry_query)
       #print(f"""Console entry: {created_session_entry}""")
        full_message = full_message + f"""\nConsole ({self.current_time_display[0]}): {created_session_entry}"""

        if self.connection:     
            insert_log_entry_query = f"""INSERT INTO tbl_Console_Log (Console_Messages, Created_Time, Edited_Time)
                VALUES(("{this_message}"),("{self.current_time_display[1]}"),("{self.current_time_display[1]}"));
            """
            created_entry = db.execute_query(self.connection,insert_log_entry_query)
            full_message = full_message + f"""\nConsole ({self.current_time_display[0]}): {created_entry}"""
        return current_console_messages



foia_session = new_session()
print(foia_session.current_date)
#print(foia_session.guitimer)

#Set fixed variables

sg.theme('DarkTeal6')

small_print = 8
medium_print = 11
large_print = 16
extra_large_print = 24
detailed_information_color= "#9b9e9d"#"#6eaa87"#"#8ed0fb"

overview_information_color = "#607786"#"#792b1c"#"#78dac0"







#------------------------------------------Section 3 GUI Layout
# ________          ___       ________      ___    ___ ________  ___  ___  _________   
#|\_____  \        |\  \     |\   __  \    |\  \  /  /|\   __  \|\  \|\  \|\___   ___\ 
#\|____|\ /_       \ \  \    \ \  \|\  \   \ \  \/  / | \  \|\  \ \  \\\  \|___ \  \_| 
#      \|\  \       \ \  \    \ \   __  \   \ \    / / \ \  \\\  \ \  \\\  \   \ \  \  
#     __\_\  \       \ \  \____\ \  \ \  \   \/  /  /   \ \  \\\  \ \  \\\  \   \ \  \ 
#    |\_______\       \ \_______\ \__\ \__\__/  / /      \ \_______\ \_______\   \ \__\
#    \|_______|        \|_______|\|__|\|__|\___/ /        \|_______|\|_______|    \|__|
#                                         \|___|/                                      
                                                                                      
                                                                                      
                                                                                                                                                     






#import psutil

#GUI Functions

def configure_canvas(event, canvas, frame_id):
    canvas.itemconfig(frame_id, width=canvas.winfo_width())

def configure_frame(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def delete_widget(widget):
    children = list(widget.children.values())
    for child in children:
        delete_widget(child)
    widget.pack_forget()
    widget.destroy()
    del widget

def new_rows():
    global index
    index += 1
    layout_frame = [[sg.Text("Hello World"), sg.Push(), sg.Button('Delete', key=('Delete', index))]]
    return [[sg.Frame(f"Frame {index:0>2d}", layout_frame, expand_x=True, key=('Frame', index))]]

def format_currency(integer):
    """Converts a number of cents to currency format (string) without a dollar sign (2 digits after the decimal)"""
   #print(integer)
    if integer == 0 or integer == "0":
        return "0.00"
    elif str(integer)[0]=="-":
        return f"({integer*(-1)}"[:-2] + "." + f"{(integer*(-1))}"[-2:] + ")"
    else:
        return f"{integer}"[:-2] + "." + f"{integer}"[-2:]





index = 0





menu_def = [
    ['&File',['&New Database','&Open Database','&Save Database', 'Database &Properties','E&xit FOIA(s)']],
    ['&Dashboard',['&Go to Dashboard']],
    ['&Applications',['&View Applications']],
    ['&Letters',['&View Letters','&Templates']],
    ['&Stakeholders',['View Re&questers','View &Applicants','View &Responders']],
    ['&Help',['&Documentation', '&About']]
]


application_information_labels_width = 20

edit_windows_border_width = 0

view_window_labels_pad = 2






#-----------------Dashboard Setup----------------


total_squestered_layout = [
    [sg.Text(f"""Carbon Sequestered""", size=(35,1), font=("",small_print), enable_events=True, key="-Dashboard_Sequestered-", justification="center", background_color=overview_information_color)],
    [sg.Text(f"""0""", size=(35,1), font=("",small_print), enable_events=True, key="-Dashboard_Sequestered_Number-", justification="center", background_color=overview_information_color)],
]

today_received_layout = [
    [sg.Text(f"""Action Items Today""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Action_Today-", justification="center", background_color=overview_information_color)],
    [sg.Text(f"""0""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Action_Today_Number-", justification="center", background_color=overview_information_color)],
]

today_sent_layout = [
    [sg.Text(f"""Letters Sent Today""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Sent_Today-", justification="center", background_color=overview_information_color)],
    [sg.Text(f"""0""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Sent_Today_Number-", justification="center", background_color=overview_information_color)],
]

month_sent_layout = [
    [sg.Text(f"""Letters Sent This Month""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Sent_This_Month-", justification="center", background_color=overview_information_color)],
    [sg.Text(f"""0""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Sent_This_Month_Number-", justification="center", background_color=overview_information_color)],
]

year_sent_layout = [
    [sg.Text(f"""Letters Sent This Year""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Sent_This_Year-", justification="center", background_color=overview_information_color)],
    [sg.Text(f"""0""", size=(35,1), font=("",small_print), enable_events=True, key="-Letters_Sent_This_Year_Number-", justification="center", background_color=overview_information_color)],
]

dashboard_column_layout = [
    [sg.Frame("",layout=total_squestered_layout, background_color=overview_information_color)],
    [sg.Frame("",layout=today_received_layout, background_color=overview_information_color)],
    [sg.Frame("",layout=today_sent_layout, background_color=overview_information_color)],
    [sg.Frame("",layout=month_sent_layout, background_color=overview_information_color)],
    [sg.Frame("",layout=year_sent_layout, background_color=overview_information_color)],
    [sg.Image(source=foia_session.logo, size=(230,221))],

]

#Create the chart of accounts display
foia_session.db_name = "Welcome to FOIA(s)"
dashboard_action_letters_layout = [
    [sg.Table(values=[],row_height=36, bind_return_key=True, col_widths=[12,27,27,12], cols_justification=["c","c","c","c"], auto_size_columns=False, headings=["Letter_ID", "Applicant Name", "Responder Name", "Status"], num_rows=25, expand_x=True, expand_y=True, font=("",medium_print), enable_events=False, justification="Center", key="-Dashboard_Display_Content-", background_color=detailed_information_color)],
]

applicants_frame_layout = [
    [sg.Text(f"""{foia_session.db_name}:\nAction Items""", size=(50,2), justification = "center", expand_x = True, expand_y=True,  font=("",medium_print), enable_events=True, key="-Chart_Of_Accounts_Header-")],
    #[sg.Column([[]],element_justification="center", justification="center")],
    [sg.Frame(f"""""", layout=dashboard_action_letters_layout, expand_x = True, expand_y=True, key="-Dashboard_Content_Frame-", size=(940,600), element_justification="Center", background_color=overview_information_color)],
    #[sg.Push(), sg.OptionMenu(values=["All Accounts","10 Assets","11 Expenses", "12 Withdrawals", "13 Liabilities", "14 Owner Equity", "15 Revenue"], enable_events=True, auto_size_text=True, default_value="All Accounts",key="-Account_Type_Picker-"), sg.Button("View Account", key="-View_Account_Button-", disabled=False), sg.Button("Delete Account", key="-Delete_Account_Button-", disabled=True), sg.Button("New Account", key="-New_Account_Button-", disabled=False)],
#expand_x = True, expand_y=True,
]

dashboard_column_layout_2 = [
    [sg.Column(applicants_frame_layout, size= (900,720), expand_x=True, expand_y=True)]
]

#-----------------TABS----------------

# _________  ________  ________  ________      
#|\___   ___\\   __  \|\   __  \|\   ____\     
#\|___ \  \_\ \  \|\  \ \  \|\ /\ \  \___|_    
#     \ \  \ \ \   __  \ \   __  \ \_____  \   
#      \ \  \ \ \  \ \  \ \  \|\  \|____|\  \  
#       \ \__\ \ \__\ \__\ \_______\____\_\  \ 
#        \|__|  \|__|\|__|\|_______|\_________\
#                                  \|_________|
                                    
                                                         
                                                         
                                                         
                                 
dashboard_tab = [
    [sg.Column(dashboard_column_layout),sg.Column(dashboard_column_layout_2, expand_x=True, expand_y=True)],
]



reports_tab = [
    [sg.Text(font=("",medium_print), size=(133,1))],
    [sg.Text("Analysis Reports")],
]

view_application_labels_layout = [
    #[sg.Text(f"",font=("",medium_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Text(f"Application: ",font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Application_Number_Display-")],
    [sg.Text(f"Requester: ",font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad+4),justification="left", background_color=overview_information_color, key="-Application_Requester_Display-")],
    [sg.Text(f"Responder: ", font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad+4),justification="left", background_color=overview_information_color, key="-Application_Responder_Display-")],
    [sg.Text(f"Applicant: ", font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Application_Applicant_Display-")],
#    [sg.Text(f"Documents: ", font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Application_Documents_Display-")],
#    [sg.Text(f"Requests: ",font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad), justification="left", background_color=overview_information_color, key="-Application_Requests_Display-")],
    [sg.Text(f"Created: ", font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad+1),justification="left", background_color=overview_information_color, key="-Application_Created_Display-")],
    [sg.Text(f"Edited: ", font=("",small_print), size=(application_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Application_Edited_Display-")],
]




view_application_edit_layout = [
    #[sg.Text(f"",font=("",medium_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Input(f"ACN-APP-10000", pad=view_window_labels_pad+1, font=("",small_print), size=(application_information_labels_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Application_Number_Input-")],    
    [sg.OptionMenu([f"None"], enable_events=True, size=(16,1),key="-Application_Requester_Input-")],
    [sg.OptionMenu([f"None"], enable_events=True, size=(16,1),key="-Application_Responder_Input-")],
    [sg.OptionMenu([f"None"], enable_events=True, size=(16,1),key="-Application_Applicant_Input-")],
    [sg.Input(f"Created Time", pad=view_window_labels_pad+1, font=("",small_print), size=(application_information_labels_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Application_Created_Input-")],
    [sg.Input(f"Edited Time", pad=view_window_labels_pad+1, font=("",small_print), size=(application_information_labels_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Application_Edited_Input-")],
]





view_applications_column_height = len(view_application_labels_layout)*26

application_doc_table_layout = [
    [sg.Table([[f""]],row_height=20, col_widths=[26], cols_justification=["c"], auto_size_columns=False, headings=["Document Number"], num_rows=4, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, justification="Center", key="-Application_Documents_Display-", background_color=detailed_information_color)],
]

application_req_table_layout = [
    [sg.Table([[f""]], row_height=20, col_widths=[26], cols_justification=["c"], auto_size_columns=False, headings=["Request"], num_rows=4, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, justification="Center", key="-Application_Requests_Display-", background_color=detailed_information_color)],

]

common_requests = ["A list or index of followup actions.","Hearing Dates","Meeting Notes","Document Text","Document List or Index","Evidence Documentation", "Photographs", "Supporting Depositions","Stenographic Notes","Hearing Summaries","911 Audio", "Call Audio", "Audio", "Video", "Bodycam Footage", "Dashcam Footage", "Electronic Media","Witness Statements"]

common_requests.sort()

view_applications_frame_layout = [
    [sg.Column(layout=view_application_labels_layout, justification = "left", background_color=overview_information_color, size=(80,view_applications_column_height)), sg.Column(layout=view_application_edit_layout, justification = "left", background_color=overview_information_color, size=(160,view_applications_column_height) )],
    [sg.Input("",key='-Application_Document_Input-',size=(22,1)),sg.Button("Add Doc", key='-Application_Add_Document_Button-')],
    [sg.Column(layout=application_doc_table_layout,size=(275,120),background_color=overview_information_color)],
    [sg.Button("↑Delete Doc↑",key='-Application_Delete_Document_Button-'),sg.Text("_/¯", font=("",18), background_color=overview_information_color),sg.Button("↓Delete Req↓",key='-Application_Delete_Request_Button-')],
    [sg.Text("Requests:",background_color=overview_information_color),sg.Push(background_color=overview_information_color),sg.OptionMenu(common_requests, enable_events=True, key="-Application_Common_Requests_Input-", size=(20,1))],
    [sg.Input("",key='-Application_Requests_Input-',size=(22,1)),sg.Button("Add Req", key='-Application_Add_Request_Button-')],  
    [sg.Column(layout=application_req_table_layout,size=(275,120),background_color=overview_information_color)],
    [sg.Text(f"Notes:", font=("",small_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Multiline(f"", font=("",medium_print), autoscroll=True, size=(application_information_labels_width*2,3),justification="left", background_color=detailed_information_color, key="-Application_Notes_Display-")],
    [sg.Push(background_color=overview_information_color),sg.OptionMenu(["None"], key="-Application_Template_Input-", enable_events=True, size=(20,1)), sg.Button(f"Generate", disabled=True,  key="-Application_Generate_Button-")],
    [sg.FileBrowse("Attach Record",size=(20,1), enable_events=True, target='-Application_Record_Input-', key='-Application_Record_Input-'),sg.Button("View",size=(5,1),key='-Application_Record_Button-'),],
]



view_applications_tab_column_1 = [
    [sg.Frame("Application: ", layout=view_applications_frame_layout, size=(275,745),font=("",medium_print,"bold"), key="-view_applications_Frame-", background_color=overview_information_color)],
]
view_applications_tab_column_2 = [
    [sg.Table(values=[],row_height=36, col_widths=[14,28,42,12], cols_justification=["c","c","c","c"], auto_size_columns=False, headings=["Application_ID", "Applicant", "Letters", "Date"], num_rows=16, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, justification="Center", key="-Applications_Content-", background_color=detailed_information_color)],
    [sg.Push(),sg.Input("",(20,1),disabled=True, enable_events=True, key="-Application_Search_Input-"),sg.Button("New Application",enable_events=True, key="-New_Application_Button-"),sg.Button("Cancel", key="-Application_Cancel_Button-"),sg.Text(" ")],
]


applications_tab = [
    #[sg.Text(font=("",medium_print), size=(133,1), justification="center")],
    [sg.Column(view_applications_tab_column_1, size=(280,755), element_justification="left"), sg.Column(view_applications_tab_column_2, size=(960,755), element_justification="center", expand_x=True, expand_y=False)],
]


current_time_info = get_current_time_info()


application_messages_layout = [
    [sg.Text(foia_session.current_console_messages[0], size=(120,5), background_color=overview_information_color, key="-Console_Log-", font=("",medium_print), expand_x=True, expand_y=True)],
    ]


console_frame_layout = [
    [sg.Frame("Console", size=(1228,200), expand_x=True, expand_y=False, layout=application_messages_layout, background_color=overview_information_color, pad=4, element_justification="center", key='-Console_Frame_Layout-')] 
]


view_properties_tab = [
    [sg.Text("Organization Name:", font=("",medium_print)), sg.Push(), sg.Input(size=(30,1), key=f"-edit_db_name-", font=("", medium_print))],
    [sg.Text("Address"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Organization_Address-",)],
    [sg.Text("Logo"), sg.Push(), sg.Image("./WalrusCarpenter_StarryNight.png",size=(250,250),key=f"-Edit_Organization_Logo-",)],
    [sg.Text("Acronym:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Organization_Acronym-",)],
    [sg.Text("Manager First Name:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Manager_First-",)],
    [sg.Text("Manager Middle Name:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Manager_Middle-",)],
    [sg.Text("Manager Last Name:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Manager_Last-",)],
    [sg.Text("Manager Preferred Name:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Manager_Preferred-",)],
    [sg.Text("Manager Full Name:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Manager_Full-",)],    
    [sg.Text("Manager Title:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Manager_Title-",)],
    [sg.Text("Phone Number: "), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Organization_Phone-",)],
    [sg.Text("Email: "), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Organization_Email-",)],
    [sg.Text("Documents Repository: "), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Documents_Repository-",)],
    [sg.Multiline("Notes: ", size=(62,9),key=f"-Edit_Organization_Notes-",)],
    [sg.Push(),sg.Button("Save Changes", size=(16,1), font=("", medium_print), enable_events=True, key="-Save_Revised_Properties-")],

]
view_timekeeping_tab = [
    [sg.Text("Organization Name:", font=("",medium_print)), sg.Push(), sg.Input(size=(30,1), key=f"-edit_db_name-", font=("", medium_print))],
    [sg.Text("Address"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Requester_Address-",)],
    [sg.Text("Owner or Financial Officer Name:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Requester_Officer-",)],
    [sg.Text("Title or Position:"), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Requester_Officer_Title-",)],
    [sg.Text("Phone Number: "), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Requester_Phone-",)],
    [sg.Text("Email: "), sg.Push(), sg.Input("",(25,1),key=f"-Edit_Requester_Email-",)],
    [sg.Text("Photo: "), sg.Push(), sg.Image(foia_session.logo,size=(220,220),key=f"-Requester_Photo-",)],
    [sg.Push(), sg.FileBrowse("Select Photo",size=(16,1),key=f"-Edit_Requester_Photo-",)],
    [sg.Multiline("Notes: ", size=(62,9),key=f"-Edit_Requester_Notes-",)],

]
letters_information_labels_width = 13

letters_information_width = 40- letters_information_labels_width

view_letters_labels_layout = [
    [sg.Text(f"Letter No: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Letter_ID_Display-")],
    [sg.Text(f"Date: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Letter_Date_Display-")],
    [sg.Text(f"To: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Letter_To_Display-")],
    [sg.Text(f"From: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Letter_From_Display-")],
    [sg.Text("",background_color=overview_information_color,font=("",10))],
    [sg.Text(f"Document: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Letter_Document_Display-")],
    [sg.Text(f"Request: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Letter_Request_Display-")],    
    [sg.Text(f"Recorded: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Ledger_Recorded_Display-")],
    [sg.Text(f"Edited: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Ledger_Edited_Display-")],
]
#sg.Multiline("",size=(12,3), disabled=True, no_scrollbar=True,rstrip=False,write_only=False,key=f"-Letter_To_Input-",)
#sg.Multiline("",size=(12,3), disabled=True, no_scrollbar=True,rstrip=False,write_only=False,key=f"-Letter_From_Input-",)

view_letters_edit_layout = [
    #[sg.Text(f"",font=("",medium_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Letter_ID_Input-")],    
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Letter_Date_Input-")],  
    [sg.OptionMenu([""],enable_events= True, key="-Letter_To_Input-",size=(16,1))],
    [sg.OptionMenu([""],enable_events= True, key="-Letter_From_Input-",size=(16,1))],
    [sg.Text("",background_color=overview_information_color,font=("",2))],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Letter_Document_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Letter_Request_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Letter_Recorded_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Letter_Edited_Input-")],

]

#default_logo = Image.open("50666888.jpg")
#default_logo.save("50666888.png")
view_letters_column_height = 215

view_letters_frame_layout = [
    [sg.Column(layout=view_letters_labels_layout, justification = "left", background_color=overview_information_color, size=(letters_information_labels_width*5,view_letters_column_height+15)), sg.Column(layout=view_letters_edit_layout, justification = "left", background_color=overview_information_color, size=(letters_information_width*9,int(view_letters_column_height+15)) )],
    [sg.OptionMenu([""], enable_events=True,disabled=True, size=(16,1), key="-Letter_Template_Input-"),sg.Button("Use Template", disabled=True, key="-Letter_Template_Button-")],
    #[sg.Combo(["Template 1","Template 2", "Template 3"],pad=view_window_labels_pad+1,font=("",small_print), size=(application_information_labels_width,1),background_color="white", key="-Letter_Template_Input-"),sg.Button("Use Template", key="-Letter_Template_Button-")],
    [sg.Multiline(f"['-Message-']", disabled=True, font=("",medium_print), autoscroll=True, size=(application_information_labels_width*2,2),justification="left", background_color=overview_information_color, key="-Letter_Message_Display-")],
    [sg.Image(foia_session.logo, key="-Letter_Image-", subsample=12, size=(193,250),enable_events=False)],#subsample=4, right_click_menu=["View Letter PDF"],
    [sg.FileBrowse('Select pdf or image',disabled=True, enable_events=True, key='-Letter_Image_Input-')],
    [sg.Push(background_color=overview_information_color),sg.Text("↕",pad=0,background_color=overview_information_color),sg.Button(button_text=f"Message", disabled=True, key="-Message_View_Button-"), sg.Text("↕",pad=0,background_color=overview_information_color),sg.Button(button_text=f"Letter", disabled=True, key="-Letter_View_Button-"), sg.Button(f"Generate", disabled=True,  key="-Letter_Generate_Button-")],
]
    


view_letters_tab_column_1 = [
    [sg.Frame("Letter: ", layout=view_letters_frame_layout, size=(275,800),font=("",medium_print,"bold"), key="-View_Letter_Frame-", background_color=overview_information_color)],
]
view_letters_tab_column_2 = [
    [sg.Table(values=[],row_height=36, col_widths=[14,14,20,20,20,14], cols_justification=["c","c","c","c","c","c"], auto_size_columns=False, header_font=("",small_print),headings=["Letter No.","Status","Responder", "Applicant", "Requester", "Date"], num_rows=18, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, key="-Letters_Display_Content-", background_color=detailed_information_color)],
    [sg.Push(),sg.Input("",(20,1),disabled=False, enable_events=True, key="-Letters_Search_Input-"),sg.Button("New Letter",enable_events=True, key="-New_Letter_Button-"), sg.Button("Cancel", key="-Letter_Cancel_Button-"), sg.Text(" ")],

]

view_requesters_labels_layout = [
    [sg.Text(f"First Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_FirstName_Display-")],
    [sg.Text(f"Middle Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_MiddleName_Display-")],
    [sg.Text(f"Last Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_LastName_Display-")],
    [sg.Text(f"Full Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_FullName_Display-")],
    [sg.Text(f"Preferred: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_PreferredName_Display-")],
    [sg.Text(f"Address: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_ReturnAddress_Display-")],
    [sg.Text(f"", font=("",10), background_color=overview_information_color)],
    [sg.Text(f"Phone: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_Phone_Display-")],
    [sg.Text(f"Email: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_Email_Display-")],
    #[sg.Text(f"Recorded: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_Recorded_Display-")],
    #[sg.Text(f"Edited: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Requester_Edited_Display-")],
]

view_requesters_edit_layout = [
    #[sg.Text(f"",font=("",medium_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_FirstName_Input-")],    
    [sg.Input(f"", pad=view_window_labels_pad+1,font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_MiddleName_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_LastName_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_FullName_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_PreferredName_Input-")],
    [sg.Multiline("",size=(25,3), disabled=True,no_scrollbar=True,rstrip=False,key=f"-Requester_ReturnAddress_Input-",)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_Phone_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_Email_Input-")],
    [sg.Input(f"", visible=False, pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_Recorded_Input-")],
    [sg.Input(f"", visible=False, pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, disabled=True, key="-Requester_Edited_Input-")],

]


view_requesters_frame_layout = [
    [sg.Input(f"Requester ID", font=("",small_print), size=(30,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Requester_ID_Display-")],    
    [sg.Column(layout=view_requesters_labels_layout, justification = "left", background_color=overview_information_color, size=(letters_information_labels_width*7-14,view_letters_column_height+20)), sg.Column(layout=view_requesters_edit_layout, justification = "left", background_color=overview_information_color, size=(letters_information_width*7,int(view_letters_column_height)+20) )],
    [sg.Text(f"Notes: ", font=("",small_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Multiline(f"", font=("",medium_print), autoscroll=True, size=(application_information_labels_width*2,3),justification="left", background_color=detailed_information_color, key="-Requester_Notes_Display-")],
    [sg.Image(foia_session.logo, key="-Requester_Photo_Display-", size=(240,240), subsample=4)],#subsample=4,
    [sg.FileBrowse(disabled=True, enable_events=True, key='-Requester_Photo_Input-')],
    [sg.Push(background_color=overview_information_color), sg.Button(f"Edit Requester", disabled=True,  key="-Edit_Requester_Button-")],
    
]
    #,  sg.Button(f"Clock In", disabled=True,  key="-Requester_Clock_Button-")
view_requesters_tab_column_1 = [
    [sg.Frame("Requester: ", layout=view_requesters_frame_layout, size=(275,755),font=("",medium_print,"bold"), key="-View_Requesters_Frame-", background_color=overview_information_color)],
]
view_requesters_tab_column_2 = [
    [sg.Table(values=[],row_height=36, col_widths=[12,30,12,18,30], cols_justification=["c","c","c","c","c"], auto_size_columns=False, header_font=("",small_print),headings=["Requester_ID", "Preferred Name", "Open Letters", "Phone", "Email"], num_rows=18, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, key="-Requesters_Display_Content-", background_color=detailed_information_color)],
    [sg.Push(), sg.Input("",(20,1),disabled=False, enable_events=True, key="-Requesters_Search_Input-"),sg.Button("New Requester",enable_events=True, key="-New_Requester_Button-"), sg.Button("Cancel",key="-Cancel_New_Requester_Button-"),  sg.Text(" ")],

]
#Title

view_applicants_labels_layout = [
    [sg.Text(f"Applicant ID: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_ID_Display-")],
    [sg.Text(f"First Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_FirstName_Display-")],
    [sg.Text(f"Middle Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_MiddleName_Display-")],
    [sg.Text(f"Last Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_LastName_Display-")],
    [sg.Text(f"Title: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_Title_Display-")],
    [sg.Text(f"Full Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_FullName_Display-")],
    [sg.Text(f"Preferred Name: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_PreferredName_Display-")],   
    [sg.Text(f"Return Address: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="--")],
    [sg.Text("",background_color=overview_information_color, font=("",12))],
    [sg.Text(f"Email: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_Email_Display-")],   


    #[sg.Text("",background_color=overview_information_color,font=("",14))],
    [sg.Text(f"Phone: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_Phone_Display-")],
    [sg.Text(f"Recorded: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_Recorded_Display-")],
    [sg.Text(f"Edited: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Applicant_Edited_Display-")],
]

view_applicants_edit_layout = [
    #[sg.Text(f"",font=("",medium_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_ID_Input-")],    
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_FirstName_Input-")],    
    [sg.Input(f"", pad=view_window_labels_pad+1,font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_MiddleName_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_LastName_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_Title_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_FullName_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_PreferredName_Input-")],
    [sg.Multiline("",size=(25,3), disabled=True,no_scrollbar=True,rstrip=False,write_only=False,key=f"-Applicant_ReturnAddress_Input-",)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_Email_Input-")],
    #[sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_ReturnAddress_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_Phone_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_Recorded_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_Edited_Input-")],

]




view_applicants_frame_layout = [
    #[sg.Input(f"Applicant ID", font=("",medium_print), size=(30,1),justification="center", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Applicant_ID_Display-")],    
    [sg.Column(layout=view_applicants_labels_layout, justification = "left", background_color=overview_information_color, size=(letters_information_labels_width*7,315)), sg.Column(layout=view_applicants_edit_layout, justification = "left", background_color=overview_information_color, size=(letters_information_width*7,315) )],
    [sg.Text(f"Notes: ", font=("",small_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Multiline(f"", font=("",medium_print), autoscroll=True, size=(application_information_labels_width*2,4),justification="left", background_color=detailed_information_color, key="-Applicant_Notes_Display-")],
    [sg.Push(background_color=overview_information_color),  sg.Button(f"Edit Applicant", disabled=True,  key="-Edit_Applicant_Button-")],
]

view_applicants_tab_column_1 = [
    [sg.Frame("Applicant: ", layout=view_applicants_frame_layout, size=(275,755),font=("",medium_print,"bold"), key="-View_Applicants_Frame-", background_color=overview_information_color)],
]

view_applicants_tab_column_2 = [
    [sg.Table(values=[],row_height=36, col_widths=[12,24,24,18,24], cols_justification=["c","c","c","c","c"], auto_size_columns=False, header_font=("",small_print),headings=["Applicant_ID", "Preferred Name", "Open Letters", "Phone", "Email"], num_rows=18, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, key="-Applicants_Display_Content-", background_color=detailed_information_color)],
    [sg.Push(),sg.Input("",(20,1),disabled=False, enable_events=True, key="-Applicants_Search_Input-"),sg.Button("New Applicant",enable_events=True, key="-New_Applicant_Button-"),sg.Button("Cancel",enable_events=True, disabled=False, key="-Applicant_Cancel_Button-"),sg.Text(" ")],
]

view_responders_labels_layout = [
    [sg.Text(f"Responder_ID: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_ID_Display-")],
    [sg.Text(f"Org Name: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Org_Name_Display-")],
    [sg.Text(f"Org Type: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Org_Type_Display-")],
    [sg.Text(f"Contact First: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Contact_First_Display-")],
    [sg.Text(f"Contact Last: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Contact_Last_Display-")],
    [sg.Text(f"Contact Email: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Contact_Email_Display-")],
    [sg.Text(f"Preferred Name: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Contact_Preferred_Display-")],
    [sg.Text(f"Phone: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Phone_Display-")],
    [sg.Text(f"Phone Type: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Phone_Type_Display-")],
    [sg.Text(f"Fax: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Fax_Display-")],
    [sg.Text(f"Address: ", font=("",small_print), size=(letters_information_labels_width+1,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_ReturnAddress_Display-")],
    [sg.Text("",background_color=overview_information_color,font=("",11))],
    [sg.Text(f"Mailing Address: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_MailingAddress_Display-")],
    [sg.Text("",background_color=overview_information_color,font=("",11))],
    [sg.Text(f"Email: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Email_Display-")],
    [sg.Text(f"Website: ", font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Website_Display-")],
    [sg.Text(f"Recorded: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Recorded_Display-")],
    [sg.Text(f"Edited: ",font=("",small_print), size=(letters_information_labels_width,1),pad=(0, view_window_labels_pad),justification="left", background_color=overview_information_color, key="-Responder_Edited_Display-")],
]

view_responders_edit_layout = [
    #[sg.Text(f"",font=("",medium_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_ID_Input-")],    
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Org_Name_Input-")],    
    [sg.Input(f"", pad=view_window_labels_pad+1,font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Org_Type_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Contact_First_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Contact_Last_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Contact_Email_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Contact_Preferred_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Phone_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Phone_Type_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Fax_Input-")],
    [sg.Multiline("",size=(25,3), disabled=True,no_scrollbar=True,rstrip=False,write_only=False,key=f"-Responder_ReturnAddress_Input-",)],
    [sg.Multiline("",size=(25,3), disabled=True,no_scrollbar=True,rstrip=False,write_only=False,key=f"-Responder_MailingAddress_Input-",)],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Email_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Website_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Recorded_Input-")],
    [sg.Input(f"", pad=view_window_labels_pad+1, font=("",small_print), size=(letters_information_width-1,1),justification="left", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_Edited_Input-")],

]
responders_column_height = 400

view_responders_frame_layout = [
    [sg.Input(f"Responder ID", font=("",medium_print), size=(30,1),justification="center", disabled_readonly_background_color=overview_information_color, background_color="white", border_width=edit_windows_border_width, readonly=True, key="-Responder_ID_Display-")],    
    [sg.Column(layout=view_responders_labels_layout, justification = "left", background_color=overview_information_color, size=(letters_information_labels_width*7,responders_column_height)), sg.Column(layout=view_responders_edit_layout, justification = "left", background_color=overview_information_color, size=(letters_information_width*7,responders_column_height) )],
    [sg.Text(f"Notes: ", font=("",small_print), size=(application_information_labels_width,1),justification="left", background_color=overview_information_color)],
    [sg.Multiline(f"", font=("",medium_print), autoscroll=True, size=(application_information_labels_width*2,4),justification="left", background_color=detailed_information_color, key="-Responder_Notes_Display-")],
    [sg.Push(background_color=overview_information_color),  sg.Button(f"Edit Responder", disabled=True,  key="-Edit_Responder_Button-")],
]


view_responders_tab_column_1 = [
    [sg.Frame("Responder: ", layout=view_responders_frame_layout, size=(275,755),font=("",medium_print,"bold"), key="-View_Responders_Frame-", background_color=overview_information_color)],
]

view_responders_tab_column_2 = [
    [sg.Table(values=[],row_height=36, col_widths=[12,24,18,18,30], cols_justification=["c","c","c","c","c"], auto_size_columns=False, header_font=("",small_print),headings=["Responder_ID", "Organization Name", "Open Letters", "Phone", "Email"], num_rows=18, expand_x=True, expand_y=True, font=("",medium_print), enable_events=True, key="-Responders_Display_Content-", background_color=detailed_information_color)],
    [sg.Push(),sg.Input("",(20,1),disabled=False, enable_events=True, key="-Responders_Search_Input-"),sg.Button("New Responder",enable_events=True, key="-New_Responder_Button-"),sg.Button("Cancel",enable_events=True, disabled=False, key="-Responders_Cancel_Button-"),sg.Text(" ")],
]

#Be sure to update tags here and in the load_selected_template function
template_tags = [
    r"['-Applicant_Preferred_Name-']",
    r"['-Applicant_First_Name-']",
    r"['-Applicant_Middle_Name-']",
    r"['-Applicant_Last_Name-']",
    r"['-Applicant_Title-']",
    r"['-Applicant_Full_Name-']",
    r"['-Applicant_Phone_Number-']",
    r"['-Applicant_Phone_Number_Type-']",
    r"['-Applicant_Fax_Number-']",
    r"['-Applicant_Return_Address-']",
    r"['-Applicant_Notes-']",
    r"['-Applicant_Email-']",
    r"['-Application_Number-']",
    r"",
    r"['-new_line-']",
    r"",
    r"['-Requested_Document-']",
    r"['-Requested_Records-']",
    r"",
    r"['-Letter_From_Field-']",
    r"['-Requester_Email-']",
    r"['-Requester_Phone-']",
    r"['-Requester_Phone_Number_Type-']",
    r"['-Requester_Preferred_Name-']",   
    r"['-Requester_First_Name-']",   
    r"['-Requester_Middle_Name-']",   
    r"['-Requester_Last_Name-']",   
    r"['-Requester_Full_Name-']",   
    r"['-Requester_Return_Address-']",   
    r"['-Requester_Fax_Number-']",   
    r"['-Requester_Notes-']",    
    r"['-Organization_Name-']" 
    r"",
    r"['-Letter_To_Field-']",
    r"['-Responder_Preferred_Name-']",
    r"['-Responder_Organization_Name-']",
    r"['-Responder_Organization_Type-']",
    r"['-Responder_Contact_First_Name-']",
    r"['-Responder_Contact_Last_Name-']",
    r"['-Responder_Contact_Email-']",
    r"['-Responder_Phone_Number-']",
    r"['-Responder_Phone_Number_Type-']",
    r"['-Responder_Fax_Number-']",
    r"['-Responder_Organization_Address-']",
    r"['-Responder_Organization_Mailing_Address-']",
    r"['-Responder_Organization_Email-']",
    r"['-Responder_Organization_Website-']",
    r"['-Responder_Notes-']",

]



templates_frame_layout = [
    [sg.Table(values=[],row_height=24, col_widths=[20], cols_justification=["c"],auto_size_columns=True, header_font=("",small_print),headings=["       Template Name       "], num_rows=8, font=("",medium_print), enable_events=True, key="-Templates_List-", background_color=detailed_information_color)],
    [sg.Push(background_color=overview_information_color),sg.Text("Search:",background_color=overview_information_color),sg.Input("",(20,1),disabled=False, enable_events=True, key="-Templates_Search_Input-")],
    [sg.Push(background_color=overview_information_color),sg.OptionMenu(values=template_tags,size=(30,1),enable_events=True, key="-Templates_Tag_Input-")],
    [sg.Text("Notes:",background_color=overview_information_color)],
    [sg.Multiline(f"", font=("",medium_print), enable_events=True, autoscroll=True, size=(30,4),justification="left", background_color=detailed_information_color, key="-Templates_Notes_Display-")],
    [sg.Push(background_color=overview_information_color),sg.Text("Name Template:",background_color=overview_information_color),sg.Input("",(20,1),disabled=True, enable_events=True, key="-Templates_Name_Input-")],
]


template_tab_column_1 = [
    [sg.Frame("Template: ", layout=templates_frame_layout, size=(275,700),font=("",medium_print,"bold"), key="-Templates_Frame-", background_color=overview_information_color)],
]

template_tab_column_2 = [
    [sg.Multiline("Select a template to get started.", size=(130,50), enable_events=True, key="-Templates_Edit_Content-", background_color=overview_information_color)],
    [sg.Push(),sg.Button("Preview", key="-Template_Preview_Button-"),sg.Button("New Template",enable_events=True, key="-New_Template_Button-"),sg.Button("Cancel",enable_events=True, disabled=False, key="-Templates_Cancel_Button-"),sg.Text(" ")],
]



while False:
    applications_tab = [
        [sg.Text(f"Applications: None", expand_x=True, font=("",medium_print), justification="center", key="-Applications_Display-")],
    ]

letters_tab = [
    [sg.Column(view_letters_tab_column_1, size=(280,775), element_justification="left"), sg.Column(view_letters_tab_column_2, size=(960,775), element_justification="center", expand_x=True, expand_y=False)],
]

responses_tab = [
    [sg.Text(f"Responses: None", expand_x=True, font=("",medium_print), justification="center", key="-Responses_Display-")],
]
forwarding_tab = [
    [sg.Text(f"Forwarding: None", expand_x=True, font=("",medium_print), justification="center", key="-Forwarding_Display-")],
]

templates_tab = [
    [sg.Column(template_tab_column_1, size=(280,755), element_justification="left"),sg.Column(template_tab_column_2, size=(960,755), element_justification="left")],
]


requesters_time_tab = [
    [sg.Column(view_requesters_tab_column_1, size=(280,755), element_justification="left"), sg.Column(view_requesters_tab_column_2, size=(960,755), element_justification="center", expand_x=True, expand_y=False)],
]
timekeeping_records_tab = [
    [sg.Text(f"Timekeeping Records: None", expand_x=True, font=("",medium_print), justification="center", key="-Timekeeping_Records_Display-")],
]

documentation_tab = [
    [sg.Text("")],
    [sg.Text("readme.pdf:   "),sg.Button(f"View Documentation", expand_x=True, font=("",medium_print), key="-Documentation_Button-")],
]


about_tab = [
    [sg.Text(f"About FOIA(s): \nVersion 1.02 (Blackbird)\n\nDeveloped in the United States by Joseph M. Basile \n\nSpecial Thanks to Kevin D. Hall and the Python, GitHub, and PySimpleGUI Communities \n\nDonations and Complaints Appreciated \nPayPal: josephmbasile@gmail.com \n\nMIT License 2024", expand_x=True, font=("",medium_print), justification="center", key="-Timekeeping_Records_Display-")],
]


applicants_tab = [
    [sg.Column(view_applicants_tab_column_1, size=(280,755), element_justification="left"), sg.Column(view_applicants_tab_column_2, size=(960,755), element_justification="center", expand_x=True, expand_y=False)],
]


responders_tab = [
    [sg.Column(view_responders_tab_column_1, size=(280,755), element_justification="left"), sg.Column(view_responders_tab_column_2, size=(960,755), element_justification="center", expand_x=True, expand_y=False)],
]
 


#-------------Overall Layout------------------------
# _____ ______   ________  ___  ________           ___       ________      ___    ___ ________  ___  ___  _________   
#|\   _ \  _   \|\   __  \|\  \|\   ___  \        |\  \     |\   __  \    |\  \  /  /|\   __  \|\  \|\  \|\___   ___\ 
#\ \  \\\__\ \  \ \  \|\  \ \  \ \  \\ \  \       \ \  \    \ \  \|\  \   \ \  \/  / | \  \|\  \ \  \\\  \|___ \  \_| 
# \ \  \\|__| \  \ \   __  \ \  \ \  \\ \  \       \ \  \    \ \   __  \   \ \    / / \ \  \\\  \ \  \\\  \   \ \  \  
#  \ \  \    \ \  \ \  \ \  \ \  \ \  \\ \  \       \ \  \____\ \  \ \  \   \/  /  /   \ \  \\\  \ \  \\\  \   \ \  \ 
#   \ \__\    \ \__\ \__\ \__\ \__\ \__\\ \__\       \ \_______\ \__\ \__\__/  / /      \ \_______\ \_______\   \ \__\
#    \|__|     \|__|\|__|\|__|\|__|\|__| \|__|        \|_______|\|__|\|__|\___/ /        \|_______|\|_______|    \|__|
#                                                                        \|___|/                                      
                                                                                                                     
                                                                                                                     



current_time = get_current_time_info()

layout1 = [
    [sg.Menu(menu_def, key="-Program_Menu-")],
    [sg.Text(f"""No Data Loaded""", key="-Load_Messages-", font=("",medium_print), size=(20,1), justification="center", expand_x=True)],
    [sg.Text(current_time[0], key='-Current_Time_Display-', font=("",medium_print), size=(133,1), justification="center", visible=True, expand_x=True)],
    [sg.TabGroup([
        [sg.Tab('Dashboard', layout=dashboard_tab, key='-Dashboard_Tab-')],#0     #Displays Applicants
        [sg.Tab('Applications', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=applications_tab, size=(800,800))]], visible=False, pad=2, key='-View_Applications_Tab-')],#1
        [sg.Tab('Reports', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=reports_tab, size=(800,800))]], visible=False, pad=2, key='-View_Analysis_Tab-')],#2
        [sg.Tab('Letters', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=letters_tab, size=(800,820))]], visible=False, pad=2, key='-View_Letters_Tab-')],#3
        [sg.Tab('Responses', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=responses_tab, size=(800,800))]], visible=False, pad=2, key='-View_Responses_Tab-')],#4
        [sg.Tab('Forwarding', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=forwarding_tab, size=(800,800))]], visible=False, pad=2, key='-View_Forwarding_Tab-')],#5
        [sg.Tab('Requesters', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=requesters_time_tab, size=(800,800))]], visible=False, pad=2, key='-Requesters_Time_Tab-')],#6
        [sg.Tab('Timekeeping Records', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=timekeeping_records_tab, size=(800,800))]], visible=False, pad=2, key='-Timekeeping_Records_Tab-')],#7
        [sg.Tab('Documentation', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=documentation_tab, size=(800,800))]], visible=False, pad=2, key='-Documentation_Tab-')],#8
        [sg.Tab('About FOIA(s)', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=about_tab, size=(800,800))]], visible=False, pad=2, key='-About_Tab-')],#9
        [sg.Tab('Database Properties', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=view_properties_tab, size=(800,800))]], visible=False, pad=2, key='-View_Properties_Tab-')],#10
        [sg.Tab('Templates', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=templates_tab, size=(800,800))]], visible=False, pad=2, key='-Templates_Tab-')],#11    
        [sg.Tab('Applicants', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=applicants_tab, size=(800,800))]], visible=False, pad=2, key='-Applicants_Tab-')],#12
        [sg.Tab('Responders', layout=[[sg.Column(scrollable=False, vertical_scroll_only=True, expand_x=True, expand_y=True, pad=0, layout=responders_tab, size=(800,800))]], visible=False, pad=2, key='-Responders_Tab-')],#13

    ], expand_x=True, expand_y=True, key='-Display_Area-', size=(800,750))   ],
    [sg.Column(console_frame_layout, size=(900,60), expand_x=True, key="-Console_Column-", scrollable=True, vertical_scroll_only=True)], #scrollable=False,
]


def new_database_layout(num):
    num = num + 1
    new_database_layout = [
        [sg.Text("DB & Letter Attributes", justification="center",font=("",medium_print), size=(57,1))],
        [sg.Text("Organization Name:", font=("",medium_print)), sg.In(size=(30,1), key=f"-db_name_{num}-", font=("", medium_print)), sg.Text(".fid", font=("", medium_print))],
        [sg.Push(), sg.Text("Filekey Save Location: ", font=("", medium_print)),sg.FolderBrowse(size=(16,1), enable_events=True, key=f"-Save_Location_{num}-", font=("", medium_print))],
        [sg.Text("Organization Acronym: "), sg.Push(), sg.In("",(5,1),key=f"-Organization_Acronym_{num}-",)],  
        [sg.Text("Address: "), sg.Push(), sg.Multiline("",size=(25,3),no_scrollbar=True,rstrip=False,write_only=False,key=f"-Organization_Address_{num}-",)],
        [sg.Text("Phone Number: "), sg.Push(), sg.In("",(25,1),key=f"-Organization_Phone_{num}-",)],
        [sg.Text("Email: "), sg.Push(), sg.In("",(25,1),key=f"-Organization_Email_{num}-",)],        
        [sg.Text("Manager First Name:"), sg.Push(), sg.In("",(25,1),key=f"-Organization_Manager_First_{num}-",)],
        [sg.Text("Manager Middle Name:"), sg.Push(), sg.In("",(25,1),key=f"-Organization_Manager_Middle_{num}-",)],
        [sg.Text("Manager Last Name:"), sg.Push(), sg.In("",(25,1),key=f"-Organization_Manager_Last_{num}-",)],
        [sg.Text("Title or Position:"), sg.Push(), sg.In("",(25,1),key=f"-Organization_Manager_Title_{num}-",)],
        [sg.Text("Manager Preferred Name:"), sg.Push(), sg.In("",(25,1),key=f"-Organization_Manager_Preferred_{num}-",)],
        [sg.Text("Manager Full Name:"), sg.Push(), sg.In("",(25,1),key=f"-Organization_Manager_Full_{num}-",)],
        [sg.Push(), sg.Text("Documents Respository Location: ", key=f"-Organization_Documents_Repository_Label_{num}-"), sg.FolderBrowse("Documents Folder",font=("",small_print),key=f"-Organization_Documents_Repository_{num}-", enable_events=True)],
        [sg.Push(), sg.Text("Photo or Logo: ", key=f"-Organization_Logo_Label_{num}-"), sg.FileBrowse("Select Image",font=("",small_print),key=f"-Organization_Logo_{num}-", enable_events=True)],
        [sg.Multiline("Notes: ", size=(62,9),key=f"-Organization_Notes_{num}-",)],
        [sg.Column([[sg.Button(button_text="Submit",size=(20,1),key=f'-Submit_New_Database_Button_{num}-', enable_events=True)],[sg.Sizer(460,60)]],justification="center", size=(480,60),element_justification="center",expand_x=True)],
    ]
    
    return new_database_layout, num


def open_database_layout(num):
    num = num + 1
    open_database_layout = [
        [sg.Text("Filekey Save Location: ", font=("", medium_print)),sg.FileBrowse(size=(20,1), enable_events=True, key=f"-Open_File_{num}-", font=("", medium_print))],
        [sg.Button("Open",key=f'-Open_Database_Button_{num}-', enable_events=True)],
    ]
    
    return open_database_layout, num


#  ____                           _                            _       
# |  _ \ ___  _ __  _   _ _ __   | |    __ _ _   _  ___  _   _| |_ ___ 
# | |_) / _ \| '_ \| | | | '_ \  | |   / _` | | | |/ _ \| | | | __/ __|
# |  __/ (_) | |_) | |_| | |_) | | |__| (_| | |_| | (_) | |_| | |_\__ \
# |_|   \___/| .__/ \__,_| .__/  |_____\__,_|\__, |\___/ \__,_|\__|___/
#            |_|         |_|                 |___/                     

def new_letter_layout(num):
    pass

def new_account_layout(num):
    """Layout for a new account window."""

    num = num + 1
    foia_session.num = num

    new_account_column = [
        [sg.Image("CHECKBOOK_ART_FREE_LICENCE_NO_COMMERCIAL.png",size=(50,50),subsample=1),sg.Column([[sg.Sizer(45,0)],[sg.HorizontalLine()],[sg.Sizer(45,0)]],size=(45,16),pad=0,vertical_alignment="center"), sg.Column([[sg.Sizer(200,8)],[sg.Text(f"New Account", size=(13,1), font=("Bold",large_print),justification="center", pad=(0,0), key=f"-Account_Title_{num}-")],[sg.Sizer(200,0)]],pad=0, size=(200,32), element_justification="center", vertical_alignment="top"),sg.Column([[sg.Sizer(120,0)],[sg.HorizontalLine()],[sg.Sizer(120,0)]],size=(120,16),pad=0,vertical_alignment="center")],
        [sg.Text("Account Name: ", font=("",medium_print)), sg.Push(), sg.Input(size=(20,1), key=f"-Account_Name_{num}-", font=("", medium_print) )],
        [sg.Text("Account Type: ", font=("",medium_print)), sg.Push(), sg.Push(), sg.OptionMenu(values=["10 Assets","11 Expenses", "12 Withdrawals", "13 Liabilities", "14 Owner Equity", "15 Revenue"], enable_events=False, auto_size_text=True, default_value="10 Assets",key=f"-Account_Type_Picker_{num}-")],
        [sg.Text("Bank: ", font=("",medium_print)), sg.Push(), sg.Input("",(16,1),key=f"-Account_Bank_{num}-")],
        [sg.Text("Bank Account Type: ", font=("",medium_print)), sg.Push(), sg.Input("",key=f"-Account_Bank_Account_Type_{num}-", size=(16,1), enable_events=False)],
        [sg.Text("Bank Account Number: ", font=("",medium_print)), sg.Push(), sg.Input("",key=f"-Account_Bank_Account_Number_{num}-", size=(16,1), enable_events=False)],
        [sg.Text("Bank Routing: ", font=("",medium_print)), sg.Push(), sg.Input("",key=f"-Account_Bank_Routing_{num}-")],
        [sg.Multiline("Notes: ", font=("",medium_print), size=(44,8),key=f"-Account_Notes_{num}-")],
    ]
    
    

    new_account_layout = [
        [sg.Column(layout=new_account_column,pad=0)],
        [sg.Column([[sg.Button(button_text="Submit",size=(20,1),key=f'-Submit_Account_Button_{num}-', enable_events=True)],[sg.Sizer(480,0)]],justification="center", size=(480,60),element_justification="center",expand_x=True)],
    ]
    
    


    return new_account_layout, num








#------------------------------------------Section 4 Data Functions

# ___   ___          ________ ___  ___  ________   ________ _________  ___  ________  ________   ________      
#|\  \ |\  \        |\  _____\\  \|\  \|\   ___  \|\   ____\\___   ___\\  \|\   __  \|\   ___  \|\   ____\     
#\ \  \\_\  \       \ \  \__/\ \  \\\  \ \  \\ \  \ \  \___\|___ \  \_\ \  \ \  \|\  \ \  \\ \  \ \  \___|_    
# \ \______  \       \ \   __\\ \  \\\  \ \  \\ \  \ \  \       \ \  \ \ \  \ \  \\\  \ \  \\ \  \ \_____  \   
#  \|_____|\  \       \ \  \_| \ \  \\\  \ \  \\ \  \ \  \____   \ \  \ \ \  \ \  \\\  \ \  \\ \  \|____|\  \  
#         \ \__\       \ \__\   \ \_______\ \__\\ \__\ \_______\  \ \__\ \ \__\ \_______\ \__\\ \__\____\_\  \ 
#          \|__|        \|__|    \|_______|\|__| \|__|\|_______|   \|__|  \|__|\|_______|\|__| \|__|\_________\
#                                                                                                  \|_________|
                                                                                                              
                                                                                                              


#Comment out the encryption functions that were moved to db_calls
#Remove when fully depreciated.
if False:
    def generate_filekey(db_name, save_location):
        key = Fernet.generate_key()
        if save_location[-1] != "/":
            save_location = save_location + "/"
        filename = f'{db_name}key'    
        file_address = f'{save_location}{db_name}key'
        with open(file_address, 'wb') as filekey:
            filekey.write(key)#-----------------------------------------------------------------------
        return key, filename

    def encrypt_database(db_name, mode, filename, save_location, new_name):
        """Encrypts or decrypts a database file. 
        Mode is 'encypt' or 'decrypt'. 
        filekey=False will generate a new filekey.
        save_location=False will save to the FOIA(s) directory."""
       #print(f"encrypt db_name {db_name}; mode: {mode}; filename: {filename}; save_location: {save_location}")
        
        db_name_2 = db_name
        if new_name:
            db_name_2 = new_name
        
        if save_location == False or save_location == "" or save_location == ".":
            save_location = "./"
        if save_location[-1] != "/":
            save_location = save_location + "/"
        if filename == False and mode == "encrypt":
            filekey, filename = generate_filekey(db_name, save_location)
        elif filename== False and mode =="decrypt":
            return "Error: Attempted decryption without key.", ""
        if mode == "encrypt":
            with open(f'{save_location}{filename}','rb') as file:
                filekey = file.read()        
            #print('filekey generated')
            #print(filekey)
            fernet=Fernet(filekey)
            with open(f'./{db_name_2}','rb') as file:
                original_db = file.read()
            #print(original_db)
            encrypted_db = fernet.encrypt(original_db)
            with open(f'./{db_name}','wb') as encrypted_file:
                encrypted_file.write(encrypted_db)
            return filekey, filename, save_location
        elif mode == "decrypt":
            with open(f'{save_location}{filename}','rb') as file:
                filekey = file.read()  
            fernet=Fernet(filekey)
            with open(f'./{db_name}','rb') as file:
                original_db = file.read()
           #print(filekey)
            encrypted_db = fernet.decrypt(original_db)
            with open(f'./{db_name_2}','wb') as encrypted_file:
                encrypted_file.write(encrypted_db)
            return filekey, filename, save_location
        else:
            return "Error: Mode not selected. (encrypt or decrypt)", ""


def synchronize_time(window, current_time_display):
    f"""Updates the time the first time after the program is opened. Returns Yes or No on whether the time updates are sychronized with the system time."""
    current_time = get_current_time_info()
    #print(values)
    if current_time_display[0] == current_time[0]:
        #print("Not Synchronized")
        return "No", current_time
    else:
        #print((current_time_display[0]))
        #print((current_time[0]))
        return "Yes", current_time


def update_time(window):
    f"""Updates the time at the top of the program."""
    current_time = get_current_time_info()
    window['-Current_Time_Display-'].update(current_time[0])
    return current_time

def create_database(values, current_console_messages,window, num, current_year):
    """Adds a new database with the name given by the registering user."""

    

    #Create database
    window['-Load_Messages-'].update(values[f"-db_name_{num}-"])
    db_name_1 = values[f"-db_name_{num}-"]
    db_name_2 = ""
    for chara in range(len(db_name_1)):
        if db_name_1[chara] == " " or db_name_1[chara] == "." or db_name_1[chara] == "," or db_name_1[chara] == "/" or db_name_1[chara] == "-" or db_name_1[chara] == "~" or db_name_1[chara] == "'" or db_name_1[chara] == "`":
            db_name_2 = db_name_2 + "_"
        else:
            db_name_2 = db_name_2 + db_name_1[chara]
    foia_session.db_name = db_name_2 + """.fid"""
    #print(foia_session.db_name)
    if foia_session.connection == False:
        foia_session.connection = db.create_connection(f"./{foia_session.db_name}")
        #print(f"460 connection: {foia_session.connection}; {foia_session.db_name}")
    
    year = datetime.datetime.now().year


   #7 Create the Console_Log Table
    create_table_6_query = f"""CREATE TABLE tbl_Console_Log (Log_ID INTEGER NOT NULL"""
    
    lines = [   """, Console_Messages VARCHAR(9999) NOT NULL""", 
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, PRIMARY KEY ("Log_ID" AUTOINCREMENT)"""
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_6_query = create_table_6_query + lines[p]
    create_table_6_query = create_table_6_query + """);"""


    created_table = db.create_tables(foia_session.connection,create_table_6_query)
   #print(f"{created_table}: tbl_Console_Log")

    



    #2 Create the table of Requesters and populate it with the requester's information

    create_table_2_query = f"""CREATE TABLE tbl_Requesters (Requester_ID INTEGER NOT NULL"""
    lines = [   """, First_Name VARCHAR(9999) NOT NULL""",
                """, Middle_Name VARCHAR(9999)""",
                """, Last_Name VARCHAR(9999) NOT NULL""",
                """, Full_Name VARCHAR(9999) NOT NULL""",
                """, Preferred_Name VARCHAR(9999) NOT NULL""",
                """, Return_Address VARCHAR(9999) NOT NULL""",
                """, Phone_Number VARCHAR(9999) NOT NULL""",
                """, Phone_Number_Type VARCHAR(9999)""",
                """, Fax_Number VARCHAR(9999)""",
                """, Email VARCHAR(9999) NOT NULL UNIQUE""",
                """, Photo VARCHAR(9999) NOT NULL UNIQUE""",
                """, Notes VARCHAR(9999)""",
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, PRIMARY KEY ("Requester_ID" AUTOINCREMENT)"""
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_2_query = create_table_2_query + lines[p]
    create_table_2_query = create_table_2_query + """);"""

    created_table = db.create_tables(foia_session.connection,create_table_2_query)
   #print(f"{created_table}: tbl_Requesters")

    #2A Create the first Requester. 

    default_requester = [values[f'-Organization_Manager_First_{num}-'],values[f'-Organization_Manager_Middle_{num}-'],values[f'-Organization_Manager_Last_{num}-'],values[f'-Organization_Manager_Full_{num}-'],values[f'-Organization_Manager_Preferred_{num}-'],values[f'-Organization_Address_{num}-'],values[f'-Organization_Phone_{num}-'],"Default","None",values[f'-Organization_Email_{num}-'], values[f'-Organization_Logo_{num}-'],"Notes: None",f"""{foia_session.current_time_display[0]}""",f"""{foia_session.current_time_display[0]}"""]
    

    
    create_default_requester_query = f"""INSERT INTO tbl_Requesters (First_Name, Middle_Name, Last_Name, Full_Name, Preferred_Name, Return_Address, Phone_Number, Phone_Number_Type,Fax_Number, Email, Photo, Notes, Created_Time, Edited_Time)
        VALUES(("{default_requester[0]}"),("{default_requester[1]}"),("{default_requester[2]}"),("{default_requester[3]}"),("{default_requester[4]}"),("{default_requester[5]}"),("{default_requester[6]}"),("{default_requester[7]}"),("{default_requester[8]}"),("{default_requester[9]}"),("{default_requester[10]}"),("{default_requester[11]}"),("{default_requester[12]}"),("{default_requester[13]}"));
    """
   #print(create_default_requester_query)
    created_requester = db.execute_query(foia_session.connection,create_default_requester_query)
    current_console_messages = foia_session.console_log(message=created_requester,current_console_messages=current_console_messages)
   #print(f"{created_requester}: {default_requester}")






    #3 Create the Applicants table

    create_table_3_query = f"""CREATE TABLE tbl_Applicants (Applicant_ID INTEGER NOT NULL"""
    lines = [   """, First_Name VARCHAR(9999) NOT NULL""",
                """, Middle_Name VARCHAR(9999)""",
                """, Last_Name VARCHAR(9999) NOT NULL""",
                """, Title VARCHAR(9999) NOT NULL""",
                """, Preferred_Name VARCHAR(9999) UNIQUE NOT NULL""",
                """, Full_Name VARCHAR(9999) NOT NULL""",
                """, Phone_Number VARCHAR(9999)""",
                """, Phone_Number_Type VARCHAR(9999)""",
                """, Fax_Number VARCHAR(9999)""",
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, Return_Address VARCHAR(9999) NOT NULL""",
                """, Notes VARCHAR(9999)""", 
                """, Email VARCHAR(9999)""",
                """, PRIMARY KEY ("Applicant_ID" AUTOINCREMENT)"""
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_3_query = create_table_3_query + lines[p]
    create_table_3_query = create_table_3_query + """);"""


    created_table = db.create_tables(foia_session.connection,create_table_3_query)
   #print(f"{created_table}: tbl_Applicants")


    #TODO: Collect user information during setup

    #4 Create the Responders Table
    create_table_4_query = f"""CREATE TABLE tbl_Responders (Responder_ID INTEGER NOT NULL"""
    
    lines = [   """, Organization_Name VARCHAR(9999) UNIQUE NOT NULL""",   
                """, Organization_Type VARCHAR(9999) NOT NULL""",   
                """, Contact_First_Name VARCHAR(9999)""",
                """, Contact_Last_Name VARCHAR(9999)""",
                """, Contact_Email VARCHAR(9999)""",
                """, Preferred_Name VARCHAR(9999) NOT NULL""",
                """, Phone_Number VARCHAR(9999) NOT NULL""",
                """, Phone_Number_Type VARCHAR(9999)""",   #Mobile, Home, Office, Work, Other
                """, Fax_Number VARCHAR(9999)""",
                """, Organization_Address VARCHAR(9999) NOT NULL""",
                """, Organization_Mailing_Address VARCHAR(9999) NOT NULL""",
                """, Organization_Email VARCHAR(9999)""",
                """, Organization_Website VARCHAR(9999)""",
                """, Notes VARCHAR(9999)""",
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, PRIMARY KEY ("Responder_ID" AUTOINCREMENT)"""
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_4_query = create_table_4_query + lines[p]
    create_table_4_query = create_table_4_query + """);"""

    created_table = db.create_tables(foia_session.connection,create_table_4_query)
   #print(f"{created_table}: tbl_Responders")

    #5 Create the Applications Table
    create_table_5_query = f"""CREATE TABLE tbl_Applications (Application_ID INTEGER NOT NULL """
    
    lines = [   """, Tracking_Number VARCHAR(9999) UNIQUE NOT NULL""",
                """, Requester_ID INTEGER NOT NULL""",
                """, Responder_ID INTEGER NOT NULL""",
                """, Date VARCHAR(9999) NOT NULL""",
                """, Applicant_ID INTEGER NOT NULL""",
                """, Letter_IDs VARCHAR NOT NULL""", #A list of Letter_ID numbers.
                """, Documents VARCHAR(9999) NOT NULL""", #A list of document numbers
                """, Requests VARCHAR(99990) NOT NULL""", #Variable foia_session.request_type. A list of the types requested, always applies to all documents.
                """, Notes VARCHAR(9999)""", 
                """, Record_Location VARCHAR(9999) NOT NULL""",#pdf or png of the application
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, PRIMARY KEY ("Application_ID" AUTOINCREMENT)""",
                """, FOREIGN KEY ("Requester_ID") REFERENCES tbl_Requesters(Requester_ID)""",
                """, FOREIGN KEY ("Responder_ID") REFERENCES tbl_Responders(Responder_ID)""",
                """, FOREIGN KEY ("Applicant_ID") REFERENCES tbl_Applicants(Applicant_ID)""",
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_5_query = create_table_5_query + lines[p]
    create_table_5_query = create_table_5_query + """);"""


    db.create_tables(foia_session.connection,create_table_5_query)
   #print(f"{created_table}: tbl_Applications")

    #6 Create the Letters Table
    create_table_7_query = f"""CREATE TABLE tbl_Letters (Letter_ID INTEGER NOT NULL"""
    
    lines = [   """, Tracking_Number VARCHAR(9999) NOT NULL""", #The tracking number for the letter, 
                """, Application_ID INTEGER""",
                """, Requester_ID INTEGER NOT NULL""",
                """, Responder_ID INTEGER NOT NULL""",
                """, Date VARCHAR(9999) NOT NULL""",
                """, Status VARCHAR (9999) NOT NULL""", #Open: The letter has been sent but no response has been received. Action: A response has been entered into the database but it has not yet been forwarded. Closed: A response has been received and forwarded to the Applicant.
                """, Document VARCHAR(9999) NOT NULL""", #The document number being requested.
                """, Request VARCHAR(9999) NOT NULL""", #The information associated with the document number that is being requested.
                #""", Subject VARCHAR(9999) NOT NULL""", #The subject of the request is part of the message
                """, Message VARCHAR(9999) NOT NULL""", #The body of the request in template format.
                """, Record VARCHAR(9999)""", #The pdf and png files that are generated for the letter.
                """, Response VARCHAR(9999)""", #The scan of the response received from the responder office. 
                """, Forwarding_Letter_Content VARCHAR(99999)""", #The text of the forwarding letter body. GUI will Generate
                """, Forwarding_Letter VARCHAR(9999)""", #The scan of the signed forwarding letter.
                """, Letter_Code VARCHAR(9999) NOT NULL""",
                """, Created_Time VARCHAR(9999) NOT NULL""",
                """, Edited_Time VARCHAR(9999) NOT NULL""",
                """, PRIMARY KEY ("Letter_ID" AUTOINCREMENT)""",
                """, FOREIGN KEY ("Application_ID") REFERENCES tbl_Applications(Application_ID)""",
                """, FOREIGN KEY ("Requester_ID") REFERENCES tbl_Requesters(Requester_ID)""",
                """, FOREIGN KEY ("Responder_ID") REFERENCES tbl_Responders(Responder_ID)""",
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_7_query = create_table_7_query + lines[p]
    create_table_7_query = create_table_7_query + """);"""


    created_table = db.create_tables(foia_session.connection,create_table_7_query)
    #print("Invoices_Table")
   #print(f"{created_table}: tbl_Letters")



    #9 Create the Properties Table
    create_table_8_query = f"""CREATE TABLE tbl_Properties (Property_ID INTEGER NOT NULL"""
    
    lines = [   """, Property_Name VARCHAR(9999) NOT NULL""", 
                """, Property_Value VARCHAR(9999) NOT NULL""", 
                """, Property_Units VARCHAR(9999) NOT NULL""", 
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, PRIMARY KEY ("Property_ID" AUTOINCREMENT)"""
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_8_query = create_table_8_query + lines[p]
    create_table_8_query = create_table_8_query + """);"""


    created_table = db.create_tables(foia_session.connection,create_table_8_query)
    #print("Invoices_Table")
   #print(f"{created_table}: tbl_Properties")

    #9.a Create the properties

    foia_session.organization_name = values[f'-db_name_{num}-']
    foia_session.organization_address = values[f'-Organization_Address_{num}-']

    foia_session.manager_firstname = values[f'-Organization_Manager_First_{num}-']
    foia_session.manager_middlename = values[f'-Organization_Manager_Middle_{num}-']
    foia_session.manager_lastname = values[f'-Organization_Manager_Last_{num}-']
    foia_session.manager_title = values[f'-Organization_Manager_Title_{num}-']
    foia_session.manager_preferredname = values[f'-Organization_Manager_Preferred_{num}-']
    foia_session.manager_fullname = values[f'-Organization_Manager_Full_{num}-']
    foia_session.manager_title = values[f'-Organization_Manager_Title_{num}-']

    foia_session.organization_phone = values[f'-Organization_Phone_{num}-']
    foia_session.organization_email = values[f'-Organization_Email_{num}-']
    foia_session.organization_notes = values[f'-Organization_Notes_{num}-']
    foia_session.documents_location = values[f'-Organization_Documents_Repository_{num}-']
    foia_session.organization_acronym = values[f'-Organization_Acronym_{num}-']
    foia_session.logo = values[f'-Organization_Logo_{num}-']

    database_properties = [
        ["Organization Name",f"{foia_session.organization_name}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Address",f"{foia_session.organization_address}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Organization Logo",f"{foia_session.logo}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Organization Acronym",f"{foia_session.organization_acronym}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Manager First Name",f"{foia_session.manager_firstname}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Manager Middle Name",f"{foia_session.manager_middlename}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Manager Last Name",f"{foia_session.manager_lastname}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Manager Preferred Name",f"{foia_session.manager_preferredname}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Manager Full Name",f"{foia_session.manager_fullname}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Manager Title",f"{foia_session.manager_title}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Organization Phone",f"{foia_session.organization_phone}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Organization Email",f"{foia_session.organization_email}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Organization Notes",f"{foia_session.organization_notes}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["Documents Repository Location",f"{foia_session.documents_location}","",foia_session.current_time_display[0],foia_session.current_time_display[0]],
    ]

    for property in database_properties:
        create_properties_query = f"""INSERT INTO tbl_Properties (Property_Name, Property_Value, Property_Units,Created_Time, Edited_Time)
            VALUES(("{property[0]}"),("{property[1]}"),("{property[2]}"),("{property[3]}"),("{property[4]}"));
        """
        #print(create_default_accounts_query)
        created_property = db.execute_query(foia_session.connection,create_properties_query)
       #print(create_properties_query)
       #print(created_property)
       #print(f"{created_property}: {property}")

    foia_session.current_console_messages = foia_session.console_log(message=f"Saved database properties for {foia_session.organization_name}. Owner: {foia_session.manager_preferredname}",current_console_messages=foia_session.current_console_messages)



    #10 Create the Letter templates. 

    #text="This sample."
    #text.replace("sample","example")

    #ledger_name_1 = f"""ledger_{foia_session.db_name[:-4]}"""
    #foia_session.ledger_name = f"""tbl_{ledger_name_1}_CY{year}"""


    create_table_1_query = f"""CREATE TABLE tbl_Templates (Template_ID INTEGER NOT NULL"""
    lines = [""", Body_Content VARCHAR(9999) NOT NULL""", #A python list "[]" which can be read back in for each section of text.
             """, Name VARCHAR(9999) UNIQUE NOT NULL""",
                """, Notes VARCHAR(9999)""",
                """, Created_Time VARCHAR(9999) NOT NULL""", 
                """, Edited_Time VARCHAR(9999) NOT NULL""" ,
                """, PRIMARY KEY ("Template_ID" AUTOINCREMENT)"""
            ]
    num_lines = len(lines)
    for p in range(num_lines):
        create_table_1_query = create_table_1_query + lines[p]
    create_table_1_query = create_table_1_query + """);"""

    created_table = db.create_tables(foia_session.connection,create_table_1_query)
    #print(f"creating ledger: {create_table_1_query}")
   #print(f"{created_table}: tbl_Templates")


    #TODO:ADD IN DEFAULT Templates
    default_templates = [
        ["""To:['-new_line-']['-Responder_Preferred_Name-']['-new_line-']['-Letter_To_Field-']['-new_line-']From:['-new_line-']['-Letter_From_Field-']['-new_line-']Subject: 5 U.S.C. §552 FOIA Request- ['-Requested_Document-']['-new_line-']['-new_line-']Dear ['-Responder_Preferred_Name-'],['-new_line-']['-new_line-']   I'm writing today on behalf of ['-Applicant_Preferred_Name-'] to request ['-Requested_Records-'] that may be associated with the following record identifier: ['-Requested_Document-'].['-new_line-']['-new_line-']Please mail the requested records to my address, or provide instructions for next steps at your earliest availability.['-new_line-']['-new_line-']['-Organization_Name-'] is a discovery advocate only and does not provide legal advice to clients.['-new_line-']['-new_line-']Thank you, I appreciate your assistance in this matter.['-new_line-']['-new_line-']Sincerely,['-new_line-']['-Requester_Preferred_Name-']['-new_line-']['-new_line-']_______________________['-new_line-']['-Requester_Phone-'] ['-new_line-']['-Requester_Email-']""",f"""FOIA Request""","Notes: None",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["""To:['-new_line-']['-Applicant_Preferred_Name-']['-new_line-']['-Applicant_Return_Address-']['-new_line-']From:['-new_line-']['-Letter_From_Field-']['-new_line-']Subject: FWD: 5 U.S.C. §552 FOIA Request- ['-Requested_Document-']['-new_line-']['-new_line-']Dear ['-Applicant_Preferred_Name-'],['-new_line-']['-new_line-']   I'm writing today to forward ['-Requested_Records-'] in relation to or associated with the following record identifier: ['-Requested_Document-'] ['-new_line-']['-new_line-']You requested this information on applicaton ['-Application_Number-'] which was entered into my database on ['-Application_Date-']. Other records in your request may still be pending. This letter and any attachments are provided for information only and no part of this communication should be construed as legal advice. ['-Organization_Name-'] disclaims all warranties express or implied. Please contact us if you need additional assistance.['-new_line-']['-new_line-']Thank you.['-new_line-']['-new_line-']Sincerely,['-new_line-']['-Requester_Preferred_Name-']['-new_line-']['-new_line-']_______________________['-new_line-']['-Requester_Phone-']['-new_line-']['-Requester_Email-']""",f"""Forwarding Letter""","Notes: None",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["""To:['-new_line-']['-Letter_To_Field-']['-new_line-']From:['-new_line-']['-Letter_From_Field-']['-new_line-']Subject: 5 U.S.C. §552 FOIA Requests - Partner Offer['-new_line-']['-new_line-']Dear ['-Prospective_Partner-'],['-new_line-']['-new_line-']   I'm writing today to offer you a partnership position with ['-Organization_Name-']. The purpose of our organization is advocacy through discovery in legal cases, although we do not offer legal advice.['-new_line-']['-new_line-']Your position in ['-Organization_Name-'] will be: ['-new_line-']['-new_line-']['-Position Description-'] ['-new_line-']['-new_line-']Please respond to this letter by ['-Offer_Deadline-'] to indicate whether you accept. ['-new_line-']['-new_line-']Thank you.['-new_line-']['-new_line-']Sincerely,['-new_line-']['-Requester_Preferred_Name-']['-new_line-']['-new_line-']_______________________['-new_line-']['-Requester_Phone-']['-new_line-']['-Requester_Email-']""",f"""Partner Offer""","Notes: None",foia_session.current_time_display[0],foia_session.current_time_display[0]],
        ["""To:['-new_line-']['-Letter_To_Field-']['-new_line-']From:['-new_line-']['-Letter_From_Field-']['-new_line-']Subject: 5 U.S.C. §552 FOIA Request- Requester Offer['-new_line-']['-new_line-']Dear ['-Responder_Preferred_Name-'],['-new_line-']['-new_line-']   I'm writing today to offer you a requester position with ['-Organization_Name-']. The purpose of our organization is advocacy through discovery in legal cases. We forward information from government offices, but we do not offer legal advice.['-new_line-']['-new_line-']Your position in ['-Organization_Name-'] will be: ['-new_line-']['-new_line-']Requester: You will collect applications for FOIA requests and generate FOIA request letters. Once a reply has been received from the responding office, you'll forward that response to the applicant. You are not to offer any advice or analysis to the applicant, as we are not a law firm. Offering unathorized legal advice to clients may be grounds for separation from the organization.['-new_line-']['-new_line-']Your compensation will be: ['-Compensation_Details-']['-new_line-']['-new_line-']Please respond to this letter by ['-Offer_Deadline-'] to indicate whether you accept. We look forward to your response.['-new_line-']['-new_line-']Thank you.['-new_line-']['-new_line-']Sincerely,['-new_line-']['-Requester_Preferred_Name-']['-new_line-']['-new_line-']_______________________['-new_line-']['-Requester_Phone-']['-new_line-']['-Requester_Email-']""",f"""Requester Offer""","Notes: None",foia_session.current_time_display[0],foia_session.current_time_display[0]],
    ]


    for template in default_templates:
        create_default_templates_query = f"""INSERT INTO tbl_Templates (Body_Content, Name, Notes, Created_Time, Edited_Time)
            VALUES("{template[0]}","{template[1]}","{template[2]}","{template[3]}","{template[4]}");
        """
        #print(create_default_accounts_query)
        created_template = db.execute_query(foia_session.connection,create_default_templates_query)
        current_console_messages = foia_session.console_log(message=created_template,current_console_messages=current_console_messages)
       #print(f"{created_template}: {template}")




    #11 Finalize
    #Condition Save Location
    foia_session.save_location = values[f"-Save_Location_{num}-"]
    #print(f"""The value of save location is: {values['-Save_Location-)}""")
    if len(values[f'-Save_Location_{num}-']) == 0: 
        foia_session.save_location = "./"
        
    elif values[f'-Save_Location_{num}-'] == "/":
        
        foia_session.save_location = "./"
    else:
        foia_session.save_location = values[f'-Save_Location_{num}-']

    #Load to memory
    foia_session.connection = db.load_db_to_memory(foia_session.connection)
    foia_session.database_loaded = True
   #print(f"connection: {foia_session.connection}")

    #Update the dashboard
    window  = update_dashboard_statistics(foia_session.window, foia_session.values)
   #print(window)
    #encrypt the database during the session
    foia_session.filekey, foia_session.filename, foia_session.save_location = db.encrypt_database(foia_session.db_name,"encrypt",False, foia_session.save_location, False)

    return foia_session.filekey, foia_session.filename
    



#def load_dashboard_initial(connection, window, values):
        #Load the dashboard

#    update_dashboard_statistics(connection, window)


def load_session_data(window, values):

    acronym_query = f"""SELECT Property_Value FROM tbl_Properties WHERE Property_Name IS 'Organization Acronym';"""
    this_acronym = db.execute_read_query_dict(foia_session.connection,acronym_query)
    #print("acronym loaded")
    #print(this_acronym[0]['Property_Value'])
    if this_acronym != [] and type(this_acronym) == list:
        foia_session.organization_acronym = this_acronym[0]['Property_Value']

        documents_query = f"""SELECT Property_Value FROM tbl_Properties WHERE Property_Name IS 'Documents Repository Location';"""
        this_folder = db.execute_read_query_dict(foia_session.connection,documents_query)
        foia_session.documents_location = this_folder[0]['Property_Value']
        #update_requesters_view(window,values)

        name_query = f"""SELECT Property_Value FROM tbl_Properties WHERE Property_Name IS 'Organization Name';"""
        this_name = db.execute_read_query_dict(foia_session.connection,name_query)
        foia_session.organization_name = this_name[0]['Property_Value']


        window['-Load_Messages-'].update(foia_session.organization_name)



def update_dashboard_statistics(window, values):
    current_year = foia_session.current_year
    #Bring the user to the dashboard
    this_tab_index = 0
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"

    #Letter Counts by Status
    get_closed_letters_count = f"""SELECT Count(*) FROM tbl_Letters WHERE Status IS 'Closed';"""
    closed_letters = db.execute_read_query_dict(foia_session.connection,get_closed_letters_count)
   #print(f"closed letters: {closed_letters[0]['Count(*)']}")
    closed_letters_count = 0
    if len(closed_letters) > 0 and type(closed_letters) == list:
        closed_letters_count = closed_letters[0]['Count(*)']

    get_open_letters_count = f"""SELECT Count(*) FROM tbl_Letters WHERE Status IS 'Open';"""
    open_letters = db.execute_read_query_dict(foia_session.connection,get_open_letters_count)
   #print(f"open letters: {open_letters[0]['Count(*)']}")
    open_letters_count = 0
    if len(open_letters) > 0 and type(open_letters) == list:
        open_letters_count = open_letters[0]['Count(*)']
    



    #Action Letters
    get_action_letters_query = f"""SELECT Tracking_Number, Application_ID, Responder_ID FROM tbl_Letters WHERE Status IS 'Action';"""
    action_letters = db.execute_read_query_dict(foia_session.connection,get_action_letters_query)
   #print(f"action letters: {action_letters}")
    window["-Letters_Action_Today_Number-"].update(f"{len(action_letters)}")

    window["-Dashboard_Sequestered_Number-"].update(f"{(len(action_letters)*2+closed_letters_count*3+open_letters_count)*1000/(800*500)} kg") 
    display_action_letters = []
    if action_letters != [] and type(action_letters) == list:
        for i in range(len(action_letters)):
            applicant_name = f"None"
            get_application_query = f"""SELECT Applicant_ID FROM tbl_Applications WHERE Application_ID IS '{action_letters[i]['Application_ID']}';"""
            application = db.execute_read_query_dict(foia_session.connection,get_application_query)
            if application != [] and type(application) == list:
                #print(f"Application: {application}")
                get_applicant_query = f"""SELECT Preferred_Name FROM tbl_Applicants WHERE Applicant_ID IS '{application[0]['Applicant_ID']}';"""
                applicant = db.execute_read_query_dict(foia_session.connection,get_applicant_query)
                if applicant != [] and type(action_letters) == list:
                    applicant_name = f"{applicant[0]['Preferred_Name']}"            
            get_responder_query = f"""SELECT Organization_Name FROM tbl_Responders WHERE Responder_ID IS '{action_letters[i]['Responder_ID']}';"""
            responder = db.execute_read_query_dict(foia_session.connection,get_responder_query)
            if responder != [] and type(responder) == list:
                display_action_letters.append([f"{action_letters[i]['Tracking_Number']}",f"{applicant_name}",f"{responder[0]['Organization_Name']}","Action"])
    

    
    
    window['-Dashboard_Display_Content-'].update(display_action_letters)


    #Daily Letters
    count_today_letters_query = f"""SELECT COUNT(*) FROM tbl_Letters WHERE Date >= '{current_date_db}';"""
    today_letters = db.execute_read_query_dict(foia_session.connection,count_today_letters_query)
    if today_letters != [] and type(today_letters) == list:
        window["-Letters_Sent_Today_Number-"].update(f"{today_letters[0]['COUNT(*)']}")

    #Monthly Letters
    count_monthly_letters_query = f"""SELECT COUNT(*) FROM tbl_Letters WHERE Date >= '{current_month}';"""
    monthly_letters = db.execute_read_query_dict(foia_session.connection,count_monthly_letters_query)
    if monthly_letters != [] and type(monthly_letters) == list:
        window['-Letters_Sent_This_Month_Number-'].update(f"{monthly_letters[0]['COUNT(*)']}")

    #Yearly Letters

    count_yearly_letters_query = f"""SELECT COUNT(*) FROM tbl_Letters WHERE Date >= '{current_year}/01/01';"""
    yearly_letters = db.execute_read_query_dict(foia_session.connection,count_yearly_letters_query)
    if yearly_letters != [] and type(yearly_letters) == list:
        window['-Letters_Sent_This_Year_Number-'].update(f"{yearly_letters[0]['COUNT(*)']}")




    return window


#Applications Functions





def activate_new_application_fields(window,values):

    #Enable and clear the form
    window['-Application_Requester_Input-'].update(disabled=False)    
    window['-Application_Responder_Input-'].update(disabled=False)  
    window['-Application_Applicant_Input-'].update(disabled=False)  
    window['-Application_Add_Document_Button-'].update(disabled=False)  
    window['-Application_Delete_Document_Button-'].update(disabled=False)  
    window['-Application_Common_Requests_Input-'].update(disabled=False)  
    window['-Application_Add_Request_Button-'].update(disabled=False)  
    window['-Application_Notes_Display-'].update(disabled=False) 
    window['-Application_Template_Input-'].update(disabled=False)  
    window['-Application_Delete_Request_Button-'].update(disabled=False)  
    window['-Application_Record_Input-'].update(disabled=False)
    window['-Application_Document_Input-'].update(disabled=False)
    window['-Application_Requests_Input-'].update(disabled=False)
    window['-Application_Record_Button-'].update(disabled=True) 
    window['-Application_Search_Input-'].update(disabled=True)  
    

    get_max_application_query = f"""SELECT MAX(Application_ID) FROM tbl_Applications;"""
    max_application = db.execute_read_query_dict(foia_session.connection,get_max_application_query)
   #print(f"max application: {max_application[0]['MAX(Application_ID)']}")
    if max_application != [] and type(max_application) == list:
        if max_application[0]['MAX(Application_ID)'] == None:
            max_application[0]['MAX(Application_ID)'] = 0
           #print(f"max application: {max_application[0]['MAX(Application_ID)']}")
        foia_session.new_application_id = int(max_application[0]['MAX(Application_ID)']) + 1
       #print(f"new application id: {foia_session.new_application_id}")
        new_application_tracking = f"{foia_session.organization_acronym}-APP-{foia_session.new_application_id+10000}"
        foia_session.this_application = {"Tracking_Number": f"{new_application_tracking}","Application_ID":foia_session.new_application_id,"Requester_ID": "","Responder_ID":"","Applicant_ID":"","Letter_IDs":[],"Documents": [],"Requests":[],"Notes":""}
        window['-Application_Number_Input-'].update(new_application_tracking)    

        window['-Applications_Content-'].update([[new_application_tracking,"Select Applicant", "Click Generate",f"{current_date_db}"]])

def save_application_record(windows, values):
    record_location = values['-Application_Record_Input-']
    update_record_query = f"""UPDATE tbl_Applications SET Record_Location = '{record_location}' WHERE Application_ID is '{foia_session.this_application_id}';"""
#asdfads
def load_application_data(window,values):
    print(values['-Applications_Content-'])
    this_application_tracking = ""
    if type(values['-Applications_Content-']) == list and len(values['-Applications_Content-']) > 0 and len(foia_session.display_applications)>0:
        this_application_tracking = foia_session.display_applications[values['-Applications_Content-'][0]][0]
       #print(f"Application Display: {this_application_tracking}")

    get_application_query = f"""SELECT * FROM tbl_Applications WHERE Tracking_Number IS '{this_application_tracking}';"""
    this_application = db.execute_read_query_dict(foia_session.connection,get_application_query)
    if type(this_application) == list and len(this_application)>0:
        foia_session.this_application_id = this_application[0]['Application_ID']
    this_responder = ""
    this_requester = ""
    this_applicant = ""

    documents_list = []
    requests_list = []


    if type(this_application) == list and this_application != []:
       #print(this_application[0])

        #print(this_application[0]['Documents'])
        #print(this_application[0]['Requests'])
        documents_list = eval(this_application[0]['Documents'].replace("~","'"))
        requests_list= eval(this_application[0]['Requests'].replace("~","'"))
    


        get_responder_query = f"""SELECT Responder_ID, Organization_Name FROM tbl_Responders WHERE Responder_ID IS '{this_application[0]['Responder_ID']}';"""
        this_responder = db.execute_read_query_dict(foia_session.connection,get_responder_query)

        get_requester_query = f"""SELECT Requester_ID, Preferred_Name FROM tbl_Requesters WHERE Requester_ID IS '{this_application[0]['Requester_ID']}';"""
        this_requester = db.execute_read_query_dict(foia_session.connection,get_requester_query)

        get_applicant_query = f"""SELECT Applicant_ID, Preferred_Name FROM tbl_Applicants WHERE Applicant_ID IS '{this_application[0]['Applicant_ID']}';"""
        this_applicant = db.execute_read_query_dict(foia_session.connection,get_applicant_query)

    
        #Disable the form
        window['-Application_Requester_Input-'].update(f"{this_requester[0]['Requester_ID']} {this_requester[0]['Preferred_Name']}",disabled=True)    
        window['-Application_Responder_Input-'].update(f"{this_responder[0]['Responder_ID']} {this_responder[0]['Organization_Name']}",disabled=True)  
        window['-Application_Applicant_Input-'].update(f"{this_applicant[0]['Applicant_ID']} {this_applicant[0]['Preferred_Name']}",disabled=True)  
        window['-Application_Created_Input-'].update(f"{this_application[0]['Created_Time']}")  
        window['-Application_Edited_Input-'].update(f"{this_application[0]['Edited_Time']}")  
        
        window['-Application_Add_Document_Button-'].update(disabled=True)  
        window['-Application_Delete_Document_Button-'].update(disabled=True)  
        window['-Application_Common_Requests_Input-'].update(disabled=True)  
        window['-Application_Add_Request_Button-'].update(disabled=True)  
        window['-Application_Notes_Display-'].update(f"{this_application[0]['Notes']}",disabled=True) 
        window['-Application_Template_Input-'].update(disabled=True)  
        window['-Application_Generate_Button-'].update(disabled=True)  
        window['-Application_Delete_Request_Button-'].update(disabled=True)  
        window['-Application_Record_Input-'].update(f"{this_application[0]['Record_Location']}",disabled=False)
        if this_application[0]['Record_Location']:
            window['-Application_Record_Button-'].update(disabled=False) 
        else:
            window['-Application_Record_Button-'].update(disabled=True) 
        window['-Application_Document_Input-'].update(disabled=True)
        window['-Application_Requests_Input-'].update(disabled=True)
        window['-New_Application_Button-'].update("New Application")
        window['-Application_Documents_Display-'].update(documents_list)
        window['-Application_Requests_Display-'].update(requests_list)



    else:
        #Disable the form
        window['-Application_Requester_Input-'].update(disabled=True)    
        window['-Application_Responder_Input-'].update(disabled=True)  
        window['-Application_Applicant_Input-'].update(disabled=True)  
        window['-Application_Add_Document_Button-'].update(disabled=True)  
        window['-Application_Delete_Document_Button-'].update(disabled=True)  
        window['-Application_Common_Requests_Input-'].update(disabled=True)  
        window['-Application_Add_Request_Button-'].update(disabled=True)  
        window['-Application_Notes_Display-'].update(disabled=True) 
        window['-Application_Template_Input-'].update(disabled=True)  
        window['-Application_Generate_Button-'].update(disabled=True)  
        window['-Application_Delete_Request_Button-'].update(disabled=True)  
        window['-Application_Record_Input-'].update(disabled=True)
        window['-Application_Record_Button-'].update(disabled=True) 
        window['-Application_Document_Input-'].update(disabled=True)
        window['-Application_Requests_Input-'].update(disabled=True)
        window['-New_Application_Button-'].update("New Application")
        window['-Application_Documents_Display-'].update(documents_list)
        window['-Application_Requests_Display-'].update(requests_list)


def generate_application(window,values,template_id):
   #print(foia_session.this_application['Applicant_ID'])
    #Find New Application Number
    window['-Application_Generate_Button-'].update(disabled=True)
    count_applications_query = f"""SELECT MAX(Application_ID) FROM tbl_Applications;"""
    max_application = db.execute_read_query_dict(foia_session.connection,count_applications_query)
   #print(str(max_application))
    if max_application[0]['MAX(Application_ID)'] == None:
        max_application[0]['MAX(Application_ID)'] = 0
        #print(max_letter)
   #print(f"max Application: {max_application[0]['MAX(Application_ID)']}")

    application_id = int(max_application[0]['MAX(Application_ID)'])+1
   #print(f"application_id: {application_id}")
    #Create the application directory
    filenames = []
    foldername = foia_session.this_application['Tracking_Number']
    folderpath = f'{foia_session.documents_location}/Applications/{foldername}'

    #Create the application directory, if it doesn't already exist
    if os.path.isdir(f'{foia_session.documents_location}/Applications') == False:
        os.mkdir(f'{foia_session.documents_location}/Applications')
    if os.path.isdir(folderpath) == False:
        os.mkdir(folderpath)
    first_letter = 0
    last_letter = 0

    #Echo the stakeholders
   #print("stakeholders:")
   #print(foia_session.this_application['Requester_ID'])
   #print(foia_session.this_application['Responder_ID'])
   #print(foia_session.this_application['Applicant_ID'])



    #Generate a letter for each document and request
    for document in foia_session.this_application['Documents']:
        for request in foia_session.this_application['Requests']:
           #print(f"document: {list(document)[0]}")
           #print(f"request: {list(request)[0]}")
            #Find New Letter Number
            count_letters_query = f"""SELECT MAX(Letter_ID) FROM tbl_Letters;"""
            max_letter = db.execute_read_query_dict(foia_session.connection,count_letters_query)
            #print(str(max_letter))
            if max_letter[0]['MAX(Letter_ID)'] == None:
                max_letter[0]['MAX(Letter_ID)'] = 0
                #print(max_letter)
           #print(f"max letter: {max_letter[0]['MAX(Letter_ID)']}")

            foia_session.new_letter = int(max_letter[0]['MAX(Letter_ID)'])+1
            foia_session.this_letter_id = f"""{foia_session.organization_acronym}-LTR-{foia_session.new_letter+10000}"""
           #print(f"letter_id: {foia_session.new_letter}")
            if first_letter == 0:
                first_letter = foia_session.new_letter
            last_letter = foia_session.new_letter

            #Load the data into the template
            foia_session.this_letter_body = load_selected_template(application_id, template_id,foia_session.this_application['Responder_ID'],foia_session.this_application['Requester_ID'],foia_session.this_application['Applicant_ID'],list(document)[0],list(request)[0])
            foia_session.this_letter = {"Tracking_Number":f"{foia_session.organization_acronym}-LTR-{foia_session.new_letter+10000}","Application_ID":application_id,'Requester_ID':foia_session.this_application['Requester_ID'],"Responder_ID":foia_session.this_application['Responder_ID'],"Date":current_date_db,"Status": "Open","Document":"","Request":""}
    

            #Generate the letter
            letter_folderpath =  f'{foia_session.documents_location}/Letters/{foia_session.this_letter['Tracking_Number']}'
            filepath, images = generate_new_letter(window,values)
           #print(images)
            for image in images:
                len(foia_session.organization_acronym)
                letter_image_destination = f"{folderpath}/{foia_session.this_letter['Tracking_Number']}{image[len(letter_folderpath)+(len(foia_session.organization_acronym))+11:]}".replace("//","/")
               #print(letter_image_destination)
                os.replace(image,letter_image_destination)
            
            #Add the letter to the database
            insert_letter_query = f"""INSERT INTO tbl_Letters (Tracking_Number, Application_ID, Requester_ID, Responder_ID, Document, Request, Message, Created_Time, Edited_Time, Date, Status, Letter_Code) VALUES ('{foia_session.this_letter['Tracking_Number']}','{foia_session.this_application['Application_ID']}','{foia_session.this_letter['Requester_ID']}', '{foia_session.this_letter['Responder_ID']}','{list(document)[0]}','{list(request)[0]}',"{foia_session.this_letter_body}",'{datetime.datetime.now()}','{datetime.datetime.now()}','{current_date_db}','Open','{foia_session.this_letter['Letter_Code']}');"""
           #print(insert_letter_query)
            inserted_letter = db.execute_query(foia_session.connection,insert_letter_query)
            foia_session.console_log(f"Inserted {values['-Letter_ID_Input-']}: {inserted_letter}",foia_session.current_console_messages)


    # convert all files ending in .png in a directory and its subdirectories tp PDF format
    dirname = folderpath
    images = []
    for r, _, f in os.walk(dirname):
        for fname in f:
            if not fname.endswith(".png"):
                continue
            images.append(os.path.join(r, fname))
    images.sort()
    dpix = dpiy = 300
    this_layout = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
    filepath = f"{folderpath}/{foldername}.pdf"
    with open(filepath,"wb") as f:
        f.write(img2pdf.convert(images,layout_fun=this_layout))    

    #Remove the images
    time.sleep(0.15)
    for image in images:
        os.remove(f"{image}")
    

    documents_string = f"{foia_session.this_application['Documents']}".replace("'","~")
    requests_string = f"{foia_session.this_application['Requests']}".replace("'","~")

    #Add the application to the database
    insert_application_query = f"""INSERT INTO tbl_Applications (Tracking_Number, Requester_ID, Responder_ID, Applicant_ID, Letter_IDs, Documents, Requests, Notes, Record_Location, Created_Time, Edited_Time, Date)
    VALUES ('{foia_session.this_application['Tracking_Number']}','{foia_session.this_letter['Requester_ID']}', '{foia_session.this_letter['Responder_ID']}','{foia_session.this_application['Applicant_ID']}','{foia_session.organization_acronym}-LTR-{int(first_letter)+10000} thru {foia_session.organization_acronym}-LTR-{int(last_letter)+10000}','{documents_string}','{requests_string}','{foia_session.this_application['Notes']}','{filepath}','{datetime.datetime.now()}','{datetime.datetime.now()}','{current_date_db}');"""
   #print(insert_application_query)
    inserted_application = db.execute_query(foia_session.connection,insert_application_query)
    foia_session.console_log(f"Inserted {foia_session.this_application['Tracking_Number']}: {inserted_application}",foia_session.current_console_messages)





    return filepath

def add_common_request_to_input(window,values):
   #print(values['-Application_Common_Requests_Input-'])
    window['-Application_Requests_Input-'].update(f"{values['-Application_Common_Requests_Input-']}")


def delete_document_from_application(window,values):
   #print(values['-Application_Documents_Display-'])
    delete_document_id = values['-Application_Documents_Display-']
    if delete_document_id != []:
        new_documents = []
        for i in range(len(foia_session.this_application['Documents'])):
            if i != delete_document_id[0]:
                new_documents.append(foia_session.this_application['Documents'][i])
        foia_session.this_application['Documents'] = new_documents
        window['-Application_Documents_Display-'].update(new_documents)

def delete_request_from_application(window,values):
   #print(values['-Application_Requests_Display-'])
    delete_request_id = values['-Application_Requests_Display-']
    if delete_request_id != []:
        new_requests = []
        for i in range(len(foia_session.this_application['Requests'])):
            if i != delete_request_id[0]:
                new_requests.append(foia_session.this_application['Requests'][i])
        foia_session.this_application['Requests'] = new_requests
        window['-Application_Requests_Display-'].update(new_requests)

def add_request_to_application(window,values):
    if values['-Application_Requests_Input-'] != "" and values['-Application_Requests_Input-'] != None:
        duplicate = False
        for request in foia_session.this_application['Requests']:
            if request == f"{values['-Application_Requests_Input-']}":
                duplicate=True
        if duplicate == False:
            this_new_request = f"{values['-Application_Requests_Input-']}"
            foia_session.this_application['Requests'].append([this_new_request])
            window['-Application_Requests_Input-'].update("")
            window['-Application_Requests_Display-'].update(foia_session.this_application['Requests'])
            
        else:
            foia_session.console_log("Duplicate Request",foia_session.current_console_messages)

def add_document_to_application(window,values):
    if values['-Application_Document_Input-'] != "" and values['-Application_Document_Input-'] != None:
        duplicate = False
        for document in foia_session.this_application['Documents']:
            if document == f"{values['-Application_Document_Input-']}":
                duplicate=True
        if duplicate == False:   
           #print(f"{values['-Application_Document_Input-']}")
            new_documents = list(foia_session.this_application['Documents'])
            this_new_document = f"{values['-Application_Document_Input-']}"
            new_documents.append([this_new_document])
            foia_session.this_application['Documents'] = new_documents
            window['-Application_Document_Input-'].update("")
            window['-Application_Documents_Display-'].update(foia_session.this_application['Documents'])
        else:
            foia_session.console_log("Duplicate Document",foia_session.current_console_messages)    
      


def update_applications_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 1
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"

    #Populate the requesters dropdown.
    get_requesters_query = f"""SELECT Requester_ID, Preferred_Name FROM tbl_Requesters;"""
    these_requesters = db.execute_read_query_dict(foia_session.connection,get_requesters_query)
    display_requesters = []
    for requester in these_requesters:
        display_requesters.append(f"{requester['Requester_ID']} {requester['Preferred_Name']}")
    display_requesters.sort()
    window['-Application_Requester_Input-'].update(values=display_requesters)

    #Populate the Responders dropdown.
    window['-Application_Responder_Input-'].update(disabled=False)
    get_responders_query = f"""SELECT Responder_ID, Organization_Name FROM tbl_Responders;"""
    these_responders = db.execute_read_query_dict(foia_session.connection,get_responders_query)
    #print(these_responders)
    if(these_responders) != [] and type(these_responders) != str:

        display_responders = []
        for responder in these_responders:
            display_responders.append(f"{responder['Responder_ID']} {responder['Organization_Name']}")
        display_responders.sort()
        window['-Application_Responder_Input-'].update(values=display_responders)
    else:
        window['-Application_Responder_Input-'].update(disabled=True)

    #Populate the Applicants dropdown.
    window['-Application_Applicant_Input-'].update(disabled=False)
    get_applicants_query = f"""SELECT Applicant_ID, Preferred_Name FROM tbl_Applicants;"""
    these_applicants = db.execute_read_query_dict(foia_session.connection,get_applicants_query)
    #print(these_applicants)
    if(these_applicants) != [] and type(these_applicants) != str:
        display_applicants = []
        for applicant in these_applicants:
            display_applicants.append(f"{applicant['Applicant_ID']} {applicant['Preferred_Name']}")
        display_applicants.sort()
        window['-Application_Applicant_Input-'].update(values=display_applicants)
    else:
        window['-Application_Applicant_Input-'].update(disabled=True)

    #Populate the Templates dropdown.
    window['-Application_Template_Input-'].update(disabled=False)
    get_templates_query = f"""SELECT Template_ID, Name FROM tbl_Templates;"""
    these_templates = db.execute_read_query_dict(foia_session.connection,get_templates_query)
   #print(these_templates)
    if(these_templates) != [] and type(these_templates) != str:

        display_templates = []
        for template in these_templates:
            display_templates.append(f"{template['Template_ID']} {template['Name']}")
        display_templates.sort()
        window['-Application_Template_Input-'].update(values=display_templates)
    else:
        window['-Application_Template_Input-'].update(disabled=True)

    #Populate the Applications List
    applications_search_term = values['-Application_Search_Input-']
   #print(f"applications_search_term: {applications_search_term}")
    get_applications_query = f"""SELECT * FROM tbl_Applications;"""
    if applications_search_term != "":
        get_applications_query = f"""SELECT * FROM tbl_Applications WHERE Tracking_Number LIKE '%{applications_search_term}%' OR Letter_IDs LIKE '%{applications_search_term}%' OR Documents LIKE '%{applications_search_term}%' OR Requests LIKE '%{applications_search_term}%' OR Notes LIKE '%{applications_search_term}%' OR Record_Location LIKE '%{applications_search_term}%';""" #Write the search function
        these_applications = db.execute_read_query_dict(foia_session.connection,get_applications_query)        
        foia_session.display_applications = []
        for application in these_applications:
            letter_ids = str(application['Letter_IDs'])
            this_applicant_name = ""
            

            for applicant in these_applicants:
                print(f"Applicant Identified: {applicant['Applicant_ID']} and {application['Applicant_ID']}")
                if applicant['Applicant_ID'] == application['Applicant_ID']:
                    this_applicant_name = f"{applicant['Preferred_Name']}"
                    print(f"Applicant Identified: {applicant['Applicant_ID']} and {application['Applicant_ID']}")
            foia_session.display_applications.append([f"{application['Tracking_Number']}",f"{this_applicant_name}",letter_ids,application['Created_Time']])
        window['-Applications_Content-'].update(foia_session.display_applications)
        window['-Application_Search_Input-'].update(disabled=False) 
    else:
        these_applications = db.execute_read_query_dict(foia_session.connection,get_applications_query)
        if these_applications != [] and type(these_applications) != str:
            foia_session.display_applications = []

            for application in these_applications:
                this_applicant_name = ""
                for applicant in these_applicants:
                    print(f"Applicant Identified: {applicant['Applicant_ID']} and {application['Applicant_ID']}")
                    if applicant['Applicant_ID'] == application['Applicant_ID']:
                        this_applicant_name = f"{applicant['Preferred_Name']}"
                        print(f"Applicant Identified: {applicant['Applicant_ID']} and {application['Applicant_ID']}")

                letter_ids = str(application['Letter_IDs'])
                foia_session.display_applications.append([f"{application['Tracking_Number']}",f"{this_applicant_name}",letter_ids,application['Created_Time']])
            window['-Applications_Content-'].update(foia_session.display_applications)
            window['-Application_Search_Input-'].update(disabled=False) 
        else:
            window['-Application_Search_Input-'].update(disabled=True) 
            window['-Applications_Content-'].update([[f"{foia_session.organization_acronym}-APP-{10000}","Click", "New Application",f"{current_date_db}"]])

    #Clear and Disable the form
    window['-Application_Requester_Input-'].update(disabled=True)    
    window['-Application_Responder_Input-'].update(disabled=True)  
    window['-Application_Applicant_Input-'].update(disabled=True)  
    window['-Application_Created_Input-'].update("Created", disabled=True)  
    window['-Application_Edited_Input-'].update("Edited", disabled=True)  
    window['-Application_Add_Document_Button-'].update(disabled=True)  
    window['-Application_Delete_Document_Button-'].update(disabled=True)  
    window['-Application_Common_Requests_Input-'].update(disabled=True)  
    window['-Application_Add_Request_Button-'].update(disabled=True)  
    window['-Application_Notes_Display-'].update("", disabled=True) 
    window['-Application_Template_Input-'].update(disabled=True)  
    window['-Application_Generate_Button-'].update(disabled=True)  
    window['-Application_Delete_Request_Button-'].update(disabled=True)  
    window['-Application_Record_Input-'].update("Attach Record", disabled=True)
    window['-Application_Record_Button-'].update(disabled=True) 
    window['-Application_Document_Input-'].update(disabled=True)
    window['-Application_Requests_Input-'].update(disabled=True)
    window['-New_Application_Button-'].update("New Application")
    

    return window

def update_analysis_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 2
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"


    return window
    
def update_letters_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 3
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"


    letters_search_term = values['-Letters_Search_Input-']

    #Update the To Picker
    get_responders_query = f"""SELECT Responder_ID, Organization_Name FROM tbl_Responders WHERE Organization_Name LIKE '%{letters_search_term}%' OR Contact_First_Name LIKE '%{letters_search_term}%' OR Contact_Last_Name LIKE '%{letters_search_term}%' OR Organization_Email LIKE '%{letters_search_term}%' OR Contact_Email LIKE '%{letters_search_term}%' OR Preferred_Name LIKE '%{letters_search_term}%' OR Phone_Number LIKE '%{letters_search_term}%' OR Phone_Number_Type LIKE '%{letters_search_term}%' OR Fax_Number LIKE '%{letters_search_term}%' OR Organization_Address LIKE '%{letters_search_term}%'  OR Created_Time LIKE '%{letters_search_term}%'OR Notes LIKE '%{letters_search_term}%' OR Organization_Website LIKE '%{letters_search_term}%' OR Organization_Mailing_Address LIKE '%{letters_search_term}%' ORDER BY Organization_Name ASC;"""
    if letters_search_term == "" or letters_search_term == None:
        get_responders_query = f"""SELECT Responder_ID, Organization_Name FROM tbl_Responders ORDER BY Organization_Name ASC;"""
    these_responders = db.execute_read_query_dict(foia_session.connection,get_responders_query)
   #print(f"these_responders: {get_responders_query}")
    if type(these_responders) and these_responders != []:
       #print(these_responders[0]['Organization_Name'])
        responder_names = []
        for responder in these_responders:
            this_responder = responder['Organization_Name']
            if len(responder['Organization_Name']) > 18:
                this_responder = this_responder[0:18]
            responder_names.append(f'{responder['Responder_ID']} {this_responder}')
       #print(responder_names)
        window['-Letter_To_Input-'].update(values=responder_names)
    else:
        these_responders = [{"Responder_ID":""}]
        window['-Letter_To_Input-'].update(values=["None"])


    #Update the From Picker
    get_requesters_query = f"""SELECT Requester_ID, Preferred_Name FROM tbl_Requesters WHERE First_Name LIKE '%{letters_search_term}%' OR Last_Name LIKE '%{letters_search_term}%' OR Full_Name LIKE '%{letters_search_term}%' OR Preferred_Name LIKE '%{letters_search_term}%' OR Return_Address LIKE '%{letters_search_term}%' OR Phone_Number LIKE '%{letters_search_term}%' OR Phone_Number_Type LIKE '%{letters_search_term}%' OR Fax_Number LIKE '%{letters_search_term}%' OR Email LIKE '%{letters_search_term}%' OR Photo LIKE '%{letters_search_term}%' OR Notes LIKE '%{letters_search_term}%' OR Created_Time LIKE '%{letters_search_term}%' ORDER BY Preferred_Name ASC;"""
    if letters_search_term == "" or letters_search_term == None:
        get_requesters_query = f"""SELECT Requester_ID, Preferred_Name FROM tbl_Requesters;"""    
    these_requesters = db.execute_read_query_dict(foia_session.connection,get_requesters_query)
   #print(f"get_requesters_query: {get_requesters_query}")
    if these_requesters != None and these_requesters != []:
       #print(f"these_requesters: {these_requesters}")
        #print(these_requesters[0]['Preferred_Name'])
        requester_names = []
        for requester in these_requesters:
            requester_names.append(f'{requester['Requester_ID']} {requester['Preferred_Name']}')
        window['-Letter_From_Input-'].update(values=requester_names)
    else:
        these_requesters = [{"Requester_ID":""}]
        window['-Letter_From_Input-'].update(values=["None"])
    
    #Update the Template Picker
    get_template_query = f"""SELECT Template_ID, Name FROM tbl_Templates;"""
    these_templates = db.execute_read_query_dict(foia_session.connection,get_template_query)
   #print(f"these_templates: {these_templates}")
    foia_session.template_names = []
    for i in range(len(these_templates)):
        foia_session.template_names.append(f"{these_templates[i]['Template_ID']} {these_templates[i]['Name']}")
    window['-Letter_Template_Input-'].update(values=foia_session.template_names)



    #get the applicants
    get_applicants_query = f"""SELECT Applicant_ID, Preferred_Name FROM tbl_Applicants WHERE First_Name LIKE '%{letters_search_term}%' OR Last_Name LIKE '%{letters_search_term}%' OR Full_Name LIKE '%{letters_search_term}%' OR Preferred_Name LIKE '%{letters_search_term}%' OR Return_Address LIKE '%{letters_search_term}%' OR Phone_Number LIKE '%{letters_search_term}%' OR Phone_Number_Type LIKE '%{letters_search_term}%' OR Fax_Number LIKE '%{letters_search_term}%' OR Email LIKE '%{letters_search_term}%' OR Notes LIKE '%{letters_search_term}%' OR Created_Time LIKE '%{letters_search_term}%' ORDER BY Preferred_Name ASC;"""
    if letters_search_term == "" or letters_search_term == None:
        get_applicants_query = f"""SELECT Applicant_ID, Preferred_Name FROM tbl_Applicants ORDER BY Preferred_Name ASC;"""
    these_applicants = db.execute_read_query_dict(foia_session.connection,get_applicants_query)
   #print(these_applicants)



    #Retrieve the letters
    retrieve_letters_query = f"""SELECT * FROM tbl_Letters WHERE Tracking_Number LIKE '%{letters_search_term}%' OR Application_ID LIKE '%{letters_search_term}%' OR Requester_ID LIKE '{these_requesters[0]['Requester_ID']}' OR Responder_ID LIKE '{these_responders[0]['Responder_ID']}' OR Date LIKE '%{letters_search_term}%' OR Status LIKE '%{letters_search_term}%' OR Document LIKE '%{letters_search_term}%' OR Request LIKE '%{letters_search_term}%' OR Message LIKE '%{letters_search_term}%' OR Record LIKE '%{letters_search_term}%' OR Response LIKE '%{letters_search_term}%' OR Forwarding_Letter LIKE '%{letters_search_term}%' OR Forwarding_Letter_Content LIKE '%{letters_search_term}%' OR Created_Time LIKE '%{letters_search_term}%' OR Letter_Code LIKE '%{letters_search_term}%';"""
    if letters_search_term == "" or letters_search_term == None:
        retrieve_letters_query = f"""SELECT * FROM tbl_Letters WHERE Date > '{current_year}/01/01' ORDER BY Date ASC;"""    
    
    these_letters = db.execute_read_query_dict(foia_session.connection,retrieve_letters_query)
   #print(f"retrieve_letters_query: {retrieve_letters_query}")
    foia_session.letter_saved == False
   #print(f'these_letters: {these_letters}')
    if len(these_letters) == 0 and retrieve_letters_query == f"""SELECT * FROM tbl_Letters WHERE Date > '{current_year}/01/01' ORDER BY Date ASC;""" :
        letters_display = [["0","No letters,","create a","New Letter","to get","started,","Requester."]]
        window['-Letters_Display_Content-'].update(letters_display)
        foia_session.new_letter = 1
        activate_new_letter_fields(foia_session.window,values)
    else:
       #print("Loading Letters Display")
        window['-Letter_ID_Input-'].update("", disabled=True)
        window['-Letter_Date_Input-'].update("", disabled=True)
        window['-Letter_To_Input-'].update("", disabled=True)
        window['-Letter_From_Input-'].update("", disabled=True)
        window['-Letter_Document_Input-'].update("", disabled=True)
        window['-Letter_Request_Input-'].update("", disabled=True)
        window['-Letter_Recorded_Input-'].update("", disabled=True)
        window['-Letter_Edited_Input-'].update("", disabled=True)
        window['-Letter_Template_Button-'].update(disabled=True)
        window['-Letter_View_Button-'].update("Letter", disabled=True)
        window['-Letter_Image-'].update("")
        window['-Letter_Image_Input-'].update("", disabled=True)
        window['-Message_View_Button-'].update("Message", disabled=True)
        window['-Letter_Message_Display-'].update("", disabled=True)
        window['-Letter_Template_Input-'].update(disabled=True)
        window['-Letter_Generate_Button-'].update(disabled=True)



        #Retrieve the current year letters and display them in the table
        foia_session.display_letters = []

        for letter in these_letters:

            retrieve_responder_query = f"""SELECT Organization_Name FROM tbl_Responders WHERE Responder_ID = '{letter['Responder_ID']}';"""
            this_responder = db.execute_read_query_dict(foia_session.connection,retrieve_responder_query)
           #print(f"this_responder: {this_responder}")
            retrieve_application_query = f"""SELECT Applicant_ID FROM tbl_Applications WHERE Application_ID = '{letter['Application_ID']}';"""
           #print(f"this_application_query: {retrieve_application_query}") 
            this_application = db.execute_read_query_dict(foia_session.connection,retrieve_application_query)    
           #print(f"this_application: {this_application}") 
            this_applicant = [{"Preferred_Name":""}]
            if type(this_application) == list:
                if len(this_application) > 0:
                    retrieve_applicant_query = f"""SELECT Preferred_Name FROM tbl_Applicants WHERE Applicant_ID = '{this_application[0]['Applicant_ID']}';"""
                   #print(f"retrieve_applicant_query: {retrieve_applicant_query}")
                    this_applicant = db.execute_read_query_dict(foia_session.connection,retrieve_applicant_query)
                   #print(f"this_applicant: {this_applicant}")
            else:
               print(f"this_applicant?: {this_applicant}")
            retrieve_requester_query = f"""SELECT Preferred_Name FROM tbl_Requesters WHERE Requester_ID = '{letter['Requester_ID']}';"""
            this_requester = db.execute_read_query_dict(foia_session.connection,retrieve_requester_query)
           #print(f"this_requester: {this_requester}")
            foia_session.display_letters.append([f"{letter['Tracking_Number']}",f"{letter['Status']}",f"{this_responder[0]['Organization_Name']}",f"{this_applicant[0]['Preferred_Name']}",f"{this_requester[0]['Preferred_Name']}",f"{letter['Date']}"])
        window['-Letters_Display_Content-'].update(foia_session.display_letters)
    return window

def load_selected_template(application_id, template_id,responder_id,requester_id,applicant_id,document,request):
   #print(f"loading template {template_id} for {document} and {request}")
    #todo: be completed with all tags here and in the variable near line 750
    
    load_template_query = f"""SELECT * FROM tbl_Templates WHERE Template_ID is '{template_id}';"""
    this_template = db.execute_read_query_dict(foia_session.connection,load_template_query)
   #print(load_template_query)
    this_template_text = this_template[0]['Body_Content'].replace("~","'")
    
    #Application

    foia_session.this_letter['Application_ID'] = application_id

    #TO Field (Responder Data)
    foia_session.this_letter['Responder_ID'] = responder_id
    get_responder_query = f"""SELECT * FROM tbl_Responders WHERE Responder_ID IS '{responder_id}';"""
   #print(get_responder_query)
    this_responder = db.execute_read_query_dict(foia_session.connection,get_responder_query)
   #print(f"""This Responder: {this_responder}""")
    if this_responder != [] and type(this_responder) == list:
        responder_org_name = this_responder[0]['Organization_Name']
        responder_address = this_responder[0]['Organization_Mailing_Address']
       #print(f'responder_address: {responder_address}')
        if responder_address == "" or responder_address == None or responder_address.replace('\n','') == "":
            responder_address = this_responder[0]['Organization_Address']

        
        split_address = responder_address.splitlines()
        responder_address = ""
        for address_line in split_address:
            responder_address = responder_address + address_line + "['-new_line-']"
            
        
        this_template_text = this_template_text.replace("['-Letter_To_Field-']",f"""{responder_org_name}['-new_line-']{responder_address}""")

        this_template_text = this_template_text.replace("['-Responder_Preferred_Name-']",f"{this_responder[0]['Preferred_Name']}")

        this_template_text = this_template_text.replace("['-Responder_Organization_Name-']",f"{this_responder[0]['Organization_Name']}")
        this_template_text = this_template_text.replace("['-Responder_Organization_Type-']",f"{this_responder[0]['Organization_Type']}")
        this_template_text = this_template_text.replace("['-Responder_Contact_First_Name-']",f"{this_responder[0]['Contact_First_Name']}")
        this_template_text = this_template_text.replace("['-Responder_Contact_Last_Name-']",f"{this_responder[0]['Contact_Last_Name']}")
        this_template_text = this_template_text.replace("['-Responder_Contact_Email-']",f"{this_responder[0]['Contact_Email']}")
        this_template_text = this_template_text.replace("['-Responder_Phone_Number-']",f"{this_responder[0]['Phone_Number']}")
        this_template_text = this_template_text.replace("['-Responder_Phone_Number_Type-']",f"{this_responder[0]['Phone_Number_Type']}")
        this_template_text = this_template_text.replace("['-Responder_Fax_Number-']",f"{this_responder[0]['Fax_Number']}")
        this_template_text = this_template_text.replace("['-Responder_Organization_Address-']",f"{this_responder[0]['Organization_Address']}")
        this_template_text = this_template_text.replace("['-Responder_Organization_Mailing_Address-']",f"{this_responder[0]['Organization_Mailing_Address']}")
        this_template_text = this_template_text.replace("['-Responder_Organization_Email-']",f"{this_responder[0]['Organization_Email']}")
        this_template_text = this_template_text.replace("['-Responder_Organization_Website-']",f"{this_responder[0]['Organization_Website']}")
        this_template_text = this_template_text.replace("['-Responder_Notes-']",f"{this_responder[0]['Notes']}")




    #FROM Field (Requester Data)
    foia_session.this_letter['Requester_ID'] = requester_id
    get_requester_query = f"""SELECT * FROM tbl_Requesters WHERE Requester_ID IS '{requester_id}';"""
    #print(get_requester_query)
    this_requester = db.execute_read_query_dict(foia_session.connection,get_requester_query)
    #print(f"""This Requester: {this_requester}""")

    if this_requester != [] and type(this_requester) == list:
        requester_name = this_requester[0]['Preferred_Name']

        requester_address = this_requester[0]['Return_Address']  

        split_address = requester_address.splitlines()
        requester_address = ""
        for address_line in split_address:
            requester_address = requester_address + address_line + "['-new_line-']"



        this_template_text = this_template_text.replace("['-Letter_From_Field-']",f'{requester_name}\n{foia_session.organization_name}\n{requester_address}')

        this_template_text = this_template_text.replace("['-Requester_Preferred_Name-']",f"{requester_name}")
        this_template_text = this_template_text.replace("['-Requester_Phone-']",f"{this_requester[0]['Phone_Number']}")
        if this_requester[0]['Phone_Number_Type'] == None:
            this_requester[0]['Phone_Number_Type'] = ""
        this_template_text = this_template_text.replace("['-Requester_Phone_Number_Type-']",f"{this_requester[0]['Phone_Number_Type']}")
        this_template_text = this_template_text.replace("['-Requester_Email-']",f"{this_requester[0]['Email']}")    

        this_template_text = this_template_text.replace("['-Requester_First_Name-']",f"{this_requester[0]['First_Name']}")
        this_template_text = this_template_text.replace("['-Requester_Middle_Name-']",f"{this_requester[0]['Middle_Name']}")
        this_template_text = this_template_text.replace("['-Requester_Last_Name-']",f"{this_requester[0]['Last_Name']}")
        this_template_text = this_template_text.replace("['-Requester_Full_Name-']",f"{this_requester[0]['Full_Name']}")
        this_template_text = this_template_text.replace("['-Requester_Return_Address-']",f"{this_requester[0]['Return_Address']}")
        this_template_text = this_template_text.replace("['-Requester_Fax_Number-']",f"{this_requester[0]['Fax_Number']}")
        this_template_text = this_template_text.replace("['-Requester_Notes-']",f"{this_requester[0]['Notes']}")




    #Application Requests
    this_template_text = this_template_text.replace("['-Requested_Records-']",f"{request}")
    this_template_text = this_template_text.replace("['-Requested_Document-']",f"{document}")



    #Applicant Data
   #print(f"Application_ID: {foia_session.this_letter['Application_ID']}")
    if application_id != "0" and int(application_id) > 0:
        get_applicant_query = f"""SELECT * FROM tbl_Applicants WHERE Applicant_ID is '{applicant_id}';"""
        #print(f"get applicant query: {get_applicant_query}")
        this_applicant = db.execute_read_query_dict(foia_session.connection,get_applicant_query)
        if this_applicant != [] and type(this_applicant) == list:
        #print(f"this applicant: {this_applicant}")

            this_template_text = this_template_text.replace("['-Applicant_Preferred_Name-']",f"{this_applicant[0]['Preferred_Name']}")
            this_template_text = this_template_text.replace("['-Applicant_First_Name-']",f"{this_applicant[0]['First_Name']}")
            this_template_text = this_template_text.replace("['-Applicant_Middle_Name-']",f"{this_applicant[0]['Middle_Name']}")
            this_template_text = this_template_text.replace("['-Applicant_Last_Name-']",f"{this_applicant[0]['Last_Name']}")
            this_template_text = this_template_text.replace("['-Applicant_Title-']",f"{this_applicant[0]['Title']}")
            this_template_text = this_template_text.replace("['-Applicant_Full_Name-']",f"{this_applicant[0]['Full_Name']}")
            this_template_text = this_template_text.replace("['-Applicant_Phone_Number-']",f"{this_applicant[0]['Phone_Number']}")
            this_template_text = this_template_text.replace("['-Applicant_Phone_Number_Type-']",f"{this_applicant[0]['Phone_Number_Type']}")
            this_template_text = this_template_text.replace("['-Applicant_Fax_Number-']",f"{this_applicant[0]['Fax_Number']}")
            this_template_text = this_template_text.replace("['-Applicant_Return_Address-']",f"{this_applicant[0]['Return_Address']}")
            this_template_text = this_template_text.replace("['-Applicant_Notes-']",f"{this_applicant[0]['Notes']}")
            this_template_text = this_template_text.replace("['-Applicant_Email-']",f"{this_applicant[0]['Email']}")

            this_template_text = this_template_text.replace("['-Application_Number-']",f"{application_id}")

    #Requester Org
    this_letter_text = this_template_text.replace("['-Organization_Name-']",f"{foia_session.organization_name}")


    charcount = 0
    corrected_text = this_letter_text
    



   #print(corrected_text)
    foia_session.this_letter['Message']=corrected_text
    foia_session.this_letter_body = corrected_text

    
    return corrected_text


def id_generator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_text_width(input_text):
    font = ImageFont.truetype('./LiberationSerif-Regular.ttf', 50)      
    test_canvas = Image.new('RGB', (2550, 3300), "white")
    test_draw = ImageDraw.Draw(test_canvas)
    input_text = f"{input_text}".replace("\\n","")
    input_text = f"{input_text}".splitlines()
    if len(input_text) == 1:
    
        return ImageDraw.ImageDraw.textlength(test_draw, text=input_text[0], font=font)
    else:
        print("Text width not found!")
        return 2100.0



def generate_new_letter(window,values):

    foia_session.this_letter['Letter_Code'] = id_generator()
    
    this_letter_id = foia_session.this_letter_id
    extra_whitespace = "    "
    this_letter_text = foia_session.this_letter_body
            
   #print(f"this_letter_text {this_letter_text}")



    charcount = 0
    corrected_text = ""
    for i in range(len(this_letter_text)):
        #Count the number of characters in the current line
        #print(this_letter_text[i-14:i])

        minimum_width = 2000
        target_width = 2100
        
        if i<=len(this_letter_text)-14:
            this_new_line = False
            for j in range(14):
                if this_letter_text[i-j:i+14-j] == "['-new_line-']":
                    this_new_line = True
            if this_new_line:
                corrected_text = corrected_text + this_letter_text[i]
               #print(f"newline found {i} to {i+14}, {charcount}")
               #print(f"corrected text {corrected_text[-15:]}")
                charcount = 0

            #Test this           
            elif charcount > 96 and this_letter_text[i] == " ":
                this_width = get_text_width(corrected_text)
                if this_width > minimum_width:
                    corrected_text = corrected_text + this_letter_text[i] + "['-new_line-']"
                    charcount = 0    
                else:
                    corrected_text = corrected_text + this_letter_text[i]
                    charcount = charcount + 1

            elif charcount == 99 and i<=len(this_letter_text)-4 and this_letter_text[i+1] != " " and this_letter_text[i+2] != " " and this_letter_text[i+3] != " " and this_letter_text[i+4] != " ":                
                corrected_text = corrected_text + this_letter_text[i] + "-['-new_line-']"
                charcount = 0 

            else:
                corrected_text = corrected_text + this_letter_text[i]
                charcount = charcount + 1
        else:
                corrected_text = corrected_text + this_letter_text[i]
            

    foia_session.this_letter_body = corrected_text
    #num_lines = len(lines)
    #print(lines)





    #Split the text into lines
    corrected_text = f"""{corrected_text}"""
   #print(corrected_text)
    lines = corrected_text.split("""['-new_line-']""")
   #print(lines)
    num_lines = len(lines)
    lines_per_page = 53
    min_lines = 12
    num_pages = int(math.ceil(num_lines/lines_per_page))
   #print(f"num_pages = {num_pages}")

    numlines_lastpage = num_lines%lines_per_page
   #print(numlines_lastpage)
    lastpage_extended = False
    if numlines_lastpage < min_lines and num_lines > lines_per_page:
        lastpage_extended = True

    #Get the organization Name
    get_org_name_query = f"""SELECT Property_Value FROM tbl_Properties WHERE Property_Name IS 'Organization Name';"""
    this_org = db.execute_read_query_dict(foia_session.connection,get_org_name_query)
    this_org_name = ""
    if this_org != [] and type(this_org) == list:
        this_org_name = this_org[0]['Property_Value']
    
    #Create the directory
    filenames = []
    foldername = foia_session.this_letter_id
    folderpath = f'{foia_session.documents_location}/Letters/{foldername}'
    #Create the letter directory, if it doesn't already exist
    if os.path.isdir(f'{foia_session.documents_location}/Letters') == False:
        os.mkdir(f'{foia_session.documents_location}/Letters')
    if os.path.isdir(folderpath) == False:
        os.mkdir(folderpath)
 

    #Generate the pages
    for i in range(num_pages):

        #Set text attributes
        font = ImageFont.truetype('./LiberationSerif-Regular.ttf', 50)      
        test_canvas = Image.new('RGB', (2550, 3300), "white")
        test_draw = ImageDraw.Draw(test_canvas)
        canvas = Image.new('RGB', (2550, 3300), "white")
        
        draw = ImageDraw.Draw(canvas)
        min_line_width = 1950
        max_line_width = 2150
        target = 2100
        this_page = ""

        if i==0:
            if i == num_pages - 2 and lastpage_extended == True:
                for line in lines[:len(lines)-min_lines]:
                    corrected_line = line
                    if len(line.splitlines()) == 1:
                        line_width = ImageDraw.ImageDraw.textlength(test_draw, text=line, font=font)
                        #print(f"line_width: {line_width}")
                        if line_width > min_line_width and line_width < target:
                            
                            for j in range(10):
                                corrected_line = corrected_line.replace("  "," ")
                                corrected_line = corrected_line.replace(" ","  ",int(j+1))
                                new_line_width = ImageDraw.ImageDraw.textlength(test_draw, text=corrected_line, font=font)
                                if new_line_width > target:

                                    break
                    this_page = this_page+f"{corrected_line}" +"\n"  
            else:
                for line in lines[:((lines_per_page)*(i+1))]:
                    corrected_line = line
                    if len(line.splitlines()) == 1:
                        line_width = ImageDraw.ImageDraw.textlength(test_draw, text=line, font=font)
                        #print(f"line_width: {line_width}")
                        if line_width > min_line_width and line_width < target:
                            
                            for j in range(10):
                                corrected_line = corrected_line.replace("  "," ")
                                corrected_line = corrected_line.replace(" ","  ",int(j+1))
                                new_line_width = ImageDraw.ImageDraw.textlength(test_draw, text=corrected_line, font=font)
                                if new_line_width > target:
                                    #print(f"new_line_width: {new_line_width}")
                                    #print(f"line: {line}")
                                    #print(f"corrected line: {corrected_line}")
                                    break
                    this_page = this_page+f"{corrected_line}"+"\n"              
        elif i < num_pages - 1:
            if i == num_pages - 2 and lastpage_extended == True:
                for line in lines[lines_per_page*i:len(lines)-min_lines]:
                    corrected_line = line
                    if len(line.splitlines()) == 1:
                        line_width = ImageDraw.ImageDraw.textlength(test_draw, text=line, font=font)
                        #print(f"line_width: {line_width}")
                        if line_width > min_line_width and line_width < target:
                            #print(f"line_width: {line_width}")
                            for j in range(10):
                                corrected_line = corrected_line.replace("  "," ")
                                corrected_line = corrected_line.replace(" ","  ",int(j+1))
                                new_line_width = ImageDraw.ImageDraw.textlength(test_draw, text=corrected_line, font=font)
                                if new_line_width > target:
                                    break
                    this_page = this_page+f"{corrected_line}" +"\n"  
            else:
                for line in lines[lines_per_page*i:(lines_per_page*(i+1))]:
                    corrected_line = line
                    if len(line.splitlines()) == 1:
                        line_width = ImageDraw.ImageDraw.textlength(test_draw, text=line, font=font)
                        #print(f"line_width: {line_width}")
                        if line_width > min_line_width and line_width < target:
                            #print(f"line_width: {line_width}")
                            for j in range(10):
                                corrected_line = corrected_line.replace("  "," ")
                                corrected_line = corrected_line.replace(" ","  ",int(j+1))
                                new_line_width = ImageDraw.ImageDraw.textlength(test_draw, text=corrected_line, font=font)
                                if new_line_width > target:
                                    break
                    this_page = this_page+f"{corrected_line}"+"\n"  
        elif i == num_pages - 1 and lastpage_extended == True:
            for line in lines[len(lines)-min_lines:]:
                corrected_line = line
                if len(line.splitlines()) == 1:
                        line_width = ImageDraw.ImageDraw.textlength(test_draw, text=line, font=font)
                        print(f"line_width: {line_width}")
                        if line_width > min_line_width and line_width < target:
                            print(f"line_width: {line_width}")
                            for j in range(10):
                                corrected_line = corrected_line.replace("  "," ")
                                corrected_line = corrected_line.replace(" ","  ",int(j+1))
                                new_line_width = ImageDraw.ImageDraw.textlength(test_draw, text=corrected_line, font=font)
                                if new_line_width > target:
                                    break
                this_page = this_page+f"{corrected_line}"+"\n"     
        elif i == num_pages - 1 and lastpage_extended == False:
            for line in lines[lines_per_page*i:]:
                corrected_line = line
                if len(line.splitlines()) == 1:
                        line_width = ImageDraw.ImageDraw.textlength(test_draw, text=line, font=font)
                        print(f"line_width: {line_width}")
                        if line_width > min_line_width and line_width < target:
                            print(f"line_width: {line_width}")
                            for j in range(10):
                                corrected_line = corrected_line.replace("  "," ")
                                corrected_line = corrected_line.replace(" ","  ",int(j+1))
                                new_line_width = ImageDraw.ImageDraw.textlength(test_draw, text=corrected_line, font=font)
                                if new_line_width > target:
                                    break
                this_page = this_page+f"{corrected_line}"+"\n"     


        filename = f"{foia_session.this_letter_id}_{i}.png"
        #CENTER IS 1275,1650

        #Find the offset for the Org Name
        left_shift = len(this_org_name)*25/2

        #Todo: correct to full justify
        #ImageDraw.textlength() #This will 

        filenames.append(filename)
        #Draw the letter page
        draw.text((225,225),f"{foia_session.this_letter_id}{extra_whitespace}                                                                                                                   {current_date}", '#000000', font)
        draw.text((225,325),this_page, '#000000', font)
        draw.text((1275-(20*25),3035),f"{foia_session.this_letter['Letter_Code']}",'#000000',font)
        draw.text((1275-left_shift,3100),f"{this_org_name}",'#000000',font)
        draw.text((1275-(7*25),3165),f"Page {i+1} of {num_pages}",'#000000',font)
        


        canvas.save(f'{folderpath}/{filename}', "PNG")
        #img2pdf
        

       #print(f"Generated Page {i+1}")

    # convert all files ending in .png in a directory and its subdirectories tp PDF format
    dirname = folderpath
    images = []
    for r, _, f in os.walk(dirname):
        for fname in f:
            if not fname.endswith(".png"):
                continue
            images.append(os.path.join(r, fname))
    images.sort()
    dpix = dpiy = 300
    this_layout = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
    filepath = f"{folderpath}/{foldername}.pdf"
    with open(filepath,"wb") as f:
        f.write(img2pdf.convert(images,layout_fun=this_layout))    

    #DO not remove images
    #time.sleep(0.15)
    #for image in images:
    #    os.remove(f"{image}")
    
    
    #these_flags = os.O_RDWR
    #os.open(filepath,flags=these_flags)

    #subprocess.Popen([filepath],shell=True)
    #Opens the pdf. Should be modified so that it doesn't open a new pdf for each letter when processing an application.
    

    foia_session.console_log(f"Letter {this_letter_id} Generated",foia_session.current_console_messages)


    return filepath, images


def update_requesters_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the requesters
    this_tab_index = 6
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    current_year = datetime.datetime.now().year
    #start_date = f"{current_year[2:]}-01-01"
    #end_date = f"{int(current_year[2:])+1}-01-01"

   #print('Requesters_Search_Input')
   #print(values['-Requesters_Search_Input-'])
    
    if values['-Requesters_Search_Input-'] == '':
        retrieve_requesters_query = f"""SELECT * FROM tbl_Requesters;"""
        requesters = db.execute_read_query_dict(foia_session.connection,retrieve_requesters_query)
       #print(retrieve_requesters_query)
       #print(requesters)
        #Requester_ID, Preferred_Name, Phone, Email, Created_Time

        foia_session.requesters = []
        if requesters != [] and type(requesters) == list:
            for requester in requesters:

                get_open_letters_query = f"""SELECT Count(*) FROM tbl_Letters WHERE Status is 'Open' AND Requester_ID IS '{requester['Requester_ID']}' OR Status is 'Action' AND Requester_ID IS '{requester['Requester_ID']}';"""
                open_letters_count = db.execute_read_query_dict(foia_session.connection,get_open_letters_query)
                open_letters_number = 0
                if type(open_letters_count) == list and len(open_letters_count) == 1:
                    open_letters_number = open_letters_count[0]['Count(*)']
                foia_session.requesters.append([requester['Requester_ID'],requester['Preferred_Name'],f"{open_letters_number}",requester['Phone_Number'],requester['Email']])
        window['-Requesters_Display_Content-'].update(foia_session.requesters)
        return window        
    else:
        retrieve_requesters_query = f"""SELECT * FROM tbl_Requesters WHERE Requester_ID = '{values['-Requesters_Search_Input-']}' OR First_Name LIKE '%{values['-Requesters_Search_Input-']}%' OR Middle_Name LIKE '%{values['-Requesters_Search_Input-']}%' OR Last_Name LIKE '%{values['-Requesters_Search_Input-']}%' OR Full_Name LIKE '%{values['-Requesters_Search_Input-']}%' OR Preferred_Name LIKE '%{values['-Requesters_Search_Input-']}%' OR Return_Address LIKE '%{values['-Requesters_Search_Input-']}%' OR Phone_Number LIKE '%{values['-Requesters_Search_Input-']}%' OR Fax_Number LIKE '%{values['-Requesters_Search_Input-']}%' OR Email LIKE '%{values['-Requesters_Search_Input-']}%' OR Photo LIKE '%{values['-Requesters_Search_Input-']}%' OR Notes LIKE '%{values['-Requesters_Search_Input-']}%';"""
        requesters = db.execute_read_query_dict(foia_session.connection,retrieve_requesters_query)
       #print(retrieve_requesters_query)
       #print(requesters)
        #Requester_ID, Preferred_Name, Phone, Email, Created_Time
        foia_session.requesters = []
        if requesters != [] and type(requesters) == list:
            for requester in requesters:
                get_open_letters_query = f"""SELECT Count(*) FROM tbl_Letters WHERE Status is 'Open' AND Requester_ID IS '{requester['Requester_ID']}' OR Status is 'Action' AND Requester_ID IS '{requester['Requester_ID']}';"""
                open_letters_count = db.execute_read_query_dict(foia_session.connection,get_open_letters_query)
                open_letters_number = 0
                if type(open_letters_count) == list and len(open_letters_count) == 1:
                    open_letters_number = open_letters_count[0]['Count(*)']
                foia_session.requesters.append([requester['Requester_ID'],requester['Preferred_Name'],f"{open_letters_number}",requester['Phone_Number'],requester['Email']])

        window['-Requesters_Display_Content-'].update(foia_session.requesters)
        return window

def update_view_records_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 7
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"


    return window    

def update_documentation_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 8
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"


    return window       

def update_about_view(window,values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 9
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"


    return window      

def update_properties_view(window, values, connection):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 10
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"
    if connection==False:
       print("Error: load_database_properties_tab did not execute. Not connected to database.")
    else:

        retrieve_properties_query = f"""SELECT * FROM tbl_Properties"""

        current_properties = db.execute_read_query_dict(connection, retrieve_properties_query)
       #print(current_properties)
        if current_properties != [] and type(current_properties) == list:
            for property in current_properties:

                property_name = property['Property_Name']
                property_value = property['Property_Value']

                if property_name == "Organization Name":
                    window['-edit_db_name-'].update(property_value)
                elif property_name == "Address":
                    window['-Edit_Organization_Address-'].update(property_value)
                elif property_name == "Organization Acronym":
                    window['-Edit_Organization_Acronym-'].update(property_value)
                elif property_name == "Manager First Name":
                    window['-Edit_Manager_First-'].update(property_value)
                elif property_name == "Manager Middle Name":
                    window['-Edit_Manager_Middle-'].update(property_value)

                elif property_name == "Manager Last Name":
                    window['-Edit_Manager_Last-'].update(property_value)
                elif property_name == "Manager Preferred Name":
                    window['-Edit_Manager_Preferred-'].update(property_value)
                elif property_name == "Manager Full Name":
                    window['-Edit_Manager_Full-'].update(property_value)
                elif property_name == "Manager Title":
                    window['-Edit_Manager_Title-'].update(property_value)

                elif property_name == "Organization Phone":
                    window['-Edit_Organization_Phone-'].update(property_value)
                elif property_name == "Organization Email":
                    window['-Edit_Organization_Email-'].update(property_value)
                elif property_name == "Organization Notes":
                    window['-Edit_Organization_Notes-'].update(property_value)
                elif property_name == "Documents Repository Location":
                    window['-Edit_Documents_Repository-'].update(property_value)
    return window

def generate_template_preview(window,values):

    this_template_text = values['-Templates_Edit_Content-']
    this_letter_id = f"{foia_session.organization_acronym}-LTR-{10000}"
    extra_whitespace = "    "




            

    charcount = 0
    corrected_text = ""
    for i in range(len(this_template_text)):
        #Count the number of characters in the current line
        #print(this_letter_text[i-14:i])
        if this_template_text[i-14:i] == "['-new_line-']":
            corrected_text = corrected_text + this_template_text[i]
            #print(f"newline found {i}, {charcount}")
            charcount = 1
        elif charcount > 96 and this_template_text[i] == " ":
            corrected_text = corrected_text + "['-new_line-']"
            charcount = 0            
        elif charcount == 99 and i<=len(this_template_text)-3 and this_template_text[i+1] != " " and this_template_text[i+2] != " " and this_template_text[i+3] != " ":
            corrected_text = corrected_text + this_template_text[i] + "-['-new_line-']"
            charcount = 0 
        else:
            corrected_text = corrected_text + this_template_text[i]
            charcount = charcount + 1


    
    #num_lines = len(lines)
    #print(lines)


    #Split the text into lines
    lines = corrected_text.split("['-new_line-']")
   #print(lines)
    num_lines = len(lines)
    lines_per_page = 54
    min_lines = 12
    num_pages = int(math.ceil(num_lines/lines_per_page))
   #print(f"num_pages = {num_pages}")

    numlines_lastpage = num_lines%lines_per_page
   #print(numlines_lastpage)
    lastpage_extended = False
    if numlines_lastpage < min_lines and num_lines > lines_per_page:
        lastpage_extended = True

    filenames = []
    folderpath = f'{foia_session.documents_location}'
    #Create the letter directory, if it doesn't already exist

    #Generate the pages
    for i in range(num_pages):
        this_page = ""

        if i==0:
            if i == num_pages - 2 and lastpage_extended == True:
                for line in lines[:len(lines)-min_lines]:
                    this_page = this_page+line +"\n"  
            else:
                for line in lines[:((lines_per_page)*(i+1))]:
                    this_page = this_page+line+"\n"              
        elif i < num_pages - 1:
            if i == num_pages - 2 and lastpage_extended == True:
                for line in lines[lines_per_page*i:len(lines)-min_lines]:
                    this_page = this_page+line +"\n"  
            else:
                for line in lines[lines_per_page*i:(lines_per_page*(i+1))]:
                    this_page = this_page+line+"\n"  
        elif i == num_pages - 1 and lastpage_extended == True:
            for line in lines[len(lines)-min_lines:]:
                this_page = this_page+line+"\n"     
        elif i == num_pages - 1 and lastpage_extended == False:
            for line in lines[lines_per_page*i:]:
                this_page = this_page+line+"\n"     
        #Set text attributes
        font = ImageFont.truetype('./LiberationSerif-Regular.ttf', 50)        
        canvas = Image.new('RGB', (2550, 3300), "white")
        draw = ImageDraw.Draw(canvas)
        filename = f"{this_letter_id}_{i}.png"
        #CENTER IS 1275,1650

        #Find the offset for the Org Name
        org_name = foia_session.organization_name
        left_shift = len(org_name)*25/2


        filenames.append(filename)
        #Draw the letter page
        draw.text((225,225),f"{this_letter_id}{extra_whitespace}                                                                                                                   {current_date}", '#000000', font)
        draw.text((225,325),this_page, '#000000', font)
        draw.text((1275-left_shift,3100),f"{org_name}",'#000000',font)
        draw.text((1275-(7*25),3165),f"Page {i+1} of {num_pages}",'#000000',font)
        


        canvas.save(f'{folderpath}/{filename}', "PNG")
        #img2pdf
        

       #print(f"Generated Page {i+1}")

    # convert all files ending in .png in a directory and its subdirectories tp PDF format
    dirname = folderpath
    images = []
    for r, _, f in os.walk(dirname):
        for fname in f:
            if not fname.endswith(".png"):
                continue
            images.append(os.path.join(r, fname))
    images.sort()
    dpix = dpiy = 300
    this_layout = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
    if os.path.isdir(f'{foia_session.documents_location}/Preview') == False:
        os.mkdir(f'{foia_session.documents_location}/Preview')
    filepath = f"{folderpath}/Preview/template_preview.pdf"
    with open(filepath,"wb") as f:
        f.write(img2pdf.convert(images,layout_fun=this_layout))    

    time.sleep(0.15)
    for image in images:
        os.remove(f"{image}")
    
    
    #these_flags = os.O_RDWR
    #os.open(filepath,flags=these_flags)

    #subprocess.Popen([filepath],shell=True)
    #Opens the pdf. Should be modified so that it doesn't open a new pdf for each letter when processing an application.
    subprocess.call(["xdg-open", filepath])

    foia_session.console_log(f"Letter Template Generated",foia_session.current_console_messages)




def edit_selected_template(window, values):
    template_index = values['-Templates_List-'][0]
    template_input = foia_session.display_templates[template_index][0]
   #print(window['-Templates_List-'])
   #print(f"Template_Input: {template_input}")
    template_id = ""
    for char in template_input:
        if char == "0" or char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6" or char == "7" or char == "8" or char == "9":
            template_id = template_id + char
        elif char == " ":
            break
    
    get_template_query = f"""SELECT * FROM tbl_Templates WHERE Template_ID IS '{template_id}';"""
    foia_session.this_template = db.execute_read_query_dict(foia_session.connection,get_template_query)
   #print(f"{foia_session.this_template}")
    if foia_session.this_template != [] and type(foia_session.this_template) == list:
        window['-Templates_Edit_Content-'].update(foia_session.this_template[0]['Body_Content'].replace("~","'"))
        window['-Templates_Notes_Display-'].update(foia_session.this_template[0]['Notes'].replace("~","'"))
        window['-New_Template_Button-'].update("Save Changes")
        window['-Templates_Name_Input-'].update(foia_session.this_template[0]['Name'], disabled=True)

def save_edit_template(window,values) :
    
    save_edit_template_query = f"""UPDATE tbl_Templates SET """

    now, nowish = get_current_time_info()
   #print(nowish)

    corrected_body_content = f"""{values['-Templates_Edit_Content-']}""".replace("'","~")
    corrected_notes = f"""{values['-Templates_Notes_Display-']}""".replace("'","~")

    lines = [
        f"""Name = '{values['-Templates_Name_Input-']}', """,
        f"""Body_Content = '{corrected_body_content}', """,
        f"""Notes = '{corrected_notes}', """,
        f"""Edited_Time = '{now}' """,
    ]
    closing_statement = f"""WHERE Template_ID = '{foia_session.this_template[0]['Template_ID']}';"""
    for line in lines:
        save_edit_template_query = save_edit_template_query + line
    save_edit_template_query = save_edit_template_query + closing_statement


   #print(f"save_edit_template_query: {save_edit_template_query}")

    saved_template = db.execute_query(foia_session.connection,save_edit_template_query)
    foia_session.console_log(f"Saved Template {foia_session.this_template} {values['-Templates_Name_Input-']}: {saved_template}", foia_session.current_console_messages)



def save_new_template(window,values):
    corrected_body_content = f"""{values['-Templates_Edit_Content-']}""".replace("'","~")
    corrected_notes = f"""{values['-Templates_Notes_Display-']}""".replace("'","~")


    save_new_template_query = f"""INSERT INTO tbl_Templates (Body_Content, Name, Notes, Created_Time, Edited_Time) VALUES('{corrected_body_content}','{values['-Templates_Name_Input-']}','{corrected_notes}','{now}','{now}');"""
    #print(f"save_new_template_query: {save_new_template_query}")
    saved_template = db.execute_query(foia_session.connection,save_new_template_query)
    saved_template_string = f"{saved_template}"
   #print(saved_template_string[:4])
    if saved_template_string[:4] != "UNIQ":
        update_templates_view(foia_session.window, values)   
        foia_session.window['-New_Template_Button-'].update("New Template")  
        foia_session.console_log(f"Saved new Template {foia_session.new_template_number} {values['-Templates_Name_Input-']}: {saved_template}",foia_session.current_console_messages)
    else:
        foia_session.console_log(f"Check New Template Name: Must be Unique",foia_session.current_console_messages)



def update_new_template_list(window,values):
    new_template_name = f"{values['-Templates_Name_Input-']}"#.replace(" ","\ ") 
    window['-Templates_List-'].update([[f"""{foia_session.new_template_number} {new_template_name}"""]])

def activate_new_template_fields(window,values):
    new_template_format = f"""To:['-new_line-']['-Letter_To_Field-']['-new_line-']['-new_line-']From:['-new_line-']['-Letter_From_Field-']['-new_line-']['-new_line-']Subject: ['-new_line-']['-new_line-']Dear ['-Requester_Preferred_Name-'],['-new_line-']   Body Content goes here.['-new_line-']['-new_line-']Sincerely,['-new_line-']['-Requester_Preferred_Name-']['-new_line-']________________________['-new_line-']['-Requester_Phone-']['-new_line-']['-Requester_Email-']"""
    window['-Templates_Edit_Content-'].update(new_template_format)
    window['-Templates_Notes_Display-'].update("Notes: ")
    get_max_template_query = f"""SELECT MAX(Template_ID) FROM tbl_Templates;"""
    max_template = db.execute_read_query_dict(foia_session.connection,get_max_template_query)
    if max_template != [] and type(max_template) == list:
        foia_session.new_template_number = int(max_template[0]['MAX(Template_ID)'])+1
        
        window['-Templates_List-'].update([[f"{foia_session.new_template_number} Enter Name"]])
        window['-Templates_Search_Input-'].update("")
        window['-Templates_Name_Input-'].update("", disabled=False)

def update_templates_view(window, values):
    foia_session.this_template = 0
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 11
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"
    template_search_term = values['-Templates_Search_Input-']
    get_templates_query = f"""SELECT * FROM tbl_Templates WHERE Name LIKE '%{template_search_term}%' or Body_Content LIKE '%{template_search_term}%' or Notes LIKE '%{template_search_term}%';"""
    if template_search_term == None or template_search_term == "":
        get_templates_query = f"""SELECT * FROM tbl_Templates;"""
    these_templates = db.execute_read_query_dict(foia_session.connection,get_templates_query)
   #print(f"these_templates: {these_templates}")
    foia_session.display_templates = []
    if these_templates != [] and type(these_templates) == list:
        for template in these_templates:
            entry = [f"""{template['Template_ID']} {template['Name']}"""]
           #print(entry)
            foia_session.display_templates.append(entry)
    window['-Templates_List-'].update(foia_session.display_templates)
    
    window['-Templates_Notes_Display-'].update("")
    window['-Templates_Edit_Content-'].update("Select a template to get started.")
    window['-New_Template_Button-'].update("New Template")
    window['-Templates_Name_Input-'].update("", disabled=True)
    foia_session.new_template_number = 0
    return window        

def update_applicants_view(window, values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 12
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"

   #print('Applicants_Search_Input')
   #print(values['-Applicants_Search_Input-'])
    
    if values['-Applicants_Search_Input-'] == '':
        retrieve_applicants_query = f"""SELECT * FROM tbl_Applicants;"""
        applicants = db.execute_read_query_dict(foia_session.connection,retrieve_applicants_query)
       #print(retrieve_applicants_query)
       #print(applicants)
        #Applicant_ID, Preferred_Name, Phone, Email, Created_Time
        foia_session.applicants = []
        if applicants != [] and type(applicants) == list:
            for applicant in applicants:
                get_applications_query = f"""SELECT Application_ID FROM tbl_Applications WHERE Applicant_ID IS '{applicant['Applicant_ID']}';"""
                these_applications = db.execute_read_query_dict(foia_session.connection,get_applications_query)
                applicant_open_letters = 0
               #print(these_applications)
                if len(these_applications) > 0 and type(these_applications) == list:
                    for i in range(len(these_applications)):
                        count_open_letters_query = f"""SELECT Count(*) FROM tbl_Letters WHERE Application_ID IS '{these_applications[i]['Application_ID']}' AND Status IS 'Open' OR Application_ID IS '{these_applications[i]['Application_ID']}' AND Status IS 'Action';"""
                        open_letters_count = db.execute_read_query_dict(foia_session.connection,count_open_letters_query)
                       #print(open_letters_count)
                        if len(open_letters_count) > 0 and type(open_letters_count) == list:
                            applicant_open_letters = applicant_open_letters + open_letters_count[0]['Count(*)']
                foia_session.applicants.append([applicant['Applicant_ID'],applicant['Preferred_Name'],applicant_open_letters,applicant['Phone_Number'],applicant['Email']])
        window['-Applicants_Display_Content-'].update(foia_session.applicants)
        return window        
    else:
        retrieve_applicants_query = f"""SELECT * FROM tbl_Applicants WHERE Applicant_ID = '{values['-Applicants_Search_Input-']}' OR First_Name LIKE '%{values['-Applicants_Search_Input-']}%' OR Middle_Name LIKE '%{values['-Applicants_Search_Input-']}%' OR Last_Name LIKE '%{values['-Applicants_Search_Input-']}%' OR Full_Name LIKE '%{values['-Applicants_Search_Input-']}%' OR Preferred_Name LIKE '%{values['-Applicants_Search_Input-']}%' OR Return_Address LIKE '%{values['-Applicants_Search_Input-']}%' OR Phone_Number LIKE '%{values['-Applicants_Search_Input-']}%' OR Fax_Number LIKE '%{values['-Applicants_Search_Input-']}%' OR Email LIKE '%{values['-Applicants_Search_Input-']}%' OR Title LIKE '%{values['-Applicants_Search_Input-']}%' OR Notes LIKE '%{values['-Applicants_Search_Input-']}%';"""
        applicants = db.execute_read_query_dict(foia_session.connection,retrieve_applicants_query)
       #print(retrieve_applicants_query)
       #print(applicants)
        #Applicant_ID, Preferred_Name, Phone, Email, Created_Time
        foia_session.applicants = []
        if applicants != [] and type(applicants) == list:
            for applicant in applicants:
                get_applications_query = f"""SELECT Application_ID FROM tbl_Applications WHERE Applicant_ID IS '{applicant['Applicant_ID']}';"""
                these_applications = db.execute_read_query_dict(foia_session.connection,get_applications_query)
                applicant_open_letters = 0
               #print(these_applications)
                if len(these_applications) > 0 and type(these_applications) == list:
                    for i in range(len(these_applications)):
                        count_open_letters_query = f"""SELECT Count(*) FROM tbl_Letters WHERE Application_ID IS '{these_applications[i]['Application_ID']}' AND Status IS 'Open' OR Application_ID IS '{these_applications[i]['Application_ID']}' AND Status IS 'Action';"""
                        open_letters_count = db.execute_read_query_dict(foia_session.connection,count_open_letters_query)
                       #print(open_letters_count)
                        if len(open_letters_count) > 0 and type(open_letters_count) == list:
                            applicant_open_letters = applicant_open_letters + open_letters_count[0]['Count(*)']

                foia_session.applicants.append([applicant['Applicant_ID'],applicant['Preferred_Name'],f"{applicant_open_letters}",applicant['Phone_Number'],applicant['Email']])
        window['-Applicants_Display_Content-'].update(foia_session.applicants)
        return window

def deactivate_applicant_fields(window,values):
    new_applicant_query = f"""SELECT MAX(Applicant_ID) FROM tbl_Applicants;"""
    query_results = db.execute_read_query_dict(foia_session.connection,new_applicant_query)
   #print(query_results)
    new_applicant = ""
    if query_results != [] and type(query_results) == list:
        new_applicant =query_results[0]['MAX(Applicant_ID)']
    if new_applicant == None or new_applicant == "":
        new_applicant = 1
    else:
        new_applicant = new_applicant + 1
    window['-Applicant_ID_Input-'].update(f"""""")
    window['-New_Applicant_Button-'].update(f"New Applicant")
    window['-Applicant_FirstName_Input-'].update("", disabled=True)
    window['-Applicant_MiddleName_Input-'].update("", disabled=True)
    window['-Applicant_LastName_Input-'].update("", disabled=True)
    window['-Applicant_FullName_Input-'].update("", disabled=True)
    window['-Applicant_Title_Input-'].update("", disabled=True)
    window['-Applicant_PreferredName_Input-'].update("", disabled=True)
    window['-Applicant_ReturnAddress_Input-'].update("", disabled=True)
    window['-Applicant_Phone_Input-'].update("", disabled=True)
    window['-Applicant_Email_Input-'].update("", disabled=True)
    window['-Applicant_Notes_Display-'].update("", disabled=True)
    window['-Edit_Applicant_Button-'].update(disabled=True)
    window['-Applicant_Recorded_Input-'].update("")
    window['-Applicant_Edited_Input-'].update("")



def activate_new_applicant_fields(window,values):
    new_applicant_query = f"""SELECT MAX(Applicant_ID) FROM tbl_Applicants;"""
    query_results = db.execute_read_query_dict(foia_session.connection,new_applicant_query)
   #print(query_results)
    new_applicant = ""
    if query_results != [] and type(query_results) == list:
        new_applicant = query_results[0]['MAX(Applicant_ID)']
    if new_applicant == None:
        new_applicant = 1
    else:
        new_applicant = new_applicant + 1
    window['-Applicant_ID_Input-'].update(f"""Applicant {new_applicant}""")
    window['-New_Applicant_Button-'].update(f"Save New")
    window['-Applicant_FirstName_Input-'].update("", disabled=False)
    window['-Applicant_MiddleName_Input-'].update("", disabled=False)
    window['-Applicant_LastName_Input-'].update("", disabled=False)
    window['-Applicant_FullName_Input-'].update("", disabled=False)
    window['-Applicant_Title_Input-'].update("", disabled=False)
    window['-Applicant_PreferredName_Input-'].update("", disabled=False)
    window['-Applicant_ReturnAddress_Input-'].update("", disabled=False)
    window['-Applicant_Phone_Input-'].update("", disabled=False)
    window['-Applicant_Email_Input-'].update("", disabled=False)
    window['-Applicant_Notes_Display-'].update("", disabled=False)
    window['-Edit_Applicant_Button-'].update(disabled=True)
    window['-Applicant_Recorded_Input-'].update("")
    window['-Applicant_Edited_Input-'].update("")
    window['-Applicants_Display_Content-'].update([[new_applicant,"Add attributes","To the left","Thank You","Phone","Email","Date"]])

def activate_edit_applicant_fields(window, values):
    window['-Applicant_FirstName_Input-'].update(disabled=False)
    window['-Applicant_MiddleName_Input-'].update(disabled=False)
    window['-Applicant_LastName_Input-'].update(disabled=False)
    window['-Applicant_FullName_Input-'].update(disabled=False)
    window['-Applicant_Title_Input-'].update(disabled=False)
    window['-Applicant_PreferredName_Input-'].update(disabled=False)
    window['-Applicant_ReturnAddress_Input-'].update(disabled=False)
    window['-Applicant_Phone_Input-'].update(disabled=False)
    window['-Applicant_Email_Input-'].update(disabled=False)
    window['-Applicant_Notes_Display-'].update(disabled=False)
    window['-Edit_Applicant_Button-'].update("Save Changes")
    window['-Applicant_Recorded_Input-'].update("")
    window['-Applicant_Edited_Input-'].update("")
 

def save_new_applicant(window,values):
    add_applicant_query = f"""INSERT INTO tbl_Applicants (First_Name,Middle_Name,Last_Name, Title, Full_Name, Preferred_Name, Return_Address, Email, Phone_Number, Notes, Created_Time, Edited_Time) VALUES("""

    now, nowish = get_current_time_info()
   #print(nowish)
    lines = [
        f"""'{values['-Applicant_FirstName_Input-']}', """,
        f"""'{values['-Applicant_MiddleName_Input-']}', """,
        f"""'{values['-Applicant_LastName_Input-']}', """,
        f"""'{values['-Applicant_Title_Input-']}', """,
        f"""'{values['-Applicant_FullName_Input-']}', """,
        f"""'{values['-Applicant_PreferredName_Input-']}', """,
        f"""'{values['-Applicant_ReturnAddress_Input-']}', """,
        f"""'{values['-Applicant_Email_Input-']}', """,
        f"""'{values['-Applicant_Phone_Input-']}', """,
        f"""'{values['-Applicant_Notes_Display-']}', """,
        f"""'{now}', """,
        f"""'{now}' """,
    ]   
    closing_statement = f""");"""
    for line in lines:
        add_applicant_query = add_applicant_query + line
    add_applicant_query = add_applicant_query + closing_statement
    updated_applicant = db.execute_query(foia_session.connection,add_applicant_query)
    foia_session.console_log(f'updated_Applicant: {updated_applicant}',foia_session.current_console_messages)
    window['-Applicant_FirstName_Input-'].update(disabled=True)
    window['-Applicant_MiddleName_Input-'].update(disabled=True)
    window['-Applicant_LastName_Input-'].update(disabled=True)
    window['-Applicant_Title_Input-'].update(disabled=True)
    window['-Applicant_FullName_Input-'].update(disabled=True)
    window['-Applicant_PreferredName_Input-'].update(disabled=True)
    window['-Applicant_ReturnAddress_Input-'].update(disabled=True)
    window['-Applicant_Phone_Input-'].update(disabled=True)
    window['-Applicant_Email_Input-'].update(disabled=True)
    window['-Applicant_Notes_Display-'].update(disabled=True)
    window['-New_Applicant_Button-'].update("New Applicant", disabled=False)

    update_applicants_view(window,values)


def load_applicant_data(window,values,this_applicant):
    if window['-Edit_Applicant_Button-'].ButtonText == 'Save Changes':
        window['-Edit_Applicant_Button-'].update('Edit Applicant')  
    if window['-New_Applicant_Button-'].ButtonText == 'New Applicant':  
        window['-Edit_Applicant_Button-'].update(disabled=False)  
        #window['-New_Applicant_Button-'].update(disabled=True) 
        #window['-Edit_Applicant_Button-'].update('Save Changes')  
        #
        retrieve_applicant_query = f"""SELECT * FROM tbl_Applicants WHERE Applicant_ID={this_applicant};"""
        applicants = db.execute_read_query_dict(foia_session.connection,retrieve_applicant_query)
       #print(retrieve_applicant_query)
       #print(applicants)
        
        if applicants != [] and type(applicants) == list:
            window['-Applicant_ID_Input-'].update(f"""Applicant {applicants[0]['Applicant_ID']}""")
            window['-Applicant_FirstName_Input-'].update(f"""{applicants[0]['First_Name']}""")
            window['-Applicant_MiddleName_Input-'].update(f"""{applicants[0]['Middle_Name']}""")
            window['-Applicant_LastName_Input-'].update(f"""{applicants[0]['Last_Name']}""")
            window['-Applicant_FullName_Input-'].update(f"""{applicants[0]['Full_Name']}""")
            window['-Applicant_Title_Input-'].update(f"""{applicants[0]['Title']}""")
            window['-Applicant_PreferredName_Input-'].update(f"""{applicants[0]['Preferred_Name']}""")
            window['-Applicant_ReturnAddress_Input-'].update(f"""{applicants[0]['Return_Address']}""")
            window['-Applicant_Phone_Input-'].update(f"""{applicants[0]['Phone_Number']}""")
            window['-Applicant_Email_Input-'].update(f"""{applicants[0]['Email']}""")
            window['-Applicant_Recorded_Input-'].update(f"""{applicants[0]['Created_Time']}""")
            window['-Applicant_Edited_Input-'].update(f"""{applicants[0]['Edited_Time']}""")
            window['-Applicant_Notes_Display-'].update(f"""{applicants[0]['Notes']}""")
        
        return window     
    else:
        return window         

def save_applicant_changes(window,values,applicant_id):
    update_applicant_query = f"""UPDATE tbl_Applicants SET """

    now, nowish = get_current_time_info()
   #print(nowish)
    lines = [
        f"""First_Name = '{values['-Applicant_FirstName_Input-']}', """,
        f"""Middle_Name = '{values['-Applicant_MiddleName_Input-']}', """,
        f"""Last_Name = '{values['-Applicant_LastName_Input-']}', """,
        f"""Title = '{values['-Applicant_Title_Input-']}', """,
        f"""Full_Name = '{values['-Applicant_FullName_Input-']}', """,
        f"""Preferred_Name = '{values['-Applicant_PreferredName_Input-']}', """,
        f"""Return_Address = '{values['-Applicant_ReturnAddress_Input-']}', """,
        f"""Phone_Number = '{values['-Applicant_Phone_Input-']}', """,
        f"""Email = '{values['-Applicant_Email_Input-']}', """,
        f"""Notes = '{values['-Applicant_Notes_Display-']}', """,
        f"""Edited_Time = '{now}' """,
    ]
    closing_statement = f"""WHERE Applicant_ID = {applicant_id};"""
    for line in lines:
        update_applicant_query = update_applicant_query + line
    update_applicant_query = update_applicant_query + closing_statement
    updated_applicant = db.execute_query(foia_session.connection,update_applicant_query)
    foia_session.console_log(f'updated_applicant: {updated_applicant}',foia_session.current_console_messages)
    window['-Applicant_FirstName_Input-'].update(disabled=True)
    window['-Applicant_MiddleName_Input-'].update(disabled=True)
    window['-Applicant_LastName_Input-'].update(disabled=True)
    window['-Applicant_Title_Input-'].update(disabled=True)
    window['-Applicant_FullName_Input-'].update(disabled=True)
    window['-Applicant_PreferredName_Input-'].update(disabled=True)
    window['-Applicant_ReturnAddress_Input-'].update(disabled=True)
    window['-Applicant_Phone_Input-'].update(disabled=True)
    window['-Applicant_Email_Input-'].update(disabled=True)
    window['-Applicant_Notes_Display-'].update(disabled=True)
    load_applicant_data(window,values,applicant_id)








def load_requester_data(window,values, this_requester):
    
    if window['-Edit_Requester_Button-'].ButtonText == 'Save Changes':
        window['-Edit_Requester_Button-'].update('Edit Requester')  
    if window['-New_Requester_Button-'].ButtonText == 'New Requester':  
        window['-Edit_Requester_Button-'].update(disabled=False)  
        #window['-New_Requester_Button-'].update(disabled=True) 
        #window['-Edit_Requester_Button-'].update('Save Changes')  
        #
        retrieve_requester_query = f"""SELECT * FROM tbl_Requesters WHERE Requester_ID={this_requester};"""
        requesters = db.execute_read_query_dict(foia_session.connection,retrieve_requester_query)
       #print(retrieve_requester_query)
       #print(requesters)
        if requesters != [] and type(requesters) == list:
            window['-Requester_ID_Display-'].update(f"""Requester {requesters[0]['Requester_ID']}""")
            window['-Requester_FirstName_Input-'].update(f"""{requesters[0]['First_Name']}""")
            window['-Requester_MiddleName_Input-'].update(f"""{requesters[0]['Middle_Name']}""")
            window['-Requester_LastName_Input-'].update(f"""{requesters[0]['Last_Name']}""")
            window['-Requester_FullName_Input-'].update(f"""{requesters[0]['Full_Name']}""")
            window['-Requester_PreferredName_Input-'].update(f"""{requesters[0]['Preferred_Name']}""")
            window['-Requester_ReturnAddress_Input-'].update(f"""{requesters[0]['Return_Address']}""")
            window['-Requester_Phone_Input-'].update(f"""{requesters[0]['Phone_Number']}""")
            window['-Requester_Email_Input-'].update(f"""{requesters[0]['Email']}""")
            window['-Requester_Recorded_Input-'].update(f"""{requesters[0]['Created_Time']}""")
            window['-Requester_Edited_Input-'].update(f"""{requesters[0]['Edited_Time']}""")
            window['-Requester_Notes_Display-'].update(f"""{requesters[0]['Notes']}""")
            window['-Requester_Photo_Display-'].update(f"""{requesters[0]['Photo']}""", subsample=4)
            window['-Requester_Photo_Input-'].update(f"""{requesters[0]['Photo']}""")
            foia_session.requester_photo = requesters[0]['Photo']
        
        return window     
    else:
        return window



def activate_requester_fields(window,values):
    window['-Requester_FirstName_Input-'].update(disabled=False)
    window['-Requester_MiddleName_Input-'].update(disabled=False)
    window['-Requester_LastName_Input-'].update(disabled=False)
    window['-Requester_FullName_Input-'].update(disabled=False)
    window['-Requester_PreferredName_Input-'].update(disabled=False)
    window['-Requester_ReturnAddress_Input-'].update(disabled=False)
    window['-Requester_Phone_Input-'].update(disabled=False)
    window['-Requester_Email_Input-'].update(disabled=False)
    window['-Requester_Notes_Display-'].update(disabled=False)
    window['-Requester_Photo_Input-'].update(disabled=False)
    window['-Requester_Photo_Input-'].update(f"""{foia_session.requester_photo}""")

def save_requester_changes(window,values, requester_id):
   #print(f"values['-Requester_Photo_Input-']: {values['-Requester_Photo_Input-']}")
    update_requester_query = f"""UPDATE tbl_Requesters SET """

    now, nowish = get_current_time_info()
   #print(nowish)
    lines = [
        f"""First_Name = '{values['-Requester_FirstName_Input-']}', """,
        f"""Middle_Name = '{values['-Requester_MiddleName_Input-']}', """,
        f"""Last_Name = '{values['-Requester_LastName_Input-']}', """,
        f"""Full_Name = '{values['-Requester_FullName_Input-']}', """,
        f"""Preferred_Name = '{values['-Requester_PreferredName_Input-']}', """,
        f"""Return_Address = '{values['-Requester_ReturnAddress_Input-']}', """,
        f"""Phone_Number = '{values['-Requester_Phone_Input-']}', """,
        f"""Email = '{values['-Requester_Email_Input-']}', """,
        f"""Notes = '{values['-Requester_Notes_Display-']}', """,
        f"""Photo = '{values['-Requester_Photo_Input-']}', """,
        f"""Edited_Time = '{now}' """,
    ]
    closing_statement = f"""WHERE Requester_ID = {requester_id};"""
    for line in lines:
        update_requester_query = update_requester_query + line
    update_requester_query = update_requester_query + closing_statement
    updated_requester = db.execute_query(foia_session.connection,update_requester_query)
    foia_session.console_log(f'updated_requester: {updated_requester}',foia_session.current_console_messages)
    window['-Requester_FirstName_Input-'].update(disabled=True)
    window['-Requester_MiddleName_Input-'].update(disabled=True)
    window['-Requester_LastName_Input-'].update(disabled=True)
    window['-Requester_FullName_Input-'].update(disabled=True)
    window['-Requester_PreferredName_Input-'].update(disabled=True)
    window['-Requester_ReturnAddress_Input-'].update(disabled=True)
    window['-Requester_Phone_Input-'].update(disabled=True)
    window['-Requester_Email_Input-'].update(disabled=True)
    window['-Requester_Notes_Display-'].update(disabled=True)
    window['-Requester_Photo_Input-'].update(disabled=True)
    load_requester_data(window,values,requester_id)

def add_new_requester_fields(window, values,new_requester):
    window['-Requester_ID_Display-'].update(f"""Requester {new_requester}""")
    window['-New_Requester_Button-'].update(f"Save New")
    window['-Requester_FirstName_Input-'].update("", disabled=False)
    window['-Requester_MiddleName_Input-'].update("", disabled=False)
    window['-Requester_LastName_Input-'].update("", disabled=False)
    window['-Requester_FullName_Input-'].update("", disabled=False)
    window['-Requester_PreferredName_Input-'].update("", disabled=False)
    window['-Requester_ReturnAddress_Input-'].update("", disabled=False)
    window['-Requester_Phone_Input-'].update("", disabled=False)
    window['-Requester_Email_Input-'].update("", disabled=False)
    window['-Requester_Notes_Display-'].update("", disabled=False)
    window['-Requester_Photo_Input-'].update("", disabled=False)
    window['-Requester_Photo_Display-'].update("", subsample=4)
    window['-Edit_Requester_Button-'].update(disabled=True)
    window['-Requester_Recorded_Input-'].update("")
    window['-Requester_Edited_Input-'].update("")
    window['-Requesters_Display_Content-'].update([[new_requester,"Add attributes","To the left","Thank You","Phone","Email","Date"]])
    
def disable_requester_fields(window,values):    
    window['-New_Requester_Button-'].update(f"New Requester")
    window['-Requester_FirstName_Input-'].update("", disabled=True)
    window['-Requester_MiddleName_Input-'].update("", disabled=True)
    window['-Requester_LastName_Input-'].update("", disabled=True)
    window['-Requester_FullName_Input-'].update("", disabled=True)
    window['-Requester_PreferredName_Input-'].update("", disabled=True)
    window['-Requester_ReturnAddress_Input-'].update("", disabled=True)
    window['-Requester_Phone_Input-'].update("", disabled=True)
    window['-Requester_Email_Input-'].update("", disabled=True)
    window['-Requester_Notes_Display-'].update("", disabled=True)
    window['-Requester_Photo_Input-'].update("", disabled=True)
    window['-Edit_Requester_Button-'].update(disabled=True)
    window['-Requester_Recorded_Input-'].update("")
    window['-Requester_Edited_Input-'].update("")

def save_new_requester(window,values, requester_id):
    
   #print(f"values['-Requester_Photo_Input-']: {values['-Requester_Photo_Input-']}")
    add_requester_query = f"""INSERT INTO tbl_Requesters (First_Name,Middle_Name,Last_Name, Full_Name, Preferred_Name, Return_Address, Phone_Number, Email, Notes, Photo, Created_Time, Edited_Time) VALUES("""

    now, nowish = get_current_time_info()
   #print(nowish)
    lines = [
        f"""'{values['-Requester_FirstName_Input-']}', """,
        f"""'{values['-Requester_MiddleName_Input-']}', """,
        f"""'{values['-Requester_LastName_Input-']}', """,
        f"""'{values['-Requester_FullName_Input-']}', """,
        f"""'{values['-Requester_PreferredName_Input-']}', """,
        f"""'{values['-Requester_ReturnAddress_Input-']}', """,
        f"""'{values['-Requester_Phone_Input-']}', """,
        f"""'{values['-Requester_Email_Input-']}', """,
        f"""'{values['-Requester_Notes_Display-']}', """,
        f"""'{values['-Requester_Photo_Input-']}', """,
        f"""'{now}', """,
        f"""'{now}' """,
    ]   
    closing_statement = f""");"""
    for line in lines:
        add_requester_query = add_requester_query + line
    add_requester_query = add_requester_query + closing_statement
    updated_requester = db.execute_query(foia_session.connection,add_requester_query)
    foia_session.console_log(f'updated_requester: {updated_requester}',foia_session.current_console_messages)
    window['-Requester_FirstName_Input-'].update(disabled=True)
    window['-Requester_MiddleName_Input-'].update(disabled=True)
    window['-Requester_LastName_Input-'].update(disabled=True)
    window['-Requester_FullName_Input-'].update(disabled=True)
    window['-Requester_PreferredName_Input-'].update(disabled=True)
    window['-Requester_ReturnAddress_Input-'].update(disabled=True)
    window['-Requester_Phone_Input-'].update(disabled=True)
    window['-Requester_Email_Input-'].update(disabled=True)
    window['-Requester_Notes_Display-'].update(disabled=True)
    window['-Requester_Photo_Input-'].update(disabled=True)
    window['-New_Requester_Button-'].update("New Requester", disabled=False)


def get_id_from_optionmenu(this_input):
    f"""Retrieves the id number from the name listed on OptionMenu elements"""
    this_id = ""
    for char in this_input:
        if char == "0" or char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6" or char == "7" or char == "8" or char == "9":
            this_id = this_id + char
        elif char == " ":
            break
    if this_id == "":
        this_id = "0"
    return int(this_id)


def activate_new_letter_fields(window,values):
    count_letters_query = f"""SELECT MAX(Letter_ID) FROM tbl_Letters;"""
    max_letter = db.execute_read_query_dict(foia_session.connection,count_letters_query)
   #print(str(max_letter))
    max_letter_number = 0
    if max_letter[0]['MAX(Letter_ID)'] != None and max_letter != [] and type(max_letter) == list:
        max_letter_number = int(max_letter[0]['MAX(Letter_ID)'])
       #print(max_letter)
   #print(f"max letter: {max_letter_number}")
    foia_session.new_letter = max_letter_number + 1
    foia_session.console_log(f"New Letter Number: {foia_session.new_letter}",foia_session.current_console_messages)
    foia_session.letter_saved = False
    foia_session.this_letter['Letter_ID'] = foia_session.new_letter

    letter_number = f"""{foia_session.organization_acronym}-LTR-{foia_session.new_letter+10000}"""
    foia_session.this_letter['Tracking_Number'] = letter_number
    window['-Letter_ID_Input-'].update(f"{letter_number}", disabled=True)
    window['-Letter_Date_Input-'].update(current_date, disabled=True)
    window['-Letter_To_Input-'].update("", disabled=False)
    window['-Letter_From_Input-'].update("", disabled=False)
    window['-Letter_Document_Input-'].update("", disabled=False)
    window['-Letter_Request_Input-'].update("", disabled=False)
    window['-Letter_Recorded_Input-'].update("", disabled=True)
    window['-Letter_Edited_Input-'].update("", disabled=True)
    window['-Letter_Template_Button-'].update(disabled=True)
    window['-Letter_View_Button-'].update("Letter", disabled=False)
    window['-Letter_Image-'].update("")
    window['-Letter_Image_Input-'].update("", disabled=False)
    window['-Message_View_Button-'].update("Message", disabled=False)
    window['-Letter_Message_Display-'].update("", disabled=False)
    window['-Letter_Template_Input-'].update(disabled=False)
    window['-Letter_Generate_Button-'].update(disabled=True)#Disabled to prevent bad Letter Codes

    #add_new_requester_fields(foia_session.window,values,foia_session.new_letter)
    foia_session.display_letters = [[f"""{foia_session.organization_acronym}-LTR-{foia_session.new_letter+10000}""","Add attributes","To the left","Thank You","Responder","Applicant","Requester"]]
    window['-Letters_Display_Content-'].update(foia_session.display_letters)







    #Tell the GUI that the letter has not yet been saved.
    foia_session.letter_saved = False

    return window

def save_letter_image_input(window,values):
    sanitized_letter_content = f"""{values['-Letter_Message_Display-']}""".replace("'","~") 
    if values['-Letter_Image_Input-'] == "":
        return window
    elif window['-Letter_View_Button-'].ButtonText == "Letter":
        if foia_session.letter_saved != True:
            insert_letter_query = f"""INSERT INTO tbl_Letters (Tracking_Number, Application_ID, Requester_ID, Responder_ID, Document, Request, Message, Record, Created_Time, Edited_Time, Date, Status, Letter_Code)
            VALUES ('{values['-Letter_ID_Input-']}','{foia_session.this_application['Application_ID']}','{foia_session.this_letter['Requester_ID']}', '{foia_session.this_letter['Responder_ID']}','{values['-Letter_Document_Input-']}','{values['-Letter_Request_Input-']}',"{sanitized_letter_content}",'{values['-Letter_Image_Input-']}','{datetime.datetime.now()}','{datetime.datetime.now()}','{current_date_db}','Open','{foia_session.this_letter['Letter_Code']}');"""
           #print(insert_letter_query)
            inserted_letter = db.execute_query(foia_session.connection,insert_letter_query)
            foia_session.console_log(f"Inserted {values['-Letter_ID_Input-']}: {inserted_letter}",foia_session.current_console_messages)
            foia_session.letter_saved = True
        elif foia_session.letter_saved == True:
            update_letter_query = f"""UPDATE tbl_Letters SET Tracking_Number = '{values['-Letter_ID_Input-']}', Application_ID = '{foia_session.this_letter['Application_ID']}', Requester_ID = '{foia_session.this_letter['Requester_ID']}', Responder_ID = '{foia_session.this_letter['Responder_ID']}', Document = '{values['-Letter_Document_Input-']}', Request = '{values['-Letter_Request_Input-']}', Message = '{sanitized_letter_content}', Record = '{values['-Letter_Image_Input-']}', Edited_Time = '{now}', Date='{current_date_db}' WHERE Letter_ID = '{foia_session.this_letter['Letter_ID']}';"""
            udpated_letter = db.execute_query(foia_session.connection,update_letter_query)
            foia_session.console_log(f"Updated {values['-Letter_ID_Input-']}: {udpated_letter}",current_console_messages=foia_session.current_console_messages)
    elif window['-Letter_View_Button-'].ButtonText == "Response":
        update_letter_query = f"""UPDATE tbl_Letters SET Tracking_Number = '{values['-Letter_ID_Input-']}', Application_ID = '{foia_session.this_letter['Application_ID']}', Requester_ID = '{foia_session.this_letter['Requester_ID']}', Responder_ID = '{foia_session.this_letter['Responder_ID']}', Document = '{values['-Letter_Document_Input-']}', Request = '{values['-Letter_Request_Input-']}', Response = '{values['-Letter_Image_Input-']}', Edited_Time = '{now}', Status = 'Action' WHERE Letter_ID = '{foia_session.this_letter['Letter_ID']}';"""
        udpated_letter = db.execute_query(foia_session.connection,update_letter_query)
       #print(update_letter_query)
       #print(udpated_letter)
        foia_session.console_log(f"Updated {values['-Letter_ID_Input-']}: {udpated_letter}",current_console_messages=foia_session.current_console_messages)    
    elif window['-Letter_View_Button-'].ButtonText == "Forward":
        
        update_letter_query = f"""UPDATE tbl_Letters SET Tracking_Number = '{values['-Letter_ID_Input-']}', Application_ID = '{foia_session.this_letter['Application_ID']}', Requester_ID = '{foia_session.this_letter['Requester_ID']}', Responder_ID = '{foia_session.this_letter['Responder_ID']}', Document = '{values['-Letter_Document_Input-']}', Request = '{values['-Letter_Request_Input-']}', Forwarding_Letter_Content = '{sanitized_letter_content}', Forwarding_Letter = '{values['-Letter_Image_Input-']}', Edited_Time = '{now}', Status = 'Closed' WHERE Letter_ID = '{foia_session.this_letter['Letter_ID']}';"""
        udpated_letter = db.execute_query(foia_session.connection,update_letter_query)
        foia_session.console_log(f"Updated {values['-Letter_ID_Input-']}: {udpated_letter}",current_console_messages=foia_session.current_console_messages)    

    #Convert image to png
    png_image = convert_pdf_to_png(values['-Letter_Image_Input-'])
    window['-Letter_Image-'].update(png_image[0])


    foia_session.letter_saved = True
    foia_session.new_letter = 0

    return window

def letter_message_button_function(window,values):
    if window['-Message_View_Button-'].ButtonText == "Message":
        window['-Message_View_Button-'].update("Fwd Msg")
        if foia_session.letter_saved == True:
            get_fwd_query = f"""SELECT Forwarding_Letter_Content FROM tbl_Letters WHERE Letter_ID IS '{foia_session.this_letter['Letter_ID']}';"""
            forward_message = db.execute_read_query_dict(foia_session.connection,get_fwd_query)
            if forward_message != [] and type(forward_message) == list:
                fwd_content = f"{forward_message[0]['Forwarding_Letter_Content']}".replace("~","'")
                if fwd_content == "None":
                    fwd_content = "Select Template" 
                    window['-Letter_Message_Display-'].update(fwd_content, disabled=False)  
                    window['-Letter_Template_Input-'].update(disabled=False)
                    window['-Letter_Template_Button-'].update(disabled=False)
                    window['-Letter_Generate_Button-'].update(disabled=True)     #  #Disabled to prevent bad Letter Codes
                else:
                    window['-Letter_Message_Display-'].update(fwd_content, disabled=True)  
                    window['-Letter_Template_Input-'].update(disabled=True)
                    window['-Letter_Template_Button-'].update(disabled=True)
                    window['-Letter_Generate_Button-'].update(disabled=True) 
                
            else:
                window['-Letter_Message_Display-'].update("", disabled=False)  
                window['-Letter_Template_Input-'].update(disabled=False)
                window['-Letter_Template_Button-'].update(disabled=False)
                window['-Letter_Generate_Button-'].update(disabled=True)#Disabled to prevent bad Letter Codes
        else:
                window['-Letter_Message_Display-'].update("")    
    elif window['-Message_View_Button-'].ButtonText == "Fwd Msg":
        window['-Message_View_Button-'].update("Message")
        if foia_session.letter_saved == True:
            get_fwd_query = f"""SELECT Message FROM tbl_Letters WHERE Letter_ID IS '{foia_session.this_letter['Letter_ID']}';"""
            message = db.execute_read_query_dict(foia_session.connection,get_fwd_query)
            if message != [] and type(message)  == list:
                message_content = f"{message[0]['Message']}"
                if message_content == "None":
                    message_content = "Select Template"
                window['-Letter_Message_Display-'].update(f"{message[0]['Message']}", disabled = True)   
                window['-Letter_Template_Input-'].update(disabled=True)
                window['-Letter_Template_Button-'].update(disabled=True)
                window['-Letter_Generate_Button-'].update(disabled=True)  
            else:
                window['-Letter_Message_Display-'].update("", disabled=False) 
                window['-Letter_Template_Input-'].update(disabled=False)
                window['-Letter_Template_Button-'].update(disabled=False)
                window['-Letter_Generate_Button-'].update(disabled=True)  #Disabled to prevent bad Letter Codes

        else:
            window['-Letter_Message_Display-'].update("", disabled=False) 
            window['-Letter_Template_Input-'].update(disabled=False)
            window['-Letter_Template_Button-'].update(disabled=False)
            window['-Letter_Generate_Button-'].update(disabled=True)      #Disabled to prevent bad Letter Codes  

def load_letter_data(window,values):
   #print(values['-Letters_Display_Content-'])
    letter_tracking = foia_session.display_letters[values['-Letters_Display_Content-'][0]][0]
    get_letter_query = f"""SELECT * FROM tbl_Letters WHERE Tracking_Number is '{letter_tracking}';"""
   #print(get_letter_query)
    retreived_letter = db.execute_read_query_dict(foia_session.connection,get_letter_query)
   #print(retreived_letter)
    if retreived_letter != [] and type(retreived_letter) == list:
        foia_session.this_letter  = retreived_letter[0]
        foia_session.letter_saved = True
        window['-Letter_ID_Input-'].update(f"{letter_tracking}", disabled=True)
        window['-Letter_Date_Input-'].update(f"{foia_session.this_letter['Date']}", disabled=True)
        this_responder = foia_session.display_letters[values['-Letters_Display_Content-'][0]][2]
        if len(this_responder) > 18:
            this_responder = this_responder[0:18]
       #print(f"this_responder: {this_responder}")
        window['-Letter_To_Input-'].update(f"{foia_session.this_letter['Responder_ID']} {this_responder}", disabled=True)
        this_requester = foia_session.display_letters[values['-Letters_Display_Content-'][0]][4]
        if len(this_requester) > 18:
            this_requester = this_requester[0:18]
        window['-Letter_From_Input-'].update(f"{foia_session.this_letter['Requester_ID']} {this_requester}", disabled=True)
        window['-Letter_Document_Input-'].update(f"{foia_session.this_letter['Document']}", disabled=True)
        window['-Letter_Request_Input-'].update(f"{foia_session.this_letter['Request']}", disabled=True)
        window['-Letter_Recorded_Input-'].update(f"{foia_session.this_letter['Created_Time']}", disabled=True)
        window['-Letter_Edited_Input-'].update(f"{foia_session.this_letter['Edited_Time']}", disabled=True)
        window['-Letter_Template_Button-'].update(disabled=True)
        window['-Letter_View_Button-'].update("Letter", disabled=False)
        window['-Letter_Image_Input-'].update(f"{foia_session.this_letter['Record']}", disabled=False)
        window['-Message_View_Button-'].update("Message", disabled=False)
        window['-Letter_Message_Display-'].update(f"""{foia_session.this_letter['Message']}""".replace('~',"'"), disabled=True)
        window['-Letter_Template_Input-'].update(disabled=True)
        window['-Letter_Generate_Button-'].update(disabled=True)
        
        #window['-Letter_Image-'].update(f"{foia_session.this_letter['Record'][:-4]}_0.png")





def letter_view_button_function(window,values):
    #print(window['-Letter_View_Button-'].ButtonText)
    if window['-Letter_View_Button-'].ButtonText == "Letter":
        #print(window['-Letter_View_Button-'].ButtonText)
        window['-Letter_View_Button-'].update("Response")
        #print(window['-Letter_View_Button-'].ButtonText)
        if foia_session.letter_saved == True:
            get_response_query = f"""SELECT Response FROM tbl_Letters WHERE Letter_ID IS '{foia_session.this_letter['Letter_ID']}';"""
            response = db.execute_read_query_dict(foia_session.connection,get_response_query)
           #print(get_response_query)
           #print(response)
            if response != [] and type(response) == list:
                if response[0]['Response'] != None:
                    window['-Letter_Image-'].update(f"{response[0]['Response'][:-4]}_0.png")
                    window['-Letter_Image_Input-'].update(response[0]['Response'])
                else:
                    window['-Letter_Image-'].update("")
                    window['-Letter_Image_Input-'].update("")                 
    elif window['-Letter_View_Button-'].ButtonText == "Response":
        window['-Letter_View_Button-'].update("Forward")
        if foia_session.letter_saved == True:
            get_forward_query = f"""SELECT Forwarding_Letter FROM tbl_Letters WHERE Letter_ID IS '{foia_session.this_letter['Letter_ID']}';"""
            forward = db.execute_read_query_dict(foia_session.connection,get_forward_query)
            if forward != [] and type(forward) == list:
                if forward[0]['Forwarding_Letter'] != None:
                    window['-Letter_Image-'].update(f"{forward[0]['Forwarding_Letter'][:-4]}_0.png")
                    window['-Letter_Image_Input-'].update(forward[0]['Forwarding_Letter'])  
                else:
                    window['-Letter_Image-'].update("")
                    window['-Letter_Image_Input-'].update("")                  
    elif window['-Letter_View_Button-'].ButtonText == "Forward":
        window['-Letter_View_Button-'].update("Letter")
        if foia_session.letter_saved == True:
            get_record_query = f"""SELECT Record FROM tbl_Letters WHERE Letter_ID IS '{foia_session.this_letter['Letter_ID']}';"""
            record = db.execute_read_query_dict(foia_session.connection,get_record_query)
            if record != [] and type(record) == list:
                if record[0]['Record'] != None:
                    window['-Letter_Image-'].update(f"{record[0]['Record'][:-4]}_0.png")
                    window['-Letter_Image_Input-'].update(record[0]['Record'])   
                else:
                    window['-Letter_Image-'].update("")
                    window['-Letter_Image_Input-'].update("")                   





#RESPONDER SECTION
def deactivate_responder_fields(window, values):
    window['-Responder_ID_Input-'].update(f"""""")
    window['-New_Responder_Button-'].update(f"New Responder")
    window['-Responder_Org_Name_Input-'].update("", disabled=True)
    window['-Responder_Org_Type_Input-'].update("", disabled=True)
    window['-Responder_Contact_First_Input-'].update("", disabled=True)
    window['-Responder_Contact_Last_Input-'].update("", disabled=True)
    window['-Responder_Contact_Email_Input-'].update("", disabled=True)
    window['-Responder_Contact_Preferred_Input-'].update("", disabled=True)
    window['-Responder_Phone_Input-'].update("", disabled=True)
    window['-Responder_Phone_Type_Input-'].update("", disabled=True)
    window['-Responder_Fax_Input-'].update("", disabled=True)
    window['-Responder_Email_Input-'].update("", disabled=True)
    window['-Responder_Website_Input-'].update("", disabled=True)
    window['-Responder_ReturnAddress_Input-'].update("", disabled=True)
    window['-Responder_MailingAddress_Input-'].update("", disabled=True)
    window['-Responder_Notes_Display-'].update("", disabled=True)
    window['-Edit_Responder_Button-'].update(disabled=True)
    window['-Responder_Recorded_Input-'].update("")
    window['-Responder_Edited_Input-'].update("")

def update_responders_view(window, values):
    current_year = foia_session.current_year
    #Bring the user to the applications
    this_tab_index = 13
    for i in range(len(foia_session.tab_key_list)):
        if i == this_tab_index:
            window[foia_session.tab_key_list[i]].update(visible=True)
            window[foia_session.tab_key_list[i]].select()
        else:
            window[foia_session.tab_key_list[i]].update(visible=False)
    #Set the time range (default = current YTD)
    #current_year = datetime.datetime.now().year
    start_date = f"{current_year[2:]}-01-01"
    end_date = f"{int(current_year[2:])+1}-01-01"

    
    if values['-Responders_Search_Input-'] == '':
        retrieve_responders_query = f"""SELECT * FROM tbl_Responders;"""
        responders = db.execute_read_query_dict(foia_session.connection,retrieve_responders_query)
       #print(retrieve_responders_query)
       #print(responders)
        
        #Responder_ID, Preferred_Name, Phone, Email, Created_Time
        foia_session.responders = []
        if responders != [] and type(responders) == list:
            for responder in responders:
                get_open_letters_query = f"""SELECT Count(*) FROM tbl_Letters WHERE Status is 'Open' AND Responder_ID IS '{responder['Responder_ID']}' OR Status is 'Action' AND Responder_ID IS '{responder['Responder_ID']}';"""
                open_letters_count = db.execute_read_query_dict(foia_session.connection,get_open_letters_query)
                open_letters_number = 0
                if type(open_letters_count) == list and len(open_letters_count) == 1:
                    open_letters_number = open_letters_count[0]['Count(*)']
                foia_session.responders.append([responder['Responder_ID'],responder['Organization_Name'],f"{open_letters_number}",responder['Phone_Number'],responder['Organization_Email']])
        window['-Responders_Display_Content-'].update(foia_session.responders)
        return window        
    else:
        retrieve_responders_query = f"""SELECT * FROM tbl_Responders WHERE Responder_ID = '{values['-Responders_Search_Input-']}' OR Organization_Name LIKE '%{values['-Responders_Search_Input-']}%' OR Organization_Type LIKE '%{values['-Responders_Search_Input-']}%' OR Contact_First_Name LIKE '%{values['-Responders_Search_Input-']}%' OR Contact_Last_Name LIKE '%{values['-Responders_Search_Input-']}%' OR Contact_Email LIKE '%{values['-Responders_Search_Input-']}%' OR Preferred_Name LIKE '%{values['-Responders_Search_Input-']}%' OR Organization_Address LIKE '%{values['-Responders_Search_Input-']}%' OR Organization_Mailing_Address LIKE '%{values['-Responders_Search_Input-']}%' OR Phone_Number LIKE '%{values['-Responders_Search_Input-']}%' OR Fax_Number LIKE '%{values['-Responders_Search_Input-']}%' OR Organization_Email LIKE '%{values['-Responders_Search_Input-']}%' OR Organization_Website LIKE '%{values['-Responders_Search_Input-']}%' OR Notes LIKE '%{values['-Responders_Search_Input-']}%';"""
        responders = db.execute_read_query_dict(foia_session.connection,retrieve_responders_query)
       #print(retrieve_responders_query)
       #print(responders)
        #Responder_ID, Preferred_Name, Phone, Email, Created_Time
        foia_session.responders = []
        if responders != [] and type(responders) == list:
            for responder in responders:

                get_open_letters_query = f"""SELECT Count(*) FROM tbl_Letters WHERE Status is 'Open' AND Responder_ID IS '{responder['Responder_ID']}' OR Status is 'Action' AND Responder_ID IS '{responder['Responder_ID']}';"""
                open_letters_count = db.execute_read_query_dict(foia_session.connection,get_open_letters_query)
                open_letters_number = 0
                if type(open_letters_count) == list and len(open_letters_count) == 1:
                    open_letters_number = open_letters_count[0]['Count(*)']
                foia_session.responders.append([responder['Responder_ID'],responder['Organization_Name'],f"{open_letters_number}",responder['Phone_Number'],responder['Organization_Email']])


        window['-Responders_Display_Content-'].update(foia_session.responders)
        return window

def activate_new_responder_fields(window,values):

    new_responder_query = f"""SELECT MAX(Responder_ID) FROM tbl_Responders;"""
    query_results = db.execute_read_query_dict(foia_session.connection,new_responder_query)
   #print(query_results)
    if query_results != [] and type(query_results) == list:
        new_responder =query_results[0]['MAX(Responder_ID)']
        if new_responder == None:
            new_responder = 1
        else:
            new_responder = new_responder + 1
        window['-Responder_ID_Input-'].update(f"""Responder {new_responder}""")
        window['-New_Responder_Button-'].update(f"Save New")
        window['-Responder_Org_Name_Input-'].update("", disabled=False)
        window['-Responder_Org_Type_Input-'].update("", disabled=False)
        window['-Responder_Contact_First_Input-'].update("", disabled=False)
        window['-Responder_Contact_Last_Input-'].update("", disabled=False)
        window['-Responder_Contact_Email_Input-'].update("", disabled=False)
        window['-Responder_Contact_Preferred_Input-'].update("", disabled=False)
        window['-Responder_Phone_Input-'].update("", disabled=False)
        window['-Responder_Phone_Type_Input-'].update("", disabled=False)
        window['-Responder_Fax_Input-'].update("", disabled=False)
        window['-Responder_Email_Input-'].update("", disabled=False)
        window['-Responder_Website_Input-'].update("", disabled=False)
        window['-Responder_ReturnAddress_Input-'].update("", disabled=False)
        window['-Responder_MailingAddress_Input-'].update("", disabled=False)
        window['-Responder_Notes_Display-'].update("", disabled=False)
        window['-Edit_Responder_Button-'].update(disabled=True)
        window['-Responder_Recorded_Input-'].update("")
        window['-Responder_Edited_Input-'].update("")
        window['-Responders_Display_Content-'].update([[new_responder,"Add attributes","To the left","Thank You","Email"]])

def save_new_responder(window,values):

    add_responder_query = f"""INSERT INTO tbl_Responders (Organization_Name,Organization_Type,Contact_First_Name,Contact_Last_Name, Contact_Email, Preferred_Name, Phone_Number, Phone_Number_Type, Fax_Number, Organization_Address, Organization_Mailing_Address, Organization_Email, Organization_Website, Notes, Created_Time, Edited_Time) VALUES("""

    now, nowish = get_current_time_info()
   #print(nowish)
    lines = [
        f"""'{values['-Responder_Org_Name_Input-']}', """,
        f"""'{values['-Responder_Org_Type_Input-']}', """,
        f"""'{values['-Responder_Contact_First_Input-']}', """,
        f"""'{values['-Responder_Contact_Last_Input-']}', """,
        f"""'{values['-Responder_Contact_Email_Input-']}', """,
        f"""'{values['-Responder_Contact_Preferred_Input-']}', """,
        f"""'{values['-Responder_Phone_Input-']}', """,
        f"""'{values['-Responder_Phone_Type_Input-']}', """,
        f"""'{values['-Responder_Fax_Input-']}', """,
        f"""'{values['-Responder_ReturnAddress_Input-']}', """,
        f"""'{values['-Responder_MailingAddress_Input-']}', """,
        f"""'{values['-Responder_Email_Input-']}', """,
        f"""'{values['-Responder_Website_Input-']}', """,
        f"""'{values['-Responder_Notes_Display-']}', """,
        f"""'{now}', """,
        f"""'{now}' """,
    ]   
    closing_statement = f""");"""
    for line in lines:
        add_responder_query = add_responder_query + line
    add_responder_query = add_responder_query + closing_statement
    updated_responder = db.execute_query(foia_session.connection,add_responder_query)
    foia_session.console_log(f'updated_Responder: {updated_responder}',foia_session.current_console_messages)
    window['-Responder_Org_Name_Input-'].update(disabled=True)
    window['-Responder_Org_Type_Input-'].update(disabled=True)
    window['-Responder_Contact_First_Input-'].update(disabled=True)
    window['-Responder_Contact_Last_Input-'].update(disabled=True)
    window['-Responder_Contact_Email_Input-'].update(disabled=True)
    window['-Responder_Contact_Preferred_Input-'].update(disabled=True)
    window['-Responder_Phone_Input-'].update(disabled=True)
    window['-Responder_Phone_Type_Input-'].update(disabled=True)
    window['-Responder_Fax_Input-'].update(disabled=True)
    window['-Responder_ReturnAddress_Input-'].update(disabled=True)
    window['-Responder_MailingAddress_Input-'].update(disabled=True)
    window['-Responder_Email_Input-'].update(disabled=True)
    window['-Responder_Website_Input-'].update(disabled=True)
    window['-Responder_Notes_Display-'].update(disabled=True)
    window['-New_Responder_Button-'].update("New Responder", disabled=False)

    update_responders_view(window,values)

def load_responder_data(window,values,this_responder):

    if window['-Edit_Responder_Button-'].ButtonText == 'Save Changes':
        window['-Edit_Responder_Button-'].update('Edit Responder')  
    if window['-New_Responder_Button-'].ButtonText == 'New Responder':  
        window['-Edit_Responder_Button-'].update(disabled=False)  
        #window['-New_Responder_Button-'].update(disabled=True) 
        #window['-Edit_Responder_Button-'].update('Save Changes')  
        #
        retrieve_responder_query = f"""SELECT * FROM tbl_Responders WHERE Responder_ID={this_responder};"""
        responders = db.execute_read_query_dict(foia_session.connection,retrieve_responder_query)
       #print(retrieve_responder_query)
       #print(responders)
        #Responder_ID, Preferred_Name, Phone, Email, Created_Time
        if responders != [] and type(responders) == list:
            window['-Responder_ID_Input-'].update(f"""Responder {responders[0]['Responder_ID']}""")
            window['-Responder_Org_Name_Input-'].update(f"""{responders[0]['Organization_Name']}""")
            window['-Responder_Org_Type_Input-'].update(f"""{responders[0]['Organization_Type']}""")
            window['-Responder_Contact_First_Input-'].update(f"""{responders[0]['Contact_First_Name']}""")
            window['-Responder_Contact_Last_Input-'].update(f"""{responders[0]['Contact_Last_Name']}""")
            window['-Responder_Contact_Email_Input-'].update(f"""{responders[0]['Contact_Email']}""")
            window['-Responder_Contact_Preferred_Input-'].update(f"""{responders[0]['Preferred_Name']}""")
            window['-Responder_Phone_Input-'].update(f"""{responders[0]['Phone_Number']}""")
            window['-Responder_Phone_Type_Input-'].update(f"""{responders[0]['Phone_Number_Type']}""")
            window['-Responder_Fax_Input-'].update(f"""{responders[0]['Fax_Number']}""")
            window['-Responder_ReturnAddress_Input-'].update(f"""{responders[0]['Organization_Address']}""")
            window['-Responder_MailingAddress_Input-'].update(f"""{responders[0]['Organization_Mailing_Address']}""")
            window['-Responder_Email_Input-'].update(f"""{responders[0]['Organization_Email']}""")
            window['-Responder_Website_Input-'].update(f"""{responders[0]['Organization_Website']}""")
            window['-Responder_Recorded_Input-'].update(f"""{responders[0]['Created_Time']}""")
            window['-Responder_Edited_Input-'].update(f"""{responders[0]['Edited_Time']}""")
            window['-Responder_Notes_Display-'].update(f"""{responders[0]['Notes']}""")
        
        return window     
    else:
        return window          

def activate_edit_responder_fields(window,values):
    window['-Responder_Org_Name_Input-'].update(disabled=False)
    window['-Responder_Org_Type_Input-'].update(disabled=False)
    window['-Responder_Contact_First_Input-'].update(disabled=False)
    window['-Responder_Contact_Last_Input-'].update(disabled=False)
    window['-Responder_Contact_Email_Input-'].update(disabled=False)
    window['-Responder_Contact_Preferred_Input-'].update(disabled=False)
    window['-Responder_Phone_Input-'].update(disabled=False)
    window['-Responder_Phone_Type_Input-'].update(disabled=False)
    window['-Responder_Fax_Input-'].update(disabled=False)
    window['-Responder_ReturnAddress_Input-'].update(disabled=False)
    window['-Responder_MailingAddress_Input-'].update(disabled=False)
    window['-Responder_Email_Input-'].update(disabled=False)
    window['-Responder_Website_Input-'].update(disabled=False)
    window['-Responder_Notes_Display-'].update(disabled=False)
    window['-Edit_Responder_Button-'].update("Save Changes")
    window['-Responder_Recorded_Input-'].update("")
    window['-Responder_Edited_Input-'].update("")

def save_responder_changes(window,values,responder_id):

    update_responder_query = f"""UPDATE tbl_Responders SET """

    now, nowish = get_current_time_info()
   #print(nowish)
    lines = [
        f"""Organization_Name = '{values['-Responder_Org_Name_Input-']}', """,
        f"""Organization_Type = '{values['-Responder_Org_Type_Input-']}', """,
        f"""Contact_First_Name = '{values['-Responder_Contact_First_Input-']}', """,
        f"""Contact_Last_Name = '{values['-Responder_Contact_Last_Input-']}', """,
        f"""Contact_Email = '{values['-Responder_Contact_Email_Input-']}', """,
        f"""Preferred_Name = '{values['-Responder_Contact_Preferred_Input-']}', """,
        f"""Phone_Number = '{values['-Responder_Phone_Input-']}', """,
        f"""Phone_Number_Type = '{values['-Responder_Phone_Type_Input-']}', """,
        f"""Fax_Number = '{values['-Responder_Fax_Input-']}', """,
        f"""Organization_Address = '{values['-Responder_ReturnAddress_Input-']}', """,
        f"""Organization_Mailing_Address = '{values['-Responder_MailingAddress_Input-']}', """,
        f"""Organization_Email = '{values['-Responder_Email_Input-']}', """,
        f"""Organization_Website = '{values['-Responder_Website_Input-']}', """,
        f"""Notes = '{values['-Responder_Notes_Display-']}', """,
        f"""Edited_Time = '{now}' """,
    ]
    closing_statement = f"""WHERE Responder_ID = {responder_id};"""
    for line in lines:
        update_responder_query = update_responder_query + line
    update_responder_query = update_responder_query + closing_statement
    updated_responder = db.execute_query(foia_session.connection,update_responder_query)
    foia_session.console_log(f'updated_responder: {updated_responder}',foia_session.current_console_messages)

    window['-Responder_Org_Name_Input-'].update(disabled=True)
    window['-Responder_Org_Type_Input-'].update(disabled=True)
    window['-Responder_Contact_First_Input-'].update(disabled=True)
    window['-Responder_Contact_Last_Input-'].update(disabled=True)
    window['-Responder_Contact_Email_Input-'].update(disabled=True)
    window['-Responder_Contact_Preferred_Input-'].update(disabled=True)
    window['-Responder_Phone_Input-'].update(disabled=True)
    window['-Responder_Phone_Type_Input-'].update(disabled=True)
    window['-Responder_Fax_Input-'].update(disabled=True)
    window['-Responder_ReturnAddress_Input-'].update(disabled=True)
    window['-Responder_MailingAddress_Input-'].update(disabled=True)
    window['-Responder_Email_Input-'].update(disabled=True)
    window['-Responder_Website_Input-'].update(disabled=True)
    window['-Responder_Notes_Display-'].update(disabled=True)
    window['-Edit_Responder_Button-'].update("Save Changes")
    window['-Responder_Recorded_Input-'].update("")
    window['-Responder_Edited_Input-'].update("")



    load_responder_data(window,values,responder_id)






def convert_pdf_to_png(image_url):
    """Converts a pdf file to png images. 
    Returns a list of images, each representing a page from the pdf."""
    if image_url[-4:] == ".pdf" :
       #print(f"Converting pdf: {image_url}")
        with tempfile.TemporaryDirectory() as path:
            pdf_location = os.path
            #print(pdf_location)
            images_from_path = convert_from_path(image_url, output_folder=path, size=350, paths_only=True, fmt="png")
           #print(images_from_path)
            # Do something here
            remove_to = image_url[::-1].index("/")
            #print(remove_to)
            image_location = image_url[:len(image_url)-remove_to]
           #print(image_url)
           #print(image_location)
            image_name_0 = image_url[-remove_to:]            
            image_name = image_name_0[:-4]
           #print(image_name)
            new_images = []
            for i in range(len(images_from_path)):
                new_image = f"{image_location}{image_name}_{i}.png"
                shutil.copyfile(images_from_path[i],new_image)
                new_images.append(new_image)
            return new_images
    else:
        return "Error: File is not a pdf"


#------------------------------------------Section 5 Window and Event Loop

# ________           _______   ___      ___ _______   ________   _________        ___       ________  ________  ________   
#|\   ____\         |\  ___ \ |\  \    /  /|\  ___ \ |\   ___  \|\___   ___\     |\  \     |\   __  \|\   __  \|\   __  \  
#\ \  \___|_        \ \   __/|\ \  \  /  / | \   __/|\ \  \\ \  \|___ \  \_|     \ \  \    \ \  \|\  \ \  \|\  \ \  \|\  \ 
# \ \_____  \        \ \  \_|/_\ \  \/  / / \ \  \_|/_\ \  \\ \  \   \ \  \       \ \  \    \ \  \\\  \ \  \\\  \ \   ____\
#  \|____|\  \        \ \  \_|\ \ \    / /   \ \  \_|\ \ \  \\ \  \   \ \  \       \ \  \____\ \  \\\  \ \  \\\  \ \  \___|
#    ____\_\  \        \ \_______\ \__/ /     \ \_______\ \__\\ \__\   \ \__\       \ \_______\ \_______\ \_______\ \__\   
#   |\_________\        \|_______|\|__|/       \|_______|\|__| \|__|    \|__|        \|_______|\|_______|\|_______|\|__|   
#   \|_________|                                                                                                           
                                                                                                                          
                                                                                                                          

foia_session.window = sg.Window(title="FOIA(s)", layout= layout1, margins=(10,10), resizable=True, size=(1280,980), finalize=True)
event, values = foia_session.window.read(10)
foia_session.values= values
foia_session.console_log(f"""{foia_session.current_console_messages[0]}""",[])


foia_session.current_time_display = get_current_time_info()

while True:
    if event == "Exit FOIA(s)" or event == sg.WIN_CLOSED:

        if foia_session.save_location == None or foia_session.save_location== "" or foia_session.save_location == ".":
            foia_session.save_location = "./"
        if foia_session.save_location[-1] != "/":
            foia_session.save_location = foia_session.save_location + "/"
        db.save_database(foia_session.session_log_connection,"sessions.fid","sessions.fidkey",False)
        break
    event, values = foia_session.window.read(timeout=990)
    if event == '__TIMEOUT__':
        #Synchronizes the time
        

        if foia_session.guitimer == "Initializing": 
            
           #print("Initializing: " + foia_session.current_time_display[0])
            #print(foia_session.current_time_display[1][-6:-4])
            foia_session.guitimer = int(foia_session.current_time_display[1][-6:-4])

        elif foia_session.guitimer >57 or foia_session.guitimer == 0:
                foia_session.synchronized = synchronize_time(foia_session.window, foia_session.current_time_display)
                if foia_session.synchronized[0] == "No":
                    #print(f"""Synchronizing: {timer}""")
                    foia_session.guitimer = int(foia_session.synchronized[1][1][-6:-4])
                else:
                    foia_session.current_time_display = foia_session.synchronized[1]
                    foia_session.guitimer = int(foia_session.current_time_display[1][-6:-4])
                    foia_session.window['-Current_Time_Display-'].update(foia_session.current_time_display[0])


                    if (int(foia_session.current_time_display[1][-9:-7]))%10 == 0 and foia_session.database_loaded:

                        if foia_session.save_location == None or foia_session.save_location== "" or foia_session.save_location == ".":
                            foia_session.save_location = "./"
                        if foia_session.save_location[-1] != "/":
                            foia_session.save_location = foia_session.save_location + "/"
                        message, foia_session.connection = db.save_database(foia_session.connection, foia_session.db_name, foia_session.filename, foia_session.save_location)
                        #update_dashboard_statistics(foia_session.connection, window, ledger_name, foia_session.db_name, values)
                        foia_session.current_console_messages = foia_session.console_log(message, foia_session.current_console_messages)
                        #current_console_messages = console_log(window, "Dashboard statistics updated.", current_console_messages)


                    #print(f"""Synchronized: {foia_session.current_time_display[0]}""")
                    #print(f"""{timer}""")
                    if foia_session.guitimer > 0:
                        conditional_s = "s"
                        if foia_session.guitimer == 1:
                            conditional_s = ""
                        foia_session.current_console_messages = foia_session.console_log(f"""Minute update delayed by {foia_session.guitimer} second{conditional_s}.""", foia_session.current_console_messages)
        else:
            current_time = get_current_time_info()
            foia_session.guitimer = int(current_time[1][-6:-4])
    else:
        function_triggered = True
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        #elif event == "-Create_Database-":
        #    foia_session.filekey,foia_session.filename, foia_session.ledger_name = create_database(values, connection, current_console_messages,foia_session.window)
        #    current_console_messages = console_log(foia_session.window, f"""Filekey: {filekey}, filename: {filename}""",connection,current_console_messages)
        elif event == "Go to Dashboard":
            this_tab_index = 0
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_dashboard_statistics(foia_session.window, values)









        #Applications Section
        elif event == "View Applications":
            this_tab_index = 1
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_applications_view(foia_session.window, values)
        elif event == "-New_Application_Button-" and foia_session.database_loaded:
            if foia_session.window['-New_Application_Button-'].ButtonText == "New Application":
                foia_session.window['-New_Application_Button-'].update("Save New")
                
                activate_new_application_fields(foia_session.window,values)
            else:
                foia_session.window['-New_Application_Button-'].update("New Application")
                #save_new_application(foia_session.window,values)                
        elif event == "-Application_Cancel_Button-" and foia_session.database_loaded:
            foia_session.this_application = {"Application_ID":0}
            foia_session.window['-Application_Documents_Display-'].update([])
            foia_session.window['-Application_Requests_Display-'].update([])
            foia_session.window['-Application_Search_Input-'].update("")
            if foia_session.database_loaded:
                update_applications_view(foia_session.window, values)
        elif event =="-Application_Add_Document_Button-" and foia_session.database_loaded:
            add_document_to_application(foia_session.window,values)
        elif event =="-Application_Add_Request_Button-" and foia_session.database_loaded:
            add_request_to_application(foia_session.window,values)
        elif event == '-Application_Delete_Document_Button-' and foia_session.database_loaded:
            delete_document_from_application(foia_session.window,values)
        elif event == '-Application_Delete_Request_Button-' and foia_session.database_loaded:
            delete_request_from_application(foia_session.window,values)
        elif event == '-Application_Common_Requests_Input-' and foia_session.database_loaded:
            add_common_request_to_input(foia_session.window,values)
        elif event == '-Application_Template_Input-' and foia_session.database_loaded:
            if foia_session.window["-New_Application_Button-"].ButtonText == "Save New":
                foia_session.window["-Application_Generate_Button-"].update(disabled=False)
        elif event == "-Application_Generate_Button-" and foia_session.database_loaded:


            #check inputs:
           #print(values['-Application_Requester_Input-'])
           #print(values['-Application_Responder_Input-'])
           #print(values['-Application_Applicant_Input-'])
           #print(foia_session.this_application['Documents'])
           #print(foia_session.this_application['Requests'])
            if values['-Application_Requester_Input-'] and values['-Application_Responder_Input-'] and values['-Application_Applicant_Input-'] and foia_session.this_application['Documents'] != [] and foia_session.this_application['Requests'] != []:
                template_input = values['-Application_Template_Input-']
                template_id = get_id_from_optionmenu(template_input)
                foia_session.this_application['Notes'] = values['-Application_Notes_Display-']
                filepath = generate_application(foia_session.window,values,template_id)
                subprocess.call(["xdg-open", filepath])#Linux
                #subprocess.call([filepath])#Windows
                # os.system('open', filepath) issue: Opening the pdf automatically on Windows and MacOS
                #os.startfile(f"{filepath}")
            else:
                foia_session.console_log("Please fill in all fields.",foia_session.current_console_messages)
        elif event == '-Application_Requester_Input-' and foia_session.database_loaded:
            foia_session.this_application['Requester_ID'] = get_id_from_optionmenu(values['-Application_Requester_Input-'])
        elif event == '-Application_Responder_Input-' and foia_session.database_loaded:
            foia_session.this_application['Responder_ID'] = get_id_from_optionmenu(values['-Application_Responder_Input-'])
        elif event == '-Application_Applicant_Input-' and foia_session.database_loaded:    
            foia_session.this_application['Applicant_ID'] = get_id_from_optionmenu(values['-Application_Applicant_Input-'])
           #print(f"applicant_id: {foia_session.this_application['Applicant_ID']}")
        elif event == "-Applications_Content-" and foia_session.database_loaded:
            if foia_session.database_loaded:
                load_application_data(foia_session.window,values)
        elif event == '-Application_Record_Input-' and foia_session.database_loaded:
            #print(f"record_input: {values['-Application_Record_Input-']}")
            #foia_session.window['-Application_Record_Input-'].update(f"{values['-Application_Record_Input-']}")
            save_application_record(foia_session.window, values)
            foia_session.window['-Application_Record_Button-'].update(disabled=False)
        elif event == '-Application_Record_Button-' and foia_session.database_loaded:
            subprocess.call(["xdg-open", f"{foia_session.window['-Application_Record_Input-'].ButtonText}"])
        elif event == '-Application_Search_Input-' and foia_session.database_loaded:
            time.sleep(0.01)
            update_applications_view(foia_session.window, values)





        #Letters section
        elif event == '-Letter_To_Input-' and foia_session.database_loaded:
            foia_session.this_letter['Responder_ID'] = get_id_from_optionmenu(values['-Letter_To_Input-'])
        elif event == '-Letter_From_Input-' and foia_session.database_loaded:
            foia_session.this_letter['Requester_ID'] = get_id_from_optionmenu(values['-Letter_From_Input-'])
        elif event == "-Letter_Cancel_Button-" and foia_session.database_loaded:
            foia_session.window['-Letters_Search_Input-'].update("")
            update_letters_view(foia_session.window, values)
        elif event == "View Letters" or event == '-Letters_Search_Input-':
            this_tab_index = 3
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_letters_view(foia_session.window, values)
        elif event == '-Letter_Generate_Button-' and foia_session.database_loaded:
            if values['-Letter_Message_Display-'] and values['-Letter_To_Input-'] and values['-Letter_From_Input-'] and values['-Letter_Document_Input-'] and values['-Letter_Request_Input-']:
                foia_session.this_letter_id = f"{values['-Letter_ID_Input-']}"
                if foia_session.window['-Message_View_Button-'].ButtonText == "Fwd Msg":
                    foia_session.this_letter_id = f"{values['-Letter_ID_Input-']}-FWD"
                    extra_whitespace = ""

                foia_session.this_letter_body = values['-Letter_Message_Display-']
                filepath, images = generate_new_letter(foia_session.window,values)
                #print(filepath)
                   #Remove the images
                time.sleep(0.15)
                for image in images:
                    os.remove(f"{image}")
                subprocess.call(["xdg-open", filepath])
            else:
                foia_session.console_log("Please fill out all fields.",foia_session.current_console_messages)


        elif event == "-Letter_Image_Input-" and foia_session.database_loaded:
           #print("Letter attach Is working")
            save_letter_image_input(foia_session.window,values)

        elif event == "-Message_View_Button-" and foia_session.database_loaded:
            letter_message_button_function(foia_session.window,values)

        elif event == "-Letter_View_Button-" and foia_session.database_loaded:
            letter_view_button_function(foia_session.window,values)
        elif event == "-Letters_Display_Content-" and foia_session.database_loaded:
            if values['-Letters_Display_Content-'] != []:
                if foia_session.display_letters[0][0] != f"""{foia_session.organization_acronym}-LTR-{foia_session.new_letter+10000}""":
                    load_letter_data(foia_session.window,values)
        elif event == '-New_Letter_Button-' and foia_session.database_loaded:
            if foia_session.database_loaded:
                activate_new_letter_fields(foia_session.window,values)
        elif event == '-Letter_Template_Input-' and foia_session.database_loaded:
           #print(f"Letter_Template_Input: {(values['-Letter_Template_Input-'])}")
            if values['-Letter_Template_Input-'] == "":
                foia_session.window['-Letter_Template_Button-'].update("Use Template", disabled=True)
            else:
                foia_session.window['-Letter_Template_Button-'].update("Use Template", disabled=False)
        elif event == '-Letter_Template_Button-' and foia_session.database_loaded:

            #Input check
            if values['-Letter_To_Input-'] and values['-Letter_From_Input-'] and values['-Letter_Document_Input-'] and values['-Letter_Request_Input-']:

                if foia_session.window['-Letter_Template_Button-'].ButtonText == "Use Template":
                    foia_session.window['-Letter_Template_Button-'].update("Really?")
                else:
                    if values['-Letter_To_Input-'] != "" and values['-Letter_From_Input-'] != "":
                        foia_session.window['-Letter_Template_Button-'].update("Use Template", disabled=True)

                        #To Field (Responder)
                        responder_input = values['-Letter_To_Input-']
                        responder_id = get_id_from_optionmenu(responder_input)
                       #print(responder_id)

                        #From Field (Requester)
                        requester_input = values['-Letter_From_Input-']

                        requester_id = get_id_from_optionmenu(requester_input)
                       #print(requester_id)
                        

                        #Template id
                        template_input = values['-Letter_Template_Input-']
                        template_id = get_id_from_optionmenu(template_input)
                        

                        #Document and Request
                        document = values['-Letter_Document_Input-']
                        request = values['-Letter_Request_Input-']

                        #Enter dummy application variables for standalone letter
                        applicant_id = 0
                        application_id = 0

                        #Check if the letter is associated with an application and retrieve the IDs 
                        letter_tracking = values['-Letter_ID_Input-']
                        get_letter_query = f"""SELECT Application_ID FROM tbl_Letters WHERE Tracking_Number IS '{letter_tracking}';"""
                        this_letter = db.execute_read_query_dict(foia_session.connection,get_letter_query)
                        if type(this_letter) == list and len(this_letter) > 0:
                            application_id = this_letter[0]['Application_ID']
                            get_applicant_id_query = f"""SELECT Applicant_ID from tbl_Applications WHERE Application_ID IS '{application_id}';"""
                            this_applicant = db.execute_read_query_dict(foia_session.connection,get_applicant_id_query)
                            if type(this_applicant) == list and len(this_applicant) > 0:
                                applicant_id = this_applicant[0]['Applicant_ID']



                        corrected_text = load_selected_template(application_id, template_id,responder_id,requester_id,applicant_id,document, request)
                        foia_session.window['-Letter_Message_Display-'].update(corrected_text)
                    else:
                        foia_session.window['-Letter_Template_Button-'].update("Use Template")
                        foia_session.window['-Letter_Message_Display-'].update("Please choose a Requester and a Responder.")
            else:
                foia_session.console_log("Please fill out all inputs.",foia_session.current_console_messages)

        


        elif event == "-Documentation_Button-":

            subprocess.call(["xdg-open", "readme.pdf"])

        elif event == "Documentation":
            this_tab_index = 8
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
                    
            update_documentation_view(foia_session.window, values)
        elif event == "About":
            this_tab_index = 9
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            update_about_view(foia_session.window, values)
        elif event == "New Database":
            
            this_layout, foia_session.num = new_database_layout(foia_session.num)
            #print(this_layout, foia_session.num)
            new_database_window = sg.Window(title="Create a New Database", location=(900,200),layout= this_layout, margins=(10,10), resizable=True, size=(480,660))
            new_database_window.close_destroys_window = True
            event_newdb, values_newdb = new_database_window.read(close=True)
            values.update(values_newdb)
            if event_newdb == "Exit FOIA(s)" or event == sg.WIN_CLOSED:
                foia_session.guitimer = "Initializing"
            elif event_newdb == f"-Submit_New_Database_Button_{foia_session.num}-": 
                foia_session.connection = False
                foia_session.filekey, foia_session.filename = create_database(values, foia_session.current_console_messages, foia_session.window, foia_session.num, current_year)
                #print(ledger_name)
                foia_session.current_console_messages = foia_session.console_log(f"Database created: {foia_session.db_name}", foia_session.current_console_messages)
                foia_session.current_console_messages = foia_session.console_log(f"Filekey created: {foia_session.filename}", foia_session.current_console_messages)
                foia_session.current_console_messages = foia_session.console_log("Dashboard statistics updated.", foia_session.current_console_messages)
                foia_session.guitimer = "Initializing"
        elif event == "Open Database":    
            
            this_layout, foia_session.num = open_database_layout(foia_session.num)
            #print(this_layout, foia_session.num)
            new_database_window = sg.Window(title="Open a Database", location=(900,500),layout= this_layout, margins=(10,10), resizable=True, size=(480,120))
            event_opendb, values_opendb = new_database_window.read(close=True)
            values.update(values_opendb)
            if event_opendb == f"-Open_Database_Button_{foia_session.num}-": 
                
                
                fileloc = str(values[f"-Open_File_{foia_session.num}-"])
                db_name_0 = fileloc[:-3]
                foia_session.filekey=""
                filename_0 = fileloc
                
                
                remove_to = filename_0[::-1].index("/")
                #print("1042")
                foia_session.filename = filename_0[-remove_to:]

                #print(f"1053 filename: {foia_session.filename}")

                
                
                
                remove_to = db_name_0[::-1].index("/")
                #print("1042")
                foia_session.db_name = db_name_0[-remove_to:]
                #print(foia_session.db_name)
                foia_session.save_location = db_name_0[:-remove_to]
                if foia_session.save_location == None or foia_session.save_location== "" or foia_session.save_location == ".":
                    foia_session.save_location = "./"
                if foia_session.save_location[-1] != "/":
                    foia_session.save_location = foia_session.save_location + "/"
                #print(f"1044 {foia_session.filekey} {foia_session.db_name}; {foia_session.save_location}")
                with open(f"{foia_session.save_location}{foia_session.filename}",'rb') as file:
                    foia_session.filekey = file.read()
                #print(f"1049 filekey: {foia_session.filekey}; db_name: {foia_session.db_name}; save_location: {foia_session.save_location}")
                foia_session.connection, foia_session.filekey = db.open_database(foia_session.filename, foia_session.db_name, foia_session.save_location)
                foia_session.window = update_dashboard_statistics(foia_session.window, values)
                #print(foia_session.ledger_name)
                load_session_data(foia_session.window, values)
                #Backforth 34636
                foia_session.database_loaded = True



                foia_session.current_console_messages = foia_session.console_log(f"Filekey Read: {foia_session.filename}", foia_session.current_console_messages)
                foia_session.current_console_messages = foia_session.console_log(f"Database Opened: {foia_session.db_name}", foia_session.current_console_messages)
                foia_session.current_console_messages = foia_session.console_log("Dashboard statistics updated.", foia_session.current_console_messages)
            
        elif event == "Save Database" and foia_session.database_loaded:    
                if foia_session.save_location == None or foia_session.save_location== "" or foia_session.save_location == ".":
                    foia_session.save_location = "./"
                if foia_session.save_location[-1] != "/":
                    foia_session.save_location = foia_session.save_location + "/"
                message, foia_session.connection = db.save_database(foia_session.connection, foia_session.db_name, foia_session.filename, foia_session.save_location)
                #update_dashboard_statistics(foia_session.connection, window, ledger_name, foia_session.db_name, values)
                foia_session.current_console_messages = foia_session.console_log(message, foia_session.current_console_messages)
                #current_console_messages = console_log(window, "Dashboard statistics updated.", current_console_messages)
        elif event == "Database Properties":
            this_tab_index = 10
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_properties_view(foia_session.window, values, foia_session.connection)            
 
        elif event == "View Applicants":
            this_tab_index = 12
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_applicants_view(foia_session.window, values)             
        elif event == "View Responders":
            this_tab_index = 13
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_responders_view(foia_session.window, values)   
        









        #TEMPLATES SECTION

        elif event == "-Templates_Tag_Input-" and foia_session.database_loaded:
           #print(f"values['-Templates_Tag_Input-']")
            clipboard_content = Tk()
            clipboard_content.withdraw()
            clipboard_content.clipboard_clear()
            clipboard_content.clipboard_append(f"{values['-Templates_Tag_Input-']}")
            clipboard_content.update()
            clipboard_content.destroy()        

        elif event == "Templates":
            this_tab_index = 11
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_templates_view(foia_session.window, values)    
        elif event == "-Templates_List-" and foia_session.database_loaded:
           #print(f"templates_list: {values['-Templates_List-']}")
           #print(len(values['-Templates_List-']))
            if values['-Templates_List-'] != []:
                edit_selected_template(foia_session.window, values)
        elif event == '-Template_Preview_Button-' and foia_session.database_loaded:
            generate_template_preview(foia_session.window,values)
        elif event == '-Templates_Search_Input-' and foia_session.database_loaded:
            update_templates_view(foia_session.window, values)    
        elif event == '-Templates_Cancel_Button-' and foia_session.database_loaded:
            foia_session.window['-Templates_Search_Input-'].update("")
            update_templates_view(foia_session.window, values)    
        elif event == '-New_Template_Button-' and foia_session.database_loaded:
            if foia_session.window['-New_Template_Button-'].ButtonText == "New Template":
                activate_new_template_fields(foia_session.window,values)
                foia_session.window['-New_Template_Button-'].update("Save New")   
            elif foia_session.window['-New_Template_Button-'].ButtonText == "Save New":
                save_new_template(foia_session.window,values)
 
            elif foia_session.window['-New_Template_Button-'].ButtonText == "Save Changes":
                save_edit_template(foia_session.window,values) 
        elif event == '-Templates_Name_Input-' and foia_session.database_loaded:
            update_new_template_list(foia_session.window,values)
            










        #REQUESTER SECTION

        elif event == "View Requesters":
            this_tab_index = 6
            for i in range(len(foia_session.tab_key_list)):
                if i == this_tab_index:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=True)
                    foia_session.window[foia_session.tab_key_list[i]].select()
                else:
                    foia_session.window[foia_session.tab_key_list[i]].update(visible=False)
            if foia_session.database_loaded:
                update_requesters_view(foia_session.window, values)

        elif event == "-Requesters_Display_Content-" and foia_session.database_loaded:
            if foia_session.window['-New_Requester_Button-'].ButtonText == "New Requester":   
               #print("requesters display content:")
               #print(values['-Requesters_Display_Content-'])
               #print('foia_session.requesters')
               #print(foia_session.requesters)
                
                if values['-Requesters_Display_Content-'] != []:
                    foia_session.this_requester = foia_session.requesters[values['-Requesters_Display_Content-'][0]][0] 
                load_requester_data(foia_session.window,values,foia_session.this_requester)
        elif event == "-Edit_Requester_Button-" and foia_session.database_loaded:
            if foia_session.window['-Edit_Requester_Button-'].ButtonText == "Edit Requester":
                foia_session.window['-Edit_Requester_Button-'].update("Save Changes")
                foia_session.window['-New_Requester_Button-'].update(disabled=True)
                activate_requester_fields(foia_session.window,values)
            elif foia_session.window['-Edit_Requester_Button-'].ButtonText == "Save Changes":
                foia_session.window['-Edit_Requester_Button-'].update("Edit Requester")
                foia_session.window['-New_Requester_Button-'].update("New Requester", disabled=False)

                save_requester_changes(foia_session.window,values,foia_session.requesters[values['-Requesters_Display_Content-'][0]][0])
                update_requesters_view(foia_session.window, values)
        elif event == '-Requester_Photo_Input-' and foia_session.database_loaded:
            foia_session.window['-Requester_Photo_Display-'].update(values['-Requester_Photo_Input-'], subsample=4)
        elif event == '-New_Requester_Button-' and foia_session.database_loaded:
            if foia_session.window['-New_Requester_Button-'].ButtonText == "New Requester":
                count_requesters_query = f"""SELECT MAX(Requester_ID) FROM tbl_Requesters;"""
                max_requester = db.execute_read_query_dict(foia_session.connection,count_requesters_query)
                foia_session.new_requester = 1
                if max_requester != [] and type(max_requester) == list:
                   #print(f"max requester: {max_requester[0]['MAX(Requester_ID)']}")
                    foia_session.new_requester = int(max_requester[0]['MAX(Requester_ID)']) + 1
                add_new_requester_fields(foia_session.window,values,foia_session.new_requester)
            elif foia_session.window['-New_Requester_Button-'].ButtonText == "Save New":
                if values['-Requester_FirstName_Input-'] and values['-Requester_LastName_Input-'] and values['-Requester_MiddleName_Input-'] and values['-Requester_FullName_Input-'] and values['-Requester_PreferredName_Input-'] and values['-Requester_ReturnAddress_Input-'] and values['-Requester_Phone_Input-'] and values['-Requester_Email_Input-']:
                    save_new_requester(foia_session.window,values, foia_session.new_requester)
                    update_requesters_view(foia_session.window, values)
                else:
                    foia_session.console_log("Please Fill Out All Fields",foia_session.current_console_messages)
        elif event == '-Cancel_New_Requester_Button-' and foia_session.database_loaded:
            for i in range(2):
                update_requesters_view(foia_session.window, values)
                foia_session.window['-New_Requester_Button-'].update('New Requester')
                disable_requester_fields(foia_session.window,values)
                time.sleep(0.1)




        #APPLICANT SECTION

            
        elif event == "-New_Applicant_Button-" and foia_session.database_loaded:
            if foia_session.window['-New_Applicant_Button-'].ButtonText == "New Applicant" and foia_session.database_loaded:
                activate_new_applicant_fields(foia_session.window,values)
                #there are ∞ types of people: those who understand limits and those who don't.
            elif values['-Applicant_FirstName_Input-'] and values['-Applicant_LastName_Input-'] and values['-Applicant_FullName_Input-'] and values['-Applicant_PreferredName_Input-'] and values['-Applicant_ReturnAddress_Input-']:
                if values['-Applicant_Email_Input-'] and values['-Applicant_Phone_Input-']:

                    save_new_applicant(foia_session.window,values)
        elif event == "-Applicants_Display_Content-" and foia_session.database_loaded:
            if foia_session.window['-New_Applicant_Button-'].ButtonText == "New Applicant" and foia_session.database_loaded:  
               #print("applicants display content:")
               #print(values['-Applicants_Display_Content-'])
               #print('foia_session.applicants')
               #print(foia_session.applicants)
                
                if values['-Applicants_Display_Content-'] != []:
                    foia_session.this_applicant = foia_session.applicants[values['-Applicants_Display_Content-'][0]][0] 
                
                load_applicant_data(foia_session.window,values,foia_session.this_applicant)            
        elif event == "-Edit_Applicant_Button-" and foia_session.database_loaded:
            if foia_session.window['-Edit_Applicant_Button-'].ButtonText == "Edit Applicant":
                foia_session.window['-Edit_Applicant_Button-'].update("Save Changes")
                foia_session.window['-New_Applicant_Button-'].update(disabled=True)
                activate_edit_applicant_fields(foia_session.window,values)
            elif foia_session.window['-Edit_Applicant_Button-'].ButtonText == "Save Changes":
                foia_session.window['-Edit_Applicant_Button-'].update("Edit Applicant")
                foia_session.window['-New_Applicant_Button-'].update("New Applicant", disabled=False)

                save_applicant_changes(foia_session.window,values,foia_session.applicants[values['-Applicants_Display_Content-'][0]][0])
                update_applicants_view(foia_session.window, values)
        elif event == "-Applicant_Cancel_Button-" and foia_session.database_loaded:
            foia_session.window['-Applicants_Search_Input-'].update("")
            update_applicants_view(foia_session.window, values)
            deactivate_applicant_fields(foia_session.window,values)
        elif event == "-Applicants_Search_Input-" and foia_session.database_loaded:
            update_applicants_view(foia_session.window, values)


        #RESPONDER SECTION

        elif event == "-New_Responder_Button-" and foia_session.database_loaded:
            if foia_session.window['-New_Responder_Button-'].ButtonText == "New Responder" and foia_session.database_loaded:
                activate_new_responder_fields(foia_session.window,values)
                #there are ∞ types of people: those who understand limits and those who don't.
            elif values['-Responder_Org_Name_Input-'] and values['-Responder_Org_Type_Input-'] and values['-Responder_Contact_First_Input-'] and values['-Responder_Contact_Last_Input-'] and values['-Responder_Contact_Preferred_Input-'] and values['-Responder_Phone_Input-']:
                if values['-Responder_ReturnAddress_Input-'] or values['-Responder_MailingAddress_Input-']:
                    save_new_responder(foia_session.window,values)
        elif event == "-Responders_Display_Content-" and foia_session.database_loaded:
            if foia_session.window['-New_Responder_Button-'].ButtonText == "New Responder":   
               #print("responders display content:")
               #print(values['-Responders_Display_Content-'])
               #print('foia_session.responders')
               #print(foia_session.responders)
                
                if values['-Responders_Display_Content-'] != []:
                    foia_session.this_responder = foia_session.responders[values['-Responders_Display_Content-'][0]][0] 
                load_responder_data(foia_session.window,values,foia_session.this_responder)            
        elif event == "-Edit_Responder_Button-" and foia_session.database_loaded:
            if foia_session.window['-Edit_Responder_Button-'].ButtonText == "Edit Responder":
                foia_session.window['-Edit_Responder_Button-'].update("Save Changes")
                foia_session.window['-New_Responder_Button-'].update(disabled=True)
                activate_edit_responder_fields(foia_session.window,values)
            elif foia_session.window['-Edit_Responder_Button-'].ButtonText == "Save Changes":
                foia_session.window['-Edit_Responder_Button-'].update("Edit Responder")
                foia_session.window['-New_Responder_Button-'].update("New Responder", disabled=False)

                save_responder_changes(foia_session.window,values,foia_session.responders[values['-Responders_Display_Content-'][0]][0])
                update_responders_view(foia_session.window, values)
        elif event == "-Responders_Cancel_Button-" and foia_session.database_loaded:
            foia_session.window['-Responders_Search_Input-'].update("")
            update_responders_view(foia_session.window, values)
            deactivate_responder_fields(foia_session.window, values)
        elif event == "-Responders_Search_Input-" and foia_session.database_loaded:
            update_responders_view(foia_session.window, values)



        #MENU SECTION#Backforth 34636
        #elif event == 'Save Database':



foia_session.window.close()
