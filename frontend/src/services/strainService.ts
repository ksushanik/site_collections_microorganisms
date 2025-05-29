interface Strain {
  id: string
  collection: string
  collection_name: string
  collection_code: string
  strain_number: string
  alternative_numbers: string
  full_name: string
  scientific_name: string
  genus: string
  species: string
  subspecies: string
  organism_type: string
  organism_type_display: string
  isolation_source: string
  habitat_type: string
  habitat_type_display: string
  geographic_location: string
  latitude: string | null
  longitude: string | null
  depth_meters: number | null
  optimal_temperature: string | null
  temperature_range_min: string | null
  temperature_range_max: string | null
  optimal_ph: string | null
  ph_range_min: string | null
  ph_range_max: string | null
  is_psychrophile: boolean
  is_thermophile: boolean
  is_halophile: boolean
  is_acidophile: boolean
  is_alkaliphile: boolean
  is_barophile: boolean
  produces_antibiotics: boolean
  produces_enzymes: boolean
  produces_metabolites: boolean
  nitrogen_fixation: boolean
  genome_size: number | null
  gc_content: number | null
  has_genome_sequence: boolean
  isolation_date: string
  deposit_date: string
  is_available: boolean
  is_type_strain: boolean
  description: string
  special_properties: string
  cultivation_notes: string
  is_baikal_endemic: boolean
  extremophile_types: string[]
  genome_sequences: any[]
  genome_count: number
  created_at: string
  updated_at: string
}

class StrainService {
  private baseUrl = '/api'

  async getAllStrains(): Promise<Strain[]> {
    try {
      const response = await fetch(`${this.baseUrl}/strains/`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Обрабатываем ответ от Django API
      if (Array.isArray(data)) {
        return data
      } else if (data.results && Array.isArray(data.results)) {
        return data.results
      } else {
        throw new Error('Неожиданный формат данных от API')
      }
    } catch (error) {
      console.error('Ошибка загрузки штаммов:', error)
      throw error
    }
  }

  async getStrainById(id: string): Promise<Strain> {
    try {
      const response = await fetch(`${this.baseUrl}/strains/${id}/`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Ошибка загрузки штамма:', error)
      throw error
    }
  }

  async searchStrains(query: string): Promise<Strain[]> {
    try {
      const response = await fetch(`${this.baseUrl}/strains/search/?q=${encodeURIComponent(query)}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      return Array.isArray(data) ? data : data.results || []
    } catch (error) {
      console.error('Ошибка поиска штаммов:', error)
      throw error
    }
  }

  async exportStrains(format: 'csv' | 'fasta'): Promise<Blob> {
    try {
      const response = await fetch(`${this.baseUrl}/export/${format}/`)
      
      if (!response.ok) {
        throw new Error('Ошибка экспорта данных')
      }
      
      return await response.blob()
    } catch (error) {
      console.error('Ошибка экспорта:', error)
      throw error
    }
  }
}

export const strainService = new StrainService()
export type { Strain } 