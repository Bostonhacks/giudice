const csvFilePath='./submissions.csv'
const csv=require('csvtojson')
csv()
.fromFile(csvFilePath)
.then((jsonObj) => {
	let tableAssignmentIterator = 0;

    for (var i in jsonObj) { // Iterate through all projects and assign table
    	var project = jsonObj[i]
    	project.table = tableAssignmentIterator;
		tableAssignmentIterator++;
    }

    console.log(jsonObj);
}).then(() => {
	const jsonArray = csv().fromFile(csvFilePath);
})
