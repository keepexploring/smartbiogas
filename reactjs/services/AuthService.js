import * as constants from '../utils/Constants';
import Authenticated from '../models/Authenticated';

export default class AuthService {
	static isLoggedIn = false;
	static currentUser;

	static clearCurrentUser() {
		this.isLoggedIn = false;
		this.currentUser = null;
		localStorage.clear();
	}

	static initialise() {
		let u = JSON.parse(localStorage.getItem('currentUser'));
		if (u) {
			let user = new Authenticated (
				u.access_token, 
				u.token_type, 
				u.expires_in, 
				u.refresh_token,
				u.scope
			);
			this.currentUser = user;
			this.isLoggedIn = true;
			return user;
		}
		localStorage.clear();
	}
	
	static setCurrentUser(authenticated) {
		localStorage.clear();
		localStorage.setItem('currentUser', JSON.stringify(authenticated));
		this.isLoggedIn = true;
		this.currentUser = authenticated;
	}
}
