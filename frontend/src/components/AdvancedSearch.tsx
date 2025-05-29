import React, { useState, useCallback, useMemo } from 'react'
import {
  Box, Paper, Typography, Grid, TextField, FormControl, InputLabel, 
  Select, MenuItem, Slider, Autocomplete, Chip, Button, IconButton,
  Accordion, AccordionSummary, AccordionDetails, FormControlLabel,
  Switch, Divider, Tooltip, Badge, Alert, Collapse
} from '@mui/material'
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Clear as ClearIcon,
  Save as SaveIcon,
  Restore as RestoreIcon,
  ExpandMore as ExpandIcon,
  LocationOn as LocationIcon,
  Science as ScienceIcon,
  Thermostat as TempIcon,
  WaterDrop as PhIcon,
  Biotech as BioIcon,
  Close as CloseIcon
} from '@mui/icons-material'

interface SearchFilters {
  // Текстовый поиск
  query: string
  scientificName: string
  
  // Коллекции и типы
  collections: string[]
  organismTypes: string[]
  
  // Температурные характеристики
  temperatureRange: [number, number]
  isPsychrophile: boolean | null
  isThermophile: boolean | null
  
  // pH характеристики
  phRange: [number, number]
  
  // Географические фильтры
  regions: string[]
  depthRange: [number, number]
  coordinates: {
    enabled: boolean
    minLat: number
    maxLat: number
    minLng: number
    maxLng: number
  }
  
  // Биологические свойства
  isHalophile: boolean | null
  hasGenomeSequence: boolean | null
  producesAntibiotics: boolean | null
  producesEnzymes: boolean | null
  nitrogenFixation: boolean | null
  
  // Метаданные
  isolationYear: [number, number]
  hasPublication: boolean | null
}

interface AdvancedSearchProps {
  onSearch: (filters: SearchFilters) => void
  loading?: boolean
  resultsCount?: number
}

