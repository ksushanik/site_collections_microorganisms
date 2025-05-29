from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import csv
import json

from .models import Collection, Strain, GenomeSequence, Publication
from .serializers import (
    CollectionSerializer, StrainSerializer, 
    GenomeSequenceSerializer, PublicationSerializer,
    StrainSearchSerializer
)
from .filters import StrainFilter


# Веб-интерфейс представления
class CatalogHomeView(TemplateView):
    """Главная страница каталога"""
    template_name = 'catalog/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Общая статистика
        context.update({
            'total_collections': Collection.objects.filter(is_active=True).count(),
            'total_strains': Strain.objects.filter(is_available=True).count(),
            'total_extremophiles': Strain.objects.filter(
                Q(is_psychrophile=True) | Q(is_thermophile=True) | 
                Q(is_halophile=True) | Q(is_acidophile=True) | 
                Q(is_alkaliphile=True) | Q(is_barophile=True)
            ).count(),
            'baikal_strains': Strain.objects.filter(
                habitat_type__in=[
                    'baikal_surface', 'baikal_deep', 
                    'baikal_bottom', 'baikal_coastal'
                ]
            ).count(),
            'recent_strains': Strain.objects.filter(
                is_available=True
            ).order_by('-created_at')[:5],
            'featured_collections': Collection.objects.filter(
                is_active=True
            ).annotate(
                strain_count=Count('strains')
            ).order_by('-strain_count')[:6],
        })
        
        return context


class CollectionListView(ListView):
    """Список коллекций"""
    model = Collection
    template_name = 'catalog/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Collection.objects.filter(is_active=True).annotate(
            strain_count=Count('strains')
        ).order_by('name')
        
        # Фильтрация по типу коллекции
        collection_type = self.request.GET.get('type')
        if collection_type:
            queryset = queryset.filter(collection_type=collection_type)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_types'] = Collection.COLLECTION_TYPES
        context['selected_type'] = self.request.GET.get('type', '')
        return context


class CollectionDetailView(DetailView):
    """Детальная страница коллекции"""
    model = Collection
    template_name = 'catalog/collection_detail.html'
    context_object_name = 'collection'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.object
        
        # Статистика по штаммам в коллекции
        strains = collection.strains.filter(is_available=True)
        
        context.update({
            'strains': strains.order_by('strain_number')[:10],
            'total_strains': strains.count(),
            'extremophile_count': strains.filter(
                Q(is_psychrophile=True) | Q(is_thermophile=True) | 
                Q(is_halophile=True) | Q(is_acidophile=True) | 
                Q(is_alkaliphile=True) | Q(is_barophile=True)
            ).count(),
            'genome_count': strains.filter(has_genome_sequence=True).count(),
            'biotech_count': strains.filter(
                Q(produces_antibiotics=True) | Q(produces_enzymes=True) | 
                Q(produces_metabolites=True) | Q(nitrogen_fixation=True)
            ).count(),
        })
        
        return context


