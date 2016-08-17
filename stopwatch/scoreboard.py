#!/usr/bin/python

############################### Twisted Server ##################################
#                                                                               #
#   Simple twisted server with GET and POST endpoints.                          #
#                                                                               #
# Last Update: 3/30/2016                                                        #
#                                                                               #
#################################################################################

try:
	import sys
	import json
	import logging
	import traceback
	import exceptions
	import logging.handlers
	from os import mkdir
	from twisted.internet import reactor
	from twisted.python import log as tlog
	from twisted.application import service
	from twisted.web import resource, server
	from os.path import dirname, realpath, join, isdir
	from signal import signal, SIGTERM, SIGHUP, SIGINT
except ImportError:
	print(('\n' * 2).join(["Error importing a module:",
			'\t' + str(sys.exc_info()[1]), 'Install the module and try again.']))
	raise SystemExit(1)

port = 23456
cfgLogLevel = 'info'
scores = []

class Score:
	#Variables
	player = ""
	score = 0.0

	# score class init method
	def __init__(self, player, score):
		self.player = player
		self.score = score

	def __lt__(self, other):
		return self.score < other.score

	def getPlayer(self):
		return self.player

	def getScore(self):
		return self.score

# Class for error logging
class ErrorLog(tlog.FileLogObserver):
	def emit(self, logEntryDict):
		if not logEntryDict.get('isError'): return
		tlog.FileLogObserver.emit(self, logEntryDict)

class ErrLogService(service.Service):
	def __init__(self, logName, logDir):
		self.logName = logName
		self.logDir = logDir
		self.maxLogSize = 1048576

	def startService(self):
		# logfile is a file-like object that supports rotation
		self.logFile = logfile.LogFile(self.logName, self.logDir, rotateLength=self.maxLogSize)
		self.logFile.rotate( ) # force rotation each time restarted
		self.errlog = ErrorLog(self.logFile)
		self.errlog.start( )

	def stopService(self):
		self.errlog.stop( )
		self.logFile.close( )
		del(self.logFile)

# Function to handle a shutdown signal.
def shutdown(sigNum, frame):
	reactor.stop()
	with open('scores.csv', 'w') as saveFile:
		for s in scores:
			saveFile.write(s.getPlayer() + "," + s.getScore() + '\n')

	if log is not None:
		log.info('Server has been shut down.')
	print ""
	return

class HelloResource(resource.Resource):
	isLeaf = True

	def render_GET(self, request):
		if request.path == "/saveScore":
			player = None
			score = None
			if 'player' in request.args:
				player = request.args['player'][0]
			if 'score' in request.args:
				score = request.args['score'][0]

			temp = Score(player, score)
			scores.append(temp)
			scores.sort()

			request.responseHeaders.addRawHeader(b"content-type", b"application/json")
			request.responseHeaders.addRawHeader(b"Access-Control-Allow-Origin", b"*")
			return json.dumps({'succes': True})
		elif request.path == "/highscores":
			count = 0
			ret = ""
			for s in scores:
				t = s.getScore()
				t = str(int(float(t) / 60)) + ":" + str(float(t) % 60).zfill(4)
				ret += s.getPlayer() + " at "+ t + ","
				count += 1
				if count > 2: break

			request.responseHeaders.addRawHeader(b"content-type", b"application/json")
			request.responseHeaders.addRawHeader(b"Access-Control-Allow-Origin", b"*")
			return json.dumps({'scores': ret[:-1]})
		elif request.path == "/scoreboard":
			ret = ""
			for s in scores:
				t = s.getScore()
				t = str(int(float(t) / 60)) + ":" + str(float(t) % 60).zfill(4)
				ret += s.getPlayer() + " at "+ t + ","

			request.responseHeaders.addRawHeader(b"content-type", b"application/json")
			request.responseHeaders.addRawHeader(b"Access-Control-Allow-Origin", b"*")
			return json.dumps({'scores': ret[:-1]})
		else:
			request.setResponseCode(501)
			return ""

	def render_POST(self, request):
		if request.path == "/submit":
			foo, bar = None
			if 'foo' in request.args:
				foo = request.args['foo'][0]
			if 'bar' in request.args:
				bar = request.args['bar'][0]

			log.info("foo: " + str(foo) + "\tbar: " + str(bar))
			request.responseHeaders.addRawHeader(b"content-type", b"application/json")
			return json.dumps({'foo': foo, 'bar': bar})
		else:
			request.setResponseCode(501)
			return ""

if __name__ == '__main__':
	# Add handler to system terminate signal
	signal(SIGINT, shutdown)
	signal(SIGHUP, shutdown)
	signal(SIGTERM, shutdown)

	#----- Logging Configuration ------#
	# Logging Levels:
	#	logging.CRITICAL
	#	logging.WARNING
	#	logging.INFO
	#	logging.DEBUG

	# Logger
	if cfgLogLevel == 'critical':
		logLevel = logging.CRITICAL
	elif cfgLogLevel == 'warning':
		logLevel = logging.WARNING
	elif cfgLogLevel == 'debug':
		logLevel = logging.DEBUG
	else:
		logLevel = logging.INFO

	# To log to file instead of console, set this to False
	logToConsole = True

	# Name of log file
	installPath = dirname(realpath(__file__))
	logFile = join(installPath, 'log', 'loggin.log')
	if not isdir(join(installPath, 'log')):
		mkdir(join(installPath, 'log'))

	# Log size in Bytes
	#logSize = 1048576
	# Number of log files to keep
	#logBackupCount = 5
	# Text prior to message...which is a timestamp in this case.
	logFormat = '[%(asctime)s] - %(levelname)s - %(message)s'
	#-------------------------------#

	# Logger
	log = logging.getLogger('loggin')
	log.propagate = logToConsole
	log.setLevel(logLevel)

	# Twisted Native Logger
	#observer = tlog.PythonLoggingObserver(loggerName='loggin')
	#observer.start()

	# Create custom handler to manage rotating logs and auto log cleanup
	loggingHandler = logging.handlers.RotatingFileHandler(logFile, maxBytes=1048576, backupCount=5)
	loggingHandler.setFormatter(logging.Formatter(logFormat))
	log.addHandler(loggingHandler)

	application = service.Application("twistedServer")
	ErrLogService('loggin', join(installPath, 'log')).setServiceParent(application)

	try:
		lines = [line.rstrip('\n') for line in open('scores.csv')]
		for line in lines:
			s = line.split(',')
			temp = Score(s[0],s[1])
			scores.append(temp)

		reactor.listenTCP(port, server.Site(HelloResource()))
		log.info("Server started on port " + str(port))
		reactor.run()
	except:
		error = 'Failure: ' + str(sys.exc_info()[0])
		print error
		log.critical(error)
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
		error = ''.join('!! ' + line for line in lines)
		print error
		log.critical(error)
		exit(1)
