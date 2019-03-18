import csv
import random

# GLOBAL VARS
# These are constants and should NOT be changed
TOTAL_JUDGING_TIME = 90 # How many minutes long is our judging period?
TIME_PER_PROJ = 9 # How many minutes should a judge spend judging a project?
VIEWS_PER_PROJ = 3 # How many judges should view a project?
PROJS_PER_JUDGE = TOTAL_JUDGING_TIME // TIME_PER_PROJ # How many projects should each judge be responsible for?

# These are variables that will be changed and added to throughout
total_projects = 0
num_judgements = 0
projects = {} # Key -> table number ; Value -> {"project":"project_name", "num_of_prizes":num, "num_judges":{category:num,cat:num...}}
# Key -> Prize name ; Value -> array of table numbers that applied for that *NON-SPONSORED* category
our_tracks = {"General":[], "[TRACK] Giving Back to Veterans Prize":[], "[TRACK] Data for Urban Good Prize":[], "[TRACK] The Smart Home prize":[]} # Non-sponsored categories
# Key -> Prize name ; Value -> array of table numbers that applied for that *SPONSORED* category
sponsor_tracks = {"Spark! Fellowship Award":[], "ITG - Best Fintech Hack":[], "[Weekly Challenge] Best Social Good Hack from Fidelity":[], "Best use of Google Cloud Platform":[], 
					"Best use of GIPHY API":[], "Liberty Mutual  - Best Hack to Live Safe":[], "Twilio Best use of Twilio API":[], "Best use of Algolia":[], "Best Domain Name from Domain.com":[], 
					"Best IoT Hack Using a Qualcomm Device":[], "[Weekly Challenge] Best Chat Bot using Botkit & Cisco Webex Teams":[], "Best use of HERE.com":[], 
					"[Weekly Challenge] Best use of Clarifai\'s API":[], "[Weekly Challenge] Snap Kit Weekly Challenge":[], "[Weekly Challenge] Best Social Good Hack from Fidelity":[], "Best use of Authorize.net":[], 
					"Bose - Most creative use of Bose SoundTouch Speaker API":[], "IBM - Best Use of IBM Cloud":[], "ITG - Best Fintech Hack":[], "OneDB - Best Use of OneDB Platform":[]} # Sponsor tracks
track_judges = {} # The judges assigned to each track; where the key is the track and the value is an arr of judges

def process_csv():
	"""
	Process the CSV for project info from DevPost

	:return: a dictionary of each table number as a key and the project info as a value
	:rtype: dict
	"""
	# Process the CSV file that contains submissions data from Devpost by assigning tables and recording what prizes a project was entered for
	with open("submissions.csv") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		table_number = 0
		for row in csv_reader:
			if table_number == 0:
				table_number += 1
			else:
				# Add a project name to the dictionary with a table number
				projects[table_number] = {"project":row[0], "num_of_our_prizes":1, "num_judges":{}} 
				# num_of_prizes is 1 by default bc they are entered for general prize
				# Enter into General category by default
				our_tracks["General"].append(table_number)
				projects[table_number]["num_judges"]["General"] = 0
				desired_prizes = row[6].split(", ")

				# Submit table number for entry for each prize they entered for on Devpost
				for prize in desired_prizes:
					if prize in our_tracks.keys():
						projects[table_number]["num_of_our_prizes"] += 1
						our_tracks[prize].append(table_number)
						projects[table_number]["num_judges"][prize] = 0
					elif prize in sponsor_tracks.keys():
						sponsor_tracks[prize].append(table_number)
				table_number += 1
		total_projects = table_number - 1
		print("Processed {0} projects.".format(total_projects))
		#print(our_tracks)
	return projects


def assign_tables_to_judges():
	"""
	Assign tables to judges

	:return: Key -> judge name ; Value -> {"category":[tables], "category": [tables]...}
	:rtype: dict
	"""
	process_csv()
	judge_assignments = {} # For each track, contains a dictionary w/ keys as judge names and vals as projects assigned
	judges = [] 
	with open("judges.txt", "r") as judges_txt:
		for judge in judges_txt:
			# judge_assignments[judge] = {}
			judges.append(judge)

	# Get num of judges needed for each track (both for loops are intended for this)
	num_track_judges = {} # The number of judges that should be assigned to each track
	for track in our_tracks.keys():
		num_track_judges[track] = num_judges_for_track(track)
	slice_beginning = 0
	slice_end = 0 # Index of the current judge
	for track in num_track_judges.keys():
		slice_end += num_track_judges[track]
		track_judges[track] = judges[slice_beginning:slice_end]
		slice_beginning = slice_end

	# Assign projects to each judge
	for track in track_judges.keys():
		judge_assignments[track] = assign_judges_to_track(track, track_judges[track])

	return judge_assignments


