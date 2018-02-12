var axios = require('axios');

var http = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  // headers: {
  //   'Authorization': 'Bearer M0SFhKOKDstRIXUFWEnTWZtEwFvlXB'
  // }
});

module.exports = http;
