
import { createRouter, createWebHistory } from 'vue-router'


import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';

import { useAuthStore } from '../store.ts';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''


const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/other/', name: 'Other Page', component: OtherPage },
    ]
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();


    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

    if (to.meta.requiresAuth && !isAuthenticated) {
      window.location.href = 'http://localhost:8000/login';
    } else {
      next(); 
    }
  });

export default router