<template>
  <div class="  ">
    <button class="" @click="logout">Logout</button>

    <!-- {{ title }} -->
    <div v-if="loading" class="w-full h-64 flex justify-center items-end">
      <svg width="48" height="48" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="animate-spin">
        <path
          d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
          class="spinner_P7sC" />
      </svg>
    </div>
    <div v-else>
      <div v-for="(articles, categoryName) in articlesByCategory" :key="categoryName">
        <h2 class="CatName">{{ categoryName }}</h2>

        <ul class="list-group">
          <div class="flex flex-col items-center">


            <li v-for="article in articles" :key="article.id"
              class="border border-gray-50 rounded-xl p-3 flex flex-col mb-4 max-w-5xl bg-white w-100" :id="'article-' + article.id">
              <p class="text-2xl">{{ article.title }}</p>
              <br>
              <a :href="article.newsapi_id" target="_blank">Read more</a>
              <hr>

              <button @click="toggleDropdown(article.id)">View Comments</button>
              <div id="news-comment-dropdown" v-if="isDropdownOpen[article.id]">

                <form @submit.prevent="postComment(article)" class="flex mt-3">
                  <textarea class="w-100 p-2 px-3 h-10 border rounded flex overflow-y-scroll no-scrollbar" v-model="newComments[article.id]"
                    placeholder="Type your comment"></textarea>
                  <button class="px-3 border rounded flex items-center justify-center bg-green-600 " type="submit">
                    <img src="../assets/post.svg" width="20">
                  </button>
                </form>


                <ul>

                  <li v-for="comment in article.comments" :key="comment.id">
                    <div class="commentbox">


                      <p class="comment-content">
                        "{{ comment.content }}"
                      </p>
                      <p class="comment-author"> -
                        {{ comment.author }}
                      </p>
                    </div>

                    <div>
                      <button class="editbutton" v-if="canEditComment(comment)"
                        @click="enableEditMode(comment.id, null)">Edit</button>
                      <button class="deletebutton" v-if="canEditComment(comment)"
                        @click="deleteComment(comment.id)">Delete</button>

                      <div v-if="editingCommentId === comment.id">
                        <textarea class="textbox" v-model="editingContent"></textarea>
                        <button class="savebutton" @click="submitEdit(comment.id, article.id, null)">Save</button>
                        <button class="cancelbutton" @click="cancelEdit">Cancel</button>
                      </div>
                    </div>
                    <button class="replybutton" @click="showReplyForm(comment.id)">Reply</button>

                    <div v-if="replyingTo === comment.id">
                      <textarea v-model="replyContent" placeholder="Type your reply"></textarea>
                      <button class="replybutton" @click="submitReply(comment.id, article.id)">Submit Reply</button>
                    </div>

                    <ul v-if="comment.replies && comment.replies.length">
                      <li v-for="reply in comment.replies" :key="reply.id">
                        <div class="commentbox">


                          <p class="comment-content">
                            "{{ reply.content }}"
                          </p>
                          <p class="comment-author"> -
                            {{ reply.author }}
                          </p>
                        </div>
                        <button class="editbutton" v-if="canEditComment(reply)"
                          @click="enableEditMode(reply.id, comment.id)">Edit</button>
                        <button class="deletebutton" v-if="canEditComment(reply)"
                          @click="deleteComment(reply.id)">Delete</button>
                        <div v-if="editingCommentId === reply.id">
                          <textarea v-model="editingContent"></textarea>
                          <button class="savebutton" @click="submitEdit(reply.id, article.id, comment.id)">Save</button>
                          <button class="cancelbutton" @click="cancelEdit">Cancel</button>
                        </div>
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>

            </li>
          </div>
        </ul>
      </div>
    </div>
    <div v-if="errorMessage">
      {{ errorMessage }}
    </div>
  </div>
</template>





<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useAuthStore } from '../store.ts';


interface Article {
  id: number;
  title: string;
  category: number;
  category_name: string;
  comments?: Comment[];
  newsapi_id: string;
}

interface Comment {
  id: number;
  content: string;
  author: string;
  replies?: Comment[];
}

interface CategoryMap {
  [categoryName: string]: Article[];
}

interface CommentMap {
  [key: number]: string;
}

const newComments = ref<CommentMap>({});

