import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react()
  ],
  
  define: {
    'process.env.VITE_API_URL': JSON.stringify(
      process.env.VITE_API_URL || 'http://localhost:8001'
    ),
  },
  
  server: {
    host: '0.0.0.0',
    port: 3000,
    
    // Проксируем API запросы к Django
    proxy: {
      '/api': {
        target: process.env.NODE_ENV === 'development' 
          ? (process.env.VITE_API_BASE_URL || 'http://backend:8000')
          : 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
      '/admin': {
        target: process.env.NODE_ENV === 'development' 
          ? (process.env.VITE_API_BASE_URL || 'http://backend:8000')
          : 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
      '/static': {
        target: process.env.NODE_ENV === 'development' 
          ? (process.env.VITE_API_BASE_URL || 'http://backend:8000')
          : 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      }
    },
    
    // CORS настройки для Django
    cors: {
      origin: ['http://localhost:8001', 'http://127.0.0.1:8001'],
      credentials: true
    }
  },
  
  build: {
    outDir: 'dist',
    sourcemap: true,
    
    // Оптимизация для продакшена  
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          mui: ['@mui/material', '@mui/icons-material'],
          charts: ['chart.js', 'react-chartjs-2'],
          maps: ['leaflet', 'react-leaflet']
        }
      }
    },
    
    // Настройки для больших приложений
    chunkSizeWarningLimit: 1000
  },
  
  // CSS настройки
  css: {
    postcss: {
      plugins: []
    },
    devSourcemap: true
  },
  
  // Предварительная сборка зависимостей
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      '@mui/material',
      '@mui/icons-material',
      'axios'
    ]
  },
  
  // Резолвинг модулей  
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@pages': '/src/pages',
      '@services': '/src/services',
      '@types': '/src/types',
      '@utils': '/src/utils',
      '@hooks': '/src/hooks'
    }
  }
}) 