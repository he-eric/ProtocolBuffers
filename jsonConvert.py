import json
import sys
import time

INPUT_FILE = "input.txt"
JSON_FILE  = "result.json"
JSON_TO_TEXT_FILE = "output_json.txt"

def convertJsonToFile():
    START = int(round(time.time() * 1000))
    list = []
    f = open(JSON_FILE, 'r')
    data = json.load(f)
    f.close()

    for record in data:
        stringRecord = record['id'] + "," + record['lastName'] + "," + record['firstName']
        if 'email' in record:
            stringRecord += "," + record['email']
        for dicts in record['CourseMarks']:
            stringRecord += ":" + dicts['CourseName'] + "," + str(dicts['CourseScore'])
        list.append(stringRecord)

    f = open(JSON_TO_TEXT_FILE, 'w')
    f.writelines("%s\n" % place for place in list)
    f.close()
    END = int(round(time.time() * 1000))
    global DESERIAL_TIME
    DESERIAL_TIME = END - START

def convertFileToJson():
    START = int(round(time.time() * 1000))
    file = open(INPUT_FILE, 'r')
    lines = file.readlines()
    count = 0
    recordList = []
    for line in lines:
        lineWithOutLineBreak = line.split('\n')
        lineSplitByColon     = lineWithOutLineBreak[0].split(':')
        listStudentInfo      = lineSplitByColon[0].split(',')
        listStudentCourses   = lineSplitByColon[1:]
        #print(listStudentCourses)
        #print(listStudentInfo)

        dict = {}
        dict['lastName'] = listStudentInfo[1]
        #if len(listStudentInfo) != 2:
        dict['firstName'] = listStudentInfo[2]
        arrayOfDicts = []

        for pair in listStudentCourses:
            key_value = pair.split(',')
            sub_dict = {}
            sub_dict['CourseScore'] = int(key_value[1])
            sub_dict['CourseName']  = key_value[0]
            arrayOfDicts.append(sub_dict)
            #print(sub_dict)
        #print(arrayOfDicts)

        dict['CourseMarks'] = arrayOfDicts
        dict['id'] = listStudentInfo[0]
        if len(listStudentInfo) == 4:
            dict['email'] = listStudentInfo[3]
        #print(dict)
        recordList.append(dict)
        #count += 1
    file.close()

    outfile = open(JSON_FILE, 'w')
    json.dump(recordList, outfile, indent=2)
    outfile.close()

    END = int(round(time.time() * 1000))
    global SERIAL_TIME
    SERIAL_TIME = END - START


if __name__== "__main__":

    if sys.argv[1] == 'serial':
        INPUT_FILE = sys.argv[2]
        with open(JSON_FILE, 'w') as outfile:
            json.dump(convertFileToJson(), outfile, indent=2)
    elif sys.argv[1] == 'deserial':
        convertJsonToFile()
    else:
        INPUT_FILE = sys.argv[2]
        convertFileToJson()
        convertJsonToFile()
        TOTAL_TIME = SERIAL_TIME + DESERIAL_TIME
        print(str(SERIAL_TIME) + " " + str(DESERIAL_TIME) + " " + str(TOTAL_TIME))
