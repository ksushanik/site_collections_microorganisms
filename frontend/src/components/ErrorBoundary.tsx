import { Component, type ErrorInfo, type ReactNode } from 'react'
import { Alert, AlertTitle, Button, Box, Typography } from '@mui/material'
import { Refresh } from '@mui/icons-material'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
  errorInfo?: ErrorInfo
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    // Обновляем состояние, чтобы следующий рендер показал fallback UI
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Логируем ошибку
    console.error('ErrorBoundary поймал ошибку:', error, errorInfo)
    
    this.setState({
      error,
      errorInfo
    })

    // Здесь можно отправить ошибку в сервис мониторинга (Sentry, LogRocket и т.д.)
    // logErrorToService(error, errorInfo)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined })
  }

  render() {
    if (this.state.hasError) {
      // Если передан кастомный fallback, используем его
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Стандартный fallback UI
      return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
          <Alert severity="error" sx={{ mb: 2 }}>
            <AlertTitle>⚠️ Произошла ошибка</AlertTitle>
            К сожалению, что-то пошло не так при загрузке приложения.
          </Alert>

          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Что можно попробовать:
            </Typography>
            <Typography variant="body2" color="text.secondary" component="ul" sx={{ pl: 2 }}>
              <li>Обновить страницу</li>
              <li>Проверить подключение к интернету</li>
              <li>Очистить кэш браузера</li>
              <li>Связаться с поддержкой</li>
            </Typography>
          </Box>

          <Button
            variant="contained"
            startIcon={<Refresh />}
            onClick={this.handleRetry}
            sx={{ mr: 2 }}
          >
            Попробовать снова
          </Button>

          <Button
            variant="outlined"
            onClick={() => window.location.reload()}
          >
            Перезагрузить страницу
          </Button>

          {/* Показываем детали ошибки в development режиме */}
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <Box sx={{ mt: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle2" gutterBottom>
                Детали ошибки (только в режиме разработки):
              </Typography>
              <Typography 
                variant="body2" 
                component="pre" 
                sx={{ 
                  fontSize: '0.75rem', 
                  overflow: 'auto',
                  fontFamily: 'monospace'
                }}
              >
                {this.state.error.toString()}
                {this.state.errorInfo?.componentStack}
              </Typography>
            </Box>
          )}
        </Box>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary 