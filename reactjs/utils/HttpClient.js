var axios = require('axios');

var http = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Authorization': 'Bearer M0SFhKOKDstRIXUFWEnTWZtEwFvlXB'
  }
});

module.exports = http;
