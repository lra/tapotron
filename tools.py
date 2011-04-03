import os


# Are we on the dev server?
# Returns True if we are
def on_dev_server():
	return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
