import axios from 'axios';


export default class HttpClient {
  static token;

  static currentInstance;

  static httpConfig = {
    baseURL: 'http://127.0.0.1:8000'
  }

  static initialise(token) {
    this.token = token;
    this.httpConfig.headers = {
      'Authorization': 'Bearer ' + this.token
    };
    this.currentInstance = axios.create(this.httpConfig);
  }
}
