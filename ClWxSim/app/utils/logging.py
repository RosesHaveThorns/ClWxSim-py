import os
import time

class Logger:

	currentLogPath = ""
	maxSize = 512	# max size of log files before a new one is created, in MB

	def __init__(self, maxSize=512):
		self.currentLogPath = "{}.LOG".format(str(time.strftime('%Y%m%d-%H%M%S')))
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
		if self.fileSize(self.currentLogPath) > self.maxSize:
			self.currentLogPath = "{str(time.strftime('%Y%m%d-%H%M%S'))}.LOG"

		updateText = time.strftime("%Y-%m-%d %H:%M:%S") + " >>> " + txt + "\n"
		print(updateText)

		f_Log = open(self.currentLogPath, 'a+')
		f_Log.write(updateText)
		f_Log.close()
