import axios from 'axios';
import type { Job, Candidate } from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

console.log('API Base URL:', API_BASE);

const api = axios.create({
  baseURL: API_BASE,
  timeout: 300000, // 5 minutes for ranking
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.data);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.method?.toUpperCase(), response.config.url, response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.config?.method?.toUpperCase(), error.config?.url, error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export const jobsApi = {
  list: () => api.get<Job[]>('/jobs'),
  create: (data: { title: string; description: string }) => api.post<Job>('/jobs', data),
  get: (jobId: string) => api.get<Job>(`/jobs/${jobId}`),
  update: (jobId: string, data: { description: string }) => api.put<Job>(`/jobs/${jobId}`, data),
};

export const candidatesApi = {
  list: (jobId: string) => api.get<Candidate[]>(`/jobs/${jobId}/candidates`),
  get: (candidateId: string) => api.get<Candidate>(`/candidates/${candidateId}`),
  uploadResumes: (jobId: string, files: File[]) => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    return api.post(`/jobs/${jobId}/resumes`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const rankingApi = {
  trigger: (jobId: string) => api.post(`/jobs/${jobId}/rank`),
  getRankings: (jobId: string) => api.get<Candidate[]>(`/jobs/${jobId}/rankings`),
  rescore: (candidateId: string) => api.post(`/candidates/${candidateId}/rescore`),
};

export default api;
