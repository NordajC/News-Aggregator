import { createPinia } from 'pinia';
const pinia = createPinia();
export default pinia;

import { defineStore } from 'pinia';
import { ref } from 'vue';
 
interface User {
  username: string;
  email: string;
  profilePicture: URL;
  favouriteCategories: string;
}
 
export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(localStorage.getItem('isAuthenticated') === 'true');
  const userData = ref<User | null>(null);
 
  async function checkAuth() {
    try {
      const response = await fetch('http://localhost:8000/user/profile/', {
        method: 'GET',
        credentials: 'include' 
      });
 
      if (response.ok) {
        const data = await response.json();
        isAuthenticated.value = true;
        localStorage.setItem('isAuthenticated', 'true'); 
        userData.value = { username: data.username, email: data.email, profilePicture: data.profilePicture, favouriteCategories: data.favouriteCategories }; // Adjust according to your response structure
      } else {
        isAuthenticated.value = false;
        userData.value = null;
      }
    } catch (error) {
      console.error('Error checking authentication:', error);
      isAuthenticated.value = false;
      localStorage.setItem('isAuthenticated', 'false'); 

    }
  }
  async function logout() {
    try {
      const response = await fetch('http://localhost:8000/logout/', {
        method: 'POST',
        credentials: 'include',  
        headers: {
        },
      });
      if (response.ok) {
        isAuthenticated.value = false;
        userData.value = null;
        localStorage.removeItem('isAuthenticated');
        window.location.href = 'http://localhost:8000/login/';
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  return { isAuthenticated, userData, checkAuth, logout };
});