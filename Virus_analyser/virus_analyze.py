import argparse
import urllib
import urllib2
import postfile
import hashlib
import os
import json
import time
import thread
import threading
import Queue
import logging


class CounterTime(object):
	def __init__(self, samples_per_minute):
		self.samples_per_minute = samples_per_minute
		self.counter = 0
		self.lock_objetct = threading.Lock()
		self.last_time = time.time()

	def counter_incrementer(self):
		self.lock_objetct.acquire()
		counter += 1
		self.lock_objetct.release()

	def do_work(self):
		now = time.time()
		diff = now - self.last_time
		self.lock_objetct.acquire()
		if self.counter >= self.samples_per_minute:
			response = False
		else:
			response = True
		if diff >= 60:
			self.reset()
			response = True
		self.lock_objetct.release()
		return response

	def reset(self):
		self.counter = 0
		self.last_time = time.time()


class ThreadCore(threading.Thread):
	def __init__(self, stack_in, stack_out, counter, key):
		self.thread_stop = False
		self.stack_in = stack_in
		self.stack_out = stack_out
		self.counter = counter
		self.key = key
		threading.Thread.__init__(self)

	def run(self):
		while self.stack_in.empty() == False and self.thread_stop == False:
			if self.counter.do_work() == False:
				time.sleep(1)
				continue
			path = self.stack_in.get()
			host = "www.virustotal.com"
			web = "https://www.virustotal.com/vtapi/v2/file/scan"
			fields = [("apikey", self.key)]
			file_object = open(path, 'rb')
			file_read = file_object.read()
			file_object.close()
			files = [("file", str(path), path)]
			json_result = postfile.post_multipart(host, web, fields, files)
			# report
			while True:
				url = "https://www.virustotal.com/vtapi/v2/file/report"
				parameters = {"resource": hashlib.md5(path).hexdigest(),
			  		  	  	  "apikey": self.key}
				data = urllib.urlencode(parameters)
				req = urllib2.Request(url, data)
				response = urllib2.urlopen(req)
				json_result = response.read()
				if not json_result == "":
					json_res = json.loads(json_result)
				else:
					print "Wait 30 seconds."
					time.sleep(30)
					continue
				if 'Scan finished' in json_res['verbose_msg']:
					break
				else:
					print "Wait 30 second: " + json_result['verbose_msg']
					time.sleep(30)
			self.stack_out.put(json_res)

	def stop(self):
		self.thread_stop = True
		self.join()

def fill_queue(stack_in, path):
	filelist = os.listdir(path)
	for filename in filelist:
		fullpath = os.path.join(path, filename)
		if os.path.isdir(fullpath):
			fill_queue(stack_in, fullpath)
		else:
			stack_in.put(fullpath)


def main():
	terminal = argparse.ArgumentParser()
	terminal.add_argument('-f', '--file', dest='File', help="type the file", metavar='PATH', type=str)
	terminal.add_argument('-t', '--thread', dest='num_threads', help="Specify the number of the Threads", type=int)
	terminal.add_argument('-r', '--rate', dest='rate', help="Introduce the number for samples per samples_per_minute", type=int)
	terminal.add_argument('-k', '--key', dest='key', help="Introduce your apikey", type=str)
	args = terminal.parse_args()
	stack_in = Queue.Queue()
	stack_out = Queue.Queue()
	counter = CounterTime(args.rate)
	key = "b484ad3a564ba4697eca233e8f425353b9c43657fb15889ebf1bd3d8a166e7fd"
	fill_queue(stack_in, args.File)
	pool = []
	try:
		for i in xrange(args.num_threads):
			t = ThreadCore(stack_in, stack_out, counter, key)
			t.start()
			pool.append(t)
		for t in pool:
			t.join()
	except KeyboardInterrupt, SystemExit:
		for t in pool:
			t.stop()
	while True:
		try:
			path = stack_in.get()
			#hash_check = hashlib.md5(path).hexdigest()
			report = stack_out.get()
			print path, ":", "\n"
			print report['md5']
			print report['verbose_msg']
			print "Positives: ", report['positives']
			print "Total antivirus what analyzed it: ", report['total'], "\n"
		except Queue.Empty:
			break
 

if __name__ == "__main__":
	main()