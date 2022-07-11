export const getUptime = (date) => {
	if (date === undefined) {
		return ''
	}
	const startTime = new Date(date);
	const currentTime = new Date();
	const diff = (currentTime - startTime) / 3600000;
	const floor = Math.floor(diff)
	const hours = floor;
	const minutes = Math.round((diff - floor) * 60);
	return (hours != 0) ? `${hours} h ${minutes} min`
					: minutes < 1 ? '<1 min' : `${minutes} min`
}