from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import uuid


class Collection(models.Model):
    """Модель коллекции микроорганизмов СИФИБР"""
    
    COLLECTION_TYPES = [
        ('autotrophic', 'Автотрофные микроорганизмы'),
        ('nitrogen_fixing', 'Азотфиксирующие микроорганизмы'), 
        ('bioactive', 'Продуценты биологически активных веществ'),
        ('antibiotic', 'Продуценты антибиотиков'),
        ('extremophiles', 'Экстремофильные микроорганизмы'),
        ('baikal_endemic', 'Эндемики озера Байкал'),
        ('psychrophiles', 'Психрофильные микроорганизмы'),
        ('deep_water', 'Глубоководные формы'),
        ('symbiotic', 'Симбиотические микроорганизмы'),
        ('marine', 'Морские микроорганизмы'),
        ('freshwater', 'Пресноводные микроорганизмы'),
        ('soil', 'Почвенные микроорганизмы'),
        ('industrial', 'Промышленные штаммы'),
        ('medical', 'Медицинские штаммы'),
        ('agricultural', 'Сельскохозяйственные штаммы'),
        ('environmental', 'Экологические штаммы'),
        ('other', 'Прочие'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Название коллекции")
    code = models.CharField(max_length=20, unique=True, verbose_name="Код коллекции")
    collection_type = models.CharField(
        max_length=50, 
        choices=COLLECTION_TYPES,
        verbose_name="Тип коллекции"
    )
    description = models.TextField(verbose_name="Описание коллекции")
    curator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Куратор"
    )
    established_date = models.DateField(verbose_name="Дата создания коллекции")
    is_active = models.BooleanField(default=True, verbose_name="Активная коллекция")
    
    # Метаданные для FAIR принципов
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Публичная'),
            ('restricted', 'Ограниченная'),
            ('private', 'Частная'),
        ],
        default='public',
        verbose_name="Уровень доступа"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code}: {self.name}"
    
    def get_absolute_url(self):
        return reverse('catalog:collection_detail', kwargs={'pk': self.pk})


