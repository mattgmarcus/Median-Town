#!/usr/bin/env python
import re
import urllib
import sys
import json
sys.path.append("../lib/BeautifulSoup")
from bs4 import BeautifulSoup

#Global variables
course_info_file = "../data/course_descriptions.json"
root_url = "http://dartmouth.smartcatalogiq.com"
base_url = "http://dartmouth.smartcatalogiq.com/en/2014/orc/Departments-Programs-Undergraduate/"

dept_pairs = [("AAAS", "African-and-African-American-Studies"), ("ANTH", "Anthropology"), ("ARTH", "Art-History"), ("AMES", "Asian-and-Middle-Eastern-Studies"), ("COCO", "College-Courses"), ("WPS", "War-and-Peace-Studies"), ("ECON", "Economics"), ("EDUC", "Education"), ("FILM", "Film-and-Media-Studies"), ("GEOG", "Geography"), ("GERM", "German-Studies"), ("HIST", "History"), ("HUM", "Humanities"), ("JWST", "Jewish-Studies"), ("LACS", "Latin-American-Latino-and-Caribbean-Studies"), ("MSS", "Mathematics-and-Social-Sciences"), ("PHIL", "Philosophy"), ("PSYC", "Psychological-and-Brain-Sciences"), ("REL", "Religion"), ("RUSS", "Russian-Language-and-Literature"), ("SSOC", "Social-Science"), ("SOCY", "Sociology"), ("SART", "Studio-Art"), ("THEA", "Theater"), ("TUCK", "Tuck-Undergraduate")]
special_sets = [("AMEL", "Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese", "AMEL-Asian-and-Middle-Eastern-Languages-and-LiteraturesAMELL"), ("ARAB", "Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese", "ARAB-Arabic"), ("CHIN", "Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese", "CHIN-Chinese"), ("HEBR", "Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese", "HEBR-Hebrew"), ("JAPN", "Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese", "JAPN-Japanese"), ("BIOL", "Biological-Sciences", "BIOL-Biological-Sciences-Undergraduate"), ("CHEM", "Chemistry", "CHEM-Chemistry-Undergraduate"), ("CLST", "Classics-Classical-Studies-Greek-Latin", "CLST-Classical-Studies"), ("ENGL", "English", "ENGL-English/Section-I-Non-Major-Courses"), ("ENGL", "English", "ENGL-English/Section-II-Major-Courses"), ("ENGL", "English", "ENGL-English/Section-III-Special-Topics-Courses"), ("ENGL", "English", "ENGL-English/Section-IV-Junior-Colloquia"), ("ENGL", "English", "ENGL-English/Section-V-Senior-Seminars"), ("ENGL", "English", "ENGL-English/Section-VI-Creative-Writing"), ("ENGL", "English", "ENGL-English/Section-VII-Foreign-Study-Courses"), ("ENGL", "English", "ENGL-English/Section-VIII-Independent-Study-and-Honors"), ("GRK", "Classics-Classical-Studies-Greek-Latin", "GRK-Greek"), ("LAT", "Classics-Classical-Studies-Greek-Latin", "LAT-Latin"), ("COLT", "Comparative-Literature", "COLT-Comparative-Literature-Undergraduate"), ("COSC", "Computer-Science", "COSC-Computer-Science-Undergraduate"), ("INTS", "The-John-Sloan-Dickey-Center-For-International-Understanding", "INTS-International-Studies"), ("EARS", "Earth-Sciences", "EARS-Earth-Sciences-Undergraduate"), ("ENGS", "Engineering-Sciences", "ENGS-Engineering-Sciences-Undergraduate"), ("ENVS", "Environmental-Studies-Program", "ENVS-Environmental-Studies"), ("FREN", "French-and-Italian-Languages-and-Literatures", "FREN-French"), ("FRIT", "French-and-Italian-Languages-and-Literatures", "FRIT-French-and-Italian-in-Translation"), ("ITAL", "French-and-Italian-Languages-and-Literatures", "ITAL-Italian"), ("GOVT", "Government", "GOVT-Government/Introductory-Courses"), ("GOVT", "Government", "GOVT-Government/Political-Analysis"), ("GOVT", "Government", "GOVT-Government/Upper-Level-Courses-the-Cross-Subfields"), ("GOVT", "Government", "GOVT-Government/American-Government"), ("GOVT", "Government", "GOVT-Government/Comparative-Politics"), ("GOVT", "Government", "GOVT-Government/International-Relations"), ("GOVT", "Government", "GOVT-Government/Political-Theory-and-Public-Law"), ("GOVT", "Government", "GOVT-Government/Advanced-Courses"), ("LATS", "Latin-American-Latino-and-Caribbean-Studies", "LATS-Latino-Studies"), ("COGS", "Linguistics-and-Cognitive-Science", "COGS-Cognitive-Science"), ("LING", "Linguistics-and-Cognitive-Science", "LING-Linguistics"), ("MATH", "Mathematics", "MATH-Mathematics-Undergraduate"), ("MUS", "Music", "MUS-Music-Undergraduate/Introductory-Courses"), ("MUS", "Music", "MUS-Music-Undergraduate/Theory-and-Composition"), ("MUS", "Music", "MUS-Music-Undergraduate/Music-History-Courses"), ("MUS", "Music", "MUS-Music-Undergraduate/Introductory-Courses/Performance-Courses"), ("MUS", "Music", "MUS-Music-Undergraduate/Individual-Instruction-Program-IIP"), ("MUS", "Music", "MUS-Music-Undergraduate/Foreign-Study-Courses"), ("MUS", "Music", "MUS-Music-Undergraduate/Independent-Research-Courses"), ("NAS", "Native-American-Studies-Program", "Native-American-Studies"), ("ASTR", "Physics-and-Astronomy", "ASTR-Astronomy-Undergraduate"), ("PHYS", "Physics-and-Astronomy", "PHYS-Physics-Undergraduate"), ("PBPL", "The-Nelson-A-Rockefeller-Center-for-Public-Policy/Public-Policy-Minor", "PBPL-Public-Policy"), ("SPAN", "Spanish-and-Portuguese-Languages-and-Literatures", "SPAN-Spanish"), ("PORT", "Spanish-and-Portuguese-Languages-and-Literatures", "PORT-Portuguese"), ("WGST", "Womens-and-Gender-Studies-Program", "WGST-Womens-and-Gender-Studies"), ("SPEE", "Institute-for-Writing-and-Rhetoric", "SPEE-Speech"), ("WRIT", "Institute-for-Writing-and-Rhetoric", "WRIT-Writing")]

