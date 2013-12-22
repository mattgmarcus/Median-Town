#!/usr/bin/env python
import sys
import json
sys.path.append("../lib/BeautifulSoup")
from bs4 import BeautifulSoup

#Global variables
raw_course_info_file = "../data/raw_course_descriptions.json"
usable_course_info_file = "../data/usable_course_descriptions.json"

def translateInfoFiles():
    data = json.load(open(raw_course_info_file))["courses"]

    info = {}

    for course in data:
        name = course["subject"].encode("ascii") + " " + course["number"].encode("ascii")

        dirty_description = course["description"].encode("ascii", "ignore")
        soup = BeautifulSoup(dirty_description).get_text()
        clean_description = "".join(line.strip() for line in soup.split("\n"))

        info[name] = {"title": course["title"].encode("ascii", "ignore"), "description": clean_description.encode("ascii", "ignore")}


        with open(usable_course_info_file, "w") as f:
            f.write(json.dumps(info))

if __name__=="__main__":
    translateInfoFiles()
