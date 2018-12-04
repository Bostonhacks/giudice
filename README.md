
# Giudice :black_nib:

Avoid the traffic jam that is judging through automation!


## Description :snake:

A Python Flask web application that eases the judging process at hackathons.  

* Current Features:
	* Assigns each project a table number
	* Sorts projects by category so that sponsors know what tables to go to for their categories
	* Assigns judges to each project
	* Calculates the number of judges needed based on the number of submitted projects
* Planned Features:
	* Easy way to submit Devpost CSV
	* Login to let judges judge projects directly from a mobile device or laptop and record their responses,
	  including ranking projects and taking notes on them
	* Login for admin view to see all submitted scores
	* Ability to export scoring data into a separate file


## How Judging Works at BostonHacks

Note for future contributors/users, here is how we at BostonHacks expect judging to work:

* Utilize Devpost for project submissions (this is important, as Giudice relies on Devpost data - see next section for more on this)

* Judges go to their assigned tables and give each project a score based on its unsponsored track

* We leave the judging of sponsor tracks up to those sponsors, however this app will still let the sponsors know which tables to judge for their tracks.

* In the case of a project with no given track, it will be judged solely overall.

Feel free to fork this repository and adjust Giudice according to your hackathon's own judging process!


## Using Giudice :eyes:

Giudice relies on Devpost to get its submission data.  Devpost provides a CSV file with all the necessary submission data.
You can find it for your hackathon by going to your hackathon on your hackthon's admin Devpost account, and clicking: "Manage hackathon" >> "Metrics".
From there, you can click "Generate .csv report", using the default options.  This is the CSV file you should give to Giudice.

Giudice will also need a list of your judges.  This list can be updated in the `judges.txt` file.  Enter each judge's name on a separate line.


## Running Giudice Locally :pray:

To install dependencies, run:
```bash
$ pip install -r requirements.txt
```

To run Giudice, use the following command:
```bash
$ ./scripts/run-flask.sh
```

To run tests, use the following command:
```bash
$ python -c 'from tests.main_tests import *; print test_assign_judges()'
```
Replace `main_tests` with the appropriate file name, and `test_assign_judges()` with the appropriate function.


## Contribution Guidelines :wave:

* **EVERY** pull request made on this repository must have at least one reviewer that approves it.
If the code contribution is significant (a new feature, large commits, etc.) there must be at least two approving reviewers.
If you feel your contribution is just too significant, it is okay to request a group review at a team meeting!
You can explain your changes to us, and we will discuss them in the meeting.

* This project follows Sphynx styling, and thus requires a docstring for every function.

A simple example of how to format a docstring in the Sphynx style would be:

```python
def add(x, y):
	"""
	Add two numbers together

	:param int x: a number to be added
	:param int y: a number to be added
	:return: a sum of the two inputs
	:rtype: int
	"""
	return x + y
```

Other types beyond 'int' include, but are not limited to, 'bool', 'dict' and 'str', and *must* be spelled as such.  For more on Sphynx, see [here](http://www.sphinx-doc.org/en/master/).

* For every new feature added, please update the README accordingly.

* For every new dependency added, please include it in the `requirements.txt` file on a newline.

* Commits should have descriptive messages that state not WHAT you changed, but rather WHY you changed it.  Remember: we generally know how to read your code, but we might not know why you did it!
If you feel that your code is unclear as to WHAT you changed as well, only then is it necessary to state the "what" in the commit message, or if the "why" is self-evident.
Please see the [BostonHacks code guidelines](https://github.com/Bostonhacks/guidelines) for more details on proper formatting.

* Write a test in the `tests` directory for new significant functions



