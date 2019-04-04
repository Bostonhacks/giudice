from giudice.projects import assign_tables_to_judges
from giudice.projects import judging_csv
from giudice.projects import sponsorship_csv


################
# PUT ALL TESTS FOR projects.py FILE HERE
################

JUDGE_ASSIGNMENTS = assign_tables_to_judges()

def run_tests():
	"""
	Run all test functions here
	"""
	test_assign_judges()
	test_repeat_assignments()
	test_judging_csv()
	test_sponsorship_csv()


def test_assign_judges():
	"""
	Test that when assigning judges, each project is seen the appropriate amount of times
	"""
	tables = [0]*93 # Make an array to count each table's appearances
	#judge_assignments = assign_tables_to_judges()
	for assignments in JUDGE_ASSIGNMENTS.values(): # assignments ex. --> {'[TRACK] The Smart Home prize': [66, 71, 76, 78], '[TRACK] Data for Urban Good Prize': [9, 12, 14, 17, 18, 35]}
		assigned_tables = assignments.values() # ex. --> [[66, 71, 76, 78], [9, 12, 14, 17, 18, 35]]
		for table_group in assigned_tables:
			for table in table_group:
				tables[table-1] += 1 # Count an appearance of a given table
	#print(tables)
	for appearances in tables:
		assert appearances % 3 == 0 # Make sure each project has been seen 3 times in each category


def test_repeat_assignments():
	#judge_assignments = assign_tables_to_judges()

	for assignments in JUDGE_ASSIGNMENTS.values():
		for jAssignments in assignments.values():
			while len(jAssignments) > 0:
				proj = jAssignments.pop(0)
				if proj in jAssignments:
					raise Exception('Duplicates found!!!!')		


def test_judging_csv():
	judging_csv()


def test_sponsorship_csv():
	sponsorship_csv()
	
