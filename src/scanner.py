import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial

def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: Could not resolve hostname '{target}'. Please check the target and try again.")
        exit(1)

def scan_port(target_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    
    try:
        result = s.connect_ex((target_ip, port))
        if result == 0:
            banner = grab_banner(s)
            if banner:
                print(f"Port {port} is OPEN | Banner: {banner}")
            else:
                print(f"Port {port} is OPEN | No Banner received")
        else:
            print(f"Port {port} is CLOSED")
    except socket.timeout:
        print(f"Port {port} is FILTERED")
    finally:
        s.close()

def grab_banner(s):
    try:
        s.settimeout(1)
        banner = s.recv(1024)
        return banner.decode(errors="ignore").strip()
    except socket.timeout:
        return None

def scan_range(target_ip, start_port, end_port):
    ports = range(start_port, end_port + 1)
    scan_with_target = partial(scan_port, target_ip)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_with_target, ports)

def valid_port(value):
    port = int(value)
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError(f"{value} is not a valid port (must be 1-65535)")
    return port

def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple TCP port scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("start_port", type=valid_port, help="Starting port number")
    parser.add_argument("end_port", type=valid_port, help="Ending port number")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.start_port > args.end_port:
        print("Error: start_port cannot be greater than end_port.")
        exit(1)
    
    target_ip = resolve_target(args.target)
    scan_range(target_ip, args.start_port, args.end_port)