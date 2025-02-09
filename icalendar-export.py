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
    print("BEGIN:VCALENDAR")
    print("VERSION:2.0")
    print("PRODID:f59afe55-e3c2-432b-a923-2d1b6bc2781c")

    for interval in intervals:
        if not "end" in interval:
            continue

        print("BEGIN:VEVENT")
        if "tags" in interval:
            print("SUMMARY:" + ", ".join(interval["tags"] or ""))
        print("DTSTAMP:" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))
        print("DTSTART:" + interval["start"])
        print("DTEND:" + interval["end"])
        print("UID:" + "TIMEWARRIOR" + interval["start"])
        print("CLASS:PRIVATE")
        print("END:VEVENT")

    print("END:VCALENDAR")


if __name__ == "__main__":
    config, intervals = parse_stdin()

    print_ical(intervals)
