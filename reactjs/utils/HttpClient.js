var axios = require('axios');

var http = axios.create({
  baseURL: 'http://localhost:10524'
});

module.exports = http;
