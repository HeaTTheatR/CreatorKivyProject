# -*- coding: utf-8 -*-

import os
import sys

import argparse
import traceback
import shutil

from kivy.logger import Logger
from kivy.logger import PY2


if PY2:
    FileNotFoundError = IOError


def write_file(in_file, out_file, values=False):
    string_file = open(out_file).read()
    if values:
        for key in values.keys():
            if not values[key]:
                continue
            string_file = string_file.replace(key, values[key])
        if PY2:
            open(in_file, 'w').write(string_file)
        else:
            open(in_file, 'w', encoding='utf-8').write(string_file)
    else:
        if PY2:
            open(in_file, 'w').write(string_file)
        else:
            open(in_file, 'w', encoding='utf-8').write(string_file)


def copy_files(directory):
    print(directory)
    for directory, dirs, files in os.walk(directory):
        directory_created = directory.split(prog_path)[1]
        print(FULL_PATH_TO_PROJECT + directory_created)
        os.mkdir(FULL_PATH_TO_PROJECT + directory_created)
        for file in files:
            file_created = \
                FULL_PATH_TO_PROJECT + os.path.join(directory_created, file)
            print('        ' + file_created)
            shutil.copyfile(os.path.join(directory, file), file_created)
        print()


__version__ = '2.3.0'
Logger.info('Creator Kivy Project version: ' + __version__)

if len(sys.argv) <= 1:
    Logger.warning('''
Use a script with string arguments:

'name' - project name
'version' - project version
'path' - project directory
'repo' - address of the repository on GitHub (optional)
'author' - name of the author of the project (optional)
'mail' - mail of the author of the project (optional)
'site' - project site (optional)
''')
    sys.exit(0)

prog_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.dont_write_bytecode = True

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Project name')
parser.add_argument('version', type=str, help='Project version')
parser.add_argument('copyright', type=str, help='Copyright')
parser.add_argument('path', type=str, help='Project directory')
parser.add_argument('-repo', type=str,
                    help='Address of the repository on GitHub')
parser.add_argument('-author', type=str,
                    help='Name of the author of the project')
parser.add_argument('-mail', type=str,
                    help='Mail of the author of the project')
parser.add_argument('-site', type=str, help='Project site')

SITE_PROJECT = parser.parse_args().site
VERSION_PROJECT = parser.parse_args().version
COPYRIGHT_PROJECT = parser.parse_args().copyright
NAME_PROJECT = parser.parse_args().name
DIR_PROJECT = parser.parse_args().path
REPO_PROJECT = parser.parse_args().repo
NAME_AUTHOR = parser.parse_args().author
ADDRESS_MAIL = parser.parse_args().mail
FULL_PATH_TO_PROJECT = os.path.join(DIR_PROJECT, NAME_PROJECT)

if os.path.exists(FULL_PATH_TO_PROJECT):
    Logger.error('Project {} already exists!'.format(NAME_PROJECT))
    sys.exit(0)

try:
    os.makedirs(FULL_PATH_TO_PROJECT)
    Logger.info(
        'Created project directory {} ...'.format(FULL_PATH_TO_PROJECT))
except FileNotFoundError:
    Logger.error(
        'The specified {} directory does not exist!'.format(DIR_PROJECT))
except Exception:
    print(traceback.format_exc())
    Logger.error(
        'You are not authorized to create a project in '
        '{} directory!'.format(DIR_PROJECT))

try:
    Logger.info('Create entry point main.py ...')
    write_file(
        os.path.join(FULL_PATH_TO_PROJECT, 'main.py'),
        os.path.join(prog_path, 'files', 'main'),
        {
            'REPO_PROJECT': REPO_PROJECT, 'VERSION_PROJECT': VERSION_PROJECT,
            'name_project': NAME_PROJECT.lower(), 'NAME_PROJECT': NAME_PROJECT
        }
    )
    Logger.info('Create file README.md ...')
    open(os.path.join(FULL_PATH_TO_PROJECT, 'README.md'), 'w').write('')
    Logger.info('Creating a code file program.py ...')
    write_file(
        os.path.join(FULL_PATH_TO_PROJECT, '%s.py' % NAME_PROJECT.lower()),
        os.path.join(prog_path, 'files',  'program'),
         {
             'NAME_PROJECT': NAME_PROJECT,
             'NAME_AUTHOR': NAME_AUTHOR, 'REPO_PROJECT': REPO_PROJECT,
             'name_project': NAME_PROJECT.lower()
         }
     )
    Logger.info(
        'Creating a Makefile to compile language localization files ...'
    )
    write_file(
        os.path.join(FULL_PATH_TO_PROJECT, 'Makefile'),
        os.path.join(prog_path, 'files', 'Makefile'),
        {'NAME_PROJECT': NAME_PROJECT}
    )
    Logger.info('Creating a license file ...')
    write_file(
        os.path.join(
            FULL_PATH_TO_PROJECT, 'LICENSE'),
            os.path.join(prog_path, 'files', 'LICENSE'),
        {'COPYRIGHT_PROJECT': COPYRIGHT_PROJECT}
    )

    Logger.info('Copying files project...')
    copy_files(os.path.join(prog_path, 'libs'))
    copy_files(os.path.join(prog_path, 'data'))
    copy_files(os.path.join(prog_path, 'test'))
    Logger.info('Create file navdrawer.kv ...')
    write_file(
        os.path.join(
            FULL_PATH_TO_PROJECT, 'libs', 'uix', 'kv', 'navdrawer.kv'),
            os.path.join(prog_path, 'files', 'navdrawer'),
        {'VERSION_PROJECT': VERSION_PROJECT}
    )
except FileNotFoundError as exc:
    Logger.error('I can not find the project file - ' + str(exc))
    shutil.rmtree(FULL_PATH_TO_PROJECT)
    sys.exit(0)
except Exception as exc:
    Logger.error('Unknown error - \n' + traceback.format_exc())
    shutil.rmtree(FULL_PATH_TO_PROJECT)
    sys.exit(0)

Logger.info('Installing the KivyMD library ...')

PATH_TO_APPLIBS = os.path.join(FULL_PATH_TO_PROJECT, 'libs', 'applibs')
PATH_TO_KIVYMD = os.path.join(PATH_TO_APPLIBS, 'KivyMD')
PATH_TO_KIVYMD_OLD = os.path.join(PATH_TO_APPLIBS, 'KivyMD_old')

os.chdir(PATH_TO_APPLIBS)
os.system('git clone https://github.com/HeaTTheatR/KivyMD')

try:
    os.rename(PATH_TO_KIVYMD, PATH_TO_KIVYMD_OLD)
    shutil.move(os.path.join(PATH_TO_KIVYMD_OLD, 'kivymd'), PATH_TO_APPLIBS)
    Logger.info('Clean KivyMD files ...')
    shutil.rmtree(PATH_TO_KIVYMD_OLD)
except OSError:
    Logger.error('KivyMD library not installed!')
else:
    Logger.info('KivyMD library installation completed!')
    Logger.info('Installing the Pillow library ...')
    os.system('sudo python -m pip install pillow')
    os.system('sudo python3 -m pip install pillow')
    Logger.info('Project {} successfully created!'.format(NAME_PROJECT))
