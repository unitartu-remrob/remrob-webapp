import { api } from "../util/api.js";

class ImageHandler {
	constructor({
		images,
		imageOptionsSim,
		defaultImageSim,
		imageOptionsPhysbot,
		defaultImagePhysbot
	}) {
		this.images = images;
		this.imageOptionsSim = imageOptionsSim;
		this.defaultImageSim = defaultImageSim;
		this.imageOptionsPhysbot = imageOptionsPhysbot;
		this.defaultImagePhysbot = defaultImagePhysbot;
	}

	getImageLabel(imageTag) {
		return this.images.find(image => image.imageTag === imageTag)?.label;
	}

	getImageRosVersion(imageTag) {
		return this.images.find(image => image.imageTag === imageTag)?.rosVersion;
	}

	versionLogo(imageTag) {
		const rosVersion = this.getImageRosVersion(imageTag);
		if (rosVersion) {
			try {
				return require(`../assets/${rosVersion}.png`);
			} catch (e) {
				return null;
			}
		}
		return null;
	}
}

export const getImageOptions = async () => {
	const res = await api.get("/containers/images");
	const images = res.data;
	const physbotImages = images.filter(image => !image.simulationExclusive)
	
	const imageOptionsSim = images.map(({ imageTag, label }) => {
		return { value: imageTag, text: label }
	})
	const defaultImageSim = images.find(image => image.default)?.imageTag ?? images[0].imageTag;

	const imageOptionsPhysbot = physbotImages.map(({ imageTag, label }) => {
		return { value: imageTag, text: label }
	})
	
	const defaultImagePhysbot = physbotImages.find(image => image.default)?.imageTag ?? physbotImages[0].imageTag;	

	return new ImageHandler({
		images,
		imageOptionsSim,
		defaultImageSim,
		imageOptionsPhysbot,
		defaultImagePhysbot
	});
}