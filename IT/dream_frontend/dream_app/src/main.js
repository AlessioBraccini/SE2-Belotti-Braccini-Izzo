import { createApp } from 'vue'
import App from './App.vue'
import router from "./router"

// Mounting point of the vue app
createApp(App).use(router).mount('#app')
