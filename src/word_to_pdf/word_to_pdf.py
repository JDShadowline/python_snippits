#!/usr/bin/python
#####################
# Description / Notes
#
#   At this point we have created the directories required and the script to convert RTF to XML. I beleive XML might be easier to work with but this is yet to be proven.
# We also have a list/template for the file names. 
#
# Logic:
#   For each file in input dir, convert and copy to the xml folder. Then iterate over the XML folder to check against the file name list. If a file exists as a LH or RH make two copies and edit each?
#
#################
# Imports
#####################
from cgitb import enable
from genericpath import isdir
from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter
from docx2pdf import convert
import re, os, pathlib
from datetime import datetime

import win32com.client
from alive_progress import alive_it
from PyPDF4 import PdfFileWriter, PdfFileReader

import easygui as eg
import PySimpleGUI as sg
import threading

#################
# Global Variables
#####################
try:
    home_path = pathlib.Path(__file__).parent.resolve() # get script path
except:
    home_path = pathlib.Path().resolve() # fallback to current dir

#################
# Set default watermark file
# This assumes the watermark.pdf file is in the same directory as the script
# This also returns a pathlib object for the watermark file
watermark_file = "watermark.pdf"
default_watermark_path = pathlib.Path(os.path.join(home_path, watermark_file))
if os.path.exists(default_watermark_path):
    watermark_file = default_watermark_path.name
#################
# GUI/Layout
#####################
def main_window(theme):
    sg.theme(theme)
    layout = []

    page_main = [
        [sg.Text('Main')],
        
        ]
    page_batch = [
        [sg.Text('Batch')],
        [sg.Multiline(autoscroll=True,size=(80,20), key='-batch-', expand_x=True, auto_refresh=True,write_only=True)],
        [sg.Text('Input:',size=(10,1)),sg.Input(default_text=sg.user_settings_get_entry('-dir_input-', ''),key='-batch-input-', text_color='grey14', readonly=True, size=(60,1), expand_x=True),sg.Button('Browse', key='-batch-input-browse-', size=(10,1))],
        [sg.Text('Output:',size=(10,1)),sg.Input(default_text=sg.user_settings_get_entry('-dir_output-', ''), key='-batch-output-', text_color='grey14', readonly=True, size=(60,1), expand_x=True),sg.Button('Browse', key='-batch-output-browse-', size=(10,1))],
        [sg.Checkbox('Watermark', key='-watermark-', enable_events=True, size=(10,1)), sg.Input(default_text=watermark_file,key='-watermark-input-',disabled=True,disabled_readonly_background_color = 'dim gray', size=(60,1),expand_x=True), sg.Button('Browse', key='-watermark-browse-',disabled=True, size=(10,1))],
        [sg.Text('')],
        [sg.Button('Start Batch', size=(10,2), key='-batch-start-',bind_return_key=True, expand_x=True)],

        ]
    page_single = [
        [sg.Text('Single')],
       
        ]

    layout += [
        [sg.TabGroup([[sg.Tab('Home', page_main),sg.Tab('Batch Process', page_batch), sg.Tab('Single File', page_single)]], enable_events=False, key='-tab-group-')],
        [sg.StatusBar(text='', key='-status-', size=(80,1), text_color='white', background_color='grey13', relief=sg.RELIEF_SUNKEN, expand_x=True, justification='center')],
        ]
    window = sg.Window('DOCX to PDF file converter', layout, grab_anywhere=False, resizable=True, margins=(0, 0), use_custom_titlebar=True, finalize=True, keep_on_top=False,
                        enable_close_attempted_event=True, 
                        # location=sg.user_settings_get_entry('-location-', (None, None))  # This is reading the saved location from the user settings file
                       )
    window.set_min_size(window.size)
    return window



#################
# Classes/Functions
#####################

def convert_batch(window,values, input_path, output_path, watermark):
    window['-batch-'].update('') ## Clear output
    docxfiles, pdffiles, outputfiles, existingfiles = check_folders(window, values, input_path, output_path)
        
    if len(docxfiles) > 0:
        for file in docxfiles:
            if file.name not in outputfiles: # if the file is not in the output directory
                convert(file, output_path)
                if watermark:
                    outfile = os.path.join(output_path, file.name.replace('.docx','.pdf'))
                    watermarker(window, values, outfile, output_path)
                window['-batch-'].update('Converted '+file.name+' to PDF\n', append=True)
    if len(pdffiles) > 0:
        if not watermark:
            sg.popup('PDF files selected without watermark option. Please select watermark option.')
        else:
            for file in pdffiles:
                if file.name not in outputfiles: # if the file is not in the output directory
                    outfile = os.path.join(output_path, file.name.replace('.pdf','.pdf'))
                    watermarker(window, values, outfile, output_path)
                    window['-batch-'].update('Watermarked '+file.name+'\n', append=True)

