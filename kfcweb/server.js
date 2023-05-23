const express = require('express')
const app = express()
const port = 3000
const cors = require("cors");
const pool = require("./db");

const http = require('http')
const server = http.createServer(app)
const { Server } = require('socket.io');
const io = new Server(server, {
  cors:{
    origin: true
  },
  pingInterval: 100, //100 ms
  pingTimeout: 1
});

app.use(
    cors({
        origin: true
    })
);

app.get('/email', async (req, res) => {
  var data= req.param('add');
  const ok = await pool.query("SHOW TABLES LIKE '"+data+"'");
  if(ok[0]==''){
    const mama = await pool.query("CREATE TABLE `userDB`.`" +data+"` (`email` VARCHAR(45) NOT NULL, `nick` VARCHAR(45) NOT NULL, `ip` VARCHAR(45) NOT NULL, `id` INT NOT NULL, PRIMARY KEY (`id`)));
  }
  //const ood = await pool.query("select * from "+data );
  console.log(ok);
  res.send(ok[0]); 
})

io.on("connection", async (socket) => {
    const ret = await pool.query("select * from sensing order by time desc limit 10");
    socket.emit("fromser", ret[0]);
  
    socket.on("bbq", (arg) => {
      console.log(arg);
    })
  })

server.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})