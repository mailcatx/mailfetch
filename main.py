#!/usr/bin/env python3

import getpass
import pathlib
import platform
import shutil
import subprocess
import sys


def get_cpu_name():
    for line in pathlib.Path("/proc/cpuinfo").read_text().splitlines():
        if line.startswith("model name"):
            return line.split(":", 1)[1].strip()
    return "Unknown"


def get_gpu_name():
    if shutil.which("lspci") is None:
        return "lspci not found (install pciutils)"

    result = subprocess.run(
        ["lspci"],
        capture_output=True,
        text=True,
        check=True,
    )
    gpu_types = ("vga compatible controller", "3d controller", "display controller")
    for line in result.stdout.splitlines():
        if any(gpu_type in line.lower() for gpu_type in gpu_types):
            return line.rsplit(": ", 1)[-1]
    return "Unknown"


def get_os_name():
    for line in pathlib.Path("/etc/os-release").read_text().splitlines():
        if line.startswith("PRETTY_NAME="):
            return line.split("=", 1)[1].strip('"')
    return "Linux"


def get_memory_info():
    memory = {}
    for line in pathlib.Path("/proc/meminfo").read_text().splitlines():
        key, value = line.split(":", 1)
        if key in {"MemTotal", "MemAvailable"}:
            memory[key] = int(value.split()[0])

    total_mib = memory["MemTotal"] // 1024
    available_mib = memory["MemAvailable"] // 1024
    used_mib = total_mib - available_mib
    return f"{used_mib:,} MiB / {total_mib:,} MiB"


def get_uptime():
    seconds = int(float(pathlib.Path("/proc/uptime").read_text().split()[0]))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def main():
    hostname = platform.node()
    title = f"{getpass.getuser()}@{hostname}"
    rows = [
        ("OS", get_os_name()),
        ("Host", hostname),
        ("Kernel", platform.release()),
        ("Uptime", get_uptime()),
        ("CPU", get_cpu_name()),
        ("GPU", get_gpu_name()),
        ("Memory", get_memory_info()),
    ]

    label_width = max(len(label) for label, _ in rows)
    use_color = sys.stdout.isatty()
    cyan = "\033[36m" if use_color else ""
    reset = "\033[0m" if use_color else ""
    bold = "\033[1m" if use_color else ""

    print(f"{bold}{cyan}{title}{reset}")
    print(f"{cyan}{'─' * len(title)}{reset}")
    for label, value in rows:
        print(f"{cyan}{label:<{label_width}}{reset}  {value}")


if __name__ == "__main__":
    main()
