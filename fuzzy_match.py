# coding: utf-8
#follow the link: http://python.jobbole.com/81775/
#simplest  fuzzy match program

import re
collection = [ 'django_migrations.py',
'django_admin_log.py',
'main_generator.py',
'api_user.doc',
'migrations.py',
'user_group.doc',
'account.txt'
,]

def fuzzyfinder(user_input, collection):
    suggesstions=[]
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item)
        if match:
            suggesstions.append(item)
    return suggesstions


def fuzzyfinder_v2(user_input,collection):
    suggesstions = []
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item)
        if match:
            suggesstions.append((match.start(),item))
    return [x for _, x in sorted(suggesstions)]



def fuzzyfinder_v3(user_input,collection):
	suggesstions = []
	pattern = '.*'.join(user_input)
	regex = re.compile(pattern)
	for item in collection:
		match = regex.search(item)
		if match:
			suggesstions.append((len(match.group()),match.start(),item))
	return [x for _, _, x in sorted(suggesstions)]




def fuzzyfinder_v4(user_input,collection):
	suggesstions = []
	pattern = '.*?'.join(user_input)
	regex = re.compile(pattern)
	for item in collection:
		match = regex.search(item)
		if match:
			suggesstions.append((len(match.group()),match.start(),item))
	return [x for _, _, x in sorted(suggesstions)]

#v1 original implement
print fuzzyfinder('djm',collection)
print fuzzyfinder('mig',collection)

#match with rank (first match go first)
print fuzzyfinder_v2('djm',collection)
print fuzzyfinder_v2('mig',collection)

#sort by relatively
print fuzzyfinder_v3('mig',collection)

print fuzzyfinder_v4('mig',collection)
