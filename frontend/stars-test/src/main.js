import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import './style.css'
import { VueTelegramPlugin } from "vue-tg";


const app = createApp(App)

app.use(VueTelegramPlugin);
app.use(router)
app.mount('#app')
