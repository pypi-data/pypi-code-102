'''
This module contains functions that are used to add or remove keys to the registry of Windows, for the purposes
of accessing pdf2bib by right clicking on a file or a directory
'''

import logging
from sys import executable as python_path
from os import path
import os

if os.name == 'nt':
    import winreg as reg

logger = logging.getLogger("pdf2bib")



def delete_sub_key(key0, current_key, arch_key=0):
    #Code inpsired by Orsiris de Jong's solution https://stackoverflow.com/questions/38205784/python-how-to-delete-registry-key-and-subkeys-from-hklm-getting-error-5
    open_key = reg.OpenKey(key0, current_key, 0, reg.KEY_ALL_ACCESS | arch_key)
    info_key = reg.QueryInfoKey(open_key)
    for x in range(0, info_key[0]):
        # NOTE:: This code is to delete the key and all sub_keys.
        # If you just want to walk through them, then
        # you should pass x to EnumKey. sub_key = reg.EnumKey(open_key, x)
        # Deleting the sub_key will change the sub_key count used by EnumKey.
        # We must always pass 0 to EnumKey so we
        # always get back the new first sub_key.
        sub_key =reg.EnumKey(open_key, 0)
        try:
            reg.DeleteKey(open_key, sub_key)
            logger.info("Removed %s\\%s " % (current_key, sub_key))
        except OSError:
            delete_sub_key(key0, "\\".join([current_key,sub_key]), arch_key)
            # No extra delete here since each call
            # to delete_sub_key will try to delete itself when its empty.

    reg.DeleteKey(open_key, "")
    open_key.Close()
    logger.info("Removed %s" % current_key)
    return

def install_right_click():
    if not(os.name == 'nt'):
        logger.error(f'This functionality is currently implemented only for Windows.')
        return
    python_folder = path.dirname(python_path)
    if python_folder[-7:].lower() == 'scripts': #This typically happens when python is installed in a virtual environment
        path_pdf2bib = python_folder + "\pdf2bib.exe"
    else:
        path_pdf2bib = python_folder + "\scripts\pdf2bib.exe"

    logger.info(f'Adding pdf2bib to the right-click context menu by adding keys to the system register...')
    try:

        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'Directory\shell\pdf2bib')
        reg.SetValueEx(key, 'MUIVerb', 0, reg.REG_SZ, 'pdf2bib')
        reg.SetValueEx(key, 'subcommands', 0, reg.REG_SZ, '')
        reg.CloseKey(key)
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'Directory\shell\pdf2bib\shell')
        reg.CloseKey(key)

        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'Directory\shell\pdf2bib\shell\pdf2bib_copybibtex')
        reg.SetValue(key, '', reg.REG_SZ, 'Retrieve and copy bibtex entries of all pdf files in this folder...')
        reg.CloseKey(key)
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'Directory\shell\pdf2bib\shell\pdf2bib_copybibtex\command')
        reg.SetValue(key, '', reg.REG_SZ, path_pdf2bib + " \"%1\" -bclip")
        reg.CloseKey(key)


        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'SystemFileAssociations\.pdf\shell\pdf2bib')
        reg.SetValueEx(key, 'MUIVerb', 0, reg.REG_SZ, 'pdf2bib')
        reg.SetValueEx(key, 'subcommands', 0, reg.REG_SZ, '')
        reg.CloseKey(key)
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'SystemFileAssociations\.pdf\shell\pdf2bib\shell')
        reg.CloseKey(key)

        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'SystemFileAssociations\.pdf\shell\pdf2bib\shell\pdf2bib_copybibtex')
        reg.SetValue(key, '', reg.REG_SZ, 'Retrieve and copy bibtex entry of this file...')
        reg.CloseKey(key)
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, 'SystemFileAssociations\.pdf\shell\pdf2bib\shell\pdf2bib_copybibtex\command')
        reg.SetValue(key, '', reg.REG_SZ, path_pdf2bib + " \"%1\" -bclip")
        reg.CloseKey(key)


        logger.info(f'All necessary keys were added to the system register.')
    except Exception as e:
        logger.error(e)
        logger.error(f'A problem occurred when trying to add pdf2bib to the right-click context menu.\nNOTE: this functionality is only available in Windows, and it has to be installed from a terminal with administrator rights.')
 
def uninstall_right_click():
    if not(os.name == 'nt'):
        logger.error(f'This functionality is currently implemented only for Windows.')
        return
    logger.info(f'Removing all keys associated to pdf2bib from the system register...')
    try:
        delete_sub_key(reg.HKEY_CLASSES_ROOT, "SystemFileAssociations\.pdf\shell\pdf2bib")
        delete_sub_key(reg.HKEY_CLASSES_ROOT, "Directory\shell\pdf2bib")
        logger.info(f'All keys were removed.')
    except Exception as e:
        logger.error(e)
        logger.error(f'A problem occurred when trying to remove keys from the system registry.\nNOTE: this command needs to be executed from a terminal with administrator rights.')
 
