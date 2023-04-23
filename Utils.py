import re, sys

def get_ipv4s_from_log(log_dictionary):
    # Define regex pattern for IP addresses
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    #ip_address_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

    # Find all IP addresses in the log string
    ip_addresses = re.findall(ipv4_pattern, log_dictionary['message'])

    return ip_addresses

# Function that take a log in form of a dictionary and returns a username in its message
def get_user_from_log(log_dictionary):
    # Initialize message from fictionary
    message = log_dictionary.get("message")
    
    # If message is empty return None
    if message is None:
        return None
    
    # Define regex pattern for username
    username_pattern = r"user (\w+)"
    match = re.search(username_pattern, message)
    if match:
        return match.group(1)
    # If previous pattern didn't match try another one
    else:
        username_pattern = r"user=(\w+)"
        match = re.search(username_pattern, message)
        if match:
            return match.group(1)
        # If previous pattern didn't match try another one
        else:
            username_pattern = r"for (\w+)"
            match = re.search(username_pattern, message)
            if match:
                return match.group(1)
        
    return None

# Function that takes a message as a string and returns its type as a string
def get_message_type(message):
    # Regex patterns for different types of messages
    success_pattern = re.compile(r'accepted\s+password', re.IGNORECASE)
    fail_pattern = re.compile(r'authentication\s+failure', re.IGNORECASE)
    disconnect_pattern = re.compile(r'received\s+disconnect', re.IGNORECASE)
    password_fail_pattern = re.compile(r'failed\s+password', re.IGNORECASE)
    username_fail_pattern = re.compile(r'invalid\s+user', re.IGNORECASE)
    break_in_pattern = re.compile(r'possible\s+break-in', re.IGNORECASE)
    
    # Check for matching patterns in the message
    if success_pattern.search(message):
        return "Authentication succeeded."
    elif fail_pattern.search(message):
        return "Authentication failed."
    elif disconnect_pattern.search(message):
        return "Disconnected."
    elif password_fail_pattern.search(message):
        return "Incorrect password."
    elif username_fail_pattern.search(message):
        return "Incorrect username."
    elif break_in_pattern.search(message):
        return "Break-in attempt."
    else:
        return "Other"
    
def failedPasswordArgs(message):
    pattern1 = r'Failed\s+password\s+for\s+invalid\s+user\s+(\w+)\s+from\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+port\s+(\d+)\s+ssh2'
    pattern2 = r'Failed\s+password\s+for\s+(\w+)\s+from\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+port\s+(\d+)\s+ssh2'
    match = re.search(pattern1, message)
    if match:
        return (match.group(1),match.group(2),match.group(3))
    else:
        match = re.search(pattern2, message)
        if match:
            return (match.group(1),match.group(2),match.group(3))
        else:
            return None
        
def acceptedPasswordArgs(message):
    pattern = r'Accepted\s+password\s+for\s+(\w+)\s+from\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+port\s+(\d+)\s+ssh2'
    match = re.search(pattern, message)
    if match:
        return (match.group(1),match.group(2),match.group(3))
    else:
        return None
    
def errorArgs(message):
    pattern = r'Received\s+disconnect\s+from\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):\s+(\d+):\s+(\w+)'
    match = re.search(pattern, message)
    if match:
        return (match.group(1),match.group(2),match.group(3))
    else:
        return None