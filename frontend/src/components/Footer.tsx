import React from 'react'
import {
  Box, Typography, Container, Grid, Link, Divider,
  IconButton, Tooltip
} from '@mui/material'
import {
  Email as EmailIcon,
  Phone as PhoneIcon,
  LocationOn as LocationIcon,
  Language as WebIcon,
  GitHub as GitHubIcon,
  Science as ScienceIcon
} from '@mui/icons-material'

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        background: 'linear-gradient(135deg, #0D47A1 0%, #1565C0 100%)',
        color: 'white',
        py: 6,
        mt: 8
      }}
    >
      <Container maxWidth="xl">
        <Grid container spacing={4}>
          {/* Информация об организации */}
          <Grid item xs={12} md={4}>
            <Box display="flex" alignItems="center" gap={2} mb={3}>
              <Box display="flex" alignItems="center" gap={1}>
                <span style={{ fontSize: '2rem' }}>🦠</span>
                <span style={{ fontSize: '2rem' }}>🔬</span>
              </Box>
              <Box>
                <Typography variant="h6" fontWeight="bold">
                  СИФИБР СО РАН
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.9 }}>
                  Коллекции микроорганизмов
                </Typography>
              </Box>
            </Box>

            <Typography variant="body2" sx={{ mb: 3, opacity: 0.9, lineHeight: 1.6 }}>
              Сибирский институт физиологии и биохимии растений Сибирского отделения 
              Российской академии наук - ведущий научный центр в области исследования 
              байкальских микроорганизмов.
            </Typography>

            <Box display="flex" gap={1}>
              <Tooltip title="Официальный сайт СИФИБР">
                <IconButton 
                  color="inherit" 
                  href="http://sifibr.irk.ru" 
                  target="_blank"
                  sx={{ 
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    '&:hover': { 
                      backgroundColor: 'rgba(255,255,255,0.2)',
                      transform: 'scale(1.1)'
                    }
                  }}
                >
                  <WebIcon />
                </IconButton>
              </Tooltip>
              
              <Tooltip title="Исходный код проекта">
                <IconButton 
                  color="inherit"
                  sx={{ 
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    '&:hover': { 
                      backgroundColor: 'rgba(255,255,255,0.2)',
                      transform: 'scale(1.1)'
                    }
                  }}
                >
                  <GitHubIcon />
                </IconButton>
              </Tooltip>

              <Tooltip title="СО РАН">
                <IconButton 
                  color="inherit" 
                  href="http://www.sbras.ru" 
                  target="_blank"
                  sx={{ 
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    '&:hover': { 
                      backgroundColor: 'rgba(255,255,255,0.2)',
                      transform: 'scale(1.1)'
                    }
                  }}
                >
                  <ScienceIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Grid>

          {/* Быстрые ссылки */}
          <Grid item xs={12} md={4}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              🗂️ Разделы каталога
            </Typography>
            
            <Grid container spacing={1}>
              <Grid item xs={6}>
                <Link 
                  href="#catalog" 
                  color="inherit" 
                  underline="hover"
                  sx={{ 
                    display: 'block', 
                    py: 0.5,
                    opacity: 0.9,
                    '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                    transition: 'all 0.2s ease'
                  }}
                >
                  🦠 Бактерии
                </Link>
                <Link 
                  href="#catalog" 
                  color="inherit" 
                  underline="hover"
                  sx={{ 
                    display: 'block', 
                    py: 0.5,
                    opacity: 0.9,
                    '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                    transition: 'all 0.2s ease'
                  }}
                >
                  🧬 Археи
                </Link>
                <Link 
                  href="#catalog" 
                  color="inherit" 
                  underline="hover"
                  sx={{ 
                    display: 'block', 
                    py: 0.5,
                    opacity: 0.9,
                    '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                    transition: 'all 0.2s ease'
                  }}
                >
                  🍄 Грибы
                </Link>
              </Grid>
              
              <Grid item xs={6}>
                <Link 
                  href="#catalog" 
                  color="inherit" 
                  underline="hover"
                  sx={{ 
                    display: 'block', 
                    py: 0.5,
                    opacity: 0.9,
                    '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                    transition: 'all 0.2s ease'
                  }}
                >
                  ❄️ Психрофилы
                </Link>
                <Link 
                  href="#catalog" 
                  color="inherit" 
                  underline="hover"
                  sx={{ 
                    display: 'block', 
                    py: 0.5,
                    opacity: 0.9,
                    '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                    transition: 'all 0.2s ease'
                  }}
                >
                  🔥 Термофилы
                </Link>
                <Link 
                  href="#catalog" 
                  color="inherit" 
                  underline="hover"
                  sx={{ 
                    display: 'block', 
                    py: 0.5,
                    opacity: 0.9,
                    '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                    transition: 'all 0.2s ease'
                  }}
                >
                  🧂 Галофилы
                </Link>
              </Grid>
            </Grid>

            <Typography variant="h6" fontWeight="bold" gutterBottom sx={{ mt: 3 }}>
              📊 Данные
            </Typography>
            
            <Link 
              href="#catalog" 
              color="inherit" 
              underline="hover"
              sx={{ 
                display: 'block', 
                py: 0.5,
                opacity: 0.9,
                '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                transition: 'all 0.2s ease'
              }}
            >
              📥 Экспорт CSV
            </Link>
            <Link 
              href="#catalog" 
              color="inherit" 
              underline="hover"
              sx={{ 
                display: 'block', 
                py: 0.5,
                opacity: 0.9,
                '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                transition: 'all 0.2s ease'
              }}
            >
              🧬 Экспорт FASTA
            </Link>
            <Link 
              href="http://localhost:8001/admin/" 
              target="_blank"
              color="inherit" 
              underline="hover"
              sx={{ 
                display: 'block', 
                py: 0.5,
                opacity: 0.9,
                '&:hover': { opacity: 1, transform: 'translateX(4px)' },
                transition: 'all 0.2s ease'
              }}
            >
              ⚙️ Админ панель
            </Link>
          </Grid>

          {/* Контактная информация */}
          <Grid item xs={12} md={4}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              📞 Контакты
            </Typography>

            <Box display="flex" alignItems="center" gap={2} mb={2}>
              <LocationIcon sx={{ opacity: 0.8 }} />
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  Адрес
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  664033, Иркутск, ул. Лермонтова, 132
                </Typography>
              </Box>
            </Box>

            <Box display="flex" alignItems="center" gap={2} mb={2}>
              <PhoneIcon sx={{ opacity: 0.8 }} />
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  Телефон
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  +7 (3952) 42-47-45
                </Typography>
              </Box>
            </Box>

            <Box display="flex" alignItems="center" gap={2} mb={2}>
              <EmailIcon sx={{ opacity: 0.8 }} />
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  Email
                </Typography>
                <Link 
                  href="mailto:sifibr@sifibr.irk.ru" 
                  color="inherit" 
                  underline="hover"
                  sx={{ opacity: 0.9 }}
                >
                  sifibr@sifibr.irk.ru
                </Link>
              </Box>
            </Box>

            <Box 
              sx={{ 
                mt: 3, 
                p: 2, 
                backgroundColor: 'rgba(255,255,255,0.1)', 
                borderRadius: 2,
                border: '1px solid rgba(255,255,255,0.2)'
              }}
            >
              <Typography variant="body2" fontWeight="bold" gutterBottom>
                🌊 Озеро Байкал
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                Уникальная экосистема с эндемичными микроорганизмами, 
                адаптированными к экстремальным условиям глубочайшего озера планеты.
              </Typography>
            </Box>
          </Grid>
        </Grid>

        <Divider sx={{ my: 4, borderColor: 'rgba(255,255,255,0.2)' }} />

        {/* Нижняя часть футера */}
        <Grid container justifyContent="space-between" alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              © 2025 СИФИБР СО РАН. Все права защищены.
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.7 }}>
              Создано с ❤️ для научного сообщества
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6} textAlign={{ xs: 'left', md: 'right' }}>
            <Typography variant="caption" sx={{ opacity: 0.7 }}>
              Технологии: React.js • TypeScript • Material-UI • Django REST
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}

export default Footer 