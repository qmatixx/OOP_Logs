
# class SSHLogEntry(metaclass=abc.ABCMeta):

#     @abc.abstractclassmethod
#     def validate():

        
#     # To string method
#     def __str__(self):
#         return f"{self.timestamp} {self.host} {self.process_name}[{self.pid}]: {self.message}"

            
#     # Method that returns the IP address from its message and None if there is no IP address
#     def get_ipv4(self):
#         # Znalazłem taki regex śmieszny w necie, ale nie wiem jak działa XD
#         pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
#         match = re.search(pattern, self.message)
#         if match:
#             return ipaddress.IPv4Address(match.group(0))
#         else:
#             return None