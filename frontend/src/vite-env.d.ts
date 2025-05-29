/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
  readonly VITE_DJANGO_HOST: string
  readonly VITE_DJANGO_PORT: string
  // Добавляйте сюда другие переменные окружения с префиксом VITE_
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 