def sentence_analyze(context):
	packaged_results = []
	#WHEN ANSWERS
	for word in ['when', 'until', 'minutes', 'minute', 'seconds', 'second', 'days', 'day', 'week', 'weeks', 'month', 'months', 'year', 'years', 'time']:
		if word in context['sentence']:
			if context['type'] == "step":
				step = context['name']
				questions = ["how long do I " + context['name'],
								"for how long do I " + context['name'],
								"until when do I " + context['name'],
								"how long am I supposed to " + context['name'],
								"how long do I do this",
								'how long do I do this step',
								'when do I do this',
								"when do I do this step"]
				description = context['sentence']
				package = {'description' : description, 'step' : step, 'questions' : questions}
				packaged_results.append(package)
				break
	#WHERE ANSWERS
	for word in ['where', 'aim', 'edge', 'center', 'location', 'place', 'area', 'around', 'out', 'in', 'near']:
		if word in context['sentence']:
			if context['type'] == 'step':
				step = context['name']
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
								'where do I do this']
				description = context['sentence']
				package = {'description' : description, 'step' : step, 'questions' : questions}
				packaged_results.append(package)
				break
	#CAREFUL FOR ANSWERS
	for word in ['if', 'make sure']:
		if word in context['sentence']:
			if context['type'] == 'step':
				try:
					substring = context['sentence'].split(',')[0]
				except:
					try:
						substring = context['sentence'].split('if')[1]
					except:
						substring = "if"
				substring = substring.replace("you", "I")
				step = context['name']
				questions = ["what should I watch out for",
								"what happens " + substring,
								"what " + substring]
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