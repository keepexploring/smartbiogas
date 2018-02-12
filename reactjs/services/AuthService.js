import http from '../utils/HttpClient';
import * as constants from '../utils/Constants';

export const requestToken = (username, password) => {
	let params = new URLSearchParams();
	params.append('username', username);
	params.append('password', password);
	params.append('grant_type', 'password');
	params.append('client_id', '123456');
	params.append('client_secret', '123456');

	let config = { headers: { 
		'Content-Type': 'application/x-www-form-urlencoded',
		'Accept': 'application/json',
	} };

	return http.post(constants.tokenEndpoint, params, config);
}

export let isLoggedIn = false;
