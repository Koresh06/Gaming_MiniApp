import { createApp } from 'vue'
import App from './App.vue'
import VueTelegram from 'vue-tg'

const app = createApp(App)
app.use(VueTelegram)
app.mount('#app')
