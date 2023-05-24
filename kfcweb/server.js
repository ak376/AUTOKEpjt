const express = require("express");
let app = express();
const port = 3000;
const cors = require("cors");
const pool = require("./db");

const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server, {
  cors: {
    origin: true,
  },
  pingInterval: 100, //100 ms
  pingTimeout: 1,
});

app.use(
  cors({
    origin: true,
  }),
  express.urlencoded({
    extended: true,
  })
);
let ok;
app.get("/", async (req, res) => {
  const table = await pool.query("SHOW TABLES FROM userDB");

  res.send(table[0]);
});
app.get("/email", async (req, res) => {
  const data = req.param("add");

  try {
    ok = await pool.query("SELECT * FROM `userDB`." + data);
    const userdata = { result: ok[0] };
    //console.log(res);
    res.send(userdata);
  } catch (error) {
    try {
      const ok2 = await pool.query(
        "CREATE TABLE `userDB`." +
          data +
          " ( `nick` VARCHAR(45) NOT NULL, `ip` VARCHAR(45) NOT NULL, `id` INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id`))"
      );

      res.send("create user");
    } catch (error) {
      res.send("errorrrrr");
    }
  }
});

app.post("/add", async (req, res) => {
  const { email, nick, ip } = req.body;
  console.log(req.userid);
  try {
    ok = await pool.query(
      "INSERT INTO " + email + "(nick, ip) values (?, ?);",
      [nick, ip]
    );
    const userdata = { result: ok[0] };
    //console.log(res);
    res.send(userdata);
  } catch (error) {
    res.send(error);
  }
});

app.post("/delete", async (req, res) => {
  const { email, index } = req.body;
  console.log(email, index);
  try {
    ok = await pool.query(
      "delete from " +
        email +
        " where id = (select id from(select row_number() over(order by id ) as num, nick, ip, id from " +
        email +
        ") as a where a.num=" +
        index +
        ")"
    );
    const userdata = { result: ok[0] };
    //console.log(res);
    res.send(userdata);
  } catch (error) {
    res.send(error);
  }
});

server.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

