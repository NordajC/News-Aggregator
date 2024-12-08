<template>
    <main class="justify-start p-3 bg-gray-50">
        <div  class="w-full m-0 inline-flex flex-row justify-between rounded lg:px-60 sm:px-10 py-3">
            <router-link class="text-2xl flex items-center no-underline p-2 border rounded text-white bg-red-400 transition ease-in-out delay-150 hover:scale-110 hover:bg-red-600 duration-300" :to="{ name: 'Main Page' }">
                Not Reddit
            </router-link>

            
                <button id="avatarDropDown" class="flex flex-col items-center justify-center gap-2 p-2x"
                @click="toggleDropdown">
                    <span class=" flex flex-col items-center w-10 max-w-30 transition linear delay-100 hover:scale-110">
                        <img src="./assets/blank pp.webp" alt="" srcset="" class="w-10 rounded justify-self-center">
                    </span>
                </button>

            <div v-if="isDropdownOpen" class="absolute top-14 right-20 mt-2 w-36 bg-white shadow-lg rounded-b py-2 border">
                <span id="dropdown-item" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    <router-link class="" :to="{ name: 'Other Page' }">
                        Settings
                    </router-link>
                </span>
                <span id="dropdown-item" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    <p>otheritems</p>
                </span>
            </div>



        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import { RouterView } from "vue-router";
// test

// import { useAuthStore } from './store.ts';
// const authStore = useAuthStore();
// interface UserProfile {
//   profile_image: string;
//   // Add other properties if needed
// }

// const userProfile = ref<UserProfile | null>(null);
// const profileImageFile = ref(null);
// const errorMessage = ref("");
// const loading = ref(true);
//

// export default defineComponent({
//     components: { RouterView },
//     computed: {
//         profileImageUrl() {
//             if (userProfile.value && userProfile.value.profile_image) {
//                 return `http://localhost:8000/${userProfile.value.profile_image}`;
//             }
//             return '';
//         }
//     }
// });

//test
// onMounted(async () => {
//     await authStore.checkAuth();
//     if (authStore.isAuthenticated) {
//         try {
//             const response = await fetch('http://localhost:8000/user/profile/', {
//                 method: 'GET',
//                 credentials: 'include'
//             });

//             if (response.ok) {
//                 userProfile.value = await response.json();
//             } else {
//                 errorMessage.value = `Failed to fetch user profile: ${response.status} ${response.statusText}`;
//                 console.error(errorMessage.value);
//             }
//         } catch (error) {
//             errorMessage.value = "An error occurred while fetching the user profile.";
//             console.error(errorMessage.value, error);
//         }
//     } else {
//         errorMessage.value = "User is not authenticated.";
//     }
//     loading.value = false;
// });

// const profileImageUrl = computed(() => {
//   if (userProfile.value && userProfile.value.profile_image) {
//     return `http://localhost:8000/${userProfile.value.profile_image}`;
//   }
//   return '';
// });
//

export default {
  data() {
    return {
      isDropdownOpen: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
  },
};

</script>

<style scoped>
.container-pt-4 {
    background-color: #15202b;
    color: white;
}


.nav-items {
    background-color: red;
    display: inline-flex;
    padding: 0 1em 0 1em;

}

.navbar {
    width: 100vw;
    display: flex;
    flex-direction: row;
    background-color: aquamarine;

}
</style>
