import React from 'react'
import {
  Box, Typography, Container, Grid, Card, CardContent, Button,
  Chip, Avatar
} from '@mui/material'
import {
  Science as ScienceIcon,
  Explore as ExploreIcon,
  Download as DownloadIcon,
  TrendingUp as TrendingIcon
} from '@mui/icons-material'

const HeroSection = () => {
  const scrollToCatalog = () => {
    const element = document.getElementById('catalog')
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <Box
      id="hero"
      sx={{
        background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 50%, #1B5E20 100%)',
        position: 'relative',
        overflow: 'hidden',
        pt: { xs: 12, md: 16 },
        pb: { xs: 8, md: 12 },
        color: 'white'
      }}
    >
      {/* Фоновые элементы */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 70%, rgba(66,165,245,0.2) 0%, transparent 50%)
          `,
          animation: 'float 6s ease-in-out infinite alternate'
        }}
      />

      <Container maxWidth="xl" sx={{ position: 'relative', zIndex: 1 }}>
        <Grid container spacing={6} alignItems="center">
          {/* Левая часть - основная информация */}
          <Grid item xs={12} lg={7}>
            <Box textAlign={{ xs: 'center', lg: 'left' }}>
              {/* Badges */}
              <Box display="flex" gap={2} mb={3} justifyContent={{ xs: 'center', lg: 'flex-start' }} flexWrap="wrap">
                <Chip
                  label="🏛️ СО РАН"
                  sx={{
                    background: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontWeight: 600,
                    backdropFilter: 'blur(10px)'
                  }}
                />
                <Chip
                  label="🌊 Озеро Байкал"
                  sx={{
                    background: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontWeight: 600,
                    backdropFilter: 'blur(10px)'
                  }}
                />
                <Chip
                  label="🦠 17 коллекций"
                  sx={{
                    background: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontWeight: 600,
                    backdropFilter: 'blur(10px)'
                  }}
                />
              </Box>

              {/* Заголовок */}
              <Typography
                variant="h2"
                component="h1"
                sx={{
                  fontWeight: 900,
                  mb: 3,
                  fontSize: { xs: '2.5rem', md: '3.5rem', lg: '4rem' },
                  background: 'linear-gradient(45deg, #ffffff 30%, #E3F2FD 90%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  lineHeight: 1.1
                }}
              >
                Микроорганизмы
                <br />
                <span style={{ fontSize: '0.8em' }}>озера Байкал</span>
              </Typography>

              {/* Подзаголовок */}
              <Typography
                variant="h5"
                sx={{
                  mb: 4,
                  opacity: 0.95,
                  fontWeight: 400,
                  lineHeight: 1.4,
                  maxWidth: 600
                }}
              >
                Сибирский институт физиологии и биохимии растений СО РАН представляет
                уникальные коллекции экстремофильных микроорганизмов
              </Typography>

              {/* Ключевые цифры */}
              <Grid container spacing={3} sx={{ mb: 5, maxWidth: 500 }}>
                <Grid item xs={4}>
                  <Box textAlign="center">
                    <Typography variant="h3" fontWeight="bold" color="primary.light">
                      77
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      штаммов
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={4}>
                  <Box textAlign="center">
                    <Typography variant="h3" fontWeight="bold" color="success.light">
                      12
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      коллекций
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={4}>
                  <Box textAlign="center">
                    <Typography variant="h3" fontWeight="bold" color="warning.light">
                      5
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      типов
                    </Typography>
                  </Box>
                </Grid>
              </Grid>

              {/* Кнопки действий */}
              <Box display="flex" gap={2} flexWrap="wrap" justifyContent={{ xs: 'center', lg: 'flex-start' }}>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<ExploreIcon />}
                  onClick={scrollToCatalog}
                  sx={{
                    background: 'rgba(255,255,255,0.2)',
                    backdropFilter: 'blur(10px)',
                    color: 'white',
                    py: 1.5,
                    px: 4,
                    fontSize: '1.1rem',
                    fontWeight: 600,
                    border: '1px solid rgba(255,255,255,0.3)',
                    '&:hover': {
                      background: 'rgba(255,255,255,0.3)',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 8px 25px rgba(0,0,0,0.3)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  Исследовать каталог
                </Button>

                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<DownloadIcon />}
                  sx={{
                    color: 'white',
                    borderColor: 'rgba(255,255,255,0.5)',
                    py: 1.5,
                    px: 4,
                    fontSize: '1.1rem',
                    fontWeight: 600,
                    '&:hover': {
                      borderColor: 'white',
                      background: 'rgba(255,255,255,0.1)',
                      transform: 'translateY(-2px)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  Скачать данные
                </Button>
              </Box>
            </Box>
          </Grid>

          {/* Правая часть - карточки особенностей */}
          <Grid item xs={12} lg={5}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <Card
                  sx={{
                    background: 'rgba(255,255,255,0.1)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: 'white',
                    height: '100%'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <Avatar
                      sx={{
                        background: 'linear-gradient(45deg, #42A5F5, #1E88E5)',
                        width: 60,
                        height: 60,
                        mx: 'auto',
                        mb: 2
                      }}
                    >
                      ❄️
                    </Avatar>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Психрофилы
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Холодолюбивые микроорганизмы, адаптированные к низким температурам
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Card
                  sx={{
                    background: 'rgba(255,255,255,0.1)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: 'white',
                    height: '100%'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <Avatar
                      sx={{
                        background: 'linear-gradient(45deg, #FF7043, #F4511E)',
                        width: 60,
                        height: 60,
                        mx: 'auto',
                        mb: 2
                      }}
                    >
                      🔥
                    </Avatar>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Термофилы
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Теплолюбивые организмы из геотермальных источников
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Card
                  sx={{
                    background: 'rgba(255,255,255,0.1)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: 'white',
                    height: '100%'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <Avatar
                      sx={{
                        background: 'linear-gradient(45deg, #FFA726, #FF9800)',
                        width: 60,
                        height: 60,
                        mx: 'auto',
                        mb: 2
                      }}
                    >
                      🧂
                    </Avatar>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Галофилы
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Солелюбивые микроорганизмы высокой солености
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Card
                  sx={{
                    background: 'rgba(255,255,255,0.1)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: 'white',
                    height: '100%'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <Avatar
                      sx={{
                        background: 'linear-gradient(45deg, #66BB6A, #4CAF50)',
                        width: 60,
                        height: 60,
                        mx: 'auto',
                        mb: 2
                      }}
                    >
                      🧬
                    </Avatar>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Геномика
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Полная геномная характеристика уникальных штаммов
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Container>

      <style>
        {`
          @keyframes float {
            from {
              transform: translateY(0px) rotate(0deg);
            }
            to {
              transform: translateY(-10px) rotate(2deg);
            }
          }
        `}
      </style>
    </Box>
  )
}

export default HeroSection 