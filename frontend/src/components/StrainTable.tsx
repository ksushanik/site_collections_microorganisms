import React, { useState, useEffect, useMemo } from 'react'
import {
  Box, Typography, Card, CardContent, Grid, Paper, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Chip, Button, TextField,
  FormControl, InputLabel, Select, MenuItem, CircularProgress, IconButton,
  Tooltip, Alert, TablePagination, Dialog, DialogTitle, DialogContent,
  DialogActions, Divider
} from '@mui/material'
import { 
  Search, Download, Refresh, Science as ScienceIcon, 
  Map as MapIcon, Biotech, Psychology, Visibility as ViewIcon,
  LocationOn as LocationIcon, Close as CloseIcon, Thermostat,
  Science, WaterDrop
} from '@mui/icons-material'
import type { SelectChangeEvent } from '@mui/material/Select'
import { strainService, type Strain } from '../services/strainService'
import AdvancedSearch from './AdvancedSearch'

// Интерфейс для фильтров поиска (импортируем из AdvancedSearch)
interface SearchFilters {
  query: string
  scientificName: string
  collections: string[]
  organismTypes: string[]
  temperatureRange: [number, number]
  isPsychrophile: boolean | null
  isThermophile: boolean | null
  phRange: [number, number]
  regions: string[]
  depthRange: [number, number]
  coordinates: {
    enabled: boolean
    minLat: number
    maxLat: number
    minLng: number
    maxLng: number
  }
  isHalophile: boolean | null
  hasGenomeSequence: boolean | null
  producesAntibiotics: boolean | null
  producesEnzymes: boolean | null
  nitrogenFixation: boolean | null
  isolationYear: [number, number]
  hasPublication: boolean | null
}

