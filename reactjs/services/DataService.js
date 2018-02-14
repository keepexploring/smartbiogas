import HttpClient from '../utils/HttpClient';
import * as constants from '../utils/Constants';

export const getDashboardData = () => {
	return HttpClient.currentInstance.get(constants.dashboardEndpoint);
}
