import axios from 'axios';
import type { ApiResponse, Strain, Collection, Statistics, StrainFilters } from '../types/strain.types';

// Базовая конфигурация API
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL.endsWith('/api') ? API_BASE_URL : `${API_BASE_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Для работы с CORS
});

// Добавляем CSRF токен для Django
api.interceptors.request.use(
  (config) => {
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Получение CSRF токена из cookie
function getCsrfToken(): string | null {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Обработка ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API методы для штаммов
export const strainService = {
  // Получить список штаммов с фильтрацией
  getStrains: async (filters?: StrainFilters, page = 1): Promise<ApiResponse<Strain>> => {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }
    
    params.append('page', page.toString());
    
    const response = await api.get<ApiResponse<Strain>>(`/strains/?${params.toString()}`);
    return response.data;
  },

  // Получить конкретный штамм
  getStrain: async (id: string): Promise<Strain> => {
    const response = await api.get<Strain>(`/strains/${id}/`);
    return response.data;
  },

  // Получить байкальские экстремофилы
  getBaikalExtremes: async (): Promise<ApiResponse<Strain>> => {
    const response = await api.get<ApiResponse<Strain>>('/strains/baikal/');
    return response.data;
  },

  // Получить экстремофилы
  getExtremophiles: async (): Promise<ApiResponse<Strain>> => {
    const response = await api.get<ApiResponse<Strain>>('/strains/extremophiles/');
    return response.data;
  },

  // Экспорт в CSV
  exportCsv: async (filters?: StrainFilters): Promise<Blob> => {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }

    const response = await api.get(`/strains/export_csv/?${params.toString()}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Экспорт в FASTA
  exportFasta: async (filters?: StrainFilters): Promise<Blob> => {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }

    const response = await api.get(`/strains/export_fasta/?${params.toString()}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Получить статистику
  getStatistics: async (): Promise<Statistics> => {
    const response = await api.get<Statistics>('/strains/statistics/');
    return response.data;
  },
};

// API методы для коллекций
export const collectionService = {
  // Получить список коллекций
  getCollections: async (): Promise<ApiResponse<Collection>> => {
    const response = await api.get<ApiResponse<Collection>>('/collections/');
    return response.data;
  },

  // Получить конкретную коллекцию
  getCollection: async (id: string): Promise<Collection> => {
    const response = await api.get<Collection>(`/collections/${id}/`);
    return response.data;
  },

  // Получить штаммы коллекции
  getCollectionStrains: async (id: string): Promise<ApiResponse<Strain>> => {
    const response = await api.get<ApiResponse<Strain>>(`/collections/${id}/strains/`);
    return response.data;
  },
};

// Утилиты для скачивания файлов
export const downloadUtils = {
  downloadBlob: (blob: Blob, filename: string) => {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  downloadCsv: async (filters?: StrainFilters, filename = 'strains_export.csv') => {
    const blob = await strainService.exportCsv(filters);
    downloadUtils.downloadBlob(blob, filename);
  },

  downloadFasta: async (filters?: StrainFilters, filename = 'sequences_export.fasta') => {
    const blob = await strainService.exportFasta(filters);
    downloadUtils.downloadBlob(blob, filename);
  },
};

export default api; 