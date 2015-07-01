import os
import ConfigParser

class UrqaConfigLoader(object):
	def __init__(self, path):
		self.defaultPath = os.path.isfile(path) and path or os.path.join(os.path.dirname(__file__),'config.cfg')
		self.cfg = ConfigParser.RawConfigParser()
		self.cfg.read(self.defaultPath)

	def get_config(self, option, prefix='urqa'):
		return self.cfg.get(prefix, option)