class StrainListView(ListView):
    """Список штаммов с фильтрацией"""
    model = Strain
    template_name = 'catalog/strain_list.html'
    context_object_name = 'strains'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Strain.objects.filter(
            is_available=True
        ).select_related(
            'collection'
        ).prefetch_related(
            'genome_sequences'
        ).order_by('collection__code', 'strain_number')
        
        # Фильтры
        collection_id = self.request.GET.get('collection')
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        
        organism_type = self.request.GET.get('organism_type')
        if organism_type:
            queryset = queryset.filter(organism_type=organism_type)
        
        habitat_type = self.request.GET.get('habitat_type')
        if habitat_type:
            queryset = queryset.filter(habitat_type=habitat_type)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(scientific_name__icontains=search) |
                Q(genus__icontains=search) |
                Q(species__icontains=search) |
                Q(strain_number__icontains=search) |
                Q(isolation_source__icontains=search)
            )
        
        # Специальные фильтры
        if self.request.GET.get('extremophiles'):
            queryset = queryset.filter(
                Q(is_psychrophile=True) | Q(is_thermophile=True) | 
                Q(is_halophile=True) | Q(is_acidophile=True) | 
                Q(is_alkaliphile=True) | Q(is_barophile=True)
            )
        
        if self.request.GET.get('baikal'):
            queryset = queryset.filter(
                habitat_type__in=[
                    'baikal_surface', 'baikal_deep', 
                    'baikal_bottom', 'baikal_coastal'
                ]
            )
        
        if self.request.GET.get('biotech'):
            queryset = queryset.filter(
                Q(produces_antibiotics=True) | Q(produces_enzymes=True) | 
                Q(produces_metabolites=True) | Q(nitrogen_fixation=True)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'collections': Collection.objects.filter(is_active=True),
            'organism_types': Strain.ORGANISM_TYPES,
            'habitat_types': Strain.HABITAT_TYPES,
            'filters': {
                'collection': self.request.GET.get('collection', ''),
                'organism_type': self.request.GET.get('organism_type', ''),
                'habitat_type': self.request.GET.get('habitat_type', ''),
                'search': self.request.GET.get('search', ''),
                'extremophiles': self.request.GET.get('extremophiles'),
                'baikal': self.request.GET.get('baikal'),
                'biotech': self.request.GET.get('biotech'),
            }
        })
        return context


class StrainDetailView(DetailView):
    """Детальная страница штамма"""
    model = Strain
    template_name = 'catalog/strain_detail.html'
    context_object_name = 'strain'
    
    def get_queryset(self):
        return Strain.objects.select_related(
            'collection'
        ).prefetch_related(
            'genome_sequences',
            'publications'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        strain = self.object
        
        context.update({
            'genome_sequences': strain.genome_sequences.all(),
            'publications': strain.publications.all(),
            'extremophile_types': strain.extremophile_types,
            'related_strains': Strain.objects.filter(
                genus=strain.genus,
                is_available=True
            ).exclude(id=strain.id)[:5],
        })
        
        return context


class StrainSearchView(TemplateView):
    """Расширенный поиск штаммов"""
    template_name = 'catalog/strain_search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Базовые данные для формы
        context.update({
            'collections': Collection.objects.filter(is_active=True),
            'organism_types': Strain.ORGANISM_TYPES,
            'habitat_types': Strain.HABITAT_TYPES,
        })
        
        # Выполняем поиск если есть параметры
        strains = None
        if any(self.request.GET.values()):
            strains = self.get_search_results()
        
        context['strains'] = strains
        return context
    
    def get_search_results(self):
        """Выполняет поиск штаммов по параметрам"""
        queryset = Strain.objects.filter(is_available=True).select_related('collection')
        params = self.request.GET
        
        # Общий поиск по тексту
        q = params.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(scientific_name__icontains=q) |
                Q(genus__icontains=q) |
                Q(species__icontains=q) |
                Q(strain_number__icontains=q) |
                Q(isolation_source__icontains=q) |
                Q(geographic_location__icontains=q) |
                Q(alternative_numbers__icontains=q)
            )
        
        # Фильтр по коллекции
        collection_id = params.get('collection')
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        
        # Фильтры экстремофилов
        extremophile_filters = Q()
        if params.get('is_psychrophile'):
            extremophile_filters |= Q(is_psychrophile=True)
        if params.get('is_thermophile'):
            extremophile_filters |= Q(is_thermophile=True)
        if params.get('is_halophile'):
            extremophile_filters |= Q(is_halophile=True)
        if params.get('is_acidophile'):
            extremophile_filters |= Q(is_acidophile=True)
        if params.get('is_alkaliphile'):
            extremophile_filters |= Q(is_alkaliphile=True)
        if params.get('is_barophile'):
            extremophile_filters |= Q(is_barophile=True)
        
        if extremophile_filters:
            queryset = queryset.filter(extremophile_filters)
        
        # Фильтры биотехнологий
        biotech_filters = Q()
        if params.get('produces_antibiotics'):
            biotech_filters |= Q(produces_antibiotics=True)
        if params.get('produces_enzymes'):
            biotech_filters |= Q(produces_enzymes=True)
        if params.get('nitrogen_fixation'):
            biotech_filters |= Q(nitrogen_fixation=True)
        
        if biotech_filters:
            queryset = queryset.filter(biotech_filters)
        
        # Фильтр по среде обитания
        habitat_type = params.get('habitat_type')
        if habitat_type:
            queryset = queryset.filter(habitat_type=habitat_type)
        
        # Фильтр по типу организма
        organism_type = params.get('organism_type')
        if organism_type:
            queryset = queryset.filter(organism_type=organism_type)
        
        return queryset.order_by('collection__code', 'strain_number')[:100]  # Ограничиваем результаты


