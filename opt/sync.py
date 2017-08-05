#!/usr/bin/env bash

import dropbox
import contextlib
import time
import datetime
import os
import sys

dbx =dropbox.Dropbox('LLrM_PNI3uAAAAAAAAAAKTLyTYCsEUjUGeMfOS2awbPJ65JbwPfejNd2ShCvyjKm')

#upload files
def upload(name, path, overwrite=True):
    mode = (dropbox.files.WriteMode.overwrite
        if overwrite
        else dropbox.files.WriteMode.add)
    with open(path, 'rb') as f:
        data = f.read()
        name = "/Test server/" + name
        dbx.files_upload(data, name, mode, mute = True)
    return

#download files to check
def download(path):
    try:
        md, res = dbx.files_download(path)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None
    data = res.content
    return data

#download a file o sysnc it with the actual file
def downloadToFile(localPath, name, rev=None):
    dbx.files_download_to_file(localPath, "/Test server/" + name, rev)

#open files
def openFile(path):
    with open(path, "rb") as f:
        data = f.read()
    return data

#Check if allready synced, then upload
def mainUpload(name, path):  
    path = path + name
    res = ""
    try:
        res = download("/test server/" + name)
    except:
        pass
    content = openFile(path)
    if res == content:
        print(name + " is allready synced!")
    else:
        upload(name, path)
        print(name + " is now uploaded!")
    return

#download the files to Heroku
def mainDownload(name, path):
    path = path + "/" + name
    content = ""
    try:
        content = openFile(path)
    except:
        pass
    res = download("/Test server/" + name)
    if content == res:
        print(name + " is allready downloaded")
    else:
        downloadToFile(path, name)
        print(name + " is now downloaded!")

#Checks in folders for files and folders
def folders(path, subfolder, function):
    local_dir = (path + subfolder)
    if function == True:
        files = os.listdir(local_dir)
        for filename in files:
            if "." not in filename:
                folders(path, subfolder + "/" + filename, True)
            else:
                if filename == "desktop.ini":
                    continue
                else:
                    mainUpload(subfolder + "/" + filename, path)
    else:
        for filename in dbx.files_list_folder("/Test server/" + subfolder).entries:
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            if "." not in filename.name:
                folders(path, subfolder + "/" + filename.name, False)
            else:
                mainDownload(subfolder + "/" + filename.name, path)

filesList = {"world"}

#sync files down from the cloud to Heroku
def initialSync():
    localPath = "/app/"
    for files in filesList:
        if "." not in files:
            folders(localPath + "/", files, False)
        else:
            mainDownload(files, localPath)


#sync filess up to the cloud
def normalSync():
    for name in filesList:
        path = "/app/"
        if "." not in name:
            folders(path, name, True)
        else:
            mainUpload(name, path)

#run


if sys.argv[0] == "init":
    initialSync()
    print("Done syncing.")
elif sys.argv[0] == "repeating":
    sleeptime = int(sys.argv[1])
    while True:
        normalSync()
        time.sleep(sleeptime)
else:
    normalSync()

run("repeating")


