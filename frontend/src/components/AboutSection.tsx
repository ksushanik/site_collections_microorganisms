import React from 'react'
import {
  Box, Typography, Container, Grid, Card, CardContent, 
  List, ListItem, ListItemIcon, ListItemText, Chip
} from '@mui/material'
import {
  Science as ScienceIcon,
  Explore as ExploreIcon,
  School as SchoolIcon,
  Public as PublicIcon,
  Analytics as AnalyticsIcon,
  Biotech as BiotechIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material'

const AboutSection = () => {
  return (
    <Box
      id="about"
      sx={{
        py: { xs: 8, md: 12 },
        background: 'linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%)'
      }}
    >
      <Container maxWidth="xl">
        {/* Заголовок секции */}
        <Box textAlign="center" mb={8}>
          <Chip 
            label="О ПРОЕКТЕ" 
            sx={{ 
              mb: 3,
              background: 'linear-gradient(45deg, #1565C0, #0D47A1)',
              color: 'white',
              fontWeight: 600,
              fontSize: '0.9rem',
              px: 3,
              py: 0.5
            }} 
          />
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
              mb: 3
            }}
          >
            Микроорганизмы Байкала
          </Typography>
          <Typography 
            variant="h6" 
            color="text.secondary" 
            sx={{ maxWidth: 800, mx: 'auto', lineHeight: 1.6 }}
          >
            Цифровая платформа для исследования уникальных микроорганизмов 
            самого глубокого озера планеты
          </Typography>
        </Box>

        <Grid container spacing={6} alignItems="center">
          {/* Левая часть - основная информация */}
          <Grid item xs={12} lg={7}>
            <Typography variant="h4" fontWeight="bold" gutterBottom color="primary">
              🏛️ СИФИБР СО РАН
            </Typography>
            
            <Typography variant="h6" gutterBottom sx={{ opacity: 0.8, mb: 3 }}>
              Сибирский институт физиологии и биохимии растений
            </Typography>

            <Typography variant="body1" paragraph sx={{ fontSize: '1.1rem', lineHeight: 1.7 }}>
              Наш институт является ведущим научным центром Сибирского отделения РАН 
              в области исследования микроорганизмов. Уже более 50 лет мы изучаем 
              уникальную микробиоту озера Байкал - самого глубокого и чистого 
              пресноводного озера планеты.
            </Typography>

            <Typography variant="body1" paragraph sx={{ fontSize: '1.1rem', lineHeight: 1.7 }}>
              Данная платформа объединяет <strong>17 специализированных коллекций</strong> 
              микроорганизмов, каждая из которых содержит уникальные штаммы, 
              адаптированные к экстремальным условиям байкальской экосистемы.
            </Typography>

            {/* Список достижений */}
            <List sx={{ mt: 4 }}>
              <ListItem sx={{ pl: 0 }}>
                <ListItemIcon>
                  <CheckIcon color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="850,000+ штаммов микроорганизмов"
                  secondary="Крупнейшая коллекция байкальских микроорганизмов в мире"
                />
              </ListItem>
              
              <ListItem sx={{ pl: 0 }}>
                <ListItemIcon>
                  <CheckIcon color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="Полная геномная характеристика"
                  secondary="Секвенирование ДНК уникальных экстремофильных штаммов"
                />
              </ListItem>
              
              <ListItem sx={{ pl: 0 }}>
                <ListItemIcon>
                  <CheckIcon color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="Соответствие международным стандартам"
                  secondary="FAIR принципы, WFCC и MIRRI стандарты"
                />
              </ListItem>
              
              <ListItem sx={{ pl: 0 }}>
                <ListItemIcon>
                  <CheckIcon color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="Open Science подход"
                  secondary="Открытый доступ к данным для мирового научного сообщества"
                />
              </ListItem>
            </List>
          </Grid>

          {/* Правая часть - карточки направлений */}
          <Grid item xs={12} lg={5}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <Card 
                  sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%)',
                    border: '1px solid #2196F3',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(33, 150, 243, 0.3)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <BiotechIcon sx={{ fontSize: 48, color: '#1565C0', mb: 2 }} />
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Биотехнологии
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Разработка биопрепаратов и промышленных ферментов
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Card 
                  sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%)',
                    border: '1px solid #4CAF50',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(76, 175, 80, 0.3)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <AnalyticsIcon sx={{ fontSize: 48, color: '#2E7D32', mb: 2 }} />
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Биоинформатика
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Геномный анализ и филогенетические исследования
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Card 
                  sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%)',
                    border: '1px solid #FF9800',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(255, 152, 0, 0.3)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <SchoolIcon sx={{ fontSize: 48, color: '#EF6C00', mb: 2 }} />
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Образование
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Подготовка специалистов в области микробиологии
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6}>
                <Card 
                  sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%)',
                    border: '1px solid #9C27B0',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(156, 39, 176, 0.3)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center', py: 3 }}>
                    <PublicIcon sx={{ fontSize: 48, color: '#7B1FA2', mb: 2 }} />
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Экология
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Мониторинг экосистемы озера Байкал
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>
        </Grid>

        {/* Статистика проекта */}
        <Box 
          sx={{ 
            mt: 8, 
            p: 4, 
            background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 100%)',
            borderRadius: 4,
            color: 'white',
            textAlign: 'center'
          }}
        >
          <Typography variant="h5" fontWeight="bold" gutterBottom>
            🌊 Уникальность озера Байкал
          </Typography>
          
          <Grid container spacing={4} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={3}>
              <Typography variant="h4" fontWeight="bold">1,642м</Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>Максимальная глубина</Typography>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Typography variant="h4" fontWeight="bold">25млн</Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>Возраст (лет)</Typography>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Typography variant="h4" fontWeight="bold">20%</Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>Пресной воды Земли</Typography>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Typography variant="h4" fontWeight="bold">80%</Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>Эндемичных видов</Typography>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </Box>
  )
}

export default AboutSection 