class BaikalExtremophilesView(ListView):
    """Специальная страница байкальских экстремофилов"""
    model = Strain
    template_name = 'catalog/baikal_extremophiles.html'
    context_object_name = 'strains'
    paginate_by = 20
    
    def get_queryset(self):
        return Strain.objects.filter(
            habitat_type__in=[
                'baikal_surface', 'baikal_deep', 
                'baikal_bottom', 'baikal_coastal'
            ],
            is_available=True
        ).filter(
            Q(is_psychrophile=True) | Q(is_thermophile=True) | 
            Q(is_halophile=True) | Q(is_acidophile=True) | 
            Q(is_alkaliphile=True) | Q(is_barophile=True)
        ).select_related('collection').order_by('-depth_meters', 'strain_number')


class BiotechnologyView(ListView):
    """Страница штаммов с биотехнологическим потенциалом"""
    model = Strain
    template_name = 'catalog/biotechnology.html'
    context_object_name = 'strains'
    paginate_by = 20
    
    def get_queryset(self):
        return Strain.objects.filter(
            Q(produces_antibiotics=True) | Q(produces_enzymes=True) | 
            Q(produces_metabolites=True) | Q(nitrogen_fixation=True),
            is_available=True
        ).select_related('collection').order_by('scientific_name')


class StatisticsView(TemplateView):
    """Страница статистики"""
    template_name = 'catalog/statistics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Общая статистика
        total_strains = Strain.objects.filter(is_available=True)
        
        context.update({
            'total_collections': Collection.objects.filter(is_active=True).count(),
            'total_strains': total_strains.count(),
            
            # По типам организмов
            'organism_stats': [
                {
                    'type': display_name,
                    'count': total_strains.filter(organism_type=code).count()
                }
                for code, display_name in Strain.ORGANISM_TYPES
            ],
            
            # По средам обитания
            'habitat_stats': [
                {
                    'type': display_name,
                    'count': total_strains.filter(habitat_type=code).count()
                }
                for code, display_name in Strain.HABITAT_TYPES
            ],
            
            # Экстремофилы
            'extremophile_stats': {
                'psychrophiles': total_strains.filter(is_psychrophile=True).count(),
                'thermophiles': total_strains.filter(is_thermophile=True).count(),
                'halophiles': total_strains.filter(is_halophile=True).count(),
                'acidophiles': total_strains.filter(is_acidophile=True).count(),
                'alkaliphiles': total_strains.filter(is_alkaliphile=True).count(),
                'barophiles': total_strains.filter(is_barophile=True).count(),
            },
            
            # Биотехнология
            'biotech_stats': {
                'antibiotics': total_strains.filter(produces_antibiotics=True).count(),
                'enzymes': total_strains.filter(produces_enzymes=True).count(),
                'metabolites': total_strains.filter(produces_metabolites=True).count(),
                'nitrogen_fixation': total_strains.filter(nitrogen_fixation=True).count(),
            },
            
            # Геномика
            'genome_stats': {
                'sequenced': total_strains.filter(has_genome_sequence=True).count(),
                'avg_genome_size': total_strains.exclude(
                    genome_size__isnull=True
                ).aggregate(Avg('genome_size'))['genome_size__avg'],
                'avg_gc_content': total_strains.exclude(
                    gc_content__isnull=True
                ).aggregate(Avg('gc_content'))['gc_content__avg'],
            },
        })
        
        return context


