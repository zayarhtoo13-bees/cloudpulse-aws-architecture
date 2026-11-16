import json
import os
import shutil
import time
import urllib.request

OUT = "/var/www/html/telemetry.json"
TMP = "/var/www/html/telemetry.tmp"
IMDS = "http://169.254.169.254/latest"

def get_aws():
    m = {"id": "N/A", "type": "N/A", "az": "N/A"}
    try:
        hdr = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        req = urllib.request.Request(f"{IMDS}/api/token", method="PUT", headers=hdr)
        tok = urllib.request.urlopen(req, timeout=1).read().decode()

        h2 = {"X-aws-ec2-metadata-token": tok}
        endpoints = [
            ("id", "instance-id"),
            ("type", "instance-type"),
            ("az", "placement/availability-zone")
        ]
        for k, p in endpoints:
            r2 = urllib.request.Request(f"{IMDS}/meta-data/{p}", headers=h2)
            m[k] = urllib.request.urlopen(r2, timeout=1).read().decode()
    except Exception:
        pass
    return m

def get_linux():
    load_data = open("/proc/loadavg").read().split()
    l1 = load_data[0]
    l5 = load_data[1]

    uptime_sec = float(open("/proc/uptime").read().split()[0])
    up_mins = int(uptime_sec / 60)

    mem = {}
    for line in open("/proc/meminfo"):
        parts = line.split()
        key = parts[0].rstrip(":")
        mem[key] = int(parts[1])

    mt = round(mem["MemTotal"] / 1024, 1)
    ma = round(mem["MemAvailable"] / 1024, 1)
    mu = round(mt - ma, 1)

    tb, ub, fb = shutil.disk_usage("/")
    total_gb = round(tb / 1024 / 1024 / 1024, 1)
    used_gb = round(ub / 1024 / 1024 / 1024, 1)

    return {
        "host": os.uname().nodename,
        "kernel": os.uname().release,
        "uptime": f"{up_mins} minutes",
        "cpu": f"{l1} / {l5}",
        "ram": f"{mu} / {mt} MB",
        "disk": f"{used_gb} / {total_gb} GB"
    }

if __name__ == "__main__":
    aws = get_aws()
    while True:
        data = {
            "ts": time.strftime("%H:%M:%S UTC", time.gmtime()),
            "aws": aws,
            "sys": get_linux()
        }
        open(TMP, "w").write(json.dumps(data))
        os.replace(TMP, OUT)
        time.sleep(3)
