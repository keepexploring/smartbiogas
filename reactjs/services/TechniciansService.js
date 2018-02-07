import http from '../utils/HttpClient';
import * as constants from '../utils/Constants';

export const getTechnicians = () => {
	return http.get(constants.techniciansEndpoint);
}

export const getJobs = (technicianId) => {
	return http.get(constants.technicianEndpoint + '/' + technicianId);
}
