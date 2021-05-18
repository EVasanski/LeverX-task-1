import argparse
import json
import operator
import sys
from os.path import exists

from writefile import WriteJSON, WriteXML


def parse_args():
    """ Returns arguments passed to the command line """
    parser = argparse.ArgumentParser(description='List of students living in each room.')
    parser.add_argument('students', type=str, help='Path to the students file')
    parser.add_argument('rooms', type=str, help='Path to the rooms file')
    parser.add_argument('format', type=str, help='Output format (XML or JSON)', choices=['XML', 'JSON'])
    args = parser.parse_args()
    return args


def is_file_exists(path):
    """ Checking for file existence """
    if exists(path):
        return True
    else:
        print(f'Error: the file "{path}" cannot be found.')
        sys.exit()


def reed_files(stud_file, room_file):
    """ Returns the contents of the input files """
    if is_file_exists(stud_file):
        with open(stud_file, 'r') as file:
            students = json.load(file)
    if is_file_exists(room_file):
        with open(room_file, 'r') as file:
            rooms = json.load(file)

    return students, rooms


def merge(students, rooms):
    """ Merge the list of rooms and students by room number and returns the final list """
    students = sorted(students, key=operator.itemgetter('room'))
    for student in students:
        rooms[student['room']].setdefault('students', []).append(student)
    return rooms


def main():
    args = parse_args()
    students, rooms = reed_files(args.students, args.rooms)
    data = merge(students, rooms)
    if args.format == 'JSON':
        WriteJSON().write(data)
    elif args.format == 'XML':
        WriteXML().write(data)


if __name__ == '__main__':
    main()
