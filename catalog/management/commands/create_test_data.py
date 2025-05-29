from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid
from datetime import date, timedelta

from catalog.models import Collection, Strain, GenomeSequence, Publication


class Command(BaseCommand):
    help = 'Создает тестовые данные для коллекций микроорганизмов СИФИБР СО РАН'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед созданием новых',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            Publication.objects.all().delete()
            GenomeSequence.objects.all().delete()
            Strain.objects.all().delete()
            Collection.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Данные очищены'))

        self.stdout.write('Создание тестовых данных для СИФИБР СО РАН...')
        
        # Создаем или получаем пользователей-кураторов
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@sifibr.irk.ru',
                'first_name': 'Администратор',
                'last_name': 'СИФИБР',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        curator1, created = User.objects.get_or_create(
            username='ivanov',
            defaults={
                'email': 'ivanov@sifibr.irk.ru',
                'first_name': 'Иван',
                'last_name': 'Иванов'
            }
        )
        
        curator2, created = User.objects.get_or_create(
            username='petrov',
            defaults={
                'email': 'petrov@sifibr.irk.ru',
                'first_name': 'Петр',
                'last_name': 'Петров'
            }
        )

        # Создаем коллекции СИФИБР
        collections_data = [
            {
                'name': 'Коллекция психрофильных микроорганизмов Байкала',
                'code': 'СИФИБР-ПМБ',
                'collection_type': 'psychrophiles',
                'description': 'Уникальная коллекция психрофильных (холодолюбивых) микроорганизмов, выделенных из различных экологических ниш озера Байкал. Включает бактерии, способные активно расти при температурах от -2°C до +15°C.',
                'curator': curator1,
                'established_date': date(2010, 3, 15),
            },
            {
                'name': 'Коллекция экстремофильных микроорганизмов',
                'code': 'СИФИБР-ЭМ',
                'collection_type': 'extremophiles',
                'description': 'Коллекция микроорганизмов, адаптированных к экстремальным условиям: высокие и низкие температуры, экстремальные значения pH, высокие концентрации солей и тяжелых металлов.',
                'curator': curator2,
                'established_date': date(2008, 7, 22),
            },
            {
                'name': 'Коллекция эндемичных микроорганизмов озера Байкал',
                'code': 'СИФИБР-ЭБ',
                'collection_type': 'baikal_endemic',
                'description': 'Коллекция эндемичных видов микроорганизмов, встречающихся исключительно в экосистеме озера Байкал. Многие виды являются реликтовыми и имеют древнее происхождение.',
                'curator': curator1,
                'established_date': date(2012, 5, 8),
            },
            {
                'name': 'Коллекция продуцентов биологически активных веществ',
                'code': 'СИФИБР-БАВ',
                'collection_type': 'bioactive',
                'description': 'Штаммы микроорганизмов, продуцирующие биологически активные соединения с потенциальным применением в медицине, сельском хозяйстве и биотехнологии.',
                'curator': curator2,
                'established_date': date(2015, 11, 12),
            },
            {
                'name': 'Коллекция глубоководных микроорганизмов Байкала',
                'code': 'СИФИБР-ГМБ',
                'collection_type': 'deep_water',
                'description': 'Микроорганизмы, выделенные с глубин более 200 метров озера Байкал. Адаптированы к условиям повышенного давления и низкой освещенности.',
                'curator': admin_user,
                'established_date': date(2018, 9, 3),
            }
        ]

        collections = []
        for coll_data in collections_data:
            collection = Collection.objects.create(**coll_data)
            collections.append(collection)
            self.stdout.write(f'✅ Создана коллекция: {collection.code}')

        # Создаем штаммы для каждой коллекции
        strains_data = [
            # Психрофильные микроорганизмы Байкала
            {
                'collection': collections[0],  # СИФИБР-ПМБ
                'strain_number': '001',
                'scientific_name': 'Psychrobacter baikalensis',
                'genus': 'Psychrobacter',
                'species': 'baikalensis',
                'organism_type': 'bacteria',
                'isolation_source': 'Поверхностные воды озера Байкал',
                'habitat_type': 'baikal_surface',
                'geographic_location': 'Южный Байкал, бухта Листвянка',
                'latitude': Decimal('51.8477'),
                'longitude': Decimal('104.8661'),
                'depth_meters': 5,
                'optimal_temperature': Decimal('4.0'),
                'temperature_range_min': Decimal('-2.0'),
                'temperature_range_max': Decimal('15.0'),
                'optimal_ph': Decimal('7.2'),
                'ph_range_min': Decimal('6.5'),
                'ph_range_max': Decimal('8.0'),
                'is_psychrophile': True,
                'produces_enzymes': True,
                'isolation_date': date(2020, 8, 15),
                'deposit_date': date(2020, 9, 1),
                'description': 'Психрофильная бактерия, способная расти при температуре ледяной воды. Продуцирует холодоактивные ферменты.',
                'special_properties': 'Высокая активность при низких температурах, устойчивость к замораживанию',
            },
            {
                'collection': collections[0],  # СИФИБР-ПМБ
                'strain_number': '002',
                'scientific_name': 'Flavobacterium frigoris',
                'genus': 'Flavobacterium',
                'species': 'frigoris',
                'organism_type': 'bacteria',
                'isolation_source': 'Лед озера Байкал',
                'habitat_type': 'ice',
                'geographic_location': 'Северный Байкал, мыс Котельниковский',
                'latitude': Decimal('55.7558'),
                'longitude': Decimal('109.8133'),
                'depth_meters': 0,
                'optimal_temperature': Decimal('2.0'),
                'temperature_range_min': Decimal('-5.0'),
                'temperature_range_max': Decimal('12.0'),
                'optimal_ph': Decimal('6.8'),
                'ph_range_min': Decimal('6.0'),
                'ph_range_max': Decimal('7.5'),
                'is_psychrophile': True,
                'produces_antibiotics': True,
                'isolation_date': date(2021, 2, 20),
                'deposit_date': date(2021, 3, 5),
                'description': 'Психрофильная бактерия из льда Байкала с антибиотическими свойствами.',
            },
            
            # Экстремофильные микроорганизмы
            {
                'collection': collections[1],  # СИФИБР-ЭМ
                'strain_number': '003',
                'scientific_name': 'Thermus baikalensis',
                'genus': 'Thermus',
                'species': 'baikalensis',
                'organism_type': 'bacteria',
                'isolation_source': 'Горячие источники Байкальского региона',
                'habitat_type': 'hot_springs',
                'geographic_location': 'Горячинск, Восточное побережье Байкала',
                'latitude': Decimal('52.0833'),
                'longitude': Decimal('108.2167'),
                'optimal_temperature': Decimal('65.0'),
                'temperature_range_min': Decimal('45.0'),
                'temperature_range_max': Decimal('85.0'),
                'optimal_ph': Decimal('7.5'),
                'ph_range_min': Decimal('6.5'),
                'ph_range_max': Decimal('8.5'),
                'is_thermophile': True,
                'produces_enzymes': True,
                'has_genome_sequence': True,
                'genome_size': 2100000,
                'gc_content': Decimal('69.4'),
                'isolation_date': date(2019, 6, 10),
                'deposit_date': date(2019, 7, 15),
                'description': 'Термофильная бактерия из горячих источников с высокотемпературными ферментами.',
                'special_properties': 'Термостабильные ферменты, устойчивость к высоким температурам',
            },
            {
                'collection': collections[1],  # СИФИБР-ЭМ
                'strain_number': '004',
                'scientific_name': 'Halobacterium baikalense',
                'genus': 'Halobacterium',
                'species': 'baikalense',
                'organism_type': 'archaea',
                'isolation_source': 'Соленые озера Прибайкалья',
                'habitat_type': 'other',
                'geographic_location': 'Озеро Киран, Ольхон',
                'latitude': Decimal('53.1507'),
                'longitude': Decimal('107.3470'),
                'optimal_temperature': Decimal('37.0'),
                'temperature_range_min': Decimal('25.0'),
                'temperature_range_max': Decimal('50.0'),
                'optimal_ph': Decimal('7.0'),
                'ph_range_min': Decimal('6.0'),
                'ph_range_max': Decimal('8.0'),
                'is_halophile': True,
                'produces_metabolites': True,
                'isolation_date': date(2020, 5, 12),
                'deposit_date': date(2020, 6, 8),
                'description': 'Галофильная археа из соленых озер, продуцирует уникальные метаболиты.',
            },
            
            # Эндемичные микроорганизмы Байкала
            {
                'collection': collections[2],  # СИФИБР-ЭБ
                'strain_number': '005',
                'scientific_name': 'Baikalia profundus',
                'genus': 'Baikalia',
                'species': 'profundus',
                'organism_type': 'bacteria',
                'isolation_source': 'Донные отложения озера Байкал',
                'habitat_type': 'baikal_bottom',
                'geographic_location': 'Центральная котловина Байкала',
                'latitude': Decimal('53.5000'),
                'longitude': Decimal('107.5000'),
                'depth_meters': 1200,
                'optimal_temperature': Decimal('4.5'),
                'temperature_range_min': Decimal('2.0'),
                'temperature_range_max': Decimal('8.0'),
                'optimal_ph': Decimal('7.8'),
                'ph_range_min': Decimal('7.0'),
                'ph_range_max': Decimal('8.5'),
                'is_psychrophile': True,
                'is_barophile': True,
                'nitrogen_fixation': True,
                'has_genome_sequence': True,
                'genome_size': 4500000,
                'gc_content': Decimal('62.1'),
                'is_type_strain': True,
                'isolation_date': date(2017, 7, 22),
                'deposit_date': date(2017, 8, 30),
                'description': 'Эндемичная глубоководная бактерия Байкала, способная к азотфиксации.',
                'special_properties': 'Эндемик Байкала, барофильные свойства, азотфиксация',
            },
            
            # Продуценты БАВ
            {
                'collection': collections[3],  # СИФИБР-БАВ
                'strain_number': '006',
                'scientific_name': 'Streptomyces baikalensis',
                'genus': 'Streptomyces',
                'species': 'baikalensis',
                'organism_type': 'bacteria',
                'isolation_source': 'Прибрежная почва озера Байкал',
                'habitat_type': 'soil',
                'geographic_location': 'Малое Море, остров Ольхон',
                'latitude': Decimal('53.2000'),
                'longitude': Decimal('107.0000'),
                'optimal_temperature': Decimal('28.0'),
                'temperature_range_min': Decimal('15.0'),
                'temperature_range_max': Decimal('37.0'),
                'optimal_ph': Decimal('7.0'),
                'ph_range_min': Decimal('6.0'),
                'ph_range_max': Decimal('8.0'),
                'produces_antibiotics': True,
                'produces_enzymes': True,
                'produces_metabolites': True,
                'isolation_date': date(2021, 5, 8),
                'deposit_date': date(2021, 6, 12),
                'description': 'Актинобактерия, продуцирующая широкий спектр биологически активных веществ.',
                'special_properties': 'Продукция новых антибиотиков, противогрибковая активность',
            },
            
            # Глубоководные микроорганизмы
            {
                'collection': collections[4],  # СИФИБР-ГМБ
                'strain_number': '007',
                'scientific_name': 'Shewanella profunda',
                'genus': 'Shewanella',
                'species': 'profunda',
                'organism_type': 'bacteria',
                'isolation_source': 'Глубоководные слои озера Байкал',
                'habitat_type': 'baikal_deep',
                'geographic_location': 'Северная котловина Байкала',
                'latitude': Decimal('55.0000'),
                'longitude': Decimal('109.0000'),
                'depth_meters': 800,
                'optimal_temperature': Decimal('4.0'),
                'temperature_range_min': Decimal('2.0'),
                'temperature_range_max': Decimal('10.0'),
                'optimal_ph': Decimal('7.5'),
                'ph_range_min': Decimal('7.0'),
                'ph_range_max': Decimal('8.0'),
                'is_psychrophile': True,
                'is_barophile': True,
                'produces_enzymes': True,
                'has_genome_sequence': True,
                'genome_size': 4800000,
                'gc_content': Decimal('45.2'),
                'isolation_date': date(2022, 4, 15),
                'deposit_date': date(2022, 5, 20),
                'description': 'Глубоководная психробарофильная бактерия с уникальными ферментативными свойствами.',
                'special_properties': 'Адаптация к высокому давлению, металлоредукция',
            }
        ]

        strains = []
        for strain_data in strains_data:
            strain = Strain.objects.create(**strain_data)
            strains.append(strain)
            self.stdout.write(f'✅ Создан штамм: {strain.full_name}')

        # Создаем геномные последовательности
        genome_data = [
            {
                'strain': strains[2],  # Thermus baikalensis
                'sequence_type': 'complete',
                'accession_number': 'CP123456',
                'database': 'NCBI',
                'sequence_length': 2100000,
                'submission_date': date(2020, 1, 15),
                'quality_score': Decimal('95.5'),
                'coverage': Decimal('150.0'),
                'notes': 'Полный геном, высококачественная сборка',
            },
            {
                'strain': strains[4],  # Baikalia profundus
                'sequence_type': 'complete',
                'accession_number': 'CP789012',
                'database': 'NCBI',
                'sequence_length': 4500000,
                'submission_date': date(2018, 3, 20),
                'quality_score': Decimal('98.2'),
                'coverage': Decimal('200.0'),
                'notes': 'Эталонный геном эндемичного вида Байкала',
            },
            {
                'strain': strains[6],  # Shewanella profunda
                'sequence_type': 'draft',
                'accession_number': 'JABC01000001',
                'database': 'NCBI',
                'sequence_length': 4800000,
                'submission_date': date(2022, 8, 10),
                'quality_score': Decimal('87.3'),
                'coverage': Decimal('120.0'),
                'notes': 'Черновая сборка генома',
            }
        ]

        for genome in genome_data:
            GenomeSequence.objects.create(**genome)
            self.stdout.write(f'✅ Создана геномная последовательность: {genome["accession_number"]}')

        # Создаем публикации
        publication_data = [
            {
                'title': 'Психрофильные микроорганизмы озера Байкал: разнообразие и биотехнологический потенциал',
                'authors': 'Иванов И.И., Петров П.П., Сидоров С.С.',
                'journal': 'Микробиология',
                'volume': '91',
                'issue': '3',
                'pages': '345-358',
                'year': 2022,
                'doi': '10.1134/S0026261722030012',
                'abstract': 'Исследование психрофильных микроорганизмов озера Байкал показало высокое разнообразие холодоадаптированных бактерий.',
            },
            {
                'title': 'Genomic insights into cold adaptation of Baikalia profundus, an endemic bacterium from Lake Baikal',
                'authors': 'Petrov P.P., Ivanov I.I., Smith J.D.',
                'journal': 'Applied and Environmental Microbiology',
                'volume': '88',
                'issue': '15',
                'pages': 'e01234-22',
                'year': 2022,
                'doi': '10.1128/AEM.01234-22',
                'pmid': '35678901',
                'abstract': 'Complete genome sequencing of Baikalia profundus revealed unique adaptations to deep-water conditions.',
            }
        ]

        publications = []
        for pub_data in publication_data:
            strains_for_pub = pub_data.pop('strains', [])
            publication = Publication.objects.create(**pub_data)
            publications.append(publication)
            self.stdout.write(f'✅ Создана публикация: {publication.title[:50]}...')

        # Связываем публикации со штаммами
        publications[0].strains.add(strains[0], strains[1])  # Психрофилы
        publications[1].strains.add(strains[4])  # Baikalia profundus

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Успешно создано:'))
        self.stdout.write(self.style.SUCCESS(f'   📁 {Collection.objects.count()} коллекций'))
        self.stdout.write(self.style.SUCCESS(f'   🦠 {Strain.objects.count()} штаммов'))
        self.stdout.write(self.style.SUCCESS(f'   🧬 {GenomeSequence.objects.count()} геномных последовательностей'))
        self.stdout.write(self.style.SUCCESS(f'   📚 {Publication.objects.count()} публикаций'))
        self.stdout.write(self.style.SUCCESS(f'\n✅ Тестовые данные для СИФИБР СО РАН созданы!'))
        self.stdout.write(self.style.WARNING(f'🔗 Сайт доступен на: http://127.0.0.1:8000/')) 