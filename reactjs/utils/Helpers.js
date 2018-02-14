export const handleHttpError = (error) => {
	console.log(error);
}

export const yearsAgo = (fromDate) => {
	let startDate = new Date(fromDate);
	if(!startDate) { return 0; }
	let endDate = new Date();
	let yearDiff = endDate.getFullYear() - startDate.getFullYear();
	if (startDate.getMonth() > endDate.getMonth()) {
		yearDiff--;
	} else if (startDate.getMonth() === endDate.getMonth()) {
		if (startDate.getDate() > endDate.getDate()) {
			yearDiff--;
		} else if (startDate.getDate() === endDate.getDate()) {
			if (startDate.getHours() > endDate.getHours()) {
				yearDiff--;
			} else if (startDate.getHours() === endDate.getHours()) {
				if (startDate.getMinutes() > endDate.getMinutes()) {
					yearDiff--;
				}
			}
		}
	}
	return yearDiff;
}