def assign_judges_to_track(track, judges):
	"""
	Assign judges to projects in a single, specified track with all the projects they will be looking at

	:param str track: name of the track we want judges for
	:param list judges: a list of the judges allocated for this track
	:return: a dictionary with the keys as judge names and values as an array of project numbers
	:rtype: dict
	"""
	track_projects = our_tracks[track]
	total_views = len(track_projects) * 3
	assignments = {} # The final result, with the keys as judge names and values as an array of project numbers
	project_views = [] # The total pool of projects that can be assigned to judges
	judge_idx = 0  # used to loop through all the available judges as we assign projects
	count = 0  # reused throughout
	edge = False # if we hit the edge case where all the projects left to be assigned are already assigned to the last judge
	edge_idx = len(judges) - 1  

	# Set up arrays
	for judge in judges:
		assignments[judge] = []
	for project in track_projects:
		# project_views[project] = 0
		for i in range(VIEWS_PER_PROJ):
			project_views.append(project)


	# if there are less than 5 judges, there will be suffient overlap since each project will be seen with every other project at least once
	if len(judges) < 6:  
		for project in project_views:
			assignments[judges[judge_idx]].append(project)
	
			judge_idx = (judge_idx + 1) % len(judges) # updates the judge index; reset once the last judge is reached
	
		return assignments


	# at least 6 judges; Add projects to a judge's array
	while len(project_views) > 0:  # while there are still projects left to be assigned
		random_proj = random.choice(project_views)
		count += 1 # for edge test

		if random_proj in assignments[judges[judge_idx]]: # if this judge already has this project assigned to them
			if count > len(project_views) + 2: # if we have tried len(project_views)+1 number of random projects, we are probably at the edge case
				edge = True
				break  # break to go to the edge case
			else:
				continue # if not at the edge, keep trying to get a new project

		# we now have a new project and can add it to this judge's assignments
		assignments[judges[judge_idx]].append(random_proj)
		project_views.remove(random_proj)
		count = 0

		judge_idx = (judge_idx + 1) % len(judges) # updates the judge index; reset once the last judge is reached


 	# we can assume that all the projects left to be assigned have already been assigned to this last judge
	if edge:
		count = 0  # used to sequentially step through the array of judges from index 0
		jLen = len(assignments[judges[count]]) # goal length of assignments

		while edge_idx != judge_idx-1:  # keeps going until we get to the judge we terminated the previous loop at, edge_idx starts at the last judge 
			random_proj = random.choice(assignments[judges[count]]) 

			if random_proj not in assignments[judges[edge_idx]]: 
				assignments[judges[edge_idx]].append(random_proj)
				assignments[judges[count]].remove(random_proj)
				count += 1 # next sequential judge

				edge_idx -= 1 
	

	# if there are still unassigned projects left
	if len(project_views) > 0: 
		edge_idx = 0 # sequentially step through the first judges to add the unassigned ones to them

		for project in project_views:
			assignments[judges[edge_idx]].append(project)
			edge_idx = (edge_idx + 1) % len(judges)

	return assignments


def num_judges_for_track(track):
        """
        Calculate the number of judges necessary for a given track

        :param str track: name of the track we wanna get the num judges for
        :return: number of judges we're gonna need for a specific track
        :rtype: int
        """
        proj_array = our_tracks[track]
        num_proj = len(proj_array)
        if (num_proj *VIEWS_PER_PROJ%PROJS_PER_JUDGE != 0):
        	return (num_proj *VIEWS_PER_PROJ//PROJS_PER_JUDGE) + 1
        else:
        	return num_proj *VIEWS_PER_PROJ//PROJS_PER_JUDGE


def num_judges():
        """
        Calculate the number of judges necessary given the number of projects that have been submitted

        :return: number of judges that we're gonna need
        :rtype: int
        """
        for x in our_tracks.keys():
        	num_judgements += len(our_tracks[x])
        if (num_judgements *VIEWS_PER_PROJ%PROJS_PER_JUDGE != 0):
        	return (num_judgements *VIEWS_PER_PROJ//PROJS_PER_JUDGE) + 1
        else:
        	return num_judgements *VIEWS_PER_PROJ//PROJS_PER_JUDGE        


def get_judge_assignments(judge_name):
	"""
	Get a dictionary of the projects assigned to a particular judge that has the project names and tables

	:param str judge_name: the name of the judge
	:return: the project names and tables assigned to the input judge
	:rtype: dict
	"""
	assignments = assign_tables_to_judges()
	assignments_values = assignments.values()
	assignment = []
	for value_group in assignments_values:
		for judge in value_group:
			if judge == judge_name:
				assignment = value_group[judge]
	proj_numbers = assignment
	result = {}
	for proj_num in proj_numbers:
		proj_name = projects[proj_num]["project"]
		result[proj_num] = proj_name
	return result


# def get_judge_categories(judge_name):
# 	"""
# 	Get the categories that a given judge is judging projects for

# 	:param str judge_name: the name of the judge
# 	:return: the name of the categories the judge is judging for
# 	:rtype: list
# 	"""
# 	judge_track = ''
# 	assignments = assign_tables_to_judges()
# 	for key in assignments.keys():
# 		for judge_key in assignments[key].keys()
# 			if 

# 	return judge_track

