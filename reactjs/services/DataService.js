import http from '../utils/HttpClient';
import * as constants from '../utils/Constants';

export const getDashboardData = () => {
	return http.get(constants.dashboardEndpoint);
}
