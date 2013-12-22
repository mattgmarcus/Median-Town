#!/usr/bin/env python
import sys
sys.path.append("../lib/BeautifulSoup")
from bs4 import BeautifulSoup
import urllib
import json

#Global variables
course_data_file = "../data/course_data.json"
trend_data_file = "../data/trends.json"
grade_key_dict = {"A":6, "A/A-":5.5, "A-":5, "A-/B+":4.5, "B+":4, "B+/B":3.5, "B":3, "B/B-":2.5, "B-":2, "B-/C+":1.5, "C+":1, "C+/C": 0.5, "C":0}

def isValidPage(title):
    return -1 != title.find("Median Grades")

def getAvgMedian(medians):
    #Get rid of any spaces
    medians = ["".join(median.split()) for median in medians]

    avg_median = ""
    sum_grades = 0
    num_terms = 0

    for median in medians:
        sum_grades += grade_key_dict[median]

        num_terms += 1

    sum_grades *= 1.0
    avg_grade = sum_grades / num_terms

    for pair in grade_key_dict.items():
        if pair[1] == avg_grade:
            avg_median = pair[0]

    if not avg_median:
        if 1 > avg_grade:
            avg_median = "C+/C"
        elif 2 > avg_grade:
            avg_median = "B-/C+"
        elif 3 > avg_grade:
            avg_median = "B/B-"
        elif 4 > avg_grade:
            avg_median = "B+/B"
        elif 5 > avg_grade:
            avg_median = "A-/B+"
        elif 6 > avg_grade:
            avg_median = "A/A-"
        else:
            print "Something weird happened in the median calculation"

    return avg_median

def normalizeCourseName(name):
    if None != name.p:
        name = name.p
    elif None != name.div:
        name = name.div

    name = name.string

    if -1 != name.find("-"):
        parts = name.split("-")
    
        #Get rid of any whitespace
        parts = [part.strip() for part in parts]

    else:
        #Get rid of any whitespace
        "".join(name.split())

        parts = [name[:4], name[4:7]]

    #Make sure the course number contains no extraneous zeros
    if "0" == parts[1][0]:
        if "0" == parts[1][1]:
            parts[1] = parts[1][2]
        else:
            parts[1] = parts[1][1:]

    return parts[0] + " " + parts[1]

def normalizeGrade(grade):
    if None != grade.p:
        return grade.p
    elif None != grade.div:
        return grade.div
    else:
        return grade

def normalizeSize(size):
    if None != size.p:
        return size.p
    elif None != size.div:
        return size.div
    else:
        return size

def hasCompleteInfo(course, size, grade):
    return (" " != course.replace(u"\xa0", u" ")) and (" " != size.string.replace(u"\xa0", u" ")) and (" " != grade.string.replace(u"\xa0", u" "))

def getMedians(term):
    #The key is the course name, it contains a list of the enrollment and median grade
    median_dict = {}

    url = "http://www.dartmouth.edu/~reg/transcript/medians/" + term + ".html"

    page = BeautifulSoup(urllib.urlopen(url))

    if isValidPage(page.title.string):
        raw_medians = page.table.find_all("tr")
        #print raw_medians[0].contents[1].string
        #Some tables have their first entry as the header, this gets rid of that if it does
        firstRow = raw_medians[0].contents[1]
        if None != firstRow.p:
            firstEntry = firstRow.p.string
        else:
            firstEntry = firstRow.string
        if ("Term" == firstEntry) or ("TERM" == firstEntry):
            raw_medians = raw_medians[1:]

        for median in raw_medians:
            contents = median.contents
            course_name = normalizeCourseName(contents[3])
            size = normalizeSize(contents[5])
            thisGrade = normalizeGrade(contents[7])
            if not hasCompleteInfo(course_name, size, thisGrade):
                continue

            if course_name in median_dict:
                total_enrolled = str(int(median_dict[course_name][0]) + int(size.string))
                grade = getAvgMedian([median_dict[course_name][1], thisGrade.string.strip()])
                median_dict[course_name] = [total_enrolled, grade]

            else:
                #Line below means: median_dict[course name] = [# enrolled, median]
                median_dict[course_name] = [size.string.strip(), "".join(thisGrade.string.split())]

    return median_dict

def compileMedians():
    quarters = ["F", "W", "S", "X"]
    years = ["08", "09", "10", "11", "12", "13"]
    #courses is a dictionary. The key is the course name. Its content is a list of lists, where each sublist has the term the course was, the number of students enrolled, and the median
    all_courses = {}

    for year in years:
        for quarter in quarters:
            term = year + quarter
            #08F has corrupted data so I skip it
            if "08F" == term:
                continue

            term_courses = getMedians(term)

            for course in term_courses:
                class_size = term_courses[course][0]
                median = term_courses[course][1]
               
                if course in all_courses:
                    all_courses[course].append({"term": term, "median": median, "enrollment": str(class_size)})

                else:
                    all_courses[course] = [{"term": term, "median": median, "enrollment": str(class_size)}]

    with open(course_data_file, "w") as f:
        f.write(json.dumps(all_courses))

def getTrendData():
    json_data = open(course_data_file)
    course_data = json.load(json_data)

    trend_data = {}

    for course in course_data:
        medians = course_data[course]

        num_terms = num_enrolled = 0
        median_grades = []

        for median in medians:
            num_enrolled += int(median["enrollment"])
            median_grades.append(median["median"])
            num_terms += 1

        if (0 != num_enrolled):
            avg_enrolled = num_enrolled / num_terms
            avg_median = getAvgMedian(median_grades)
            trend_data[course] = {"median": avg_median, "enrollment": str(avg_enrolled)}
            
        else:
            print "No data for this course?!?"

    with open(trend_data_file, "w") as f:
        f.write(json.dumps(trend_data))    



if __name__ == "__main__":
    compileMedians()
    getTrendData()
