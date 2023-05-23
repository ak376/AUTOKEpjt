const express = require('express')
const app = express()
const port = 3000
const cors = require("cors");

var bodyParser = require('body-parser');
app.use(
        cors({
                origin:true
        })
);

app.use(bodyParser.json());	// json 등록
app.use(bodyParser.urlencoded({ extended : false }));	// URL-encoded 등록

app.get('/user/:email', function (req, res) {
    
    var data= req.params;
    const ret = 
    res.send("User id : " + data.email );
});



app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})