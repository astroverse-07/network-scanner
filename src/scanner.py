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

def scan_range(target_ip, start_port, end_port):
    for port in range(start_port, end_port + 1):
        scan_port(target_ip, port)

# Test run
target = "scanme.nmap.org"
scan_range(target, 20, 25)