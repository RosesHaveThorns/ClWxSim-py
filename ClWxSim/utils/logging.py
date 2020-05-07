import os
import time

class Logger:

	currentLogName = ""
	log_loc = ""
	maxSize = 512	# max size of log files before a new one is created, in MB

	def __init__(self, log_ID="main", maxSize=512):
		self.log_ID = log_ID
		self.currentLogName = "{}{}.LOG".format(self.log_ID, str(time.strftime('%Y%m%d-%H%M%S')))
		self.log_loc = os.path.join(os.path.dirname(__file__), self.currentLogName)
		self.maxSize = maxSize

	def convertBytesToMB(self, num):
		mb = num/1000000
		return mb

	def fileSize(self, filePath):
		if os.path.isfile(filePath):
			fileInfo = os.stat(filePath)
			return self.convertBytesToMB(fileInfo.st_size)
		return 0

	def log(self, txt):
		if self.fileSize(self.logLoc) > self.maxSize:
			self.currentLogName = "{}{}.LOG".format(self.log_ID, str(time.strftime('%Y%m%d-%H%M%S')))
			self.log_loc = os.path.join(os.path.dirname(__file__), self.currentLogName)

		updateText = time.strftime("%Y-%m-%d %H:%M:%S") + " >>> " + txt + "\n"
		print(updateText)

		f_Log = open(self.logLoc, 'a+')
		f_Log.write(updateText)
		f_Log.close()
