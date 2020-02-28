import protocol_defn_pb2

INPUT_FILE = "input.txt"
PROTO_FILE  = "result_protobuf"
PROTO_TO_TEXT_FILE = "output_protobuf.txt"

def convertPbToFile():
    START = int(round(time.time() * 1000))
    file = open(PROTO_FILE, "rb")
    records = protocol_defn_pb2.Result()
    records.ParseFromString(file.read())
    list = []
    for record in records.student:
        stringRecord = record.id + "," + record.lastname + "," + record.firstname
        if record.HasField('email'):
            stringRecord += "," + record.email
        for mark in record.marks:
            stringRecord += ":" + mark.name + "," + str(mark.score)
        list.append(stringRecord)
    file.close()
    f = open(PROTO_TO_TEXT_FILE, 'w')
    f.writelines("%s\n" % place for place in list)
    f.close()
    END = int(round(time.time() * 1000))
    global DESERIAL_TIME
    DESERIAL_TIME = END - START

def convertFileToPb():
    START = int(round(time.time() * 1000))
    records = protocol_defn_pb2.Result()
    file = open(INPUT_FILE, 'r')
    lines = file.readlines()
    count = 0
    for line in lines:
        # if count == 1:
        #     break
        lineWithOutLineBreak = line.split('\n')
        lineSplitByColon = lineWithOutLineBreak[0].split(':')
        listStudentInfo = lineSplitByColon[0].split(',')
        listStudentCourses = lineSplitByColon[1:]
        stud = records.student.add()
        stud.id         = listStudentInfo[0]
        stud.lastname   = listStudentInfo[1]
        stud.firstname  = listStudentInfo[2]
        if len(listStudentInfo) == 4:
            stud.email = listStudentInfo[3]
        for pair in listStudentCourses:
            key_value = pair.split(',')
            m = stud.marks.add()
            m.name  = key_value[0]
            m.score = int(key_value[1])
        count += 1
    file.close()
    f = open(PROTO_FILE, "wb")
    f.write(records.SerializeToString())
    f.close()

    END = int(round(time.time() * 1000))
    global SERIAL_TIME
    SERIAL_TIME = END - START

if __name__== "__main__":
    import time
    import sys

    if sys.argv[1] == 'serial':
        INPUT_FILE = sys.argv[2]
        convertFileToPb()
    elif sys.argv[1] == 'deserial':
        convertPbToFile()
    else:
        INPUT_FILE = sys.argv[2]
        convertFileToPb()
        convertPbToFile()
        TOTAL_TIME = SERIAL_TIME + DESERIAL_TIME
        print(str(SERIAL_TIME) + " " + str(DESERIAL_TIME) + " " + str(TOTAL_TIME))