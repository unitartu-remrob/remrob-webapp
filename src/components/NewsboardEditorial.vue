<template>
  <div class="remrob-info">
    <div class="bg-main bg-cell"></div>
    <b-modal ok-title="Confirm" @ok="deletePost()" title="Delete post" id="delete-modal">
        <h4>{{`Say bye to "${this.postTitle}"?`}}</h4>
    </b-modal>
    <div class="editorial">
      <wysiwyg
        class="admin-news"
        v-model="newsContent" />
      <div class="message-picker">
        <h4>Choose message:</h4>
        <b-dropdown v-model="activeItem" :text="postTitle" size="lg" right>
          <b-dropdown-item
            v-for="item in boardItems"
            :key="item.id"
            :value="item.content"
            :active="item.active"
            @click="switchActive(item)"
            >{{ item.title }}</b-dropdown-item>
        </b-dropdown>
      </div>
      <b-form-group class="mt-3 post-controls">
        <div class="post-name-field">
          <h4 clas="muted" >Post name:</h4>
          <b-form-input type="text" placeholder="Message name" v-model="postTitle"></b-form-input>
        </div>
        <div class="post-btn-container">
          <b-button class="save-board-btn" type="button" variant="warning"
            :disabled="activeItem === null"
            @click="$bvModal.show('delete-modal')">Delete post</b-button>
          <b-button class="save-board-btn" type="button" variant="success" @click="updateNews()">Save post</b-button>
          <b-button class="save-board-btn" type="button" variant="primary"
            :disabled="activeItem === null"
            @click="createPost()">Create new post</b-button>
          <b-button class="save-board-btn" type="button" variant="info"
            :disabled="activeItem === null"
            @click="setPost()">Set as active post</b-button>
        </div>
      </b-form-group>
      <b-card class="resources">
        <Newsboard :content="newsContent"/>
      </b-card>
      <b-alert :show="dismissCountDown" dismissible @dismissed="dismissCountDown=0" :variant="alertType">{{alertMessage}}</b-alert>
    </div>
  </div>
</template>

<script>
import Newsboard from './Newsboard';

export default {
  name: 'NewsboardEditorial',
  components: {
    Newsboard
  },
  props: {

  },
  data() {
    return {
      newsContent: "",
      alertMessage: "",
      alertType: "",
      dismissSec: 3,
      dismissCountDown: 0,
      boardItems: [],
      activeItem: null,
      postTitle: ""
    };
  },
  methods: {
		fetchNews: function() {
			// fetch the message board html from the backend
			this.$api.get("/api/v1/newsboard").then((res) => {
				const data = res.data;
        if (data.length > 0) {
          this.boardItems = data;
          this.activeItem = this.boardItems.find((item) => item.active === true);
          if (this.activeItem !== undefined) {
            // console.log("ACTIVE", this.activeItem)
            this.newsContent = this.activeItem.content;
            this.postTitle = this.activeItem.title;
          }
        } else {
          this.boardItems = [];
        }
			}).catch((err) => {
        console.log(err);
      })
		},
    createPost: function() {
      this.activeItem = null,
      this.newsContent = "";
      this.postTitle = `New post ${this.boardItems.length + 1}`;
    },
    updateNews: function() {
			// fetch the message board html from the backend
      if (this.activeItem === null) {
        this.$api.post("/api/v1/newsboard", {
          content: this.newsContent,
          title: this.postTitle
        }).then((res) => {
          this.alertMessage = `Message board item "${this.postTitle}" created`;
          this.alertType = "success"; this.dismissCountDown = this.dismissSec;
          this.fetchNews();
        }).catch((err) => {
          console.log(err);
        })
      }
      else { // if item is not null expect an update
        this.$api.put(`/api/v1/newsboard/${this.activeItem.id}`, {
          content: this.newsContent,
          title: this.postTitle
        }).then((res) => {
          this.alertMessage = `Message board item "${this.activeItem.title}" updated`;
          this.alertType = "success"; this.dismissCountDown = this.dismissSec;
          this.fetchNews();
        }).catch((err) => {
          console.log(err);
        })
      }
		},
    deletePost: function() {
      this.$api.delete(`/api/v1/newsboard/${this.activeItem.id}`).then((res) => {
        this.alertMessage = `Message board item "${this.activeItem.title}" deleted`;
        this.alertType = "info"; this.dismissCountDown = this.dismissSec;
        this.fetchNews();
      }).catch((err) => {
        console.log(err);
      })
    },
    setPost: function() {
      this.$api.put(`/api/v1/newsboard/${this.activeItem.id}`, {
        active: true
      }).then((res) => {
        this.alertMessage = `Message board item "${this.activeItem.title}" is now active`;
        this.alertType = "success"; this.dismissCountDown = this.dismissSec;
        this.fetchNews();
      }).catch((err) => {
        console.log(err);
      })
    },
    switchActive: function(item) {
      this.activeItem = item;
      this.newsContent = item.content;
      this.postTitle = item.title;
    }
  },
  mounted() {
    this.fetchNews();
  },
}
</script>

<style>
@import "~vue-wysiwyg/dist/vueWysiwyg.css";

.admin-news {
    background-color: #fff;
    width: 80%;
    height: 25rem;
    border-radius: 2rem;
    padding: 2.5rem;
}

.message-picker {
  position: relative;
  float: right;
  top: -2rem;
  left: 20rem;
  width: 40%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
}

.editorial {
  position: relative;
  top: -15rem;
  left: 25%;
}

.editorial a,
.remrob-info a {
  background-color: transparent !important;
}

.post-controls {
  display: block;
  padding-top: 1rem;
}

.post-name-field {
  width: 100%;
  margin-bottom: 1rem;
  position: relative;
  left: 14rem;
}

.post-btn-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  left: 14rem;
  width: 100%;
}

.editorial .dropdown-item {
  font-size: 1.2rem;
}

.editorial .dropdown-item.active {
  color: green;
  font-weight: bold;
}

.editorial .dropdown-item.active::after {
  content: " (current)";
}
</style>