# API представления
class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """API для коллекций"""
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'code', 'description']
    filterset_fields = ['collection_type', 'access_level']
    ordering_fields = ['name', 'code', 'established_date']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def strains(self, request, pk=None):
        """Получить штаммы конкретной коллекции"""
        collection = self.get_object()
        strains = collection.strains.filter(is_available=True)
        
        page = self.paginate_queryset(strains)
        if page is not None:
            serializer = StrainSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = StrainSerializer(strains, many=True, context={'request': request})
        return Response(serializer.data)


class StrainViewSet(viewsets.ReadOnlyModelViewSet):
    """API для штаммов"""
    queryset = Strain.objects.filter(is_available=True).select_related('collection')
    serializer_class = StrainSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StrainFilter
    search_fields = [
        'scientific_name', 'genus', 'species', 'strain_number',
        'isolation_source', 'geographic_location'
    ]
    ordering_fields = [
        'scientific_name', 'genus', 'species', 'strain_number',
        'isolation_date', 'deposit_date'
    ]
    ordering = ['collection__code', 'strain_number']
    
    @action(detail=False, methods=['get'])
    def extremophiles(self, request):
        """Получить все экстремофильные штаммы"""
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                Q(is_psychrophile=True) | Q(is_thermophile=True) | 
                Q(is_halophile=True) | Q(is_acidophile=True) | 
                Q(is_alkaliphile=True) | Q(is_barophile=True)
            )
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def baikal(self, request):
        """Получить байкальские штаммы"""
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                habitat_type__in=[
                    'baikal_surface', 'baikal_deep', 
                    'baikal_bottom', 'baikal_coastal'
                ]
            )
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """Экспорт штаммов в CSV формате"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="strains_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Штамм', 'Научное название', 'Род', 'Вид', 'Коллекция',
            'Тип организма', 'Среда обитания', 'Широта', 'Долгота',
            'Температура (°C)', 'pH', 'Психрофил', 'Термофил', 'Галофил',
            'Источник выделения', 'Дата выделения', 'Особые свойства'
        ])
        
        # Применяем те же фильтры что и в основном списке
        queryset = self.filter_queryset(self.get_queryset())
        
        for strain in queryset:
            writer.writerow([
                strain.full_name,
                strain.scientific_name,
                strain.genus,
                strain.species,
                strain.collection.code,
                strain.get_organism_type_display(),
                strain.get_habitat_type_display(),
                strain.latitude or '',
                strain.longitude or '',
                strain.optimal_temperature or '',
                strain.optimal_ph or '',
                'Да' if strain.is_psychrophile else 'Нет',
                'Да' if strain.is_thermophile else 'Нет',
                'Да' if strain.is_halophile else 'Нет',
                strain.isolation_source or '',
                strain.isolation_date.strftime('%Y-%m-%d') if strain.isolation_date else '',
                strain.special_properties or ''
            ])
        
        return response

    @action(detail=False, methods=['get'])
    def export_fasta(self, request):
        """Экспорт геномных последовательностей в FASTA формате"""
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="sequences_export.fasta"'
        
        # Только штаммы с геномными последовательностями
        queryset = self.filter_queryset(self.get_queryset()).filter(has_genome_sequence=True)
        
        fasta_lines = []
        for strain in queryset:
            # Заголовок FASTA
            header = f">{strain.full_name} {strain.scientific_name}"
            if strain.latitude and strain.longitude:
                header += f" [lat={strain.latitude} lon={strain.longitude}]"
            if strain.optimal_temperature:
                header += f" [temp={strain.optimal_temperature}C]"
            header += f" [habitat={strain.habitat_type}]"
            
            fasta_lines.append(header)
            
            # Последовательность (заглушка для демонстрации)
            if strain.genome_sequences.exists():
                sequence = strain.genome_sequences.first()
                if sequence.sequence_data:
                    fasta_lines.append(sequence.sequence_data[:100] + "...")
                else:
                    # Генерируем заглушку на основе размера генома
                    seq_length = min(100, (strain.genome_size or 2500000) // 25000)
                    fasta_lines.append("A" * seq_length + "...")
            else:
                fasta_lines.append("ATCGATCGATCGATCG...")  # Заглушка
            
            fasta_lines.append("")  # Пустая строка между записями
        
        response.write('\n'.join(fasta_lines))
        return response

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Статистическая сводка по штаммам"""
        queryset = self.get_queryset()
        
        stats = {
            'total_strains': queryset.count(),
            'collections_count': queryset.values('collection').distinct().count(),
            'extremophiles': {
                'psychrophiles': queryset.filter(is_psychrophile=True).count(),
                'thermophiles': queryset.filter(is_thermophile=True).count(),
                'halophiles': queryset.filter(is_halophile=True).count(),
                'acidophiles': queryset.filter(is_acidophile=True).count(),
                'alkaliphiles': queryset.filter(is_alkaliphile=True).count(),
                'barophiles': queryset.filter(is_barophile=True).count(),
            },
            'habitat_distribution': {},
            'organism_types': {},
            'biotechnology': {
                'antibiotic_producers': queryset.filter(produces_antibiotics=True).count(),
                'enzyme_producers': queryset.filter(produces_enzymes=True).count(),
                'nitrogen_fixers': queryset.filter(nitrogen_fixation=True).count(),
                'metabolite_producers': queryset.filter(produces_metabolites=True).count(),
            },
            'genomics': {
                'sequenced': queryset.filter(has_genome_sequence=True).count(),
                'avg_genome_size': queryset.exclude(genome_size__isnull=True).aggregate(
                    avg_size=Avg('genome_size')
                )['avg_size'],
                'avg_gc_content': queryset.exclude(gc_content__isnull=True).aggregate(
                    avg_gc=Avg('gc_content')
                )['avg_gc'],
            }
        }
        
        # Распределение по средам обитания
        for choice in Strain.HABITAT_CHOICES:
            count = queryset.filter(habitat_type=choice[0]).count()
            if count > 0:
                stats['habitat_distribution'][choice[1]] = count
        
        # Распределение по типам организмов
        for choice in Strain.ORGANISM_CHOICES:
            count = queryset.filter(organism_type=choice[0]).count()
            if count > 0:
                stats['organism_types'][choice[1]] = count
        
        return Response(stats)