const AdvancedSearch: React.FC<AdvancedSearchProps> = ({ 
  onSearch, 
  loading = false, 
  resultsCount = 0 
}) => {
  // Состояние фильтров
  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    scientificName: '',
    collections: [],
    organismTypes: [],
    temperatureRange: [-5, 100],
    isPsychrophile: null,
    isThermophile: null,
    phRange: [0, 14],
    regions: [],
    depthRange: [0, 1700],
    coordinates: {
      enabled: false,
      minLat: 51.0,
      maxLat: 56.0,
      minLng: 103.0,
      maxLng: 110.0
    },
    isHalophile: null,
    hasGenomeSequence: null,
    producesAntibiotics: null,
    producesEnzymes: null,
    nitrogenFixation: null,
    isolationYear: [1970, 2025],
    hasPublication: null
  })

  // Состояние UI
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [savedSearches, setSavedSearches] = useState<Array<{id: string, name: string, filters: SearchFilters}>>([])
  const [searchName, setSearchName] = useState('')

  // Предзаполненные данные для автодополнения
  const availableCollections = [
    'СИФИБР-АВТ', 'СИФИБР-ПСИ', 'СИФИБР-ТЕР', 'СИФИБР-ГАЛ', 
    'СИФИБР-ГЕН', 'СИФИБР-БИО', 'СИФИБР-ЭКО'
  ]

  const availableOrganismTypes = [
    'bacteria', 'archaea', 'fungi', 'microalgae'
  ]

  const baykalRegions = [
    'Северный Байкал', 'Средний Байкал', 'Южный Байкал',
    'Малое Море', 'Баргузинский залив', 'Чивыркуйский залив',
    'Провал', 'Слюдянка', 'Листвянка', 'Ольхон'
  ]

  const scientificNameSuggestions = [
    'Pseudomonas baikalensis', 'Bacillus baikalensis', 'Sphingomonas baikalensis',
    'Methylobacterium baikalense', 'Flavobacterium baikalense', 'Psychrobacter baikalensis'
  ]

  // Обновление фильтров
  const updateFilter = useCallback((key: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }, [])

  // Сброс всех фильтров
  const clearFilters = useCallback(() => {
    setFilters({
      query: '',
      scientificName: '',
      collections: [],
      organismTypes: [],
      temperatureRange: [-5, 100],
      isPsychrophile: null,
      isThermophile: null,
      phRange: [0, 14],
      regions: [],
      depthRange: [0, 1700],
      coordinates: {
        enabled: false,
        minLat: 51.0,
        maxLat: 56.0,
        minLng: 103.0,
        maxLng: 110.0
      },
      isHalophile: null,
      hasGenomeSequence: null,
      producesAntibiotics: null,
      producesEnzymes: null,
      nitrogenFixation: null,
      isolationYear: [1970, 2025],
      hasPublication: null
    })
  }, [])

  // Сохранение поискового запроса
  const saveSearch = useCallback(() => {
    if (!searchName.trim()) return
    
    const newSearch = {
      id: Date.now().toString(),
      name: searchName,
      filters: { ...filters }
    }
    
    setSavedSearches(prev => [...prev, newSearch])
    setSearchName('')
  }, [searchName, filters])

  // Загрузка сохраненного поиска
  const loadSearch = useCallback((searchFilters: SearchFilters) => {
    setFilters(searchFilters)
    onSearch(searchFilters)
  }, [onSearch])

  // Подсчет активных фильтров
  const activeFiltersCount = useMemo(() => {
    let count = 0
    if (filters.query) count++
    if (filters.scientificName) count++
    if (filters.collections.length) count++
    if (filters.organismTypes.length) count++
    if (filters.temperatureRange[0] > -5 || filters.temperatureRange[1] < 100) count++
    if (filters.phRange[0] > 0 || filters.phRange[1] < 14) count++
    if (filters.regions.length) count++
    if (filters.depthRange[0] > 0 || filters.depthRange[1] < 1700) count++
    if (filters.coordinates.enabled) count++
    if (filters.isPsychrophile !== null) count++
    if (filters.isThermophile !== null) count++
    if (filters.isHalophile !== null) count++
    if (filters.hasGenomeSequence !== null) count++
    if (filters.producesAntibiotics !== null) count++
    if (filters.producesEnzymes !== null) count++
    if (filters.nitrogenFixation !== null) count++
    if (filters.isolationYear[0] > 1970 || filters.isolationYear[1] < 2025) count++
    if (filters.hasPublication !== null) count++
    return count
  }, [filters])

  // Обработка поиска
  const handleSearch = useCallback(() => {
    onSearch(filters)
  }, [filters, onSearch])

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      {/* Заголовок */}
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <Box display="flex" alignItems="center" gap={2}>
          <Typography variant="h6" display="flex" alignItems="center" gap={1}>
            <SearchIcon color="primary" />
            Расширенный поиск
          </Typography>
          {activeFiltersCount > 0 && (
            <Chip 
              label={`${activeFiltersCount} фильтр${activeFiltersCount > 1 ? 'ов' : ''}`} 
              color="primary" 
              size="small" 
            />
          )}
        </Box>
        
        <Box display="flex" gap={1}>
          <Tooltip title="Показать/скрыть дополнительные фильтры">
            <IconButton 
              onClick={() => setShowAdvanced(!showAdvanced)}
              color={showAdvanced ? "primary" : "default"}
            >
              <Badge badgeContent={activeFiltersCount} color="primary">
                <FilterIcon />
              </Badge>
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Очистить все фильтры">
            <IconButton onClick={clearFilters} disabled={activeFiltersCount === 0}>
              <ClearIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Быстрый поиск */}
      <Grid container spacing={3} alignItems="center" mb={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Быстрый поиск"
            placeholder="Название штамма, род, вид, коллекция..."
            value={filters.query}
            onChange={(e) => updateFilter('query', e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} />
            }}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Autocomplete
            options={scientificNameSuggestions}
            value={filters.scientificName}
            onChange={(_, value) => updateFilter('scientificName', value || '')}
            renderInput={(params) => (
              <TextField 
                {...params} 
                label="Научное название"
                placeholder="Начните вводить..."
              />
            )}
            freeSolo
          />
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={handleSearch}
            disabled={loading}
            startIcon={<SearchIcon />}
          >
            Поиск
          </Button>
        </Grid>
      </Grid>

      {/* Результаты */}
      {resultsCount > 0 && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Найдено штаммов: <strong>{resultsCount}</strong>
        </Alert>
      )}

      {/* Расширенные фильтры */}
      <Collapse in={showAdvanced}>
        <Divider sx={{ mb: 3 }} />
        
        <Grid container spacing={3}>
          {/* Коллекции и типы */}
          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="subtitle1" display="flex" alignItems="center" gap={1}>
                  <ScienceIcon color="primary" />
                  Коллекции и типы организмов
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Autocomplete
                      multiple
                      options={availableCollections}
                      value={filters.collections}
                      onChange={(_, value) => updateFilter('collections', value)}
                      renderTags={(value, getTagProps) =>
                        value.map((option, index) => (
                          <Chip
                            key={option}
                            label={option}
                            {...getTagProps({ index })}
                            color="primary"
                            size="small"
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField {...params} label="Коллекции" placeholder="Выберите коллекции" />
                      )}
                    />
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Autocomplete
                      multiple
                      options={availableOrganismTypes}
                      value={filters.organismTypes}
                      onChange={(_, value) => updateFilter('organismTypes', value)}
                      getOptionLabel={(option) => ({
                        bacteria: 'Бактерии',
                        archaea: 'Археи', 
                        fungi: 'Грибы',
                        microalgae: 'Микроводоросли'
                      }[option] || option)}
                      renderTags={(value, getTagProps) =>
                        value.map((option, index) => (
                          <Chip
                            key={option}
                            label={({
                              bacteria: '🦠 Бактерии',
                              archaea: '🧬 Археи',
                              fungi: '🍄 Грибы',
                              microalgae: '🌿 Микроводоросли'
                            }[option] || option)}
                            {...getTagProps({ index })}
                            color="secondary"
                            size="small"
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField {...params} label="Типы организмов" placeholder="Выберите типы" />
                      )}
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>

          {/* Физико-химические параметры */}
          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="subtitle1" display="flex" alignItems="center" gap={1}>
                  <TempIcon color="primary" />
                  Температура и pH
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={4}>
                  <Grid item xs={12} md={6}>
                    <Typography gutterBottom>
                      Оптимальная температура: {filters.temperatureRange[0]}°C - {filters.temperatureRange[1]}°C
                    </Typography>
                    <Slider
                      value={filters.temperatureRange}
                      onChange={(_, value) => updateFilter('temperatureRange', value)}
                      valueLabelDisplay="auto"
                      min={-5}
                      max={100}
                      marks={[
                        { value: -5, label: '-5°C' },
                        { value: 0, label: '0°C' },
                        { value: 37, label: '37°C' },
                        { value: 100, label: '100°C' }
                      ]}
                    />
                    
                    <Box display="flex" gap={2} mt={2}>
                      <FormControlLabel
                        control={
                          <Switch
                            checked={filters.isPsychrophile === true}
                            onChange={(e) => updateFilter('isPsychrophile', e.target.checked ? true : null)}
                          />
                        }
                        label="❄️ Психрофилы"
                      />
                      <FormControlLabel
                        control={
                          <Switch
                            checked={filters.isThermophile === true}
                            onChange={(e) => updateFilter('isThermophile', e.target.checked ? true : null)}
                          />
                        }
                        label="🔥 Термофилы"
                      />
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Typography gutterBottom>
                      Оптимальный pH: {filters.phRange[0]} - {filters.phRange[1]}
                    </Typography>
                    <Slider
                      value={filters.phRange}
                      onChange={(_, value) => updateFilter('phRange', value)}
                      valueLabelDisplay="auto"
                      min={0}
                      max={14}
                      step={0.1}
                      marks={[
                        { value: 0, label: '0' },
                        { value: 7, label: '7' },
                        { value: 14, label: '14' }
                      ]}
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>

          {/* География */}
          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="subtitle1" display="flex" alignItems="center" gap={1}>
                  <LocationIcon color="primary" />
                  География и глубина
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Autocomplete
                      multiple
                      options={baykalRegions}
                      value={filters.regions}
                      onChange={(_, value) => updateFilter('regions', value)}
                      renderTags={(value, getTagProps) =>
                        value.map((option, index) => (
                          <Chip
                            key={option}
                            label={option}
                            {...getTagProps({ index })}
                            color="info"
                            size="small"
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField {...params} label="Регионы Байкала" placeholder="Выберите регионы" />
                      )}
                    />
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Typography gutterBottom>
                      Глубина: {filters.depthRange[0]}м - {filters.depthRange[1]}м
                    </Typography>
                    <Slider
                      value={filters.depthRange}
                      onChange={(_, value) => updateFilter('depthRange', value)}
                      valueLabelDisplay="auto"
                      min={0}
                      max={1700}
                      marks={[
                        { value: 0, label: '0м' },
                        { value: 200, label: '200м' },
                        { value: 1000, label: '1км' },
                        { value: 1700, label: '1.7км' }
                      ]}
                    />
                  </Grid>

                  {/* Координаты */}
                  <Grid item xs={12}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.coordinates.enabled}
                          onChange={(e) => updateFilter('coordinates', { 
                            ...filters.coordinates, 
                            enabled: e.target.checked 
                          })}
                        />
                      }
                      label="Фильтр по координатам"
                    />
                    
                    {filters.coordinates.enabled && (
                      <Grid container spacing={2} sx={{ mt: 1 }}>
                        <Grid item xs={3}>
                          <TextField
                            type="number"
                            label="Мин. широта"
                            value={filters.coordinates.minLat}
                            onChange={(e) => updateFilter('coordinates', {
                              ...filters.coordinates,
                              minLat: Number(e.target.value)
                            })}
                            inputProps={{ step: 0.001 }}
                          />
                        </Grid>
                        <Grid item xs={3}>
                          <TextField
                            type="number"
                            label="Макс. широта"
                            value={filters.coordinates.maxLat}
                            onChange={(e) => updateFilter('coordinates', {
                              ...filters.coordinates,
                              maxLat: Number(e.target.value)
                            })}
                            inputProps={{ step: 0.001 }}
                          />
                        </Grid>
                        <Grid item xs={3}>
                          <TextField
                            type="number"
                            label="Мин. долгота"
                            value={filters.coordinates.minLng}
                            onChange={(e) => updateFilter('coordinates', {
                              ...filters.coordinates,
                              minLng: Number(e.target.value)
                            })}
                            inputProps={{ step: 0.001 }}
                          />
                        </Grid>
                        <Grid item xs={3}>
                          <TextField
                            type="number"
                            label="Макс. долгота"
                            value={filters.coordinates.maxLng}
                            onChange={(e) => updateFilter('coordinates', {
                              ...filters.coordinates,
                              maxLng: Number(e.target.value)
                            })}
                            inputProps={{ step: 0.001 }}
                          />
                        </Grid>
                      </Grid>
                    )}
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>

          {/* Биологические свойства */}
          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="subtitle1" display="flex" alignItems="center" gap={1}>
                  <BioIcon color="primary" />
                  Биологические свойства
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6} md={4}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.isHalophile === true}
                          onChange={(e) => updateFilter('isHalophile', e.target.checked ? true : null)}
                        />
                      }
                      label="🧂 Галофилы"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={4}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.hasGenomeSequence === true}
                          onChange={(e) => updateFilter('hasGenomeSequence', e.target.checked ? true : null)}
                        />
                      }
                      label="🧬 Секвенированный геном"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={4}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.producesAntibiotics === true}
                          onChange={(e) => updateFilter('producesAntibiotics', e.target.checked ? true : null)}
                        />
                      }
                      label="💊 Продуцирует антибиотики"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={4}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.producesEnzymes === true}
                          onChange={(e) => updateFilter('producesEnzymes', e.target.checked ? true : null)}
                        />
                      }
                      label="⚡ Продуцирует ферменты"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={4}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.nitrogenFixation === true}
                          onChange={(e) => updateFilter('nitrogenFixation', e.target.checked ? true : null)}
                        />
                      }
                      label="🌱 Азотфиксация"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={4}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={filters.hasPublication === true}
                          onChange={(e) => updateFilter('hasPublication', e.target.checked ? true : null)}
                        />
                      }
                      label="📄 Есть публикации"
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>

          {/* Временные фильтры */}
          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="subtitle1">
                  📅 Период выделения
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography gutterBottom>
                  Год выделения: {filters.isolationYear[0]} - {filters.isolationYear[1]}
                </Typography>
                <Slider
                  value={filters.isolationYear}
                  onChange={(_, value) => updateFilter('isolationYear', value)}
                  valueLabelDisplay="auto"
                  min={1970}
                  max={2025}
                  marks={[
                    { value: 1970, label: '1970' },
                    { value: 1990, label: '1990' },
                    { value: 2010, label: '2010' },
                    { value: 2025, label: '2025' }
                  ]}
                />
              </AccordionDetails>
            </Accordion>
          </Grid>
        </Grid>

        {/* Сохранение поисков */}
        <Divider sx={{ my: 3 }} />
        
        <Box display="flex" alignItems="center" gap={2} flexWrap="wrap">
          <TextField
            size="small"
            label="Название поиска"
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            placeholder="Например: Психрофилы Северного Байкала"
          />
          
          <Button
            variant="outlined"
            startIcon={<SaveIcon />}
            onClick={saveSearch}
            disabled={!searchName.trim() || activeFiltersCount === 0}
          >
            Сохранить поиск
          </Button>
          
          {savedSearches.length > 0 && (
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Сохраненные поиски</InputLabel>
              <Select
                label="Сохраненные поиски"
                displayEmpty
                onChange={(e) => {
                  const search = savedSearches.find(s => s.id === e.target.value)
                  if (search) loadSearch(search.filters)
                }}
              >
                {savedSearches.map((search) => (
                  <MenuItem key={search.id} value={search.id}>
                    <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
                      <span>{search.name}</span>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation()
                          setSavedSearches(prev => prev.filter(s => s.id !== search.id))
                        }}
                      >
                        <CloseIcon fontSize="small" />
                      </IconButton>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}
        </Box>
      </Collapse>
    </Paper>
  )
}

export default AdvancedSearch 