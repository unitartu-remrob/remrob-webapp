<template>
	<b-container fluid class="intro-container">
		<b-row class="justify-content-center p-3">
			<img class="remrob-preview w-75" :src="require('@/assets/browser-window-mock.jpg')" />
		</b-row>
		<b-row class="d-flex justify-content-center mt-4">
			<div class="remrob-intro">
				<h1 class="remrob-title text-ubuntu-500"> REMROB - authentic ROS development in the browser</h1>
				<p class="remrob-intro-text text-arvo-400 brief-intro">
					Remrob is a web application for working with ROS-enabled robots remotely in an authentic development environment.
					<br/><br/>
					<span class="link-pre text-ubuntu-500">IEEE TLT Article:</span>
					&nbsp;
					<a href="https://ieeexplore.ieee.org/document/10480223" target="_blank" class="remrob-link">https://ieeexplore.ieee.org/document/10480223</a>
				</p>
				<p class="remrob-intro-text text-arvo-400">
					<b-img class="gh-logo" :src="require('@/assets/github.png')"></b-img>
					&nbsp;
					<a href="https://github.com/unitartu-remrob" target="_blank" class="remrob-link gh-link">https://github.com/unitartu-remrob</a>
				</p>		
			</div>
		</b-row>
	</b-container>
</template>

<script>
export default {
	name: "RemrobIntro",
}
</script>

<style>
:root {
	--remrob-title-color: #ffaf90;
}

.remrob-title {
	color: var(--remrob-title-color);
	text-align: center;
}

.link-pre {
	color: var(--remrob-title-color);
}

.intro-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.remrob-preview {
	max-width: 60%;
    border: 1rem solid rgb(24, 18, 18);
    border-radius: 15px;
    box-shadow: 0px 10px 50px 10px rgba(0,0,0,0.5);
}

.remrob-intro {
    max-width: 80%;
}

.remrob-intro-text {
	color: rgb(255, 255, 255);
	font-size: 1.5rem;
	line-height: 1.8;
	padding-left: 10%;
}

.brief-intro {
	margin-top: 3rem;
}

.remrob-link {
	color: #21d2f1;
	text-decoration: underline;
}

.remrob-link:hover {
	color: rgb(183, 233, 253);
}

.gh-logo {
	width: 2.5rem;
	height: 2.5rem;
}

@media screen and (max-width: 1900px) {
	.remrob-intro-text {
		font-size: 1.2rem;
	}
	.brief-intro {
		margin-top: 2rem !important;
	}
	.remrob-title {
		font-size: 1.8rem;
	}
	.link-pre { 
		font-size: 1.35rem;
	}
	.remrob-link {
		font-size: 1.3rem;
	}
	.gh-link {
		font-size: 1.1rem !important;
	}

}

@media screen and (max-width: 1600px) {
	.remrob-intro-text {
		font-size: 1rem;
	}
	.brief-intro {
		margin-top: 2rem !important;
	}
	.remrob-title {
		font-size: 1.5rem;
	}
	.link-pre {
		font-size: 1.2rem;
	}
	.remrob-link {
		font-size: 1.1rem;
	}
	.gh-link {
		font-size: 0.9rem !important;
	}
}
</style>