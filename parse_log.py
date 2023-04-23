# Script to help run a script
import re
from Utils import get_user_from_log

# Function that parses a log represented by a string to a dictionary
def parse_ssh_log(log_string):
    # Define regex pattern
    pattern = r'^(.+)\s(\d+)\s(\d{2}:\d{2}:\d{2})\s(.+)\s(sshd)\[(\d+)\]:\s(.+)$'
    match = re.match(pattern, log_string)
    stringDate = match.group(1) + ' ' + match.group(2) + ' ' + match.group(3)
    # fullDate is a datetime object in format "1900 Jan 01 00:00:00" (year is not important)
    component = match.group(5)
    pid = match.group(6)
    message = match.group(7)
    host = get_user_from_log(message)
    namesList = ['timestamp','host','process_name','pid','message']
    valuesList = [stringDate, host, component, int(pid), message]
    return dict(zip(namesList, valuesList))