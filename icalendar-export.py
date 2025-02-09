#!/usr/bin/env python3

import sys
import json
from datetime import datetime


def parse_stdin():
    config = dict()
    json_body = ""

    is_header_section = True

    for line in sys.stdin:
        if is_header_section:
            if line == "\n":
                is_header_section = False
                continue

            key, value = line.split(": ")
            config[key] = value
        else:
            json_body += line

    intervals = json.loads(json_body)

    return config, intervals


def print_ical(intervals):
    print("BEGIN:VCALENDAR", end="\r\n")
    print("VERSION:2.0", end="\r\n")
    print("PRODID:f59afe55-e3c2-432b-a923-2d1b6bc2781c", end="\r\n")

    for interval in intervals:
        if not "end" in interval:
            continue

        print("BEGIN:VEVENT", end="\r\n")
        if "tags" in interval:
            print("SUMMARY:" + ", ".join(interval["tags"] or ""), end="\r\n")
        print("DTSTAMP:" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"), end="\r\n")
        print("DTSTART:" + interval["start"], end="\r\n")
        print("DTEND:" + interval["end"], end="\r\n")
        print("UID:" + "TIMEWARRIOR" + interval["start"], end="\r\n")
        print("CLASS:PRIVATE", end="\r\n")
        print("END:VEVENT", end="\r\n")

    print("END:VCALENDAR", end="\r\n")


if __name__ == "__main__":
    config, intervals = parse_stdin()

    print_ical(intervals)
