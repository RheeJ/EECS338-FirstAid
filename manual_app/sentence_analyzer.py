from question_parser import *
from PyDictionary import PyDictionary

def sentence_analyze(context):
	packaged_results = []
	#WHEN ANSWERS
	for word in ['when', 'until', 'minutes', 'minute', 'seconds', 'second', 'days', 'day', 'week', 'weeks', 'month', 'months', 'year', 'years', 'time']:
		if word in context['sentence']:
			if context['type'] == "step":
				step = context['name']
				POS_words = parseOnlineStanford(context['sentence'])
				new_string = ""
				flag = False
				for word in POS_words:
					if word[1] == "VB":
						flag = True
						new_string = word[0]
					elif flag == True:
						new_string = new_string + " " + word[0]
						if word[1] == "NN" or word[1] == "NNS":
							flag == False
							break
					else:
						pass
				questions = ["how long do I " + context['name'],
								"for how long do I " + context['name'],
								"until when do I " + context['name'],
								"how long am I supposed to " + context['name'],
								"how long do I do this",
								'how long do I do this step',
								'when do I do this',
								"when do I do this step"]
				if new_string != "":
					strings = synonymizer(new_string)
					for string in strings:
						questions.extend(("how long do I " + string,
									"for how long do I " + string,
									"until when do I " + string,
									"how long am I supposed to " + string))
				description = context['sentence']
				package = {'description' : description, 'step' : step, 'questions' : questions}
				packaged_results.append(package)
				break
	#WHERE ANSWERS
	for word in ['where', 'aim', 'edge', 'center', 'location', 'place', 'area', 'around', 'out', 'in', 'near']:
		if word in context['sentence']:
			if context['type'] == 'step':
				step = context['name']
				POS_words = parseOnlineStanford(context['sentence'])
				new_string = ""
				flag = False
				for word in POS_words:
					if word[1] == "VB":
						flag = True
						new_string = word[0]
					elif flag == True:
						new_string = new_string + " " + word[0]
						if word[1] == "NN" or word[1] == "NNS":
							flag == False
							break
					else:
						pass
				questions = ["where do I " + context['name'],
								"around where do I " + context['name'],
								"where should I " + context['name'],
								"where can I " + context['name'],
								"where could I " + context['name'],
								'where is the place to ' + context['name'],
								'what is the place to ' + context['name'],
								'where is the location to ' + context['name'],
								'what is the location to ' + context['name'],
								'where is the area to ' + context['name'],
								'what is the area to ' + context['name'],
								'where do I do this',
								'where do I do this step']
				if new_string != "":
					strings = synonymizer(new_string)
					for string in strings:
						questions.extend(("where do I " + new_string,
									"around where do I " + new_string,
									"where should I " + new_string,
									"where can I " + new_string,
									"where could I " + new_string,
									'where is the place to ' + new_string,
									'what is the place to ' + new_string,
									'where is the location to ' + new_string,
									'what is the location to ' + new_string,
									'where is the area to ' + new_string,
									'what is the area to ' + new_string))
				description = context['sentence']
				package = {'description' : description, 'step' : step, 'questions' : questions}
				packaged_results.append(package)
				break
	#CAREFUL FOR ANSWERS
	for word in ['if', 'make sure']:
		if word in context['sentence']:
			if context['type'] == 'step' or context['type'] == 'warning':
				try:
					substring = context['sentence'].split('if')[1]
					substring = 'if' + substring
					try:
						substring = substring.split(',')[0]
					except:
						pass
				except:
					substring = "if"
				substring = substring.replace("you", "I")
				ns = substring.replace("Ir", "")
				step = context['name']
				questions = ["what should I watch out for",
								"what if there is an issue"]
				if substring != "if":
					strings = synonymizer(substring)
					for string in strings:
						questions.extend(("what happens " + substring,
											"what " + substring,
											"what happens " + ns,
											"what " + ns))
				description = context['sentence']
				package = {'description' : description, 'step' : step, 'questions' : questions}
				packaged_results.append(package)
				break
	#SYMPTOMS ANSWERS
	for word in ['sign', 'signs', 'symptoms']:
		if word in context['sentence']:
			terms = context['sentence'].split(' ')
			flag = False
			keyword = ""
			for term in terms:
				if flag == True:
					keyword = term
					break
				if term == "of":
					flag = True
			if keyword != "":
				questions = ["what are the signs of " + keyword]
				description = context['sentence']
				package = {'description' : description, 'step' : step, 'questions' : questions}
				packaged_results.append(package)
				break
	#DETAILS ANSWERS
	step = context['name']
	questions = ["what are the details for this step",
					"can I have more details",
					"what else",
					"what else should I know",
					"what more",
					"why"]
	description = context['sentence']
	package = {'description' : description, 'step' : step, 'questions' : questions}
	packaged_results.append(package)
	return packaged_results

def synonymizer(string):
	return [string]