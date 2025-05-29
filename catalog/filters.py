import django_filters
from django.db import models
from .models import Strain, Collection, GenomeSequence, Publication


class StrainFilter(django_filters.FilterSet):
    """Фильтр для штаммов с расширенными возможностями"""
    
    # Текстовые поля
    scientific_name = django_filters.CharFilter(lookup_expr='icontains')
    genus = django_filters.CharFilter(lookup_expr='icontains')
    species = django_filters.CharFilter(lookup_expr='icontains')
    strain_number = django_filters.CharFilter(lookup_expr='icontains')
    isolation_source = django_filters.CharFilter(lookup_expr='icontains')
    geographic_location = django_filters.CharFilter(lookup_expr='icontains')
    
    # Выбор коллекции
    collection = django_filters.ModelChoiceFilter(
        queryset=Collection.objects.filter(is_active=True)
    )
    collection_type = django_filters.ChoiceFilter(
        field_name='collection__collection_type',
        choices=Collection.COLLECTION_TYPES
    )
    
    # Диапазоны температур
    temperature_min = django_filters.NumberFilter(
        field_name='optimal_temperature',
        lookup_expr='gte'
    )
    temperature_max = django_filters.NumberFilter(
        field_name='optimal_temperature',
        lookup_expr='lte'
    )
    temperature_range_min = django_filters.NumberFilter(
        field_name='temperature_range_min',
        lookup_expr='gte'
    )
    temperature_range_max = django_filters.NumberFilter(
        field_name='temperature_range_max',
        lookup_expr='lte'
    )
    
    # Диапазоны pH
    ph_min = django_filters.NumberFilter(
        field_name='optimal_ph',
        lookup_expr='gte'
    )
    ph_max = django_filters.NumberFilter(
        field_name='optimal_ph',
        lookup_expr='lte'
    )
    ph_range_min = django_filters.NumberFilter(
        field_name='ph_range_min',
        lookup_expr='gte'
    )
    ph_range_max = django_filters.NumberFilter(
        field_name='ph_range_max',
        lookup_expr='lte'
    )
    
    # Глубина
    depth_min = django_filters.NumberFilter(
        field_name='depth_meters',
        lookup_expr='gte'
    )
    depth_max = django_filters.NumberFilter(
        field_name='depth_meters',
        lookup_expr='lte'
    )
    
    # Географические координаты (для поиска в регионе)
    latitude_min = django_filters.NumberFilter(
        field_name='latitude',
        lookup_expr='gte'
    )
    latitude_max = django_filters.NumberFilter(
        field_name='latitude',
        lookup_expr='lte'
    )
    longitude_min = django_filters.NumberFilter(
        field_name='longitude',
        lookup_expr='gte'
    )
    longitude_max = django_filters.NumberFilter(
        field_name='longitude',
        lookup_expr='lte'
    )
    
    # Экстремофильные характеристики
    is_extremophile = django_filters.BooleanFilter(
        method='filter_extremophile'
    )
    extremophile_types = django_filters.MultipleChoiceFilter(
        choices=[
            ('psychrophile', 'Психрофил'),
            ('thermophile', 'Термофил'),
            ('halophile', 'Галофил'),
            ('acidophile', 'Ацидофил'),
            ('alkaliphile', 'Алкалифил'),
            ('barophile', 'Барофил'),
        ],
        method='filter_extremophile_types'
    )
    
    # Биотехнологический потенциал
    has_biotech_potential = django_filters.BooleanFilter(
        method='filter_biotech_potential'
    )
    biotech_types = django_filters.MultipleChoiceFilter(
        choices=[
            ('antibiotics', 'Антибиотики'),
            ('enzymes', 'Ферменты'),
            ('metabolites', 'Метаболиты'),
            ('nitrogen_fixation', 'Азотфиксация'),
        ],
        method='filter_biotech_types'
    )
    
    # Геномная информация
    genome_size_min = django_filters.NumberFilter(
        field_name='genome_size',
        lookup_expr='gte'
    )
    genome_size_max = django_filters.NumberFilter(
        field_name='genome_size',
        lookup_expr='lte'
    )
    gc_content_min = django_filters.NumberFilter(
        field_name='gc_content',
        lookup_expr='gte'
    )
    gc_content_max = django_filters.NumberFilter(
        field_name='gc_content',
        lookup_expr='lte'
    )
    
    # Специальные фильтры для байкальских штаммов
    is_baikal = django_filters.BooleanFilter(
        method='filter_baikal'
    )
    baikal_zone = django_filters.ChoiceFilter(
        field_name='habitat_type',
        choices=[
            ('baikal_surface', 'Поверхность Байкала'),
            ('baikal_deep', 'Глубины Байкала'),
            ('baikal_bottom', 'Дно Байкала'),
            ('baikal_coastal', 'Прибрежная зона'),
        ]
    )
    
    # Даты
    isolation_date_after = django_filters.DateFilter(
        field_name='isolation_date',
        lookup_expr='gte'
    )
    isolation_date_before = django_filters.DateFilter(
        field_name='isolation_date',
        lookup_expr='lte'
    )
    deposit_date_after = django_filters.DateFilter(
        field_name='deposit_date',
        lookup_expr='gte'
    )
    deposit_date_before = django_filters.DateFilter(
        field_name='deposit_date',
        lookup_expr='lte'
    )
    
    # Многократный поиск
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Strain
        fields = [
            'organism_type', 'habitat_type', 'is_available', 'is_type_strain',
            'has_genome_sequence', 'is_psychrophile', 'is_thermophile',
            'is_halophile', 'is_acidophile', 'is_alkaliphile', 'is_barophile',
            'produces_antibiotics', 'produces_enzymes', 'produces_metabolites',
            'nitrogen_fixation'
        ]
    
    def filter_extremophile(self, queryset, name, value):
        """Фильтр для любых экстремофилов"""
        if value:
            return queryset.filter(
                models.Q(is_psychrophile=True) |
                models.Q(is_thermophile=True) |
                models.Q(is_halophile=True) |
                models.Q(is_acidophile=True) |
                models.Q(is_alkaliphile=True) |
                models.Q(is_barophile=True)
            )
        return queryset
    
    def filter_extremophile_types(self, queryset, name, value):
        """Фильтр по типам экстремофилов"""
        if not value:
            return queryset
        
        conditions = models.Q()
        for extremophile_type in value:
            if extremophile_type == 'psychrophile':
                conditions |= models.Q(is_psychrophile=True)
            elif extremophile_type == 'thermophile':
                conditions |= models.Q(is_thermophile=True)
            elif extremophile_type == 'halophile':
                conditions |= models.Q(is_halophile=True)
            elif extremophile_type == 'acidophile':
                conditions |= models.Q(is_acidophile=True)
            elif extremophile_type == 'alkaliphile':
                conditions |= models.Q(is_alkaliphile=True)
            elif extremophile_type == 'barophile':
                conditions |= models.Q(is_barophile=True)
        
        return queryset.filter(conditions)
    
    def filter_biotech_potential(self, queryset, name, value):
        """Фильтр для биотехнологического потенциала"""
        if value:
            return queryset.filter(
                models.Q(produces_antibiotics=True) |
                models.Q(produces_enzymes=True) |
                models.Q(produces_metabolites=True) |
                models.Q(nitrogen_fixation=True)
            )
        return queryset
    
    def filter_biotech_types(self, queryset, name, value):
        """Фильтр по типам биотехнологического потенциала"""
        if not value:
            return queryset
        
        conditions = models.Q()
        for biotech_type in value:
            if biotech_type == 'antibiotics':
                conditions |= models.Q(produces_antibiotics=True)
            elif biotech_type == 'enzymes':
                conditions |= models.Q(produces_enzymes=True)
            elif biotech_type == 'metabolites':
                conditions |= models.Q(produces_metabolites=True)
            elif biotech_type == 'nitrogen_fixation':
                conditions |= models.Q(nitrogen_fixation=True)
        
        return queryset.filter(conditions)
    
    def filter_baikal(self, queryset, name, value):
        """Фильтр для байкальских штаммов"""
        if value:
            return queryset.filter(
                habitat_type__in=[
                    'baikal_surface', 'baikal_deep', 
                    'baikal_bottom', 'baikal_coastal'
                ]
            )
        return queryset
    
    def filter_search(self, queryset, name, value):
        """Многоцелевой поиск по различным полям"""
        if not value:
            return queryset
        
        return queryset.filter(
            models.Q(scientific_name__icontains=value) |
            models.Q(genus__icontains=value) |
            models.Q(species__icontains=value) |
            models.Q(strain_number__icontains=value) |
            models.Q(alternative_numbers__icontains=value) |
            models.Q(isolation_source__icontains=value) |
            models.Q(geographic_location__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(special_properties__icontains=value) |
            models.Q(collection__name__icontains=value) |
            models.Q(collection__code__icontains=value)
        )


class CollectionFilter(django_filters.FilterSet):
    """Фильтр для коллекций"""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    
    # Фильтр по наличию штаммов
    has_strains = django_filters.BooleanFilter(
        method='filter_has_strains'
    )
    min_strain_count = django_filters.NumberFilter(
        method='filter_min_strain_count'
    )
    
    # Даты
    established_after = django_filters.DateFilter(
        field_name='established_date',
        lookup_expr='gte'
    )
    established_before = django_filters.DateFilter(
        field_name='established_date',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Collection
        fields = [
            'collection_type', 'is_active', 'access_level', 'curator'
        ]
    
    def filter_has_strains(self, queryset, name, value):
        """Фильтр коллекций с штаммами"""
        if value:
            return queryset.filter(strains__isnull=False).distinct()
        return queryset
    
    def filter_min_strain_count(self, queryset, name, value):
        """Фильтр по минимальному количеству штаммов"""
        if value:
            return queryset.annotate(
                strain_count=models.Count('strains')
            ).filter(strain_count__gte=value)
        return queryset


class GenomeSequenceFilter(django_filters.FilterSet):
    """Фильтр для геномных последовательностей"""
    
    accession_number = django_filters.CharFilter(lookup_expr='icontains')
    strain_name = django_filters.CharFilter(
        field_name='strain__scientific_name',
        lookup_expr='icontains'
    )
    strain_number = django_filters.CharFilter(
        field_name='strain__strain_number',
        lookup_expr='icontains'
    )
    collection = django_filters.ModelChoiceFilter(
        field_name='strain__collection',
        queryset=Collection.objects.filter(is_active=True)
    )
    
    # Длина последовательности
    sequence_length_min = django_filters.NumberFilter(
        field_name='sequence_length',
        lookup_expr='gte'
    )
    sequence_length_max = django_filters.NumberFilter(
        field_name='sequence_length',
        lookup_expr='lte'
    )
    
    # Качество
    quality_score_min = django_filters.NumberFilter(
        field_name='quality_score',
        lookup_expr='gte'
    )
    quality_score_max = django_filters.NumberFilter(
        field_name='quality_score',
        lookup_expr='lte'
    )
    
    # Покрытие
    coverage_min = django_filters.NumberFilter(
        field_name='coverage',
        lookup_expr='gte'
    )
    coverage_max = django_filters.NumberFilter(
        field_name='coverage',
        lookup_expr='lte'
    )
    
    # Даты
    submission_after = django_filters.DateFilter(
        field_name='submission_date',
        lookup_expr='gte'
    )
    submission_before = django_filters.DateFilter(
        field_name='submission_date',
        lookup_expr='lte'
    )
    
    class Meta:
        model = GenomeSequence
        fields = [
            'sequence_type', 'database'
        ]


class PublicationFilter(django_filters.FilterSet):
    """Фильтр для публикаций"""
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    authors = django_filters.CharFilter(lookup_expr='icontains')
    journal = django_filters.CharFilter(lookup_expr='icontains')
    abstract = django_filters.CharFilter(lookup_expr='icontains')
    doi = django_filters.CharFilter(lookup_expr='icontains')
    
    # Диапазон годов
    year_min = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='gte'
    )
    year_max = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='lte'
    )
    
    # Связанные штаммы
    strain = django_filters.ModelChoiceFilter(
        field_name='strains',
        queryset=Strain.objects.filter(is_available=True)
    )
    collection = django_filters.ModelChoiceFilter(
        field_name='strains__collection',
        queryset=Collection.objects.filter(is_active=True)
    )
    
    # Наличие DOI/PMID
    has_doi = django_filters.BooleanFilter(
        method='filter_has_doi'
    )
    has_pmid = django_filters.BooleanFilter(
        method='filter_has_pmid'
    )
    
    class Meta:
        model = Publication
        fields = ['year']
    
    def filter_has_doi(self, queryset, name, value):
        """Фильтр публикаций с DOI"""
        if value:
            return queryset.exclude(doi='')
        else:
            return queryset.filter(doi='')
    
    def filter_has_pmid(self, queryset, name, value):
        """Фильтр публикаций с PubMed ID"""
        if value:
            return queryset.exclude(pmid='')
        else:
            return queryset.filter(pmid='') 