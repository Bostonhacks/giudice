const csvFilePath='./submissions.csv'
const csv=require('csvtojson')
csv()
.fromFile(csvFilePath)
.then((jsonObj)=>{
    console.log(jsonObj);
}).then(() => {
	const jsonArray = csv().fromFile(csvFilePath);
})