def getDeptUrl(pair):
    if 2 == len(pair):
        return base_url + pair[1] + r"/" + pair[0] + "-" + pair[1] + r"/"
    elif 3 == len(pair): #I recognize a pair technically has 2 items
        return base_url + pair[1] + r"/" + pair[2] + r"/"
    else:
        print "What was put in?"
        return None

def makeRegex(pair):
    if 2 == len(pair):
        return r"/en/2014/orc/Departments-Programs-Undergraduate/" + pair[1] + r"/" + pair[0] + "-" + pair[1] + r"/\w+-[0-9]+-*[0-9]*"
    elif 3 == len(pair):
        return r"/en/2014/orc/Departments-Programs-Undergraduate/" + pair[1] + r"/" + pair[2] + r"/\w+-[0-9]+-*[0-9]*"
    else:
        print "What was put in?"
        return None

def getDescription(pair):
    descriptions = {}

    dept_url = getDeptUrl(pair)
    dept_page = urllib.urlopen(dept_url).read()

    regex_finder = makeRegex(pair)
    course_links = set(re.findall(regex_finder, dept_page)) #Put links into set to remove duplicates                                                                                                    

    for link in course_links:
        course_page = BeautifulSoup(urllib.urlopen(root_url + link))

        course = title = description = instructor = distrib = offered = None

        if course_page.h1:
            course = course_page.h1.span.string.encode("ascii", "ignore")
            title = " ".join(course_page.h1.contents[2].encode("ascii", "ignore").split())

        if course_page.find(class_="desc"):
            description = "".join(course_page.find(class_="desc").text.encode("ascii", "ignore").strip())

        if course_page.find(id="instructor"):
            instructor = course_page.find(id="instructor").contents[1].encode("ascii", "ignore")

        if course_page.find(id="distribution"):
            distrib = course_page.find(id="distribution").contents[1].encode("ascii", "ignore")

        if course_page.find(id="offered"):
            offered = course_page.find(id="offered").contents[1].encode("ascii", "ignore")

        descriptions[course] = {"title": title, "description": description, "instructor": instructor, "distrib": distrib, "offered": offered}

    return descriptions

def main():
    descriptions = {}

    for dept_set in special_sets:
        descriptions.update(getDescription(dept_set))

    for pair in dept_pairs:
        descriptions.update(getDescription(pair))

    with open(course_info_file, "w") as f:
        f.write(json.dumps(descriptions))


if __name__=="__main__":
    main()
