import http from '../utils/HttpClient';
import * as constants from '../utils/Constants';
import * as Helpers from '../utils/Helpers';

export const getTechnicians = () => {
	return http.get(constants.techniciansEndpoint);
}

export const getJobs = (technicianId) => {
	return http.get(constants.technicianEndpoint + '/' + technicianId);
}

export const buildTechnicianDataModel = (technician) => {
	return {
		// languages: 'Languages Spoken', // not on api
		id: technician.id  || '',
		full_name: technician.first_name + ' ' + technician.last_name,
		phone_number: technician.phone_number  || '',
		address: 
			technician.district || '' + ' ' + 
			technician.neighbourhood || '' + ' ' + 
			technician.district || '' + ' ' + 
			technician.village || '' + ' ' + 
			technician.postcode || '' + ' ' + 
			technician.country || '' + ' ' + 
			technician.other_address_details || '' + ' ' +
			technician.region || '',
		country: technician.country,
		location: technician.technician_details.location || '',
		skills: technician.technician_details.specialist_skills  || '',
		datetime_created: technician.datetime_created  || '',
		image_url: technician.user_photo  || '',
		jobs_completed: technician.technician_details.number_of_jobs_completed,
		jobs_active: technician.technician_details.number_jobs_active,
		years_active: Helpers.yearsAgo(technician.datetime_created) || 0,
		status: technician.technician_details.status ? 'Active' : 'Inactive'
	}
}