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


export const getCountdown = (start, end) => {
	var now = new Date().getTime();
	
	start = new Date(start)
	end = new Date(end)

	var isActive = (now > start) && (now < end);
	var isExpired = (now > end)

	var timeleft;
	if (isActive) {
		timeleft = end - now;
	} else if (!isExpired) {
		timeleft = start - now;
	} else {
		timeleft = 0;
	}
			
	var days = Math.floor(timeleft / (1000 * 60 * 60 * 24));
	var hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	var minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
	var seconds = Math.floor((timeleft % (1000 * 60)) / 1000);

	var displayTime = (days == 1) ? `${days} day` : (days > 1) ? `${days} days` : (seconds >= 0) ? `${hours}:${minutes > 9 ? minutes : '0' + minutes}:${seconds > 9 ? seconds : '0' + seconds}` : "Finished"

	return {
		isActive,
		isExpired,
		displayTime
	}
}