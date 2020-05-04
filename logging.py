import os
import time

class logger:

	currentLogPath = ""
	maxSize = 512	# max size of log files before a new one is created, in MB

	def __init__(self, maxSize=500):
		self.currentLogPath = "{}.LOG".format(str(time.strftime('%Y%m%d-%H%M%S')))
		self.maxSize = maxSize

	def ConvertBytesToMB(self, num):
		mb = num/1000000
		return mb

	def FileSize(self, filePath):
		if os.path.isfile(filePath):
			fileInfo = os.stat(filePath)
			return self.ConvertBytesToMB(fileInfo.st_size)
		return 0

	def log(self, txt):
		if self.FileSize(self.currentLogPath) > self.maxSize:
			self.currentLogPath = "{str(time.strftime('%Y%m%d-%H%M%S'))}.LOG"

		updateText = time.strftime("%Y-%m-%d %H:%M:%S") + " >>> " + txt + "\n"
		print(updateText)

		f_Log = open(self.currentLogPath, 'a+')
		f_Log.write(updateText)
		f_Log.close()
