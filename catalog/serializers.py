from rest_framework import serializers
from .models import Collection, Strain, GenomeSequence, Publication


class CollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для коллекций"""
    strain_count = serializers.SerializerMethodField()
    curator_name = serializers.SerializerMethodField()
    collection_type_display = serializers.CharField(source='get_collection_type_display', read_only=True)
    access_level_display = serializers.CharField(source='get_access_level_display', read_only=True)
    
    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'code', 'collection_type', 'collection_type_display',
            'description', 'curator', 'curator_name', 'established_date',
            'is_active', 'access_level', 'access_level_display',
            'strain_count', 'created_at', 'updated_at'
        ]
    
    def get_strain_count(self, obj):
        return obj.strains.filter(is_available=True).count()
    
    def get_curator_name(self, obj):
        return obj.curator.get_full_name() if obj.curator else None


class GenomeSequenceSerializer(serializers.ModelSerializer):
    """Сериализатор для геномных последовательностей"""
    strain_name = serializers.CharField(source='strain.full_name', read_only=True)
    sequence_type_display = serializers.CharField(source='get_sequence_type_display', read_only=True)
    
    class Meta:
        model = GenomeSequence
        fields = [
            'id', 'strain', 'strain_name', 'sequence_type', 'sequence_type_display',
            'accession_number', 'database', 'sequence_length', 'sequence_data',
            'submission_date', 'quality_score', 'coverage', 'notes',
            'created_at', 'updated_at'
        ]


class StrainSerializer(serializers.ModelSerializer):
    """Основной сериализатор для штаммов"""
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    collection_code = serializers.CharField(source='collection.code', read_only=True)
    full_name = serializers.CharField(read_only=True)
    organism_type_display = serializers.CharField(source='get_organism_type_display', read_only=True)
    habitat_type_display = serializers.CharField(source='get_habitat_type_display', read_only=True)
    is_baikal_endemic = serializers.BooleanField(read_only=True)
    extremophile_types = serializers.ListField(read_only=True)
    genome_sequences = GenomeSequenceSerializer(many=True, read_only=True)
    genome_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Strain
        fields = [
            'id', 'collection', 'collection_name', 'collection_code',
            'strain_number', 'alternative_numbers', 'full_name',
            'scientific_name', 'genus', 'species', 'subspecies',
            'organism_type', 'organism_type_display',
            'isolation_source', 'habitat_type', 'habitat_type_display',
            'geographic_location', 'latitude', 'longitude', 'depth_meters',
            'optimal_temperature', 'temperature_range_min', 'temperature_range_max',
            'optimal_ph', 'ph_range_min', 'ph_range_max',
            'is_psychrophile', 'is_thermophile', 'is_halophile',
            'is_acidophile', 'is_alkaliphile', 'is_barophile',
            'produces_antibiotics', 'produces_enzymes', 'produces_metabolites',
            'nitrogen_fixation', 'genome_size', 'gc_content', 'has_genome_sequence',
            'isolation_date', 'deposit_date', 'is_available', 'is_type_strain',
            'description', 'special_properties', 'cultivation_notes',
            'is_baikal_endemic', 'extremophile_types', 'genome_sequences',
            'genome_count', 'created_at', 'updated_at'
        ]
    
    def get_genome_count(self, obj):
        return obj.genome_sequences.count()


class StrainListSerializer(serializers.ModelSerializer):
    """Облегченный сериализатор для списков штаммов"""
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    collection_code = serializers.CharField(source='collection.code', read_only=True)
    full_name = serializers.CharField(read_only=True)
    organism_type_display = serializers.CharField(source='get_organism_type_display', read_only=True)
    habitat_type_display = serializers.CharField(source='get_habitat_type_display', read_only=True)
    extremophile_types = serializers.ListField(read_only=True)
    
    class Meta:
        model = Strain
        fields = [
            'id', 'collection_code', 'collection_name', 'strain_number',
            'full_name', 'scientific_name', 'genus', 'species',
            'organism_type', 'organism_type_display',
            'habitat_type', 'habitat_type_display',
            'is_psychrophile', 'is_thermophile', 'is_halophile',
            'produces_antibiotics', 'produces_enzymes', 'nitrogen_fixation',
            'has_genome_sequence', 'is_available', 'is_type_strain',
            'extremophile_types'
        ]


class StrainSearchSerializer(serializers.ModelSerializer):
    """Сериализатор для расширенного поиска штаммов"""
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    organism_type_display = serializers.CharField(source='get_organism_type_display', read_only=True)
    habitat_type_display = serializers.CharField(source='get_habitat_type_display', read_only=True)
    extremophile_summary = serializers.SerializerMethodField()
    biotechnology_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Strain
        fields = [
            'id', 'collection', 'collection_name', 'strain_number', 'full_name',
            'scientific_name', 'genus', 'species', 'organism_type_display',
            'habitat_type_display', 'geographic_location', 'latitude', 'longitude',
            'depth_meters', 'optimal_temperature', 'optimal_ph',
            'extremophile_summary', 'biotechnology_summary',
            'has_genome_sequence', 'is_available', 'deposit_date'
        ]
    
    def get_extremophile_summary(self, obj):
        """Краткое описание экстремофильных свойств"""
        types = []
        if obj.is_psychrophile:
            types.append('Психрофил')
        if obj.is_thermophile:
            types.append('Термофил')
        if obj.is_halophile:
            types.append('Галофил')
        if obj.is_acidophile:
            types.append('Ацидофил')
        if obj.is_alkaliphile:
            types.append('Алкалифил')
        if obj.is_barophile:
            types.append('Барофил')
        return types
    
    def get_biotechnology_summary(self, obj):
        """Краткое описание биотехнологического потенциала"""
        potential = []
        if obj.produces_antibiotics:
            potential.append('Антибиотики')
        if obj.produces_enzymes:
            potential.append('Ферменты')
        if obj.produces_metabolites:
            potential.append('Метаболиты')
        if obj.nitrogen_fixation:
            potential.append('Азотфиксация')
        return potential


class PublicationSerializer(serializers.ModelSerializer):
    """Сериализатор для публикаций"""
    strain_count = serializers.SerializerMethodField()
    related_strains = serializers.SerializerMethodField()
    
    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'authors', 'journal', 'volume', 'issue',
            'pages', 'year', 'doi', 'pmid', 'url', 'abstract',
            'strain_count', 'related_strains', 'created_at', 'updated_at'
        ]
    
    def get_strain_count(self, obj):
        return obj.strains.count()
    
    def get_related_strains(self, obj):
        """Список связанных штаммов"""
        return [
            {
                'id': strain.id,
                'full_name': strain.full_name,
                'scientific_name': strain.scientific_name
            }
            for strain in obj.strains.all()[:5]  # Ограничиваем до 5 для производительности
        ]


class StrainGeoSerializer(serializers.ModelSerializer):
    """Сериализатор для геопространственных данных штаммов"""
    collection_code = serializers.CharField(source='collection.code', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Strain
        fields = [
            'id', 'collection_code', 'strain_number', 'full_name',
            'scientific_name', 'habitat_type', 'geographic_location',
            'latitude', 'longitude', 'depth_meters',
            'is_psychrophile', 'is_thermophile', 'is_halophile'
        ]
    
    def to_representation(self, instance):
        """Преобразуем в GeoJSON формат для карт"""
        data = super().to_representation(instance)
        
        if instance.latitude and instance.longitude:
            return {
                'type': 'Feature',
                'properties': {
                    'id': data['id'],
                    'full_name': data['full_name'],
                    'scientific_name': data['scientific_name'],
                    'habitat_type': data['habitat_type'],
                    'geographic_location': data['geographic_location'],
                    'depth_meters': data['depth_meters'],
                    'extremophile_types': instance.extremophile_types,
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        float(instance.longitude),
                        float(instance.latitude)
                    ]
                }
            }
        
        return data


class StatisticsSerializer(serializers.Serializer):
    """Сериализатор для статистических данных"""
    total_collections = serializers.IntegerField()
    total_strains = serializers.IntegerField()
    total_extremophiles = serializers.IntegerField()
    baikal_strains = serializers.IntegerField()
    genome_sequenced = serializers.IntegerField()
    biotech_potential = serializers.IntegerField()
    
    # Детальная статистика по типам
    organism_stats = serializers.ListField(child=serializers.DictField())
    habitat_stats = serializers.ListField(child=serializers.DictField())
    extremophile_stats = serializers.DictField()
    biotech_stats = serializers.DictField()
    genome_stats = serializers.DictField() 