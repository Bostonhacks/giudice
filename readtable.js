const csvFilePath='./submissions.csv';
const csv=require('csvtojson');

const TOTAL_JUDGING_TIME = 90; // How many minutes long is our judging period?
const TIME_PER_PROJ = 9; // How many minutes should a judge spend judging a project?
const VIEWS_PER_PROJ = 3; // How many judges should view a project?

const PROJS_PER_JUDGE = TOTAL_JUDGING_TIME / TIME_PER_PROJ;

function assignTables(projectsJson) {
	let tableAssignmentIterator = 1;

  for (var i in projectsJson) { // Iterate through all projects and assign tables
    var project = projectsJson[i]
    project.table = tableAssignmentIterator;
		tableAssignmentIterator++;
  }
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



let judges = ["Warren", "Sarah", "Zuul", "Bandalf", "Mari", "Pikachu", "Eevee", "Rattata", "Spearow", "Pidgey", "Professor Oak", "Professor Wayne Snyder", "Caterpie", "Charizard", "Growlithe"];


function giveProjectsToJudges(trackMap, judges) {
  judgeMap = {};
  for (var judge of judges) {
    judgeMap[judge] = {};
  }

  // VIEWS_PER_PROJ we use this
  let judgeIndex = 0;
  let numTablesAssignedToCurrentJudge = 0;


  for (var track of Object.keys(trackMap)) {
    console.log(track);
    console.log(trackMap[track]);
    for (var table of Object.values(trackMap[track])) {
      console.log(table);
      for (var i=judgeIndex; i<judgeIndex+VIEWS_PER_PROJ; i++) {
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





function findNumberOfJudges(numProjects){
  return (numProjects * VIEWS_PER_PROJ)/(TOTAL_JUDGING_TIME / TIME_PER_PROJ);
}


csv()
.fromFile(csvFilePath)
.then((jsonObj) => {
  assignTables(jsonObj);
  let trackMap = getListOfTracks(jsonObj);
  giveProjectsToJudges(trackMap, judges);
})
