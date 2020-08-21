from flask import Flask
import config
from glob import glob
from os import path
import subprocess

APP = Flask(config.APP_NAME)

DEVICES_FOLDER_PATH = path.abspath(path.join(
	APP.instance_path,
	config.DEVICES_RELATIVE_PATH))

DEVICES = glob(path.join(DEVICES_FOLDER_PATH, config.DEVICE_FILE_GLOB))

@APP.route("/get-devices")
def get_devices():
	devices = "\n".join(DEVICES)
	return f"List of devices at '{DEVICES_FOLDER_PATH}':\n{devices}\n", 200

@APP.route("/attach")
def attach():
	return call_virsh("attach-device")

@APP.route("/detach")
def detach():
	return call_virsh("detach-device")

def call_virsh(command: str):
	if command not in ("attach-device", "detach-device"):
		return f"Unknown command '{command}'\n", 400

	try:
		for dev in DEVICES:
			subprocess.run(
				[
					"virsh",
					"-c", "qemu:///system",
					command,
					config.VM_NAME,
					dev
				],
				check = True,
				capture_output = True
			)
	except subprocess.CalledProcessError as e:
		output = e.output.decode("utf-8")
		if output and not output.isspace():
			output = f"Output:\n{output}\n"
		else:
			output = ""

		return (
			f"Call to virsh failed with exit code {e.returncode}\n{output}",
			500
		)

	return "Ok\n", 200
