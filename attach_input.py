#!/usr/bin/env python3

"""
Attaches or detaches a list of devices to/from libvirt.
"""

import sys
import subprocess

VM_NAME = "win"

COMMANDS = {
    "attach": "attach-device",
    "detach": "detach-device"
}

DEVICE_XMLS = [
    "./device-mouse.xml",
    "./device-keyboard.xml"
]

def fatal(msg):
    """
    Print a message to stderr and exit with code 1.
    """

    print(msg, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        fatal("Missing command")

    virsh_command = COMMANDS.get(sys.argv[1], None)

    if virsh_command is None:
        fatal(f"Unknown command '{sys.argv[1]}'")

    for xml in DEVICE_XMLS:
        subprocess.run(
            [
                "virsh",
                "-c", "qemu:///system",
                virsh_command,
                VM_NAME,
                xml
            ],
            check=True
        )
