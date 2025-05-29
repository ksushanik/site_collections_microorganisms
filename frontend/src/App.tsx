import React, { Suspense } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { CssBaseline, Box, Container, Typography, CircularProgress } from '@mui/material'
import ErrorBoundary from './components/ErrorBoundary'

// Импорт компонентов
import Header from './components/Header'
import HeroSection from './components/HeroSection'
import AboutSection from './components/AboutSection'
import Footer from './components/Footer'

// Ленивая загрузка StrainTable
const StrainTable = React.lazy(() => import('./components/StrainTable'))

// Байкальская тема
const theme = createTheme({
  palette: {
    primary: {
      main: '#1565C0',
      light: '#42A5F5',
      dark: '#0D47A1',
    },
    secondary: {
      main: '#26A69A',
      light: '#80CBC4',
      dark: '#00695C',
    },
    background: {
      default: '#F8F9FA',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 900,
    },
    h2: {
      fontWeight: 800,
    },
    h3: {
      fontWeight: 700,
    },
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 20px rgba(0,0,0,0.08)',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
        },
      },
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          {/* Фиксированная шапка */}
          <Header />

          {/* Основной контент */}
          <Box component="main" sx={{ flexGrow: 1 }}>
            {/* Hero секция */}
            <HeroSection />

            {/* Каталог штаммов */}
            <Box 
              id="catalog"
              sx={{ 
                py: { xs: 8, md: 12 },
                background: '#ffffff'
              }}
            >
              <Container maxWidth="xl">
                <Box textAlign="center" mb={6}>
                  <Typography
                    variant="h3"
                    component="h2"
                    fontWeight="bold"
                    gutterBottom
                    sx={{
                      background: 'linear-gradient(45deg, #1565C0 30%, #0D47A1 90%)',
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      mb: 2
                    }}
                  >
                    🔬 Каталог штаммов
                  </Typography>
                  <Typography 
                    variant="h6" 
                    color="text.secondary"
                    sx={{ maxWidth: 600, mx: 'auto' }}
                  >
                    Интерактивный каталог микроорганизмов озера Байкал с возможностями 
                    поиска, фильтрации и экспорта данных
                  </Typography>
                </Box>

                <Suspense 
                  fallback={
                    <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="400px">
                      <CircularProgress size={48} thickness={4} />
                      <Typography variant="h6" color="text.secondary" sx={{ mt: 2 }}>
                        🔬 Загрузка каталога...
                      </Typography>
                    </Box>
                  }
                >
                  <StrainTable />
                </Suspense>
              </Container>
            </Box>

            {/* О проекте */}
            <AboutSection />
          </Box>

          {/* Футер */}
          <Footer />
        </Box>
      </ErrorBoundary>
    </ThemeProvider>
  )
}

export default App 