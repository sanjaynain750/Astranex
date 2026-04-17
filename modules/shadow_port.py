import socket
import concurrent.futures
from utils.logger import Logger

log = Logger("ShadowPort")

COMMON_PORTS = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except:
        pass
    return None

def scan(target, ports=None):
    if ports is None:
        ports = COMMON_PORTS
    elif isinstance(ports, str):
        if ports == "all":
            ports = range(1, 65536)
        elif "-" in ports:
            start, end = map(int, ports.split("-"))
            ports = range(start, end+1)
        else:
            ports = [int(p) for p in ports.split(",")]

    log.info(f"Scanning {target} on {len(ports)} ports...")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            result = future.result()
            if result:
                open_ports.append(result)
                log.success(f"Port {port} is open")
    return open_ports
