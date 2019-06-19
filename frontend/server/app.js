/**
Article : https://www.valentinog.com/blog/socket-react/#What_you_will_learn
**/
const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const axios = require("axios");
const port = process.env.PORT || 8001
const index = require("./routes/index");
const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const getApiAndEmit = async socket => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/api/all/",
      { headers : { "Authorization" : "Token cdc0ce48a7415b946b66e1a05380183923de8a83"}}
    );
    socket.emit("FromAPI", res.data);
  } catch (error) {
    console.error(`Error: ${error.code}`);
  }
};

let interval;
io.on("connection", socket => {
  console.log("New client connected");
  if (interval) {
    clearInterval(interval);
  }
  interval = setInterval(() => getApiAndEmit(socket), 5000);
  socket.on("disconnect", () => {
    console.log("Client disconnected");
  });
});

server.listen(port, () => console.log(`Liston on port ${port}`));
