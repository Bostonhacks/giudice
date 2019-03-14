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
sponsor_tracks = {"Spark! Fellowship Award":[], "ITG - Best Fintech Hack":[], "[Weekly Challenge] Best Social Good Hack from Fidelity":[], "Best use of Google Cloud Platform":[], "Best use of GIPHY API":[], "Liberty Mutual  - Best Hack to Live Safe":[], "Twilio Best use of Twilio API":[], "Best use of Algolia":[], "Best Domain Name from Domain.com":[], "Best IoT Hack Using a Qualcomm Device":[], "[Weekly Challenge] Best Chat Bot using Botkit & Cisco Webex Teams":[], "Best use of HERE.com":[], "[Weekly Challenge] Best use of Clarifai\'s API":[], "[Weekly Challenge] Snap Kit Weekly Challenge":[], "[Weekly Challenge] Best Social Good Hack from Fidelity":[], "Best use of Authorize.net":[], "Bose - Most creative use of Bose SoundTouch Speaker API":[], "IBM - Best Use of IBM Cloud":[], "ITG - Best Fintech Hack":[], "OneDB - Best Use of OneDB Platform":[]} # Sponsor tracks
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
	judge_assignments = {}
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
	Assign judges to projects in a single, specified track

	:param str track: name of the track we want judges for
	:param list judges: a list of the judges allocated for this track
	:return: a dictionary with the keys as judge names and values as an array of project numbers
	:rtype: dict
	"""
	track_projects = our_tracks[track]
	total_views = len(track_projects) * 3
	assignments = {} # The final result, with the keys as judge names and values as an array of project numbers
	project_views = []
	count = 0

	# Set up arrays
	for judge in judges:
		assignments[judge] = []
	for project in track_projects:
		# project_views[project] = 0
		for i in range(VIEWS_PER_PROJ):
			project_views.append(project)

	edge = False
	# Add projects to a judges array
	random_proj = random.choice(project_views)
	for judge in judges:
		for i in range(PROJS_PER_JUDGE):
			# keep choosing a new random project until it has not yet been seen by this judge
			while count != total_views:
				random_proj = random.choice(project_views)
				if random_proj not in assignments[judge]:
					break
				# Random edge case handled below (this edge case happens when all of the last few projects left unassigned is already seen by the last judge)
				# PLEASE dont touch anythign in this if clause unless you 100% understand this case
				if len(project_views) < PROJS_PER_JUDGE:
					if all(elem in assignments[judge] for elem in project_views):
						edge = True
						for i in range(len(project_views)):
							for judge2 in judges:
								if project_views[i] not in assignments[judge2]:
									assignments[judge2].append(project_views[i])
									break 
						break
			if edge:
				break
			assignments[judge].append(random_proj)
			project_views.remove(random_proj)
			count += 1
			if count == total_views:
				break
		if count == total_views or edge:
			break

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
