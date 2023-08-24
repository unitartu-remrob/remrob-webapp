<template>
  <div class="remrob-info robot-ground">
    <b-card class="resources">
      <template v-if=newsLoaded>
        <Newsboard :content="newsBoardText"/>
      </template>
    </b-card>
    <b-img class="robot-slide" :src="currentImage"></b-img>
  </div>
</template>

<script>
import Newsboard from './Newsboard';

export default {
  name: 'InfoPanel',
  components: {
		Newsboard
  },
  data() {
    return {
      images: [
        require('@/assets/robotont.png'),
        require('@/assets/robotont-left.png'),
        require('@/assets/robotont-right.png'),
      ],
      currentIndex: 0,
      newsBoardText: '',
      newsLoaded: false
    };
  },
  computed: {
    currentImage() {
      return this.images[this.currentIndex];
    }
  },
  methods: {
    startImageRotation() {
      this.imageRotationInterval = setInterval(() => {
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
      }, 3650);
    },
    stopImageRotation() {
      clearInterval(this.imageRotationInterval);
    },
    fetchNews: function() {
      this.$api.get("/api/v1/newsboard", {
        params: {
          latest: true
        }
      }).then((res) => {
        const data = res.data;
        // take first active post
        this.newsBoardText = (data.length > 0) ? data[0].content : "";
        console.log("GOT NEWS", data[0].content)
        console.log("IS equal", this.content === data[0].content)
        this.newsLoaded = true;
      })
		}
  },
  mounted() {
    this.fetchNews();
  },
  beforeCreate() {

  },
  created() {
    this.startImageRotation();
  },
  beforeDestroy() {
    this.stopImageRotation();
  },
}
</script>

<style>
.robot-slide {
  position: fixed;
  width: 15%;
  animation: drive 11s ease-in-out infinite;
  /* z-index: -2; */
  right: 18%;
  z-index: 1;
  /* right: 1rem; */
}

.robot-ground {
    padding-top: 30%;
    width: 50vw;
    /* max-width: 55vw; */
}

.admin-menu .remrob-info .resources,
.remrob-info .resources {
  background-color: rgba(255, 255, 255, 0.904);
  /* background-color: white; */
  padding: 0;
  margin: 0;
  width: 25%;
  height: 30% !important;
  position: fixed;
  top: 13%;
  right: 15%;
  border: 2px solid rgb(22, 20, 20);
  border-radius: 8px;
}

.resources {
  transform: skewY(5deg) skewX(-2deg);
  z-index: 0;
}

/* .news-text {
  transform: skewY(-5deg) skewX(2deg);
} */

@keyframes drive {
  0%, 100% {
    transform: translateX(0);
    /* transform: translateY(0); */
  }
  33% {
    transform: translateX(170px);
    transform: translateY(80px);
  }

  66% {
    transform: translateX(-600px);
    /* transform: translateY(10px); */
  }

}

</style>