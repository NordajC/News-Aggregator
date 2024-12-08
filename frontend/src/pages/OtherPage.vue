<template>
  <div class="user-profile">
    <h1>User Profile Page</h1>
    <div v-if="loading" class="loading-message">
      Loading user profile...
    </div>
    <div v-else-if="authStore.isAuthenticated && userProfile" class="profile-container">
      <p class="email-label">Email: {{ userProfile.email }}</p>
      <p class="dob-label"> Date of Birth: {{ userProfile.date_of_birth }}</p>
      <p class="img-label">Profile Image: <img :src="profileImageUrl" alt="Profile Image" class="profile-image" /></p>
      <p>Favorite Categories: {{ favoriteCategoryNames.join(', ') }}</p>

      <form @submit.prevent="updateProfileFields" class="profile-form">
        <label>Email:</label>
        <input v-model="newEmail" class="profile-input" />

        <label>Date of Birth:</label>
        <input type="date" v-model="newDateOfBirth" class="profile-input" />

        <label>Profile Picture:</label>
        <input type="file" accept="image/*" @change="handleProfileImageChange" class="profile-input" />

        <label>Favorite Categories:</label>
        <select multiple v-model="selectedCategories" class="profile-select">
          <option v-for="category in allCategories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>


        <button type="submit" class="update-button">Update Profile</button>
      </form>
    </div>
    <div v-else-if="authStore.isAuthenticated" class="error-message">

      {{ errorMessage || 'No user profile available.' }}
    </div>
    <div v-else class="error-message">
      <p>User is not authenticated.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../store.ts';

const authStore = useAuthStore();
const userProfile = ref(null);
const allCategories = ref([]);
const loading = ref(true);
const errorMessage = ref("");
const newEmail = ref('');
const newDateOfBirth = ref('');
const profileImageFile = ref(null);
const selectedCategories = ref([]);

const profileImageUrl = computed(() => {
  if (userProfile.value && userProfile.value.profile_image) {
    return `http://localhost:8000/${userProfile.value.profile_image}`;
  }
  return '';
});

const handleProfileImageChange = (event) => {
  profileImageFile.value = event.target.files[0];
};



const favoriteCategoryNames = computed(() => {
  if (!userProfile.value || !allCategories.value.length) return [];
  return userProfile.value.favorite_categories.map(categoryId => 
    allCategories.value.find(category => category.id === categoryId)?.name
  ).filter(name => name); 
});


const fetchCategories = async () => {
  try {
    const response = await fetch('http://localhost:8000/categories/', { 
      method: 'GET',
      credentials: 'include'
    });
    if (response.ok) {
      allCategories.value = await response.json();
    } else {
      console.error('Failed to fetch categories');
    }
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};


const updateSelectedCategories = () => {
  if (userProfile.value && allCategories.value.length) {
    selectedCategories.value = userProfile.value.favorite_categories.map(categoryId =>
      allCategories.value.find(category => category.id === categoryId)?.id || categoryId
    );
  }
};

const updateProfileFields = async () => {
  const formData = new FormData();
  formData.append('email', newEmail.value);
  console.log('Email:', newEmail.value);

  formData.append('date_of_birth', newDateOfBirth.value);
  console.log('Date of Birth:', newDateOfBirth.value);

  formData.append('profile_image', profileImageFile.value);


  
  
  const categoriesJSON = JSON.stringify(selectedCategories.value);
  formData.append('favorite_categories', categoriesJSON);

  try {
    const response = await fetch('http://localhost:8000/user/profile/update/', {
      method: 'POST',
      body: formData,
      credentials: 'include',
    });

    if (response.ok) {
      console.log('Profile updated successfully');
      window.location.reload();
    } else {
      console.error(`Failed to update profile: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    console.error('An error occurred while updating the user profile:', error);
  }
};

onMounted(async () => {
  await authStore.checkAuth();
  if (authStore.isAuthenticated) {
    loading.value = true;
    await fetchCategories();
    try {
      const response = await fetch('http://localhost:8000/user/profile/', {
        method: 'GET',
        credentials: 'include'
      });

      if (response.ok) {
        userProfile.value = await response.json();

        newEmail.value = userProfile.value.email;
        newDateOfBirth.value = userProfile.value.date_of_birth;


        updateSelectedCategories();
      } else {
        errorMessage.value = `Failed to fetch user profile: ${response.status} ${response.statusText}`;
        console.error(errorMessage.value);
      }
    } catch (error) {
      errorMessage.value = "An error occurred while fetching the user profile.";
      console.error(errorMessage.value, error);
    }
  } else {
    errorMessage.value = "User is not authenticated.";
  }
  loading.value = false;
});
</script>


<style scoped>
.user-profile {
  max-width: 600px;
  margin: 0 auto;

}

.loading-message {
  margin: 20px 0;
  padding: 10px;
  background-color: #d8e2b4;
  border: 1px solid #cfcfa5;
  color: #d3c75f;
  font-size: x-large;
}

.profile-container {
  padding: 20px;
  border: 1px solid #d3d3d3;
  border-radius: 5px;
  background-color: #1e2732;
}

.profile-image {
  max-width: 200px;
  height: auto;
  margin-bottom: 1 0px;
}


.profile-form {
  margin-top: 20px;
}

.profile-input,
.profile-select {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  box-sizing: border-box;
}

.update-button {
  background-color: #1d9c3b;
  color: #ffffff;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.update-button:hover {
  background-color: #2ecf44; 
}

.error-message {
  margin: 20px 0;
  padding: 10px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.dob-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: bold;

}

.email-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: bold;

}

.img-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: bold;

}

.img-label img {
  max-width: 350px;
  max-height: 250px;
  width: auto;
  height: auto;
  border: 4px solid #d3d3d3;
  border-radius: 5px;

}

html,
body {
  background-color: #721c24;
  margin: 0;
  padding: 0;
}</style>
