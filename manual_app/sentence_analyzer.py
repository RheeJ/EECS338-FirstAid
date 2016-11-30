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
	for word in ['where', 'aim', 'edge', 'center', 'location', 'place', 'area', 'around', 'out', 'in']:
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
				packaged_results.append(package)
				break
	return packaged_results