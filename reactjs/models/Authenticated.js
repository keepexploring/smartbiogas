export default class Authenticated {
	access_token;
	token_type;
	expires_in;
	refresh_token;
	scope;

	constructor (access_token, token_type, expires_in, refresh_token, scope) {
		this.access_token = access_token;
		this.token_type = token_type;
		this.expires_in = expires_in;
		this.refresh_token = refresh_token;
		this.scope = scope;
	}

}