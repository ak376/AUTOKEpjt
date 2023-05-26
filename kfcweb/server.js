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
let ok; // 쿼리문날려서 들어오는거 받는 변수 ok

//get통신으로 서버 3000포트 접속시 userDB 스키마 내부의 모든 테이블 확인
app.get("/", async (req, res) => {
  const table = await pool.query("SHOW TABLES FROM userDB");

  res.send(table[0]);
});

// get 통신부분으로 3000번 포트 뒤에 email로 접근시 "add"로 계정명 전송
// 계정이 있는경우에 테이블내부 값들 json값으로 반환
app.get("/email", async (req, res) => {
  const data = req.param("add");

  try {
    ok = await pool.query("SELECT * FROM `userDB`." + data);
    const userdata = { result: ok[0] };
    //console.log(res);
    res.send(userdata);
  } catch (error) { // 계정명 테이블이 없는경우 새로운 테이블생성
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


// get통신부분으로 data 로 접근시 "ip"부분에 전처리된 ip주소할당
// ip주소로 최근 10개 센서데이터  json 데이터로 반환
app.get("/data", async (req, res) => {
  let ip = req.param("ip");
  ip="_"+ip;
  try {
    console.log(ip);
    ok = await pool.query(
      "SELECT * FROM `userDB`." + ip + " order by time DESC limit 10"
    );
    const userdata = { result: ok[0] };
    //console.log(res);
    res.send(userdata);
  } catch (error) {
    res.send("errorrrrr");
  }
});


// 사용자가 nick과 ip 로 새로운 기기 등록part
// post통신으로 add로 접근시 req.body내부를 {email, nick, ip}에 각 파싱
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


// 사용자 계정과 index값으로 최근순으로 몇번째 데이터인지 넘겨줌
// rownum과 pk값으로 선택해서 delete 
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

