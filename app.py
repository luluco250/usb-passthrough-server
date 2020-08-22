from flask import Flask, send_from_directory
from . import config
from glob import glob
from os import path
import subprocess

APP = Flask(config.APP_NAME)

DEVICES_FOLDER_PATH = path.abspath(path.join(
	APP.instance_path,
	config.DEVICES_RELATIVE_PATH))

DEVICES = glob(path.join(DEVICES_FOLDER_PATH, config.DEVICE_FILE_GLOB))

@APP.route("/")
def index():
	return send_from_directory(f"{APP.root_path}/static/html", "index.html")

@APP.route("/get-devices")
def get_devices():
	return {
		"message": "Ok",
		"devices": DEVICES
	}

@APP.route("/attach")
def attach():
	print("Attaching...")
	return call_virsh("attach-device")

@APP.route("/detach")
def detach():
	print("Detaching...")
	return call_virsh("detach-device")

def call_virsh(command: str):
	if command not in ("attach-device", "detach-device"):
		return {"message": f"Unknown command '{command}'\n"}, 400

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

		return ({
			"message":
				f"Call to virsh failed with exit code {e.returncode}\n{output}"
		}, 500)

	return {"message": "Ok"}
