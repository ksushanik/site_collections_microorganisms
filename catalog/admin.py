from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Collection, Strain, GenomeSequence, Publication


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'collection_type', 'curator', 
        'strains_count', 'established_date', 'is_active', 'access_level'
    ]
    list_filter = [
        'collection_type', 'is_active', 'access_level', 
        'established_date', 'curator'
    ]
    search_fields = ['name', 'code', 'description']
    ordering = ['code']
    date_hierarchy = 'established_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'collection_type', 'description')
        }),
        ('Управление', {
            'fields': ('curator', 'established_date', 'is_active', 'access_level')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def strains_count(self, obj):
        count = obj.strains.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'red',
            count
        )
    strains_count.short_description = 'Количество штаммов'
    strains_count.admin_order_field = 'strains_count'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(strains_count=Count('strains'))
        return queryset


class GenomeSequenceInline(admin.TabularInline):
    model = GenomeSequence
    extra = 0
    fields = [
        'sequence_type', 'accession_number', 'database', 
        'sequence_length', 'submission_date'
    ]
    readonly_fields = ['created_at']


@admin.register(Strain)
class StrainAdmin(admin.ModelAdmin):
    list_display = [
        'full_name_display', 'scientific_name', 'organism_type', 
        'habitat_type', 'collection', 'extremophile_badges', 
        'biotechnology_badges', 'is_available', 'is_type_strain'
    ]
    list_filter = [
        'collection', 'organism_type', 'habitat_type',
        'is_psychrophile', 'is_thermophile', 'is_halophile',
        'is_acidophile', 'is_alkaliphile', 'is_barophile',
        'produces_antibiotics', 'produces_enzymes', 'nitrogen_fixation',
        'is_available', 'is_type_strain', 'has_genome_sequence'
    ]
    search_fields = [
        'strain_number', 'scientific_name', 'genus', 'species',
        'isolation_source', 'geographic_location', 'alternative_numbers'
    ]
    ordering = ['collection__code', 'strain_number']
    date_hierarchy = 'deposit_date'
    
    fieldsets = (
        ('Идентификация', {
            'fields': (
                'collection', 'strain_number', 'alternative_numbers',
                'is_type_strain', 'is_available'
            )
        }),
        ('Таксономия', {
            'fields': (
                'scientific_name', 'genus', 'species', 'subspecies',
                'organism_type'
            )
        }),
        ('География и экология', {
            'fields': (
                'isolation_source', 'habitat_type', 'geographic_location',
                'latitude', 'longitude', 'depth_meters'
            )
        }),
        ('Условия культивирования', {
            'fields': (
                'optimal_temperature', 'temperature_range_min', 'temperature_range_max',
                'optimal_ph', 'ph_range_min', 'ph_range_max'
            ),
            'classes': ('collapse',)
        }),
        ('Экстремофильные характеристики', {
            'fields': (
                'is_psychrophile', 'is_thermophile', 'is_halophile',
                'is_acidophile', 'is_alkaliphile', 'is_barophile'
            ),
            'classes': ('collapse',)
        }),
        ('Биотехнологический потенциал', {
            'fields': (
                'produces_antibiotics', 'produces_enzymes', 
                'produces_metabolites', 'nitrogen_fixation'
            ),
            'classes': ('collapse',)
        }),
        ('Геномные данные', {
            'fields': (
                'genome_size', 'gc_content', 'has_genome_sequence'
            ),
            'classes': ('collapse',)
        }),
        ('Даты и метаданные', {
            'fields': (
                'isolation_date', 'deposit_date',
                'description', 'special_properties', 'cultivation_notes'
            ),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    inlines = [GenomeSequenceInline]
    
    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'Полное название'
    full_name_display.admin_order_field = 'strain_number'
    
    def extremophile_badges(self, obj):
        badges = []
        extremophile_map = {
            'is_psychrophile': ('❄️', 'Психрофил', 'blue'),
            'is_thermophile': ('🔥', 'Термофил', 'red'),
            'is_halophile': ('🧂', 'Галофил', 'orange'),
            'is_acidophile': ('🍋', 'Ацидофил', 'yellow'),
            'is_alkaliphile': ('🧪', 'Алкалифил', 'purple'),
            'is_barophile': ('⬇️', 'Барофил', 'darkblue'),
        }
        
        for field, (emoji, name, color) in extremophile_map.items():
            if getattr(obj, field):
                badges.append(
                    f'<span style="color: {color}; font-size: 14px;" title="{name}">{emoji}</span>'
                )
        
        return format_html(''.join(badges)) if badges else '-'
    extremophile_badges.short_description = 'Экстремофилы'
    
    def biotechnology_badges(self, obj):
        badges = []
        biotech_map = {
            'produces_antibiotics': ('💊', 'Антибиотики', 'green'),
            'produces_enzymes': ('⚗️', 'Ферменты', 'blue'),
            'produces_metabolites': ('🧬', 'Метаболиты', 'purple'),
            'nitrogen_fixation': ('🌱', 'Азотфиксация', 'darkgreen'),
        }
        
        for field, (emoji, name, color) in biotech_map.items():
            if getattr(obj, field):
                badges.append(
                    f'<span style="color: {color}; font-size: 14px;" title="{name}">{emoji}</span>'
                )
        
        return format_html(''.join(badges)) if badges else '-'
    biotechnology_badges.short_description = 'Биотех потенциал'
    
    # Действия для массовых операций
    actions = ['mark_as_available', 'mark_as_unavailable', 'export_to_csv']
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(
            request, 
            f'{updated} штаммов отмечены как доступные.'
        )
    mark_as_available.short_description = 'Отметить как доступные'
    
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(
            request, 
            f'{updated} штаммов отмечены как недоступные.'
        )
    mark_as_unavailable.short_description = 'Отметить как недоступные'


@admin.register(GenomeSequence)
class GenomeSequenceAdmin(admin.ModelAdmin):
    list_display = [
        'strain_name', 'sequence_type', 'accession_number', 
        'database', 'sequence_length', 'quality_badge', 'submission_date'
    ]
    list_filter = [
        'sequence_type', 'database', 'submission_date',
        'strain__collection', 'strain__organism_type'
    ]
    search_fields = [
        'accession_number', 'strain__strain_number', 
        'strain__scientific_name', 'notes'
    ]
    ordering = ['-submission_date']
    date_hierarchy = 'submission_date'
    
    fieldsets = (
        ('Связь со штаммом', {
            'fields': ('strain',)
        }),
        ('Данные последовательности', {
            'fields': (
                'sequence_type', 'accession_number', 'database',
                'sequence_length', 'sequence_data'
            )
        }),
        ('Качество', {
            'fields': ('quality_score', 'coverage', 'submission_date'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def strain_name(self, obj):
        return obj.strain.full_name
    strain_name.short_description = 'Штамм'
    strain_name.admin_order_field = 'strain__strain_number'
    
    def quality_badge(self, obj):
        if obj.quality_score is None:
            return '-'
        
        score = float(obj.quality_score)
        if score >= 90:
            color, icon = 'green', '🟢'
        elif score >= 70:
            color, icon = 'orange', '🟡'
        else:
            color, icon = 'red', '🔴'
        
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color, icon, f'{score:.1f}'
        )
    quality_badge.short_description = 'Качество'
    quality_badge.admin_order_field = 'quality_score'


class PublicationStrainInline(admin.TabularInline):
    model = Publication.strains.through
    extra = 0
    verbose_name = "Связанный штамм"
    verbose_name_plural = "Связанные штаммы"


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        'title_short', 'authors_short', 'journal', 
        'year', 'strains_count', 'has_doi'
    ]
    list_filter = ['year', 'journal']
    search_fields = ['title', 'authors', 'journal', 'doi', 'abstract']
    ordering = ['-year', 'title']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'authors', 'abstract')
        }),
        ('Публикация', {
            'fields': ('journal', 'volume', 'issue', 'pages', 'year')
        }),
        ('Идентификаторы', {
            'fields': ('doi', 'pmid', 'url'),
            'classes': ('collapse',)
        }),
        ('Связи', {
            'fields': ('strains',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['strains']
    
    def title_short(self, obj):
        return obj.title[:60] + '...' if len(obj.title) > 60 else obj.title
    title_short.short_description = 'Название'
    title_short.admin_order_field = 'title'
    
    def authors_short(self, obj):
        return obj.authors[:40] + '...' if len(obj.authors) > 40 else obj.authors
    authors_short.short_description = 'Авторы'
    authors_short.admin_order_field = 'authors'
    
    def strains_count(self, obj):
        count = obj.strains.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    strains_count.short_description = 'Штаммов'
    strains_count.admin_order_field = 'strains_count'
    
    def has_doi(self, obj):
        return '✅' if obj.doi else '❌'
    has_doi.short_description = 'DOI'
    has_doi.admin_order_field = 'doi'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(strains_count=Count('strains'))
        return queryset


# Настройка основного заголовка админки
admin.site.site_header = "СИФИБР СО РАН - Коллекции микроорганизмов"
admin.site.site_title = "СИФИБР Каталог"
admin.site.index_title = "Управление коллекциями микроорганизмов"