class GenomeSequenceViewSet(viewsets.ReadOnlyModelViewSet):
    """API для геномных последовательностей"""
    queryset = GenomeSequence.objects.all().select_related('strain')
    serializer_class = GenomeSequenceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sequence_type', 'database', 'strain__collection']
    search_fields = ['accession_number', 'strain__scientific_name']
    ordering_fields = ['submission_date', 'sequence_length']
    ordering = ['-submission_date']


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """API для публикаций"""
    queryset = Publication.objects.all().prefetch_related('strains')
    serializer_class = PublicationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'journal']
    search_fields = ['title', 'authors', 'abstract', 'doi']
    ordering_fields = ['year', 'title']
    ordering = ['-year', 'title']


class AdvancedSearchAPIView(generics.ListAPIView):
    """API для расширенного поиска"""
    serializer_class = StrainSearchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StrainFilter
    
    def get_queryset(self):
        queryset = Strain.objects.filter(is_available=True).select_related('collection')
        
        # Дополнительные фильтры для расширенного поиска
        params = self.request.query_params
        
        # Температурный диапазон
        min_temp = params.get('min_temperature')
        max_temp = params.get('max_temperature')
        if min_temp:
            queryset = queryset.filter(temperature_range_min__gte=min_temp)
        if max_temp:
            queryset = queryset.filter(temperature_range_max__lte=max_temp)
        
        # pH диапазон
        min_ph = params.get('min_ph')
        max_ph = params.get('max_ph')
        if min_ph:
            queryset = queryset.filter(ph_range_min__gte=min_ph)
        if max_ph:
            queryset = queryset.filter(ph_range_max__lte=max_ph)
        
        # Глубина
        max_depth = params.get('max_depth')
        if max_depth:
            queryset = queryset.filter(depth_meters__lte=max_depth)
        
        return queryset


