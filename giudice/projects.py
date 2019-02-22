import csv
#import flask

# GLOBAL VARS
# These are constants and should NOT be changed
TOTAL_JUDGING_TIME = 90 # How many minutes long is our judging period?
TIME_PER_PROJ = 9 # How many minutes should a judge spend judging a project?
VIEWS_PER_PROJ = 3 # How many judges should view a project?
PROJS_PER_JUDGE = TOTAL_JUDGING_TIME // TIME_PER_PROJ # How many projects should each judge be responsible for?

# These are variables that will be changed and added to throughout
total_projects = 0
projects = {} # Key -> table number ; Value -> {"project":"project_name", "num_of_prizes":num, "num_judges":{category:num,cat:num...}}
# Key -> Prize name ; Value -> array of table numbers that applied for that *NON-SPONSORED* category
our_tracks = {"General":[], "[TRACK] Giving Back to Veterans Prize":[], "[TRACK] Data for Urban Good Prize":[], "[TRACK] The Smart Home prize":[]} # Non-sponsored categories
# Key -> Prize name ; Value -> array of table numbers that applied for that *SPONSORED* category
sponsor_tracks = {"Spark! Fellowship Award":[], "ITG - Best Fintech Hack":[], "[Weekly Challenge] Best Social Good Hack from Fidelity":[], "Best use of Google Cloud Platform":[], "Best use of GIPHY API":[], "Liberty Mutual  - Best Hack to Live Safe":[], "Twilio Best use of Twilio API":[], "Best use of Algolia":[], "Best Domain Name from Domain.com":[], "Best IoT Hack Using a Qualcomm Device":[], "[Weekly Challenge] Best Chat Bot using Botkit & Cisco Webex Teams":[], "Best use of HERE.com":[], "[Weekly Challenge] Best use of Clarifai\'s API":[], "[Weekly Challenge] Snap Kit Weekly Challenge":[], "[Weekly Challenge] Best Social Good Hack from Fidelity":[], "Best use of Authorize.net":[], "Bose - Most creative use of Bose SoundTouch Speaker API":[], "IBM - Best Use of IBM Cloud":[], "ITG - Best Fintech Hack":[], "OneDB - Best Use of OneDB Platform":[]} # Sponsor tracks


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
	with open("judges.txt", "r") as judges:
		for judge in judges:
			judge_assignments[judge] = {}

	count = 1
	while count <= VIEWS_PER_PROJ: # Continue assigning judges until each proj has enough views
		count += 1
		visited_tracks = {} # {track_name:bool} where bool is whether you are finished visiting it
		cur_table_index = 0

		for judge in judge_assignments.keys():
			if judge_assignments[judge] != {}:
				continue # We do not want to give judges double the load, so if they are already assigned stuff from the prev
						 # iteration of the while loop above, then skip that judge
			projects_assigned = 0

			for track in our_tracks.keys():
				cur_track = track
				if track in visited_tracks.keys() and visited_tracks[track] == True:
					continue
				visited_tracks[track] = False # Keep track of whether we have finished looking through the projects in the current track
				judge_assignments[judge][cur_track] = []

				while (projects_assigned < PROJS_PER_JUDGE) and (cur_table_index <= (len(our_tracks[cur_track])-1)):
					# Initialize the count for the number of views a project has in a category
					if cur_track not in projects[our_tracks[cur_track][cur_table_index]]["num_judges"]:
						projects[our_tracks[cur_track][cur_table_index]]["num_judges"][cur_track] = 0

					# Give a project another view if it does not have enough in a given track
					if projects[our_tracks[cur_track][cur_table_index]]["num_judges"][cur_track] <= VIEWS_PER_PROJ:
						judge_assignments[judge][cur_track].append(our_tracks[cur_track][cur_table_index])
						projects_assigned += 1
						projects[our_tracks[cur_track][cur_table_index]]["num_judges"][cur_track] += 1
						cur_table_index += 1

					 # If all of the projects in the current track have been seen once in this loop, go to the next track
					if cur_table_index > (len(our_tracks[cur_track])-1):
					 	visited_tracks[track] = True
					 	cur_table_index = 0
					 	break

				if len(judge_assignments[judge].keys()) == 1:
				  	break # We don't want to assign a judge to more than one track

				if projects_assigned >= PROJS_PER_JUDGE:
					break # We do not want to keep assigning projects to a judge that has enough, so break
	print()
	print(judge_assignments.values())
	return judge_assignments
