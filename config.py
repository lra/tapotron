import yaml


def get(name):
	# Get the content of the yaml config file
	file = open('config.yaml')
	content = file.read()
	file.close()
	
	yaml_data = yaml.load(content)
	
	if yaml_data.get(name):
		return yaml_data.get(name)
