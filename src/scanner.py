import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial

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
    ports = range(start_port, end_port + 1)
    scan_with_target = partial(scan_port, target_ip)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_with_target, ports)

def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple TCP port scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("start_port", type=int, help="Starting port number")
    parser.add_argument("end_port", type=int, help="Ending port number")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    scan_range(args.target, args.start_port, args.end_port)