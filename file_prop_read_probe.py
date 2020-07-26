import os
from pathlib import Path

target_dir = 'D:\Projects\T752'

# files_list=os.listdir(target_dir)
# for entry in files_list:
#     print(entry)


# with os.scandir(target_dir) as dir_entries:
#     for entry in dir_entries:
#         info = entry.stat()
#         print(info.st_mtime)
#         print(info)

# entries = Path(target_dir)
# for entry in entries.iterdir():
#     print(entry.name)
#     print(entry.stat())
#     print(entry.lstat())
#
# import win32com.client
#
# sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
# ns = sh.NameSpace(target_dir)
# columns = []
# colnum = 0
# while True:
#     colname = ns.GetDetailsOf(None, colnum)
#     if not colname:
#         break
#     columns.append(colname)
#     colnum += 1
#
# for item in ns.Items():
#     print(item.Path)
#     for colnum in range(len(columns)):
#         colval = ns.GetDetailsOf(item, colnum)
#         if colval:
#             print('\t', columns[colnum], colval)

import docx

# file_name = 'D:\Projects\T752\01-28736 test 1.slddrw'

# file_name = 'D:\Projects\T752\PDM-ODOO drawing version transfer 0.1.docx'
#
# document = docx.Document(docx = file_name)
# core_properties = document.core_properties
# print(core_properties.author)
# print(core_properties.created)
# print(core_properties.last_modified_by)
# print(core_properties.last_printed)
# print(core_properties.modified)
# print(core_properties.revision)
# print(core_properties.title)
# print(core_properties.category)
# print(core_properties.comments)
# print(core_properties.identifier)
# print(core_properties.keywords)
# print(core_properties.language)
# print(core_properties.subject)
# print(core_properties.version)
# print(core_properties.keywords)
# print(core_properties.content_status)

# import pySW

# import win32com
# import System
# t = System.Type.GetTypeFromProgID('SldWorks.Application')
# swApp = System.Activator.CreateInstance(t)
# swApp.Visible = True

# begin python

# import EdmLib
#
# myVlt = EdmVault5()
#
# myVlt.Login('***', '***', 'PDM')  # my username and password are not really all stars
#
# myFolder = myVlt.GetFolderFromPath('C:\PDM\foo')
#
# myFile = myVlt.GetFileFromPath('C:\PDM\foo\bar.txt', myFolder)
#
# # oddly this returns a tuple, so use the first one?
#
# myFile[0].GetFileCopy(1, myFile[0].CurrentVersion, myFolder.ID, 0)
#
# # end python

import os
import win32com.client  # Requires "pip install pywin32"

__all__ = ['get_xls_properties', 'get_file_details']

# https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.tools.excel.workbook.builtindocumentproperties?view=vsto-2017
BUILTIN_XLS_ATTRS = ['Title', 'Subject', 'Author', 'Keywords', 'Comments', 'Template', 'Last Author', 'Revision Number',
                     'Application Name', 'Last Print Date', 'Creation Date', 'Last Save Time', 'Total Editing Time',
                     'Number of Pages', 'Number of Words', 'Number of Characters', 'Security', 'Category', 'Format',
                     'Manager', 'Company', 'Number of Btyes', 'Number of Lines', 'Number of Paragraphs',
                     'Number of Slides', 'Number of Notes', 'Number of Hidden Slides', 'Number of Multimedia Clips',
                     'Hyperlink Base', 'Number of Characters (with spaces)']


def get_xls_properties(filename, xl=None):
    """Return the known XLS file attributes for the given .xls filename."""
    quit = False
    if xl is None:
        xl = win32com.client.DispatchEx('Excel.Application')
        quit = True

    # Open the workbook
    wb = xl.Workbooks.Open(filename)

    # Save the attributes in a dictionary
    attrs = {}
    for attrname in BUILTIN_XLS_ATTRS:
        try:
            val = wb.BuiltinDocumentProperties(attrname).Value
            if val:
                attrs[attrname] = val
        except:
            pass

    # Quit the excel application
    if quit:
        try:
            xl.Quit()
            del xl
        except:
            pass

    return attrs


def get_file_details(directory, filenames=None):
    """Collect the a file or list of files attributes.
    Args:
        directory (str): Directory or filename to get attributes for
        filenames (str/list/tuple): If the given directory is a directory then a filename or list of files must be given
    Returns:
         file_attrs (dict): Dictionary of {filename: {attribute_name: value}} or dictionary of {attribute_name: value}
            if a single file is given.
    """
    if os.path.isfile(directory):
        directory, filenames = os.path.dirname(directory), [os.path.basename(directory)]
    elif filenames is None:
        filenames = os.listdir(directory)
    elif not isinstance(filenames, (list, tuple)):
        filenames = [filenames]

    if not os.path.exists(directory):
        raise ValueError('The given directory does not exist!')

    # Open the com object
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)  # Generates local compiled with make.py
    ns = sh.NameSpace(os.path.abspath(directory))

    # Get the directory file attribute column names
    cols = {}
    for i in range(512):  # 308 seemed to be max for excel file
        attrname = ns.GetDetailsOf(None, i)
        if attrname:
            cols[i] = attrname

    # Get the information for the files.
    files = {}
    for file in filenames:
        item = ns.ParseName(os.path.basename(file))
        files[os.path.abspath(item.Path)] = attrs = {}  # Store attributes in dictionary

        # Save attributes
        for i, attrname in cols.items():
            attrs[attrname] = ns.GetDetailsOf(item, i)

        # For xls file save special properties
        if os.path.splitext(file)[-1] == '.xls':
            xls_attrs = get_xls_properties(item.Path)
            attrs.update(xls_attrs)

    # Clean up the com object
    try:
        del sh
    except:
        pass

    if len(files) == 1:
        return files[list(files.keys())[0]]
    return files


# if __name__ == '__main__':
#     import argparse
#
#     P = argparse.ArgumentParser(description="Read and print file details.")
#     P.add_argument('filename', type=str, help='Filename to read and print the details for.')
#     P.add_argument('-v', '--show-empty', action='store_true', help='If given print keys with empty values.')
#     ARGS = P.parse_args()
#
#     # Argparse Variables
#     FILENAME = ARGS.filename
#     SHOW_EMPTY = ARGS.show_empty
#     DETAILS = get_file_details(FILENAME)
#
#     print(os.path.abspath(FILENAME))
#     for k, v in DETAILS.items():
#         if v or SHOW_EMPTY:
#             print('\t', k, '=', v)
filename = '01-28736 test.SLDDRW'
properties = get_file_details(target_dir, filenames=[filename])
for prop in properties:
    print(prop)
