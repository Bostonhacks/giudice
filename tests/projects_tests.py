from giudice.projects import assign_tables_to_judges

################
# PUT ALL TESTS FOR projects.py FILE HERE
################

def run_tests():
	"""
	Run all test functions here
	"""
	test_assign_judges()

def test_assign_judges():
	"""
	Test that when assigning judges, each project is seen the appropriate amount of times
	"""
	tables = [0]*93 # Make an array to count each table's appearances
	judge_assignments = assign_tables_to_judges()
	for assignments in judge_assignments.values(): # assignments ex. --> {'[TRACK] The Smart Home prize': [66, 71, 76, 78], '[TRACK] Data for Urban Good Prize': [9, 12, 14, 17, 18, 35]}
		assigned_tables = assignments.values() # ex. --> [[66, 71, 76, 78], [9, 12, 14, 17, 18, 35]]
		for table_group in assigned_tables:
			for table in table_group:
				tables[table-1] += 1 # Count an appearance of a given table
	#print(tables)
	for appearances in tables:
		assert appearances % 3 == 0 # Make sure each project has been seen 3 times in each category
