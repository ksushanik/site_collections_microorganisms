// Типы данных для штаммов микроорганизмов
export interface Strain {
  id: string;
  strain_number: string;
  full_name: string;
  scientific_name: string;
  genus: string;
  species: string;
  collection: Collection;
  
  // Биологические характеристики
  organism_type: 'bacteria' | 'archaea' | 'fungi' | 'yeast' | 'other';
  habitat_type: 'baikal_surface' | 'baikal_deep' | 'baikal_bottom' | 'baikal_coastal' | 'soil' | 'sediment' | 'other';
  
  // Экстремофильные свойства
  is_psychrophile: boolean;
  is_thermophile: boolean;
  is_halophile: boolean;
  is_acidophile: boolean;
  is_alkaliphile: boolean;
  is_barophile: boolean;
  
  // Биотехнологические свойства
  produces_antibiotics: boolean;
  produces_enzymes: boolean;
  produces_metabolites: boolean;
  nitrogen_fixation: boolean;
  
  // Физико-химические параметры
  optimal_temperature?: number;
  temperature_range_min?: number;
  temperature_range_max?: number;
  optimal_ph?: number;
  ph_range_min?: number;
  ph_range_max?: number;
  
  // Геолокация
  latitude?: number;
  longitude?: number;
  depth_meters?: number;
  geographic_location?: string;
  isolation_source?: string;
  
  // Геномика
  has_genome_sequence: boolean;
  genome_size?: number;
  gc_content?: number;
  
  // Метаданные
  isolation_date?: string;
  deposit_date?: string;
  depositor?: string;
  isolation_method?: string;
  special_properties?: string;
  alternative_numbers?: string;
  is_available: boolean;
  
  // Timestamps
  created_at: string;
  updated_at: string;
}

export interface Collection {
  id: string;
  code: string;
  name: string;
  description?: string;
  collection_type: 'bacterial' | 'archaeal' | 'fungal' | 'mixed' | 'specialized';
  access_level: 'public' | 'restricted' | 'private';
  curator_name?: string;
  curator_email?: string;
  established_date?: string;
  is_active: boolean;
  strain_count?: number;
}

export interface GenomeSequence {
  id: string;
  strain: string;
  sequence_type: 'complete' | 'draft' | 'scaffold' | '16s_rrna' | 'plasmid';
  accession_number?: string;
  database?: string;
  sequence_length?: number;
  submission_date?: string;
  sequence_data?: string;
}

export interface Publication {
  id: string;
  title: string;
  authors: string;
  journal?: string;
  year: number;
  volume?: string;
  pages?: string;
  doi?: string;
  pmid?: string;
  abstract?: string;
  url?: string;
  strains: string[];
}

// Фильтры для поиска
export interface StrainFilters {
  search?: string;
  collection?: string;
  organism_type?: string;
  habitat_type?: string;
  extremophiles?: 'psychrophiles' | 'thermophiles' | 'halophiles' | 'acidophiles' | 'alkaliphiles' | 'barophiles';
  has_genome?: boolean;
  produces_antibiotics?: boolean;
  produces_enzymes?: boolean;
  nitrogen_fixation?: boolean;
  min_temperature?: number;
  max_temperature?: number;
  min_ph?: number;
  max_ph?: number;
  max_depth?: number;
}

// API Response типы
export interface ApiResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface Statistics {
  total_strains: number;
  collections_count: number;
  extremophiles: {
    psychrophiles: number;
    thermophiles: number;
    halophiles: number;
    acidophiles: number;
    alkaliphiles: number;
    barophiles: number;
  };
  habitat_distribution: Record<string, number>;
  organism_types: Record<string, number>;
  biotechnology: {
    antibiotic_producers: number;
    enzyme_producers: number;
    nitrogen_fixers: number;
    metabolite_producers: number;
  };
  genomics: {
    sequenced: number;
    avg_genome_size?: number;
    avg_gc_content?: number;
  };
} 