# Port Scanner

A fast, multithreaded TCP port scanner written in Python. Detects open ports, identifies services, and optionally grabs banners — all from the command line. Built as a hands-on cybersecurity and networking project.

## Features

- **Multithreaded scanning** — up to 100+ concurrent threads for fast results
- **Service detection** — identifies 20 common services (HTTP, SSH, FTP, MySQL, etc.)
- **Banner grabbing** — pulls service banners to identify software versions
- **Flexible port ranges** — scan single ports, ranges, or comma-separated lists
- **Hostname resolution** — accepts both IP addresses and domain names
- **Clean CLI output** — formatted table with port, service, banner, and timing
         
- ## Requirements
         
  - Python 3.7+
    - No external dependencies — uses only the Python standard library
             
    - ## Installation
             
      - ```bash
      git clone https://github.com/EternalCurious/port-scanner.git
      cd port-scanner
      ```

    ## Usage

    ```bash
    # Scan default ports 1-1024
    python scanner.py <target>

    # Scan a specific port range
    python scanner.py <target> -p 1-65535

    # Scan specific ports
    python scanner.py <target> -p 22,80,443,3306

    # Scan with banner grabbing enabled
    python scanner.py <target> --banner

    # Full example with all options
    python scanner.py scanme.nmap.org -p 1-1024 -t 200 --timeout 0.5 --banner
    ```

## Options

                | Flag | Description | Default |
                |------|-------------|---------|
                | `target` | Target IP address or hostname | required |
                | `-p, --ports` | Port range or list (e.g. `1-1024`, `22,80,443`) | `1-1024` |
                | `-t, --threads` | Number of concurrent threads | `100` |
                | `--timeout` | Socket timeout in seconds | `1.0` |
                | `--banner` | Enable service banner grabbing | disabled |

## Example Output

                ```
                ============================================================
                  Port Scanner  |  github.com/EternalCurious/port-scanner
                ============================================================
                  Target  : scanme.nmap.org (45.33.32.156)
                  Range   : 1 - 1024
                  Threads : 100
                  Started : 2026-06-13 14:32:01
                ============================================================

                  PORT     SERVICE          BANNER
                  --------------------------------------------------------
                  22       SSH               SSH-2.0-OpenSSH_6.6.1p1
                  80       HTTP              HTTP/1.1 200 OK

                ============================================================
                  Done in 4.83s  |  2 open port(s)
                ============================================================
                ```

  ## How It Works

1. The target hostname is resolved to an IP address
2.  All ports in the specified range are added to a thread-safe queue
3.  Worker threads pull ports from the queue and attempt TCP connections
4. Open ports are recorded with their service name and optional banner
5. Results are sorted and displayed in a formatted table                           
6. ## Legal Disclaimer
7. This tool is intended for **authorized testing only**. Only scan systems you own or have explicit permission to test. Unauthorized port scanning may be illegal.
                           
                            8. ## License
                           
                            9. MIT License — see [LICENSE](LICENSE) for details.