class StatisticsAPIView(generics.GenericAPIView):
    """API для статистики"""
    
    def get(self, request):
        total_strains = Strain.objects.filter(is_available=True)
        
        stats = {
            'total_collections': Collection.objects.filter(is_active=True).count(),
            'total_strains': total_strains.count(),
            'total_extremophiles': total_strains.filter(
                Q(is_psychrophile=True) | Q(is_thermophile=True) | 
                Q(is_halophile=True) | Q(is_acidophile=True) | 
                Q(is_alkaliphile=True) | Q(is_barophile=True)
            ).count(),
            'baikal_strains': total_strains.filter(
                habitat_type__in=[
                    'baikal_surface', 'baikal_deep', 
                    'baikal_bottom', 'baikal_coastal'
                ]
            ).count(),
            'genome_sequenced': total_strains.filter(has_genome_sequence=True).count(),
            'biotech_potential': total_strains.filter(
                Q(produces_antibiotics=True) | Q(produces_enzymes=True) | 
                Q(produces_metabolites=True) | Q(nitrogen_fixation=True)
            ).count(),
        }
        
        return Response(stats)


class ExportAPIView(generics.GenericAPIView):
    """API для экспорта данных"""
    
    def get(self, request, format):
        if format not in ['csv', 'json']:
            return Response(
                {'error': 'Поддерживаются только форматы: csv, json'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Применяем фильтры
        queryset = Strain.objects.filter(is_available=True).select_related('collection')
        
        # Можно добавить фильтрацию по параметрам запроса
        collection_id = request.query_params.get('collection')
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        
        if format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="strains.csv"'
            
            writer = csv.writer(response)
            writer.writerow([
                'Collection', 'Strain Number', 'Scientific Name', 
                'Organism Type', 'Habitat Type', 'Isolation Source',
                'Geographic Location', 'Latitude', 'Longitude',
                'Is Psychrophile', 'Is Thermophile', 'Is Halophile',
                'Produces Antibiotics', 'Produces Enzymes'
            ])
            
            for strain in queryset:
                writer.writerow([
                    strain.collection.code,
                    strain.strain_number,
                    strain.scientific_name,
                    strain.get_organism_type_display(),
                    strain.get_habitat_type_display(),
                    strain.isolation_source,
                    strain.geographic_location,
                    strain.latitude,
                    strain.longitude,
                    strain.is_psychrophile,
                    strain.is_thermophile,
                    strain.is_halophile,
                    strain.produces_antibiotics,
                    strain.produces_enzymes,
                ])
            
            return response
        
        elif format == 'json':
            data = []
            for strain in queryset:
                data.append({
                    'collection': strain.collection.code,
                    'strain_number': strain.strain_number,
                    'scientific_name': strain.scientific_name,
                    'organism_type': strain.organism_type,
                    'habitat_type': strain.habitat_type,
                    'isolation_source': strain.isolation_source,
                    'geographic_location': strain.geographic_location,
                    'coordinates': {
                        'latitude': float(strain.latitude) if strain.latitude else None,
                        'longitude': float(strain.longitude) if strain.longitude else None,
                    },
                    'extremophile_properties': {
                        'is_psychrophile': strain.is_psychrophile,
                        'is_thermophile': strain.is_thermophile,
                        'is_halophile': strain.is_halophile,
                        'is_acidophile': strain.is_acidophile,
                        'is_alkaliphile': strain.is_alkaliphile,
                        'is_barophile': strain.is_barophile,
                    },
                    'biotechnology': {
                        'produces_antibiotics': strain.produces_antibiotics,
                        'produces_enzymes': strain.produces_enzymes,
                        'produces_metabolites': strain.produces_metabolites,
                        'nitrogen_fixation': strain.nitrogen_fixation,
                    }
                })
            
            return JsonResponse(data, safe=False)
