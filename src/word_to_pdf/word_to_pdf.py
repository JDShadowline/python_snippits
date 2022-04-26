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
from genericpath import isdir
import lovely_logger as log
import tkinter as tk
from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter
# from tkinter.dialog import Dialog
import tkinter.filedialog as tk_FileDialog
import tkinter.font as tk_Font
from docx2pdf import convert
import re, os, pathlib
from datetime import datetime
import easygui as eg
import win32com.client
from alive_progress import alive_it
from PyPDF4 import PdfFileWriter, PdfFileReader

#################
# Global Variables
#####################
try:
    home_path = pathlib.Path(__file__).parent.resolve() # get script path
except:
    home_path = pathlib.Path().resolve() # fallback to current dir
    
watermark_file = "watermark.pdf"
#################
# Classes/Functions
#####################
def gui():
    choice = eg.buttonbox(msg='Convert .DOCX (Word) to .PDF (Adobe)', choices=['Single File','Folder/Batch','Cancel'])
    if choice == 'Single File':
        input_path = File_Helper.file_openbox(title="Please select .DOCX file")
        output_path = File_Helper.file_savebox(title="Please select name and directory for .pdf file.", filetypes=[("PDF files", ".pdf")])
        return convert(input_path, output_path)
    elif choice == 'Folder/Batch':
        input_path = File_Helper.dir_openbox(title="Please select input directory for .docx files")
        output_path = File_Helper.dir_openbox(title="Please select save directory for .pdf files")
        return convert(input_path, output_path)
    elif choice == 'Cancel':
        pass
    else:
        log.e('Nothing selected')


def docx_to_pdf_dir():
    input_path = File_Helper.dir_openbox(title="Please select directory for .docx files")
    output_path = File_Helper.dir_openbox(title="Please select directory for .pdf files")
    print(input_path, output_path)
    # convert(input_path, output_path)
    
def pdf_watermark(input_files, output_path):
    for file in alive_it(input_files):
        
        # print(file, pathfile.name, pathfile.stem)
        if file.endswith('.pdf'):
            watermarker(file, output_path)
            # print('File is pdf')
            
            # with open(file, "rb") as input_file:
            #     pdf = PdfFileReader(input_file)
            # with open(watermark_file, "rb") as watermark:
            #     watermark_instance = PdfFileReader(watermark_file)
            #     watermark_page = watermark_instance.getPage(0) #fetch only first page
            #     pdf_reader = PdfFileReader(file)
            #     pdf_writer = PdfFileWriter()
            #     pdf_writer.removeLinks()
            #     for page in range(pdf_reader.getNumPages()): ## Iterate through the pages and merge the watermark in.
            #         page = pdf_reader.getPage(page)
            #         page.mergePage(watermark_page)
            #         pdf_writer.addPage(page)
            #     outfile = os.path.join(output_path, pathfile.name)
            #     with open(outfile, 'wb') as out:
            #         pdf_writer.write(out)


            
def watermarker(file_path, output_path):
    pathfile = pathlib.Path(file_path).resolve()
    base_pdf = PdfReader(file_path)
    watermark_pdf = PdfReader(watermark_file)
    mark = watermark_pdf.pages[0]
    
    for page in range(len(base_pdf.pages)):
        merger = PageMerge(base_pdf.pages[page])
        merger.add(mark).render()
    
    writer = PdfWriter()
    outfile = os.path.join(output_path, pathfile.name)
    writer.write(outfile, base_pdf)
            
    
class File_Helper():
    
    def dir_openbox(title=None, default=None):
        localRoot = tk.Tk()
        localRoot.withdraw()
        localRoot.lift()
        localRoot.attributes('-topmost', 1)
        localRoot.attributes('-topmost', 0)
        if not default:
            default = home_path
        if not title:
            title = "Select Folder"
        localRoot.update()
        f = tk_FileDialog.askdirectory(
            parent=localRoot, title=title, initialdir=default, initialfile=None
        )
        localRoot.destroy()
        if not f:
            return None
        return os.path.normpath(f)

    def file_openbox(title=None, default=None):
        localRoot = tk.Tk()
        localRoot.withdraw()
        localRoot.lift()
        localRoot.attributes('-topmost', 1)
        localRoot.attributes('-topmost', 0)
        if not default:
            default = home_path
        if not title:
            title = "Select File"
        localRoot.update()
        f = tk_FileDialog.askopenfilename(
            parent=localRoot, title=title, initialdir=default, initialfile=None
        )
        localRoot.destroy()
        if not f:
            return None
        return f
    
    def file_multi_openbox(title=None, default=None):
        '''Returns a list of files'''
        localRoot = tk.Tk()
        localRoot.withdraw()
        localRoot.lift()
        localRoot.attributes('-topmost', 1)
        localRoot.attributes('-topmost', 0)
        if not default:
            default = home_path
        if not title:
            title = "Select File"
        localRoot.update()
        f = tk_FileDialog.askopenfilenames(
            parent=localRoot, title=title, initialdir=default, initialfile=None
        )
        localRoot.destroy()
        if not f:
            return None
        return f
    
    def file_savebox(title=None, default=None, filetypes=None):
        localRoot = tk.Tk()
        localRoot.withdraw()
        localRoot.lift()
        localRoot.attributes('-topmost', 1)
        localRoot.attributes('-topmost', 0)
        if not filetypes:
            filetypes = (("CSV Files",".csv"),("Excel files", ".xlsx .xls"), ("PDF files", ".pdf"))
        if not default:
            default = home_path
        if not title:
            title = "Select File"
        localRoot.update()
        f = tk_FileDialog.asksaveasfilename(
            parent=localRoot, title=title, initialdir=default, filetypes=filetypes
        )
        localRoot.destroy()
        if not f:
            return None
        return f
    
    
    




#################
# Loose Code
#####################

#################
# App
#####################
if __name__ == '__main__':
    input_files = File_Helper.file_multi_openbox()
    output_path = File_Helper.dir_openbox()
    pdf_watermark(input_files, output_path)
    # gui()