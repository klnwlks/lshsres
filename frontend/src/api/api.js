import api from '../api/axios';

export const authService = {
  login: (credentials) => api.post('/', credentials),
  getUserProfile: (userId) => api.get(`/user/${userId}/`),
};

export const chatService = {
  getGlobalMessages: () => api.get('/board/'),
  postGlobalMessage: (content) => api.post('/board/post/', { content }),
  getSectionMessages: (sectionId) => api.get(`/section/${sectionId}/`),
  postSectionMessage: (sectionId, content) => 
    api.post(`/section/${sectionId}/post/`, { content }),
};