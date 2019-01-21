from tweet_parser.tweet import Tweet
from tweet_parser.tweet_parser_errors import NotATweetError
import fileinput
import json
import sys
class twitter_parser:
	def __init__(self,file_name):
		self.file=file_name

	def parse(self):
		for line in fileinput.FileInput(self.file):
			try:
				tweet_dict = json.loads(line)
				tweet = Tweet(tweet_dict)
			except Exception as ex:
				pass
			print(tweet.all_text)


obj=twitter_parser(sys.argv[1])
obj.parse()
#"exp.json"
