import socket
import urllib
import re

"Gathers and stores local and external IP addresses"

def get_local():
#from http://tuxbalaji.wordpress.com/2012/11/01/how-to-get-ip-address-in-python/

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    local_IP = s.getsockname()[0]

    return local_IP

def get_external():
#from http://www.pythonforbeginners.com/code-snippets-source-code/check-your-external-ip-address/

    url = "http://checkip.dyndns.org"
    request = urllib.urlopen(url).read()
    ext_IP_raw = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)
    ext_IP = ext_IP_raw[0].strip('\'').strip('[').strip(']')

    return ext_IP

#possibly explore http://alastairs-place.net/projects/netifaces/
#and http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

if __name__ == "__main__":
    local = get_local()
    external = get_external()
    print "Local IP: " + str(local) + "\nExternal IP: " + str(external)
