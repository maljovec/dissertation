import sys
import re
import glob
from collections import Counter

# files = glob.glob(sys.argv[1])

skipList = []

words = []
phrases = {1:[],2:[],3:[],4:[],5:[]}

print('Files Checked:')
for filename in sys.argv[1:]:
	if filename in skipList:
		continue

	print('\t'+filename)
	with open(filename, 'r') as fin:
	    content = fin.read()

	## Chew up new lines replacing them with spaces and also remove comments
	lines = content.split('\n')
	content = ''
	sep = ''
	for line in lines:
		lineWithComment = line.split('%')[0]
		if len(lineWithComment):
			content += sep + lineWithComment
			sep = ' '

	## Replace latex newlines with spaces
	content = content.replace('\\\\', ' ')

	## Remove punctuation for our needs, this can lead to potentially misleading
	## results since it will potentially put ends of sentences together with
	## beginnings of sentences for phrases, but I care less about false positives,
	## and would prefer to err on the side of reporting too much, remember the job
	## is to make the writing more distinct.
	punctuation = '\.|!|`|,|\?|;|:|\"|\'|\(|\)'
	content = re.sub(punctuation, ' ', content)

	## Make all of the opening and closing brackets their own token for easing the
	## handling later
	content = re.sub('\{', ' { ', content)
	content = re.sub('\}', ' } ', content)
	content = re.sub('\[', ' [ ', content)
	content = re.sub('\]', ' ] ', content)

	## Let us begin the counting
	tokens = re.split('~| ', content)

	## Are we currently inside a command? If so, then ignore everything until we are
	## back at the base level
	insideCommand = 0

	## Are we currently inside a command? If so, then ignore everything until we are
	## back at the base level
	insideBracket = 0

	for i in range(len(tokens)):
		token = tokens[i]
		if not len(token):
			continue

		if token in '{}[]':
			if token == '{':
				insideCommand += 1
			elif token == '}':
				insideCommand -= 1
				if insideCommand < 0:
					print('Error where text resembles: '+' '.join(tokens[(i-5):(i+5)]))
			elif token == '[':
				insideBracket += 1
			else:
				insideBracket -= 1
				if insideBracket < 0:
					print('Error where text resembles: '+' '.join(tokens[(i-5):(i+5)]))
		elif token.startswith('\\'):
			pass
		else:
			if not (insideCommand+insideBracket):
				words.append(token.lower())
			else:
				pass

## Again can cause potentially misleading results since file order is not
## specified, and we will group words together that are from different files,
## but the goal is to identify repeated phrases, if these so happen to generate
## real phrases, then it will not hurt to show them. More likely, they will
## create non-sense phrases that will be filtered out when we look at the
## highest frequency occurences. Basically, not worth the effort to do
## it correctly.
for count in phrases.keys():
	for i in range(len(words)-count):
		phrases[count].append(' '.join(words[i:(i+count)]))

rankLimit = 20

print('\nTotal word count: %d' % len(words))
for count,phraseC in phrases.items():
	commonCounts = Counter(phraseC).most_common(rankLimit)
	print('\n%d most common %d-word phrases:' % (rankLimit,count))
	for key,val in commonCounts:
		print('\t%s: %d' % (key,val))