def check_folders(window, values, input_path=None, output_path=None):
    docxfiles       = []
    pdffiles        = []
    allfiles        = []
    outputfiles     = []
    existing_files  = []
    if input_path and output_path:
        for file in pathlib.Path(input_path).glob(f'**/*.docx'):
            docxfiles.append(file)
            allfiles.append(file)
            window['-batch-'].update('Found DOCX file: '+file.name+'\n', append=True)
        for file in pathlib.Path(input_path).glob(f'**/*.pdf'):
            pdffiles.append(file)
            allfiles.append(file)
            window['-batch-'].update('Found PDF file: '+file.name+'\n', append=True)
        window['-batch-'].update(f"DOCX files: {len(docxfiles)}, PDF files: {len(pdffiles)}\n", append=True)
        
        for file in pathlib.Path(output_path).glob(f'**/*.*'):
            outputfiles.append(file.stem)
    
        
        for file in allfiles:
            if file.stem in outputfiles:
                existing_files.append(file.stem)
        window['-batch-'].update(f"The following files already exist in the output directory\n{existing_files}\n", append=True)
    
    return docxfiles, pdffiles, outputfiles, existingfiles
        
            
def watermarker(window, values, file_path, output_path):
    pathfile = pathlib.Path(file_path).resolve()
    print(pathfile.name, pathfile.stem, pathfile)
    base_pdf = PdfReader(file_path)
    watermark_pdf = PdfReader(values['-watermark-file-'])
    mark = watermark_pdf.pages[0]
    
    for page in range(len(base_pdf.pages)):
        merger = PageMerge(base_pdf.pages[page])
        merger.add(mark).render()
    
    writer = PdfWriter()
    outfile = os.path.join(output_path, pathfile.name)
    writer.write(outfile, base_pdf)

#################
# Loose Code
#####################

#################
# App
#####################
def main():
    window = main_window(sg.theme()) ## Create the main window and set the theme externally
    watermarked = False ## Boolean to check if watermark has been applied
    inputf=''
    outputf=''
    watermarkf = ''
    

    while True:
        event, values = window.read(timeout=100)
        
        if event == '-batch-start-':
            if not inputf or not outputf:
                sg.popup('Please select input and output folders')
            else:
                print('batch start')
                # convert_batch(window,values, inputf, outputf, watermarked)
                threading.Thread(target=convert_batch, args=([window,values, inputf, outputf, watermarked]), daemon=True).start()
            # window['-batch-'].update('String'+'\n', append=True)  #values['word']
        elif event == '-batch-input-browse-':
            print('batch browse')
            inputf = values['-batch-in-folder-'] = sg.popup_get_folder('Please select folder')
            window['-batch-input-'].update(values['-batch-in-folder-'])
            threading.Thread(target=check_folders, args=(window, values, inputf, outputf), daemon=True).start()
            
        elif event == '-batch-output-browse-':
            print('batch browse')
            outputf = values['-batch-out-folder-'] = sg.popup_get_folder('Please select folder')
            window['-batch-output-'].update(values['-batch-out-folder-'])
            threading.Thread(target=check_folders, args=(window, values, inputf, outputf), daemon=True).start()
            
        elif event == '-watermark-browse-':
            print('watermark browse')
            watermarkf = values['-watermark-file-'] = sg.popup_get_file('Please select file', default_path=os.path.join(os.getcwd(), 'watermark.pdf'))
            window['-watermark-input-'].update(values['-watermark-file-'])
            
        elif event == '-watermark-':
            watermarked = not watermarked
            window['-watermark-input-'].update(disabled= not watermarked)
            window['-watermark-browse-'].update(disabled= not watermarked)
            
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            # sg.cprint_set_output_destination(window, "-status-")
            # sg.cprint(f"============ Event = {event} ==============",text_color = 'red',key='-status-') # ,sep = " \n"
            window['-status-'].update(f"== Event = {event} ==", text_color = 'red')
            
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
                
        if event in ('Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            ## Save some settings for persistance on next run
            sg.user_settings_set_entry('-location-', window.current_location())  # The line of code to save the position before exiting
            sg.user_settings_set_entry('-dir_input-', inputf)
            sg.user_settings_set_entry('-dir_output-', outputf)
            break
        
        
    window.close() # Gracefully close out the window and exit
    exit(0)

if __name__ == '__main__':
    sg.theme('Dark Grey 13')
    main()
    # input_files = File_Helper.file_multi_openbox()
    # output_path = File_Helper.dir_openbox()
    # pdf_watermark(input_files, output_path)
    # gui()