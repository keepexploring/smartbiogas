// List of endpoints: /dashboard/api/v1/
// The base url is set at HTTP client level
// Other endpoints:
// biogasplants
// biogasplantcontacts
// company

function buildEndpoint(route){
	return `/data/api/v1/${route}/?format=json`
}

export const technicianEndpoint = buildEndpoint('jobs');
export const techniciansEndpoint = buildEndpoint('users');
export const dashboardEndpoint = buildEndpoint('Dashboard'); //TODO