export default defineComponent({
  data() {
    return {
      isDropdownOpen: {} as Record<number, boolean>,
    };
  },
  methods: {
    toggleDropdown(articleId: number) {
      this.isDropdownOpen[articleId] = !this.isDropdownOpen[articleId];
    },
  },

  setup() {
    const title = "Main Page";
    const articlesByCategory = ref<CategoryMap>({});
    const loading = ref(true);
    const errorMessage = ref("");
    const authStore = useAuthStore();
    const replyingTo = ref<number | null>(null);
    const replyContent = ref("");
    const editingCommentId = ref<number | null>(null);
    const editingContent = ref<string>('');


    const categorizeArticles = (articles: Article[]): CategoryMap => {
      const categoryMap: CategoryMap = {};
      articles.forEach((article) => {
        const categoryName = article.category_name;
        if (!categoryMap[categoryName]) {
          categoryMap[categoryName] = [];
        }
        categoryMap[categoryName].push(article);
      });
      return categoryMap;
    };

    const fetchArticles = async () => {
      loading.value = true;
      errorMessage.value = "";

      try {
        const response = await fetch('http://localhost:8000/articleData/', {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          const articlesData: Article[] = await response.json();
          console.log('Received articles:', articlesData);

          articlesByCategory.value = categorizeArticles(articlesData);

          for (const article of articlesData) {
            console.log(`Article ID: ${article.id}, newsapi_id: ${article.newsapi_id}`);

            const commentsResponse = await fetch(`http://localhost:8000/articles/${article.id}/get_comments/`, {
              method: 'GET',
              credentials: 'include',
            });

            if (commentsResponse.ok) {
              const commentsData = await commentsResponse.json();
              article.comments = commentsData.comments;
            } else {
              console.error(`Failed to load comments for article ${article.id}: ${commentsResponse.status} ${commentsResponse.statusText}`);
            }
          }
        } else {
          errorMessage.value = `Failed to load articles: ${response.status} ${response.statusText}`;
        }
      } catch (error) {
        errorMessage.value = "An error occurred while fetching articles.";
        console.error(error);
      } finally {
        loading.value = false;
      }
    };


    const postComment = async (article: Article) => {
      console.log("Article ID:", article.id);
      console.log("New Comment Content:", newComments.value[article.id]);
      const response = await fetch(`http://localhost:8000/articles/${article.id}/post_comment/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: newComments.value[article.id].toString(),
          parent_id: null,
        }),
      });

      if (response.ok) {

        await fetchArticles();
        newComments.value[article.id] = "";

        const articleElement = document.querySelector(`#article-${article.id}`);
        if (articleElement) {
          articleElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      } else {
        errorMessage.value = `Failed to post comment: ${response.status} ${response.statusText}`;
      }
    };

    const getComments = async (article: Article) => {
      try {
        const response = await fetch(`http://localhost:8000/articles/${article.id}/comments/`, {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          const comments: Comment[] = await response.json();

          article.comments = comments;
        } else {
          errorMessage.value = `Failed to load comments: ${response.status} ${response.statusText}`;
        }
      } catch (error) {
        errorMessage.value = "An error occurred while fetching comments.";
      }
    };

    const showReplyForm = (commentId: number) => {
      replyingTo.value = commentId;
    };


    const submitReply = async (parentId: number, articleId: number) => {
      const response = await fetch(`http://localhost:8000/articles/${articleId}/post_comment/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: replyContent.value,
          parent_id: parentId,
        }),
      });

      if (response.ok) {

        await fetchArticles();
        replyContent.value = "";
        replyingTo.value = null;
      } else {
        errorMessage.value = `Failed to post reply: ${response.status} ${response.statusText}`;
      }
    };

    onMounted(async () => {
      await authStore.checkAuth();
      await fetchArticles();
    });


    const canEditComment = (comment: Comment) => {
      const canEdit = authStore.isAuthenticated && authStore.userData?.username === comment.author;
      console.log(`Can edit comment by ${comment.author}:`, canEdit);
      return canEdit;
    };


    const enableEditMode = (commentId: number, parentId: number | null) => {
      for (const categoryName in articlesByCategory.value) {
        for (const article of articlesByCategory.value[categoryName]) {
          let comment = article.comments?.find(c => c.id === commentId);
          if (!comment && parentId) {

            const parentComment = article.comments?.find(c => c.id === parentId);
            comment = parentComment?.replies?.find(r => r.id === commentId);
          }
          if (comment) {
            editingCommentId.value = commentId;
            editingContent.value = comment.content;
            return;
          }
        }
      }
    };


    const submitEdit = async (commentId: number, articleId: number, parentId: number | null) => {

      let url = `http://localhost:8000/articles/comment/edit/${commentId}/`;

      const response = await fetch(url, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: editingContent.value,
        }),
      });

      if (response.ok) {
        await fetchArticles();
        editingCommentId.value = null;
        editingContent.value = '';
      } else {
        const errorData = await response.json();
        errorMessage.value = errorData.message || `Failed to edit comment/reply: ${response.status}`;
      }
    };

    const cancelEdit = () => {
      editingCommentId.value = null;
      editingContent.value = '';
    };


    const deleteComment = async (commentId: number) => {
      const response = await fetch(`http://localhost:8000/comments/delete/${commentId}/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },

      });

      if (response.ok) {

        await fetchArticles();
      } else {

        const errorData = await response.json();
        errorMessage.value = errorData.message || `Failed to delete comment: ${response.status}`;
      }
    };

    function logout() {
      authStore.logout();
    }

    onMounted(async () => {
      await fetchArticles();
    });

    return {
      title,
      articlesByCategory,
      loading,
      errorMessage,
      authStore,
      newComments,
      postComment,
      getComments,
      deleteComment,
      replyingTo,
      replyContent,
      showReplyForm,
      submitReply,
      editingCommentId,
      editingContent,
      canEditComment,
      enableEditMode,
      submitEdit,
      cancelEdit,
      logout,
    };
  },
});
</script>

<style scoped>
.h1 {
  max-width: 100%;
  margin: 0;
}

.loading-message {
  font-style: italic;
  color: #888;
}

.button {
  background-color: brown;
}

.category-container {
  border: 4px solid #d3d3d3;
  border-radius: 5px;
  background-color: #c7ba9e;
  margin: 20px;
}

.CatName {
  font-size: 50px;
  text-transform: capitalize;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

.list-group {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.list-group-item {
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #1e2732;
  color: #fff;
  margin: 10px auto;
  border-radius: 12px;
  max-width: 1000px;
}

.title3 {
  font-size: 35px;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}

.link3 {
  font-size: 26px;
  color: #0d40af;
}

.comment-container {
  margin-top: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  background-color: #d4af4a;
}

.reply-container {
  margin-left: 20px;
}

.error-message {
  color: #ff0000;
  margin-top: 20px;
}

.textbox {
  width: 80%;
  height: 100px;
  border-radius: 8px;
}


.editbutton,
.logout-button,
.replybutton,
.deletebutton,
.cancelbutton,
.savebutton,
.replybutton {
  width: 100%;
  max-width: 125px;
  height: 45px;
  border-radius: 8px;
  font-size: 58%;
  margin: 2px;


}

.posty {
  background-color: rgb(112, 221, 50);
  color: #fff;
  text-transform: uppercase;
  font-weight: bolder;
  transition: background-color 0.3s ease;
  width: 100%;
  max-width: 250px;
  height: 50px;
  border-radius: 8px;
  font-size: 78%;

}

.posty:hover {
  background-color: #1f7c1f;
}

.commentbox {
  border-radius: 5px;
  background-color: #88afbe;
  border: 1px solid #ddd;
  padding: 10px;
  font-style: italic;
  font-family: Arial, Helvetica, sans-serif;
  width: 100%;
  margin: 10px;
}

.deletebutton {
  background-color: rgb(245, 75, 63);
  color: #fff;
  text-transform: uppercase;
  font-weight: bolder;
  transition: background-color 0.3s ease;
}

.deletebutton:hover {
  background-color: #990f0f;
}

.replybutton {
  background-color: rgb(50, 130, 221);
  color: #fff;
  text-transform: uppercase;
  font-weight: bolder;
  transition: background-color 0.3s ease;
}

.replybutton:hover {
  background-color: #3639c9;
}

.editbutton {
  background-color: rgb(230, 217, 49);
  color: #fff;
  text-transform: uppercase;
  font-weight: bolder;
  transition: background-color 0.3s ease;
}

.editbutton:hover {
  background-color: #aaa81d;
}

.savebutton {
  background-color: rgb(60, 122, 24);
  color: #fff;
  text-transform: uppercase;
  font-weight: bolder;
  transition: background-color 0.3s ease;
}

.savebutton:hover {
  background-color: #31df31;
}

.cancelbutton {
  background-color: rgb(199, 40, 138);
  color: #fff;
  text-transform: uppercase;
  font-weight: bolder;
  transition: background-color 0.3s ease;
}

.cancelbutton:hover {
  background-color: #920c4f;
}
</style>
