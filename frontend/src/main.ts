import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store';
import './assets/tailwind.css';  // This should be in your main.js or main.ts file

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App)

app.use(router)
app.use(pinia)

app.mount('#app')
