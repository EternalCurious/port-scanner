#!/usr/bin/env python3
"""
Port Scanner - Multithreaded TCP port scanner with service detection and banner grabbing.
Author: Ilyes Benmessaoud (EternalCurious)
Usage: python scanner.py <target> [options]
"""

import socket
import argparse
import threading
import sys
from datetime import datetime
from queue import Queue

COMMON_SERVICES = {
      21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
      80: "HTTP", 110: "POP3", 135: "MSRPC", 139: "NetBIOS", 143: "IMAP",
      443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
      5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
      8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}

print_lock = threading.Lock()
open_ports = []


def resolve_target(target):
      try:
                return socket.gethostbyname(target)
except socket.gaierror:
        print(f"[!] Could not resolve: {target}")
        sys.exit(1)


def grab_banner(ip, port, timeout):
      try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                              s.settimeout(timeout)
                              s.connect((ip, port))
                              if port in (80, 8080, 8443):
                                                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                                            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
                              return banner.split("\n")[0][:80]
      except Exception:
                return ""


def scan_port(ip, port, timeout, grab):
      try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                              s.settimeout(timeout)
                              if s.connect_ex((ip, port)) == 0:
                                                service = COMMON_SERVICES.get(port, "Unknown")
                                                banner = grab_banner(ip, port, timeout) if grab else ""
                                                with print_lock:
                                                                      open_ports.append((port, service, banner))
      except socket.error:
                pass


def worker(ip, queue, timeout, grab):
      while not queue.empty():
                port = queue.get()
                scan_port(ip, port, timeout, grab)
                queue.task_done()


def print_header(target, ip, port_range, threads):
      print("=" * 60)
      print("  Port Scanner  |  github.com/EternalCurious/port-scanner")
      print("=" * 60)
      print(f"  Target  : {target} ({ip})")
      print(f"  Range   : {port_range[0]} - {port_range[1]}")
      print(f"  Threads : {threads}")
      print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
      print("=" * 60)


def print_results(elapsed):
      if not open_ports:
                print("\n  No open ports found.")
else:
        open_ports.sort(key=lambda x: x[0])
          print(f"\n  {'PORT':<8} {'SERVICE':<16} BANNER")
        print("  " + "-" * 56)
        for port, service, banner in open_ports:
                      b = f"  {banner}" if banner else ""
                      print(f"  {port:<8} {service:<16}{b}")
              print("\n" + "=" * 60)
    print(f"  Done in {elapsed:.2f}s  |  {len(open_ports)} open port(s)")
    print("=" * 60)


def parse_ports(port_str):
      ports = []
    for part in port_str.split(","):
              part = part.strip()
              if "-" in part:
                            s, e = part.split("-")
                            ports.extend(range(int(s), int(e) + 1))
else:
            ports.append(int(part))
      return ports


def main():
      parser = argparse.ArgumentParser(
                description="Multithreaded TCP Port Scanner",
                formatter_class=argparse.RawTextHelpFormatter,
      )
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="1-1024",
                                help="Port range (default: 1-1024)\nExamples: 80, 1-65535, 22,80,443")
    parser.add_argument("-t", "--threads", type=int, default=100,
                                help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0,
                                help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("--banner", action="store_true",
                                help="Attempt to grab service banners")
    args = parser.parse_args()

    ip = resolve_target(args.target)
    ports = parse_ports(args.ports)
    print_header(args.target, ip, (min(ports), max(ports)), args.threads)

    q = Queue()
    for port in ports:
              q.put(port)

    start = datetime.now()
    num_threads = min(args.threads, len(ports))
    for _ in range(num_threads):
              threading.Thread(target=worker, args=(ip, q, args.timeout, args.banner), daemon=True).start()

    q.join()
    print_results((datetime.now() - start).total_seconds())


if __name__ == "__main__":
      main()
