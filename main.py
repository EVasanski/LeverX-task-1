import argparse
import json
import sys

from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


def parse():
    """ Returns arguments passed to the command line """
    parser = argparse.ArgumentParser(description='List of students living in each room.')
    parser.add_argument('students', type=str, help='Path to the students file')
    parser.add_argument('rooms', type=str, help='Path to the rooms file')
    parser.add_argument('format', type=str, help='Output format (XML or JSON)', choices=['XML', 'JSON'])
    args = parser.parse_args()
    return args


def reed_files(stud_file, room_file):
    """ Returns the contents of the input files """
    try:
        with open(stud_file, 'r') as file:
            students = json.load(file)
        with open(room_file, 'r') as file:
            rooms = json.load(file)
        return students, rooms
    except FileNotFoundError:
        print('Error: the file cannot be found.')
        sys.exit()


def merge(students, rooms):
    """ Merge the list of rooms and students by room number and returns the final list """
    students = sorted(students, key=lambda x: x['room'])
    room_num = 0
    for student in students:
        if student['room'] == room_num:
            rooms[room_num].setdefault('students', []).append(student)
        else:
            room_num += 1
            rooms[room_num].setdefault('students', []).append(student)
    return rooms


def write_file(data, extension):
    """ Writes the final list to a file, depending on the extension """
    if extension == 'JSON':
        with open('result.json', 'w') as file:
            json.dump(data, file, indent=3)
    elif extension == 'XML':
        with open('result.xml', 'w') as file:
            parsed = parseString(dicttoxml(data))
            file.write(parsed.toprettyxml(indent=' ' * 3))


def main():
    args = parse()
    students, rooms = reed_files(args.students, args.rooms)
    data = merge(students, rooms)
    write_file(data, args.format)


if __name__ == '__main__':
    main()
