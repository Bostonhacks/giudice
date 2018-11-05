const csvFilePath='./submissions.csv';
const csv=require('csvtojson');

const TOTAL_JUDGING_TIME = 90; // How many minutes long is our judging period?
const TIME_PER_PROJ = 9; // How many minutes should a judge spend judging a project?
const VIEWS_PER_PROJ = 3; // How many judges should view a project?

const PROJS_PER_JUDGE = TOTAL_JUDGING_TIME / TIME_PER_PROJ;

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
  //trackMap['General Prize'] = [] // This will contain every table (every project is considered for general prize)

  for (var project of projectsJson) { // Same as for..each but javascript
    tracks = project['Desired Prizes'].split(', '); // Make array of strings of prizes per team
    for (let i=0; i<tracks.length; i++) {
      if (!(tracks[i] in trackMap)) { // if track doesn't already exist in dictionary
        trackMap[tracks[i]] = [];
        //console.log(trackMap);
      }

      trackMap[tracks[i]].push(project['table']); // Appends table to list of tables signed up for that track
    }

    //trackMap['General Prize'].push(project['table']); // Append table to list of tables signed up for general prize
  }
  //console.log(trackMap);

  return trackMap;
}



let judges = ["Warren", "Sarah", "Zuul", "Bandalf", "Mari", "Pikachu", "Eevee", "Rattata", "Spearow", "Pidgey", "Professor Oak", "Professor Wayne Snyder", "Caterpie", "Charizard", "Growlithe", "Judge 16", "Judge Dredd", "Hardcodo the Great", "That One Guy", "Dad", "Mom", "Your long lost brother", "Nemo", "Julius Caesar", "Brutus", "Romeo", "Juliet", "The Witch", "The Girl with the Dragon Tattoo", "Spiderman", "Thanos the Mad Titan", "Judge 33", "Dr. Strange", "Iron Man", "Black Widow", "Vision", "Bruce Banner"]; //37 judges lol hardcoding


function giveProjectsToJudges(trackMap, judges) {
  judgeMap = {};
  for (var judge of judges) {
    judgeMap[judge] = {};
  }

  // VIEWS_PER_PROJ we use this
  let judgeIndex = 0;
  let numTablesAssignedToCurrentJudge = 0;


  for (var track of Object.keys(trackMap)) {
    console.log("PRINTING TRACKMAP:");
    console.log(trackMap);
    //console.log(track);
    //console.log(trackMap[track]);
    for (var table of Object.values(trackMap[track])) {
      //console.log("PRINTING TABLE:");
      console.log(table);
      for (var i=judgeIndex; i<judgeIndex+VIEWS_PER_PROJ; i++) {
        console.log("Judge we are trying to look at:");
        console.log(judges[i]);
        console.log("PRINTING JUDGEMAP:");
        console.log(judgeMap);
        if (!(track in judgeMap[judges[i]])) {
          judgeMap[judges[i]][track] = [];
        }

        console.log(judgeMap[judges[i]][track]);

        judgeMap[judges[i]][track].push(table);
      }
      numTablesAssignedToCurrentJudge++;
      if (numTablesAssignedToCurrentJudge >= PROJS_PER_JUDGE) {
        judgeIndex += VIEWS_PER_PROJ;
        numTablesAssignedToCurrentJudge = 0;
      }
    }
  }

  console.log(judgeMap);
  // We give X judges the same schedule where X = # views per project
  //for (var [track, tables] of Object.entries(trackMap)) {
    //if (numTablesAssignedToCurrentJudge < VIEWS_PER_PROJ) {

   // }
  //}
}


function findNumJudgements(trackMap) {
  // This is different than simply the # of projects and is needed to
  // calculate the number of judges we need.
  // Ex: At BostonHacks Fall 2017, we had 50 projects, but since many
  // projects needed to be judged on multiple tracks, there were 121
  // judgements needed to be made. We needed 37 judges but if we had used
  // 50 for our calculations, we would have calculated needing 15 judges.

  //const reducer = (accumulator, currentProject) => accumulator + asdf;
  let total = 0;

  for (var tableArr of Object.values(trackMap)) {
    total += tableArr.length;
  }

  return total;
}


function findNumberOfJudges(numJudgements){
  return (numJudgements * VIEWS_PER_PROJ)/(TOTAL_JUDGING_TIME / TIME_PER_PROJ);
}


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
  let numJudges = findNumberOfJudges(numJudgements) + 2; // +2 is needed in case of edge case track and we have a judge judging only 1 project, TODO fix this
  numJudges = Math.ceil(numJudges); // round up

  console.log("Before we get started, here are your hackathon stats:");
  console.log("* There are %d projects total.", numTables);
  console.log("* There are effectively %d projects that need judging as some projects are registered for multiple tracks.\n", numJudgements);

  console.log("Judging assumptions (YOU CAN CHANGE THESE VALUES):");
  console.log("  * The judging period is %d minutes long.", TOTAL_JUDGING_TIME);
  console.log("  * Each project must be seen by %d judges per track (excluding the overall track, except for teams that only submitted to that track).", VIEWS_PER_PROJ);
  console.log("  * Each judge spends %d minutes at each table.\n", TIME_PER_PROJ);

  console.log("Given these judging assumptions, we calculate that we need %d judges.", numJudges);

  // TODO: Get judges from json file

  //giveProjectsToJudges(trackMap, judges);
})