const StrainTable = () => {
  const [strains, setStrains] = useState<Strain[]>([])
  const [filteredStrains, setFilteredStrains] = useState<Strain[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Пагинация
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(25)
  
  // Сортировка
  const [sortBy, setSortBy] = useState<string>('code')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  // Модальное окно для деталей штамма
  const [selectedStrain, setSelectedStrain] = useState<Strain | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)

  // Загрузка данных
  useEffect(() => {
    const loadStrains = async () => {
      try {
        setLoading(true)
        const data = await strainService.getAllStrains()
        setStrains(data)
        setFilteredStrains(data)
      } catch (err) {
        setError('Ошибка загрузки штаммов: ' + (err as Error).message)
      } finally {
        setLoading(false)
      }
    }

    loadStrains()
  }, [])

  // Функция применения фильтров
  const applyFilters = (filters: SearchFilters) => {
    let filtered = [...strains]

    // Быстрый поиск
    if (filters.query) {
      const query = filters.query.toLowerCase()
      filtered = filtered.filter(strain => 
        strain.full_name.toLowerCase().includes(query) ||
        strain.scientific_name.toLowerCase().includes(query) ||
        strain.genus.toLowerCase().includes(query) ||
        strain.species.toLowerCase().includes(query) ||
        strain.collection_name?.toLowerCase().includes(query) ||
        strain.collection_code?.toLowerCase().includes(query) ||
        strain.isolation_source?.toLowerCase().includes(query) ||
        strain.geographic_location?.toLowerCase().includes(query) ||
        strain.special_properties?.toLowerCase().includes(query) ||
        strain.description?.toLowerCase().includes(query)
      )
    }

    // Поиск по научному названию
    if (filters.scientificName) {
      const name = filters.scientificName.toLowerCase()
      filtered = filtered.filter(strain => 
        strain.scientific_name.toLowerCase().includes(name) ||
        strain.genus.toLowerCase().includes(name) ||
        strain.species.toLowerCase().includes(name)
      )
    }

    // Фильтр по коллекциям
    if (filters.collections.length > 0) {
      filtered = filtered.filter(strain => 
        filters.collections.includes(strain.collection_code)
      )
    }

    // Фильтр по типам организмов
    if (filters.organismTypes.length > 0) {
      filtered = filtered.filter(strain => 
        filters.organismTypes.includes(strain.organism_type)
      )
    }

    // Фильтр по температуре
    if (filters.temperatureRange[0] > -5 || filters.temperatureRange[1] < 100) {
      filtered = filtered.filter(strain => {
        const minTemp = strain.temperature_range_min ? parseFloat(strain.temperature_range_min) : null
        const maxTemp = strain.temperature_range_max ? parseFloat(strain.temperature_range_max) : null
        
        if (minTemp == null || maxTemp == null) return false
        
        return minTemp >= filters.temperatureRange[0] && maxTemp <= filters.temperatureRange[1]
      })
    }

    // Фильтр по pH
    if (filters.phRange[0] > 0 || filters.phRange[1] < 14) {
      filtered = filtered.filter(strain => {
        const minPh = strain.ph_range_min ? parseFloat(strain.ph_range_min) : null
        const maxPh = strain.ph_range_max ? parseFloat(strain.ph_range_max) : null
        
        if (minPh == null || maxPh == null) return false
        
        return minPh >= filters.phRange[0] && maxPh <= filters.phRange[1]
      })
    }

    // Фильтр по глубине
    if (filters.depthRange[0] > 0 || filters.depthRange[1] < 1700) {
      filtered = filtered.filter(strain => {
        const depth = strain.depth_meters
        if (depth == null) return false
        
        return depth >= filters.depthRange[0] && depth <= filters.depthRange[1]
      })
    }

    // Фильтр по регионам
    if (filters.regions.length > 0) {
      filtered = filtered.filter(strain => 
        filters.regions.some(region => 
          strain.geographic_location?.includes(region) ||
          strain.isolation_source?.includes(region)
        )
      )
    }

    // Фильтр по координатам
    if (filters.coordinates.enabled) {
      filtered = filtered.filter(strain => {
        if (!strain.latitude || !strain.longitude) return false
        
        const lat = parseFloat(strain.latitude.toString())
        const lng = parseFloat(strain.longitude.toString())
        
        return lat >= filters.coordinates.minLat && 
               lat <= filters.coordinates.maxLat &&
               lng >= filters.coordinates.minLng && 
               lng <= filters.coordinates.maxLng
      })
    }

    // Фильтр по году изоляции
    if (filters.isolationYear[0] > 1970 || filters.isolationYear[1] < 2025) {
      filtered = filtered.filter(strain => {
        if (!strain.isolation_date) return false
        
        const year = new Date(strain.isolation_date).getFullYear()
        return year >= filters.isolationYear[0] && year <= filters.isolationYear[1]
      })
    }

    // Биологические фильтры
    if (filters.isPsychrophile === true) {
      filtered = filtered.filter(strain => strain.is_psychrophile === true)
    }

    if (filters.isThermophile === true) {
      filtered = filtered.filter(strain => strain.is_thermophile === true)
    }

    if (filters.isHalophile === true) {
      filtered = filtered.filter(strain => strain.is_halophile === true)
    }

    if (filters.hasGenomeSequence === true) {
      filtered = filtered.filter(strain => strain.has_genome_sequence === true)
    }

    if (filters.producesAntibiotics === true) {
      filtered = filtered.filter(strain => strain.produces_antibiotics === true)
    }

    if (filters.producesEnzymes === true) {
      filtered = filtered.filter(strain => strain.produces_enzymes === true)
    }

    if (filters.nitrogenFixation === true) {
      filtered = filtered.filter(strain => strain.nitrogen_fixation === true)
    }

    setFilteredStrains(filtered)
    setPage(0) // Сброс пагинации при новом поиске
  }

  // Сортированные данные
  const sortedStrains = useMemo(() => {
    return [...filteredStrains].sort((a, b) => {
      let aVal: string
      let bVal: string
      
      if (sortBy === 'collection') {
        aVal = a.collection_code || ''
        bVal = b.collection_code || ''
      } else if (sortBy === 'code') {
        aVal = a.full_name || ''
        bVal = b.full_name || ''
      } else {
        aVal = a[sortBy as keyof typeof a]?.toString() || ''
        bVal = b[sortBy as keyof typeof b]?.toString() || ''
      }
      
      if (sortOrder === 'asc') {
        return aVal.localeCompare(bVal)
      } else {
        return bVal.localeCompare(aVal)
      }
    })
  }, [filteredStrains, sortBy, sortOrder])

  // Данные для отображения с пагинацией
  const displayedStrains = useMemo(() => {
    const startIndex = page * rowsPerPage
    return sortedStrains.slice(startIndex, startIndex + rowsPerPage)
  }, [sortedStrains, page, rowsPerPage])

  // Обработка смены сортировки
  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortOrder('asc')
    }
  }

  // Обработка экспорта
  const handleExport = () => {
    const csvContent = [
      ['Код', 'Научное название', 'Коллекция', 'Тип', 'Источник', 'Координаты'].join(','),
      ...filteredStrains.map(strain => [
        strain.full_name,
        strain.scientific_name,
        strain.collection_code,
        strain.organism_type_display || strain.organism_type,
        strain.isolation_source || '',
        strain.latitude && strain.longitude ? `${strain.latitude}, ${strain.longitude}` : ''
      ].join(','))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `strains_export_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
  }

  const handleOpenDetails = (strain: Strain) => {
    setSelectedStrain(strain)
    setDetailsOpen(true)
  }

  const handleCloseDetails = () => {
    setDetailsOpen(false)
    setSelectedStrain(null)
  }

  if (loading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="400px">
        <CircularProgress size={48} thickness={4} />
        <Typography variant="h6" color="text.secondary" sx={{ mt: 2 }}>
          🔬 Загрузка каталога...
        </Typography>
      </Box>
    )
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    )
  }

  return (
    <Box>
      {/* Расширенный поиск */}
      <AdvancedSearch 
        onSearch={applyFilters}
        loading={loading}
        resultsCount={filteredStrains.length}
      />

      {/* Панель управления */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6">
          Найдено штаммов: <strong>{filteredStrains.length}</strong> из {strains.length}
        </Typography>
        
        <Box display="flex" gap={2} alignItems="center">
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Сортировка</InputLabel>
            <Select
              value={sortBy}
              label="Сортировка"
              onChange={(e) => setSortBy(e.target.value)}
            >
              <MenuItem value="code">По коду</MenuItem>
              <MenuItem value="scientific_name">По названию</MenuItem>
              <MenuItem value="collection_code">По коллекции</MenuItem>
              <MenuItem value="organism_type">По типу</MenuItem>
            </Select>
          </FormControl>
          
          <Tooltip title="Экспорт в CSV">
            <IconButton 
              onClick={handleExport}
              disabled={filteredStrains.length === 0}
              color="primary"
            >
              <Download />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Таблица данных */}
      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table sx={{ minWidth: 650 }} aria-label="таблица штаммов">
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell 
                onClick={() => handleSort('code')}
                sx={{ cursor: 'pointer', fontWeight: 'bold' }}
              >
                Код штамма
              </TableCell>
              <TableCell 
                onClick={() => handleSort('scientific_name')}
                sx={{ cursor: 'pointer', fontWeight: 'bold' }}
              >
                Научное название
              </TableCell>
              <TableCell 
                onClick={() => handleSort('collection_code')}
                sx={{ cursor: 'pointer', fontWeight: 'bold' }}
              >
                Коллекция
              </TableCell>
              <TableCell 
                onClick={() => handleSort('organism_type')}
                sx={{ cursor: 'pointer', fontWeight: 'bold' }}
              >
                Тип
              </TableCell>
              <TableCell>Источник выделения</TableCell>
              <TableCell>Координаты</TableCell>
              <TableCell>Параметры</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {displayedStrains.map((strain) => (
              <TableRow key={strain.full_name} hover>
                <TableCell>
                  <Typography variant="body2" fontWeight="bold" color="primary">
                    {strain.full_name}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" fontStyle="italic">
                    {strain.scientific_name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" display="block">
                    {strain.genus} {strain.species}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip 
                    label={strain.collection_code} 
                    size="small" 
                    color="primary" 
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={strain.organism_type_display || strain.organism_type}
                    size="small"
                    color="secondary"
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {strain.isolation_source}
                  </Typography>
                </TableCell>
                <TableCell>
                  {strain.latitude && strain.longitude ? (
                    <Box display="flex" alignItems="center" gap={1}>
                      <LocationIcon color="action" fontSize="small" />
                      <Typography variant="body2">
                        {parseFloat(strain.latitude.toString()).toFixed(3)}, {parseFloat(strain.longitude.toString()).toFixed(3)}
                      </Typography>
                    </Box>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      Не указаны
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <Box display="flex" flexDirection="column" gap={0.5}>
                    {strain.optimal_temperature && (
                      <Chip 
                        label={`T: ${strain.optimal_temperature}°C`} 
                        size="small" 
                        color="info"
                      />
                    )}
                    {strain.optimal_ph && (
                      <Chip 
                        label={`pH: ${strain.optimal_ph}`} 
                        size="small" 
                        color="success"
                      />
                    )}
                    {strain.depth_meters && (
                      <Chip 
                        label={`${strain.depth_meters}м`} 
                        size="small" 
                        color="default"
                      />
                    )}
                  </Box>
                </TableCell>
                <TableCell>
                  <Tooltip title="Подробности">
                    <IconButton size="small" color="primary" onClick={() => handleOpenDetails(strain)}>
                      <ViewIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Пагинация */}
      <TablePagination
        component="div"
        count={filteredStrains.length}
        page={page}
        onPageChange={(_, newPage) => setPage(newPage)}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={(e) => {
          setRowsPerPage(parseInt(e.target.value, 10))
          setPage(0)
        }}
        rowsPerPageOptions={[10, 25, 50, 100]}
        labelRowsPerPage="Строк на странице:"
        labelDisplayedRows={({ from, to, count }) => `${from}-${to} из ${count}`}
      />

      {/* Модальное окно для деталей штамма */}
      <Dialog 
        open={detailsOpen} 
        onClose={handleCloseDetails}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">
              Подробная информация о штамме
            </Typography>
            <IconButton onClick={handleCloseDetails}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {selectedStrain && (
            <Box>
              {/* Основная информация */}
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom color="primary">
                    {selectedStrain.full_name}
                  </Typography>
                  <Typography variant="h5" gutterBottom sx={{ fontStyle: 'italic' }}>
                    {selectedStrain.scientific_name}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" gutterBottom>
                    {selectedStrain.genus} {selectedStrain.species} {selectedStrain.subspecies}
                  </Typography>
                  
                  <Box mt={2}>
                    <Chip 
                      label={selectedStrain.collection_code} 
                      color="primary" 
                      sx={{ mr: 1, mb: 1 }}
                    />
                    <Chip 
                      label={selectedStrain.organism_type_display || selectedStrain.organism_type} 
                      color="secondary"
                      sx={{ mr: 1, mb: 1 }}
                    />
                    {selectedStrain.is_baikal_endemic && (
                      <Chip 
                        label="🏔️ Байкальский эндемик" 
                        color="success"
                        sx={{ mr: 1, mb: 1 }}
                      />
                    )}
                  </Box>
                </CardContent>
              </Card>

              <Grid container spacing={2}>
                {/* Физико-химические параметры */}
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        🌡️ Физико-химические параметры
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      
                      {selectedStrain.optimal_temperature && (
                        <Box display="flex" alignItems="center" mb={1}>
                          <Thermostat color="info" sx={{ mr: 1 }} />
                          <Typography>
                            Оптимальная температура: <strong>{selectedStrain.optimal_temperature}°C</strong>
                          </Typography>
                        </Box>
                      )}
                      
                      {selectedStrain.temperature_range_min && selectedStrain.temperature_range_max && (
                        <Typography variant="body2" color="text.secondary" sx={{ ml: 4, mb: 1 }}>
                          Диапазон: {selectedStrain.temperature_range_min}°C - {selectedStrain.temperature_range_max}°C
                        </Typography>
                      )}
                      
                      {selectedStrain.optimal_ph && (
                        <Box display="flex" alignItems="center" mb={1}>
                          <WaterDrop color="primary" sx={{ mr: 1 }} />
                          <Typography>
                            Оптимальный pH: <strong>{selectedStrain.optimal_ph}</strong>
                          </Typography>
                        </Box>
                      )}
                      
                      {selectedStrain.ph_range_min && selectedStrain.ph_range_max && (
                        <Typography variant="body2" color="text.secondary" sx={{ ml: 4, mb: 1 }}>
                          Диапазон pH: {selectedStrain.ph_range_min} - {selectedStrain.ph_range_max}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>

                {/* Биологические свойства */}
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        🧬 Биологические свойства
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      
                      <Box>
                        {selectedStrain.is_psychrophile && (
                          <Chip label="❄️ Психрофил" size="small" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.is_thermophile && (
                          <Chip label="🔥 Термофил" size="small" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.is_halophile && (
                          <Chip label="🧂 Галофил" size="small" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.is_acidophile && (
                          <Chip label="🍋 Ацидофил" size="small" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.is_alkaliphile && (
                          <Chip label="🧪 Алкалифил" size="small" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.is_barophile && (
                          <Chip label="⬇️ Барофил" size="small" sx={{ mr: 1, mb: 1 }} />
                        )}
                      </Box>
                      
                      <Typography variant="body2" sx={{ mt: 2 }}>
                        <strong>Биотехнологические свойства:</strong>
                      </Typography>
                      <Box mt={1}>
                        {selectedStrain.produces_antibiotics && (
                          <Chip label="💊 Антибиотики" size="small" color="error" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.produces_enzymes && (
                          <Chip label="⚡ Ферменты" size="small" color="warning" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.produces_metabolites && (
                          <Chip label="🧪 Метаболиты" size="small" color="info" sx={{ mr: 1, mb: 1 }} />
                        )}
                        {selectedStrain.nitrogen_fixation && (
                          <Chip label="🌱 Азотфиксация" size="small" color="success" sx={{ mr: 1, mb: 1 }} />
                        )}
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>

                {/* Локация и изоляция */}
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        📍 Местоположение и изоляция
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      
                      {selectedStrain.geographic_location && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Географическое положение:</strong><br />
                          {selectedStrain.geographic_location}
                        </Typography>
                      )}
                      
                      {selectedStrain.isolation_source && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Источник выделения:</strong><br />
                          {selectedStrain.isolation_source}
                        </Typography>
                      )}
                      
                      {selectedStrain.latitude && selectedStrain.longitude && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Координаты:</strong><br />
                          {parseFloat(selectedStrain.latitude.toString()).toFixed(6)}°N, {parseFloat(selectedStrain.longitude.toString()).toFixed(6)}°E
                        </Typography>
                      )}
                      
                      {selectedStrain.depth_meters && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Глубина:</strong> {selectedStrain.depth_meters} метров
                        </Typography>
                      )}
                      
                      {selectedStrain.habitat_type_display && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Тип среды обитания:</strong><br />
                          {selectedStrain.habitat_type_display}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>

                {/* Геномика и даты */}
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        🧬 Геномика и метаданные
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      
                      {selectedStrain.has_genome_sequence && (
                        <Box mb={2}>
                          <Chip label="✅ Геном секвенирован" color="success" />
                          {selectedStrain.genome_size && (
                            <Typography variant="body2" sx={{ mt: 1 }}>
                              <strong>Размер генома:</strong> {(selectedStrain.genome_size / 1000000).toFixed(2)} Мбп
                            </Typography>
                          )}
                          {selectedStrain.gc_content && (
                            <Typography variant="body2">
                              <strong>GC-состав:</strong> {selectedStrain.gc_content}%
                            </Typography>
                          )}
                        </Box>
                      )}
                      
                      {selectedStrain.isolation_date && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Дата изоляции:</strong><br />
                          {new Date(selectedStrain.isolation_date).toLocaleDateString('ru-RU')}
                        </Typography>
                      )}
                      
                      {selectedStrain.deposit_date && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Дата депонирования:</strong><br />
                          {new Date(selectedStrain.deposit_date).toLocaleDateString('ru-RU')}
                        </Typography>
                      )}
                      
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Статус:</strong>{' '}
                        <Chip 
                          label={selectedStrain.is_available ? "Доступен" : "Недоступен"} 
                          color={selectedStrain.is_available ? "success" : "error"}
                          size="small"
                        />
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                {/* Описание и особые свойства */}
                {(selectedStrain.description || selectedStrain.special_properties) && (
                  <Grid item xs={12}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          📝 Описание и особые свойства
                        </Typography>
                        <Divider sx={{ mb: 2 }} />
                        
                        {selectedStrain.description && (
                          <Typography variant="body2" sx={{ mb: 2 }}>
                            <strong>Описание:</strong><br />
                            {selectedStrain.description}
                          </Typography>
                        )}
                        
                        {selectedStrain.special_properties && (
                          <Typography variant="body2">
                            <strong>Особые свойства:</strong><br />
                            {selectedStrain.special_properties}
                          </Typography>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                )}
              </Grid>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions>
          <Button onClick={handleCloseDetails} variant="outlined">
            Закрыть
          </Button>
          {selectedStrain && (
            <Button 
              variant="contained" 
              color="primary"
              onClick={() => {
                // Здесь можно добавить функционал экспорта конкретного штамма
                console.log('Экспорт штамма:', selectedStrain.full_name)
              }}
            >
              Экспорт данных
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default StrainTable 