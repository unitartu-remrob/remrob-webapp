import axios from "axios";
import $router from "../router/router.js";

const domain = window.location.host;
const protocol = (process.env.VUE_APP_PROTOCOL === "http") ? "http" : "https";
const protocolWs = (process.env.VUE_APP_PROTOCOL === "http") ? "ws" : "wss";

const rootURL = `${protocol}://${domain}`
const wsRootURL = `${protocolWs}://${domain}`

const api = axios.create({
    baseURL: rootURL,
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    },
});


const refreshAccessToken = async () => {
    try {
        const res = await api.post("/api/v1/refresh-token")
        const token = res.data.access_token
        api.defaults.headers.common['Authorization'] = 'Bearer ' + token;
        localStorage.setItem('user', JSON.stringify(res.data));
        console.log("refresing token succeded")
        return Promise.resolve();
    } catch (err) {
        localStorage.removeItem('user');
        console.log("refreshing token failed")
        $router.push({name: "Login"})
        return Promise.reject(err);
    }
}

// on authentication failiure error, try to refresh token
api.interceptors.response.use((response) => response, async err => {
    const originalRequest = err.config;
    const { url } = err.config

    if (err.response.status === 401 && url !== "/api/v1/refresh-token") {//!originalRequest._retry) {
        //originalRequest._retry = true;
        await refreshAccessToken();
        return api(originalRequest);
    }
    return Promise.reject(err);
})

export { api, rootURL, wsRootURL }