class Strain(models.Model):
    """Модель штамма микроорганизма"""
    
    ORGANISM_TYPES = [
        ('bacteria', 'Бактерии'),
        ('archaea', 'Археи'),
        ('fungi', 'Грибы'),
        ('yeast', 'Дрожжи'),
        ('algae', 'Водоросли'),
        ('protozoa', 'Простейшие'),
        ('virus', 'Вирусы'),
        ('other', 'Прочие'),
    ]
    
    HABITAT_TYPES = [
        ('baikal_surface', 'Поверхность Байкала'),
        ('baikal_deep', 'Глубины Байкала (>200м)'),
        ('baikal_bottom', 'Дно Байкала'),
        ('baikal_coastal', 'Прибрежная зона Байкала'),
        ('hot_springs', 'Горячие источники'),
        ('permafrost', 'Вечная мерзлота'),
        ('soil', 'Почва'),
        ('sediment', 'Донные отложения'),
        ('ice', 'Лед'),
        ('snow', 'Снег'),
        ('air', 'Воздух'),
        ('plant', 'Растения'),
        ('animal', 'Животные'),
        ('industrial', 'Промышленные объекты'),
        ('other', 'Прочие'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey(
        Collection, 
        on_delete=models.CASCADE, 
        related_name='strains',
        verbose_name="Коллекция"
    )
    
    # Основная идентификация
    strain_number = models.CharField(
        max_length=50, 
        verbose_name="Номер штамма",
        help_text="Уникальный номер в коллекции"
    )
    alternative_numbers = models.TextField(
        blank=True,
        verbose_name="Альтернативные номера",
        help_text="Другие номера штамма через запятую"
    )
    
    # Таксономическая классификация
    scientific_name = models.CharField(
        max_length=200, 
        verbose_name="Научное название"
    )
    genus = models.CharField(max_length=100, verbose_name="Род")
    species = models.CharField(max_length=100, verbose_name="Вид")
    subspecies = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Подвид"
    )
    organism_type = models.CharField(
        max_length=20,
        choices=ORGANISM_TYPES,
        verbose_name="Тип организма"
    )
    
    # Географические и экологические данные
    isolation_source = models.CharField(
        max_length=200, 
        verbose_name="Источник выделения"
    )
    habitat_type = models.CharField(
        max_length=50,
        choices=HABITAT_TYPES,
        verbose_name="Тип среды обитания"
    )
    geographic_location = models.CharField(
        max_length=200, 
        verbose_name="Географическое местоположение"
    )
    
    # Координаты для байкальских штаммов
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Широта"
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Долгота"
    )
    depth_meters = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Глубина отбора (м)"
    )
    
    # Условия культивирования
    optimal_temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Оптимальная температура (°C)"
    )
    temperature_range_min = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Мин. температура (°C)"
    )
    temperature_range_max = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Макс. температура (°C)"
    )
    optimal_ph = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        verbose_name="Оптимальный pH"
    )
    ph_range_min = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        verbose_name="Мин. pH"
    )
    ph_range_max = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        verbose_name="Макс. pH"
    )
    
    # Экстремофильные характеристики
    is_psychrophile = models.BooleanField(
        default=False, 
        verbose_name="Психрофил"
    )
    is_thermophile = models.BooleanField(
        default=False, 
        verbose_name="Термофил"
    )
    is_halophile = models.BooleanField(
        default=False, 
        verbose_name="Галофил"
    )
    is_acidophile = models.BooleanField(
        default=False, 
        verbose_name="Ацидофил"
    )
    is_alkaliphile = models.BooleanField(
        default=False, 
        verbose_name="Алкалифил"
    )
    is_barophile = models.BooleanField(
        default=False, 
        verbose_name="Барофил"
    )
    
    # Биотехнологический потенциал
    produces_antibiotics = models.BooleanField(
        default=False, 
        verbose_name="Продуцирует антибиотики"
    )
    produces_enzymes = models.BooleanField(
        default=False, 
        verbose_name="Продуцирует ферменты"
    )
    produces_metabolites = models.BooleanField(
        default=False, 
        verbose_name="Продуцирует метаболиты"
    )
    nitrogen_fixation = models.BooleanField(
        default=False, 
        verbose_name="Азотфиксация"
    )
    
    # Геномные данные
    genome_size = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Размер генома (bp)"
    )
    gc_content = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="GC-состав (%)"
    )
    has_genome_sequence = models.BooleanField(
        default=False, 
        verbose_name="Геном секвенирован"
    )
    
    # Даты и статус
    isolation_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Дата выделения"
    )
    deposit_date = models.DateField(verbose_name="Дата депонирования")
    is_available = models.BooleanField(
        default=True, 
        verbose_name="Доступен для заказа"
    )
    is_type_strain = models.BooleanField(
        default=False, 
        verbose_name="Типовой штамм"
    )
    
    # Метаданные
    description = models.TextField(
        blank=True, 
        verbose_name="Описание"
    )
    special_properties = models.TextField(
        blank=True, 
        verbose_name="Особые свойства"
    )
    cultivation_notes = models.TextField(
        blank=True, 
        verbose_name="Особенности культивирования"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Штамм"
        verbose_name_plural = "Штаммы"
        ordering = ['collection', 'strain_number']
        unique_together = ['collection', 'strain_number']
        indexes = [
            models.Index(fields=['scientific_name']),
            models.Index(fields=['genus', 'species']),
            models.Index(fields=['habitat_type']),
            models.Index(fields=['is_psychrophile']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.collection.code}-{self.strain_number}: {self.scientific_name}"
    
    def get_absolute_url(self):
        return reverse('catalog:strain_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        """Полное название с коллекцией и номером"""
        return f"{self.collection.code}-{self.strain_number}"
    
    @property
    def is_baikal_endemic(self):
        """Проверка на эндемичность для Байкала"""
        baikal_habitats = [
            'baikal_surface', 'baikal_deep', 'baikal_bottom', 'baikal_coastal'
        ]
        return self.habitat_type in baikal_habitats
    
    @property
    def extremophile_types(self):
        """Список типов экстремофильности"""
        types = []
        if self.is_psychrophile:
            types.append('Психрофил')
        if self.is_thermophile:
            types.append('Термофил')
        if self.is_halophile:
            types.append('Галофил')
        if self.is_acidophile:
            types.append('Ацидофил')
        if self.is_alkaliphile:
            types.append('Алкалифил')
        if self.is_barophile:
            types.append('Барофил')
        return types


class GenomeSequence(models.Model):
    """Модель геномной последовательности"""
    
    SEQUENCE_TYPES = [
        ('complete', 'Полный геном'),
        ('draft', 'Черновой геном'),
        ('contig', 'Контиг'),
        ('scaffold', 'Скаффолд'),
        ('plasmid', 'Плазмида'),
        ('16s_rrna', '16S рРНК'),
        ('its', 'ITS'),
        ('other', 'Прочее'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain = models.ForeignKey(
        Strain, 
        on_delete=models.CASCADE, 
        related_name='genome_sequences',
        verbose_name="Штамм"
    )
    
    sequence_type = models.CharField(
        max_length=20,
        choices=SEQUENCE_TYPES,
        verbose_name="Тип последовательности"
    )
    accession_number = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Номер доступа"
    )
    database = models.CharField(
        max_length=50, 
        default='NCBI',
        verbose_name="База данных"
    )
    sequence_length = models.PositiveIntegerField(verbose_name="Длина последовательности")
    
    # FASTA последовательность (для небольших последовательностей)
    sequence_data = models.TextField(
        blank=True,
        verbose_name="Данные последовательности"
    )
    
    # Метаданные
    submission_date = models.DateField(verbose_name="Дата депонирования")
    quality_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Показатель качества"
    )
    coverage = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Покрытие"
    )
    
    notes = models.TextField(blank=True, verbose_name="Примечания")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Геномная последовательность"
        verbose_name_plural = "Геномные последовательности"
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.strain.full_name} - {self.get_sequence_type_display()} ({self.accession_number})"


class Publication(models.Model):
    """Модель научной публикации, связанной со штаммами"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strains = models.ManyToManyField(
        Strain, 
        related_name='publications',
        verbose_name="Штаммы"
    )
    
    title = models.CharField(max_length=500, verbose_name="Название")
    authors = models.TextField(verbose_name="Авторы")
    journal = models.CharField(max_length=200, verbose_name="Журнал")
    volume = models.CharField(max_length=20, blank=True, verbose_name="Том")
    issue = models.CharField(max_length=20, blank=True, verbose_name="Выпуск")
    pages = models.CharField(max_length=50, blank=True, verbose_name="Страницы")
    year = models.PositiveIntegerField(verbose_name="Год публикации")
    
    doi = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="DOI"
    )
    pmid = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="PubMed ID"
    )
    url = models.URLField(blank=True, verbose_name="URL")
    
    abstract = models.TextField(blank=True, verbose_name="Аннотация")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
