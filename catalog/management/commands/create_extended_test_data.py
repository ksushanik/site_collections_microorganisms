from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid
from datetime import date, timedelta

from catalog.models import Collection, Strain, GenomeSequence, Publication


class Command(BaseCommand):
    help = 'Создает расширенный набор тестовых данных для демонстрации возможностей системы'

    def add_arguments(self, parser):
        parser.add_argument(
            '--collections',
            type=int,
            default=10,
            help='Количество дополнительных коллекций',
        )
        parser.add_argument(
            '--strains-per-collection',
            type=int,
            default=15,
            help='Количество штаммов на коллекцию',
        )

    def handle(self, *args, **options):
        collections_count = options['collections']
        strains_per_collection = options['strains_per_collection']
        
        self.stdout.write(f'Создание {collections_count} дополнительных коллекций...')
        self.stdout.write(f'По {strains_per_collection} штаммов в каждой коллекции...')
        
        # Получаем существующих кураторов
        curators = list(User.objects.all())
        
        # Дополнительные типы коллекций и данные
        additional_collections = [
            {
                'name': 'Коллекция азотфиксирующих микроорганизмов',
                'code': 'СИФИБР-АФ',
                'collection_type': 'nitrogen_fixing',
                'description': 'Микроорганизмы, способные к фиксации атмосферного азота, важные для биогеохимических циклов Байкала.',
                'established_date': date(2016, 4, 20),
            },
            {
                'name': 'Коллекция продуцентов антибиотиков',
                'code': 'СИФИБР-АНТ',
                'collection_type': 'antibiotic',
                'description': 'Штаммы, продуцирующие антибиотические соединения с потенциалом для медицинского применения.',
                'established_date': date(2014, 8, 15),
            },
            {
                'name': 'Коллекция симбиотических микроорганизмов',
                'code': 'СИФИБР-СИМ',
                'collection_type': 'symbiotic',
                'description': 'Микроорганизмы, находящиеся в симбиотических отношениях с байкальской фауной и флорой.',
                'established_date': date(2017, 6, 12),
            },
            {
                'name': 'Коллекция почвенных микроорганизмов Прибайкалья',
                'code': 'СИФИБР-ПОЧ',
                'collection_type': 'soil',
                'description': 'Разнообразие почвенных микроорганизмов водосборного бассейна озера Байкал.',
                'established_date': date(2013, 9, 8),
            },
            {
                'name': 'Коллекция промышленных штаммов',
                'code': 'СИФИБР-ПРОМ',
                'collection_type': 'industrial',
                'description': 'Штаммы с промышленным потенциалом для биотехнологических производств.',
                'established_date': date(2019, 3, 25),
            },
            {
                'name': 'Коллекция медицинских штаммов',
                'code': 'СИФИБР-МЕД',
                'collection_type': 'medical',
                'description': 'Штаммы с потенциалом для медицинского и фармацевтического применения.',
                'established_date': date(2020, 11, 18),
            },
            {
                'name': 'Коллекция автотрофных микроорганизмов',
                'code': 'СИФИБР-АВТ',
                'collection_type': 'autotrophic',
                'description': 'Автотрофные микроорганизмы, играющие ключевую роль в первичной продукции Байкала.',
                'established_date': date(2015, 7, 30),
            },
        ]
        
        # Создаем дополнительные коллекции
        new_collections = []
        for i, coll_data in enumerate(additional_collections[:collections_count]):
            coll_data['curator'] = curators[i % len(curators)]
            collection = Collection.objects.create(**coll_data)
            new_collections.append(collection)
            self.stdout.write(f'✅ Создана коллекция: {collection.code}')
        
        # Шаблоны для генерации штаммов
        baikal_locations = [
            ('Южный Байкал, мыс Шаманский', Decimal('51.8000'), Decimal('104.8000')),
            ('Средний Байкал, остров Ольхон', Decimal('53.2000'), Decimal('107.0000')),
            ('Северный Байкал, бухта Хакусы', Decimal('55.6000'), Decimal('109.8000')),
            ('Малое Море, пролив Ольхонские ворота', Decimal('53.1000'), Decimal('106.9000')),
            ('Баргузинский залив', Decimal('53.5000'), Decimal('108.7000')),
            ('Чивыркуйский залив', Decimal('53.9000'), Decimal('109.1000')),
            ('Провал, бухта Песчаная', Decimal('51.8500'), Decimal('105.0000')),
            ('Слюдянка, южная оконечность', Decimal('51.6500'), Decimal('103.7000')),
        ]
        
        genera_templates = {
            'nitrogen_fixing': ['Azotobacter', 'Rhizobium', 'Clostridium', 'Anabaena', 'Nostoc'],
            'antibiotic': ['Streptomyces', 'Penicillium', 'Bacillus', 'Pseudomonas', 'Micromonospora'],
            'symbiotic': ['Rhizobium', 'Mycorrhiza', 'Bradyrhizobium', 'Frankia', 'Glomus'],
            'soil': ['Bacillus', 'Pseudomonas', 'Azotobacter', 'Actinomyces', 'Arthrobacter'],
            'industrial': ['Saccharomyces', 'Aspergillus', 'Rhizopus', 'Mucor', 'Penicillium'],
            'medical': ['Lactobacillus', 'Bifidobacterium', 'Streptococcus', 'Enterococcus', 'Bacillus'],
            'autotrophic': ['Synechococcus', 'Anabaena', 'Chlorella', 'Spirulina', 'Oscillatoria'],
        }
        
        habitat_mapping = {
            'nitrogen_fixing': 'soil',
            'antibiotic': 'baikal_bottom', 
            'symbiotic': 'plant',
            'soil': 'soil',
            'industrial': 'baikal_surface',
            'medical': 'baikal_coastal',
            'autotrophic': 'baikal_surface',
        }
        
        total_strains = 0
        
        # Создаем штаммы для каждой новой коллекции
        for collection in new_collections:
            genera = genera_templates.get(collection.collection_type, ['Bacterium', 'Microorganism'])
            habitat = habitat_mapping.get(collection.collection_type, 'other')
            
            for strain_num in range(1, strains_per_collection + 1):
                location, lat, lon = baikal_locations[strain_num % len(baikal_locations)]
                genus = genera[strain_num % len(genera)]
                
                strain_data = {
                    'collection': collection,
                    'strain_number': f'{strain_num:03d}',
                    'scientific_name': f'{genus} baikalensis',
                    'genus': genus,
                    'species': 'baikalensis',
                    'organism_type': 'bacteria',
                    'isolation_source': f'Образцы из {location}',
                    'habitat_type': habitat,
                    'geographic_location': location,
                    'latitude': lat + Decimal(str((strain_num * 0.01) % 0.1)),
                    'longitude': lon + Decimal(str((strain_num * 0.01) % 0.1)),
                    'depth_meters': (strain_num * 10) % 500 if habitat in ['baikal_deep', 'baikal_bottom'] else None,
                    'optimal_temperature': Decimal(str(4 + (strain_num % 20))),
                    'temperature_range_min': Decimal(str(max(-2, 4 + (strain_num % 20) - 5))),
                    'temperature_range_max': Decimal(str(4 + (strain_num % 20) + 10)),
                    'optimal_ph': Decimal(str(6.5 + (strain_num % 3) * 0.5)),
                    'ph_range_min': Decimal(str(6.0 + (strain_num % 3) * 0.3)),
                    'ph_range_max': Decimal(str(8.0 + (strain_num % 3) * 0.3)),
                    'is_psychrophile': strain_num % 3 == 0,
                    'is_thermophile': strain_num % 7 == 0,
                    'is_halophile': strain_num % 5 == 0,
                    'produces_antibiotics': collection.collection_type == 'antibiotic' or strain_num % 8 == 0,
                    'produces_enzymes': strain_num % 4 == 0,
                    'nitrogen_fixation': collection.collection_type == 'nitrogen_fixing' or strain_num % 6 == 0,
                    'produces_metabolites': strain_num % 7 == 0,
                    'has_genome_sequence': strain_num % 10 == 0,
                    'genome_size': (2000000 + strain_num * 10000) if strain_num % 10 == 0 else None,
                    'gc_content': Decimal(str(45 + (strain_num % 30))) if strain_num % 10 == 0 else None,
                    'isolation_date': date(2018, 1, 1) + timedelta(days=strain_num * 10),
                    'deposit_date': date(2018, 1, 1) + timedelta(days=strain_num * 10 + 30),
                    'description': f'Штамм {genus} baikalensis, выделенный из {location}',
                    'special_properties': self._generate_special_properties(collection.collection_type, strain_num),
                }
                
                Strain.objects.create(**strain_data)
                total_strains += 1
                
                if strain_num % 10 == 0:
                    self.stdout.write(f'  ✅ Создано {strain_num} штаммов для {collection.code}')
        
        # Создаем дополнительные геномные последовательности
        sequenced_strains = Strain.objects.filter(has_genome_sequence=True)
        sequences_count = 0
        
        for i, strain in enumerate(sequenced_strains):
            if not strain.genome_sequences.exists():  # Только если еще нет последовательностей
                sequence_data = {
                    'strain': strain,
                    'sequence_type': 'complete' if i % 3 == 0 else 'draft',
                    'accession_number': f'CP{100000 + i:06d}',
                    'database': 'NCBI',
                    'sequence_length': strain.genome_size or 2500000,
                    'submission_date': strain.deposit_date + timedelta(days=60),
                    'quality_score': Decimal(str(85 + (i % 15))),
                    'coverage': Decimal(str(100 + (i % 100))),
                    'notes': f'Геномная последовательность для {strain.scientific_name}',
                }
                GenomeSequence.objects.create(**sequence_data)
                sequences_count += 1
        
        # Статистика
        total_collections = Collection.objects.count()
        total_strains_db = Strain.objects.count()
        total_sequences = GenomeSequence.objects.count()
        total_publications = Publication.objects.count()
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🎉 РАСШИРЕННЫЕ ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ!'))
        self.stdout.write('='*60)
        self.stdout.write(f'📁 Всего коллекций: {total_collections}')
        self.stdout.write(f'🦠 Всего штаммов: {total_strains_db}')
        self.stdout.write(f'🧬 Всего геномных последовательностей: {total_sequences}')
        self.stdout.write(f'📚 Всего публикаций: {total_publications}')
        self.stdout.write('\n📊 Распределение по типам коллекций:')
        
        for collection_type, display_name in Collection.COLLECTION_TYPES:
            count = Collection.objects.filter(collection_type=collection_type).count()
            if count > 0:
                self.stdout.write(f'   {display_name}: {count} коллекций')
        
        self.stdout.write(f'\n🔗 Сайт доступен на: http://127.0.0.1:8001/')
        self.stdout.write('✅ Данные готовы для демонстрации!')
    
    def _generate_special_properties(self, collection_type, strain_num):
        """Генерирует специальные свойства в зависимости от типа коллекции"""
        properties = {
            'nitrogen_fixing': [
                'Высокая активность нитрогеназы',
                'Устойчивость к кислороду при азотфиксации',
                'Симбиоз с водными растениями',
                'Толерантность к низким температурам'
            ],
            'antibiotic': [
                'Широкий спектр антибактериальной активности',
                'Продукция новых β-лактамов',
                'Активность против грибов',
                'Низкая токсичность для эукариот'
            ],
            'symbiotic': [
                'Образование клубеньков на корнях',
                'Микоризные ассоциации',
                'Эндофитные свойства',
                'Стимуляция роста растений'
            ],
            'soil': [
                'Деградация органических полютантов',
                'Мобилизация фосфора',
                'Подавление фитопатогенов',
                'Устойчивость к засухе'
            ],
            'industrial': [
                'Продукция ферментов для пищевой промышленности',
                'Биосинтез аминокислот',
                'Устойчивость к высоким концентрациям субстрата',
                'Быстрый рост в биореакторах'
            ],
            'medical': [
                'Пробиотические свойства',
                'Иммуномодулирующая активность',
                'Антиоксидантные свойства',
                'Устойчивость к кислотности желудка'
            ],
            'autotrophic': [
                'Высокая эффективность фотосинтеза',
                'CO2-фиксация при низких температурах',
                'Продукция кислорода',
                'Накопление липидов'
            ]
        }
        
        type_properties = properties.get(collection_type, ['Уникальные адаптации к байкальским условиям'])
        return type_properties[strain_num % len(type_properties)] 