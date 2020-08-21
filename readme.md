This is an utility Flask application I made for personal use to help with
attaching and detaching USB devices to and from a libvirt virtual machine.

I share it here as backup and in case it proves useful to someone.

To use, place libvirt device XML files into a "devices" folder in the Flask
instance folder and call "attach", "detach" or "get-devices" using
curl/wget/etc.
