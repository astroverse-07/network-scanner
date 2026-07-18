import socket

def scan_port(target_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    
    try:
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"Port {port} is OPEN")
        else:
            print(f"Port {port} is CLOSED")
    except socket.timeout:
        print(f"Port {port} is FILTERED")
    finally:
        s.close()

# Test run
target = "scanme.nmap.org"
scan_port(target, 443)