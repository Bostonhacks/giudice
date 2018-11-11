const csvFilePath='./submissions.csv';
const csv=require('csvtojson');

const TOTAL_JUDGING_TIME = 90; // How many minutes long is our judging period?
const TIME_PER_PROJ = 9; // How many minutes should a judge spend judging a project?
const VIEWS_PER_PROJ = 3; // How many judges should view a project?

const PROJS_PER_JUDGE = TOTAL_JUDGING_TIME / TIME_PER_PROJ;

// These are the tracks/categories that we do not want to assign judges to, such as sponsor tracks
// TODO: populate this list in the front end, probably in a checklist
const FILTERED_LIST = ['Spark! Fellowship Award', 'ITG - Best Fintech Hack', '[Weekly Challenge] Best Social Good Hack from Fidelity', 'Best use of Google Cloud Platform', 'Best use of GIPHY API', 'Liberty Mutual  - Best Hack to Live Safe', 'Twilio — Best use of Twilio API', 'Best use of Algolia', 'Best Domain Name from Domain.com', 'Best IoT Hack Using a Qualcomm Device', '[Weekly Challenge] Best Chat Bot using Botkit & Cisco Webex Teams', 'Best use of HERE.com', '[Weekly Challenge] Best use of Clarifai\'s API', '[Weekly Challenge] Snap Kit Weekly Challenge', '[Weekly Challenge] Best Social Good Hack from Fidelity', 'Best use of Authorize.net', 'Bose - Most creative use of Bose SoundTouch Speaker API', 'IBM - Best Use of IBM Cloud', 'ITG - Best Fintech Hack', 'OneDB - Best Use of OneDB Platform'];

// This will give us a list of the tables that the tracks in the FILTERED_LIST have, ie the tables that each sponsor will be judging
let sponsorTracks = {};

// Read judges file to put judge names in an array
var fs = require('fs');
var judges = fs.readFileSync('judges.txt').toString().split("\r\n");


function assignTables(projectsJson) {
  // returns number of tables
	let tableAssignmentIterator = 1;

  for (var i in projectsJson) { // Iterate through all projects and assign tables
    var project = projectsJson[i]
    project.table = tableAssignmentIterator;
		tableAssignmentIterator++;
  }

  return tableAssignmentIterator - 1; // Minus 1 because it will be 1 too big when exiting the loop
}


function getListOfTracks(projectsJson) {
  trackMap = {} // K-V: K=track, V=array of judging tables in that track

  for (var project of projectsJson) { // Same as for..each but javascript
    tracks = project['Desired Prizes'].split(', '); // Make array of strings of prizes per team
    for (let i=0; i<tracks.length; i++) {
      if (!(tracks[i] in trackMap)) { // if track doesn't already exist in dictionary
        trackMap[tracks[i]] = [];
      }

      trackMap[tracks[i]].push(project['table']); // Appends table to list of tables signed up for that track
    }
  }

  return trackMap;
}


function giveProjectsToJudges(trackMap, judges) {
  judgeMap = {};
  for (var judge of judges) {
    // console.log(judge);
    judgeMap[judge] = {};
  }
  
  let judgeIndex = 0; // Index in the judge array of the judges we are assigning
  let numTablesAssignedToCurrentJudge = 0; // Keeps track of when we should stop assigning tables to a group of judges and increment judgeIndex


  for (var track of Object.keys(trackMap)) { // For every track,
    for (var table of Object.values(trackMap[track])) { // For every table in the track
      for (var i=judgeIndex; i<judgeIndex+VIEWS_PER_PROJ; i++) { // Assign VIEWS_PER_PROJ judges at a time
        if (!(track in judgeMap[judges[i]])) { // Prevents KeyError
          // console.log(judgeMap);
          judgeMap[judges[i]][track] = [];
        }

        judgeMap[judges[i]][track].push(table);
      }

      numTablesAssignedToCurrentJudge++;

      if (numTablesAssignedToCurrentJudge >= PROJS_PER_JUDGE) {
        judgeIndex += VIEWS_PER_PROJ;
        numTablesAssignedToCurrentJudge = 0;
      }
    }
  }

  return judgeMap;
}


function findNumJudgements(tracksMap) {
  // This is different than simply the # of projects and is needed to
  // calculate the number of judges we need.
  // Ex: At BostonHacks Fall 2017, we had 50 projects, but since many
  // projects needed to be judged on multiple tracks, there were 121
  // judgements needed to be made.

  let total = 0;
  for (var trackTables of Object.entries(tracksMap)) {
  	if (!FILTERED_LIST.includes(trackTables[0])) {
    	total += trackTables[1].length;
	} else {
		sponsorTracks[trackTables[0]] = trackTables[1];
		// Get rid of this track in the global variable, because we filtered it out
		delete trackMap[trackTables[0]];
	}
  }

  return total;
}


function findNumberOfJudges(numJudgements) {
  return (numJudgements * VIEWS_PER_PROJ)/(TOTAL_JUDGING_TIME / TIME_PER_PROJ);
}


// Main script:
csv()
.fromFile(csvFilePath)
.then((jsonObj) => {
  console.log("BostonHacks Giudice!");
  console.log("====================\n");


  console.log("Running the numbers:");
  process.stdout.write("* Assigning table #s to projects...");
  let numTables = assignTables(jsonObj);
  console.log("done.");

  process.stdout.write("* Mapping prize tracks to table #s...");
  let trackMap = getListOfTracks(jsonObj);
  console.log("done.\n");

  let numJudgements = findNumJudgements(trackMap);
  let numJudges = findNumberOfJudges(numJudgements);
  numJudges = Math.ceil(numJudges); // round up to integer
  numJudges = numJudges + (VIEWS_PER_PROJ - numJudges % VIEWS_PER_PROJ); // Round up to nearest # of judges that is divisible by VIEWS_PER_PROJ

  console.log("Before we get started, here are your hackathon stats:");
  console.log("* There are %d projects total.", numTables);
  console.log("* There are effectively %d projects that need judging as some projects are registered for multiple tracks.\n", numJudgements);

  console.log("Judging assumptions (YOU CAN CHANGE THESE VALUES):");
  console.log("  * The judging period is %d minutes long.", TOTAL_JUDGING_TIME);
  console.log("  * Each project must be seen by %d judges per track (excluding the overall track, except for teams that only submitted to that track).", VIEWS_PER_PROJ);
  console.log("  * Each judge spends %d minutes at each table.\n", TIME_PER_PROJ);

  console.log("Given these judging assumptions, we calculate that we need %d judges.\n", numJudges);

  let judgeMap = giveProjectsToJudges(trackMap, judges);
  console.log("OK, here are the tracks each judge should judge for, and their corresponding tables:\n");
  console.log(judgeMap);

  console.log("\n\nHere are the project table numbers for the tracks that were not assigned judges:\n")
  console.log(sponsorTracks);
})
