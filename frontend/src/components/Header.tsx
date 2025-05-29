import React from 'react'
import {
  AppBar, Toolbar, Typography, Button, Box, Container,
  IconButton, Tooltip
} from '@mui/material'
import {
  Science as ScienceIcon,
  Home as HomeIcon,
  TableChart as TableIcon,
  Info as InfoIcon,
  AdminPanelSettings as AdminIcon
} from '@mui/icons-material'

const Header = () => {
  const handleAdminClick = () => {
    window.open('http://localhost:8001/admin/', '_blank')
  }

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <AppBar 
      position="fixed" 
      sx={{ 
        background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 100%)',
        backdropFilter: 'blur(20px)',
        boxShadow: '0 4px 30px rgba(21, 101, 192, 0.3)'
      }}
    >
      <Container maxWidth="xl">
        <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
          {/* Логотип и название */}
          <Box display="flex" alignItems="center" gap={2}>
            <Box display="flex" alignItems="center" gap={1}>
              <span style={{ fontSize: '2rem' }}>🦠</span>
              <span style={{ fontSize: '2rem' }}>🔬</span>
            </Box>
            <Box>
              <Typography variant="h5" component="div" fontWeight="bold">
                СИФИБР СО РАН
              </Typography>
              <Typography variant="caption" display="block" sx={{ opacity: 0.9 }}>
                Коллекции микроорганизмов озера Байкал
              </Typography>
            </Box>
          </Box>

          {/* Навигация */}
          <Box display="flex" alignItems="center" gap={2}>
            <Button 
              color="inherit" 
              startIcon={<HomeIcon />}
              onClick={() => scrollToSection('hero')}
              sx={{ 
                '&:hover': { 
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  transform: 'translateY(-1px)'
                },
                transition: 'all 0.2s ease'
              }}
            >
              Главная
            </Button>
            
            <Button 
              color="inherit" 
              startIcon={<TableIcon />}
              onClick={() => scrollToSection('catalog')}
              sx={{ 
                '&:hover': { 
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  transform: 'translateY(-1px)'
                },
                transition: 'all 0.2s ease'
              }}
            >
              Каталог
            </Button>

            <Button 
              color="inherit" 
              startIcon={<InfoIcon />}
              onClick={() => scrollToSection('about')}
              sx={{ 
                '&:hover': { 
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  transform: 'translateY(-1px)'
                },
                transition: 'all 0.2s ease'
              }}
            >
              О проекте
            </Button>

            <Tooltip title="Админ панель Django">
              <IconButton 
                color="inherit" 
                onClick={handleAdminClick}
                sx={{ 
                  ml: 2,
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  '&:hover': { 
                    backgroundColor: 'rgba(255,255,255,0.2)',
                    transform: 'scale(1.05)'
                  },
                  transition: 'all 0.2s ease'
                }}
              >
                <AdminIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  )
}

export default Header 