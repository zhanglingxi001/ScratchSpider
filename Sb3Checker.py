#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zipfile
import json
import re
def sb3_checker():

    filepath = "./sb3Files/"
    allDir = os.listdir(filepath)
    for dir in allDir:
        path = os.path.join(filepath, dir)
        allZip = os.listdir(path)
        for filename in allZip:
            data = ""
            file_id = re.findall("(.+?)sb", filename)[0] + "sb2"
            with zipfile.ZipFile(os.path.join(path, filename), 'r') as zfile:
                if "project.json" in zfile.namelist():
                    data = zfile.read("project.json")
                    data = json.loads(data)
            try:
                if data["meta"]["semver"] == "3.0.0":
                    print(filename)
            except:
                os.rename(os.path.join(path, filename), os.path.join(path, file_id))


if __name__ == '__main__':
    sb3_checker()
