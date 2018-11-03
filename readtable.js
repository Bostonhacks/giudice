const csvFilePath='./submissions.csv'
const csv=require('csvtojson')



function assignTables(projectsJson) {

	let tableAssignmentIterator = 1;

    for (var i in projectsJson) { // Iterate through all projects and assign tables
    	var project = projectsJson[i]
    	project.table = tableAssignmentIterator;
		tableAssignmentIterator++;
    }

    //console.log(projectsJson);
}



function getListOfTracks(projectsJson) {
  trackMap = {} // K-V: K=track, V=array of judging tables in that track
  trackMap['General Prize'] = [] // This will contain every table (every project is considered for general prize)

  for (var project of projectsJson) { // Same as for..each but javascript
    tracks = project['Desired Prizes'].split(', '); // Make array of strings of prizes per team
    for (let i=0; i<tracks.length; i++) {
      if (!(tracks[i] in trackMap)) { // if track already exists in dictionary
        trackMap[tracks[i]] = [];
        //console.log(trackMap);
      }

      trackMap[tracks[i]].push(project['table']); // Appends table to list of tables signed up for that track
    }

    trackMap['General Prize'].push(project['table']); // Append table to list of tables signed up for general prize
  }
  //console.log(trackMap);

  return trackMap;
}

csv()
.fromFile(csvFilePath)
.then((jsonObj) => {
  assignTables(jsonObj);
  getListOfTracks(jsonObj);
})
