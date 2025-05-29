from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse


class Command(BaseCommand):
    help = 'Анализирует существующий прототип сайта коллекций микроорганизмов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default='https://dencr0m8eu.space.minimax.io/',
            help='URL прототипа для анализа',
        )
        parser.add_argument(
            '--output',
            type=str,
            default='prototype_analysis.json',
            help='Файл для сохранения результатов анализа',
        )

    def handle(self, *args, **options):
        prototype_url = options['url']
        output_file = options['output']
        
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('🔍 АНАЛИЗ ПРОТОТИПА СИФИБР'))
        self.stdout.write('='*60)
        self.stdout.write(f'📍 URL: {prototype_url}')
        self.stdout.write('')
        
        analysis_results = {
            'url': prototype_url,
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'accessibility': {},
            'ui_elements': {},
            'technical_stack': {},
            'performance': {},
            'features': {},
            'content_analysis': {},
            'recommendations': []
        }
        
        try:
            # 1. Проверяем доступность
            self.stdout.write('1️⃣ Проверка доступности...')
            response = requests.get(prototype_url, timeout=10)
            analysis_results['accessibility'] = {
                'status_code': response.status_code,
                'response_time_ms': response.elapsed.total_seconds() * 1000,
                'accessible': response.status_code == 200,
                'content_length': len(response.content),
                'encoding': response.encoding
            }
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f'   ✅ Сайт доступен (HTTP {response.status_code})'))
                self.stdout.write(f'   ⏱️ Время ответа: {response.elapsed.total_seconds()*1000:.0f}ms')
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Сайт недоступен (HTTP {response.status_code})'))
                return
            
            # 2. Анализируем HTML структуру
            self.stdout.write('\n2️⃣ Анализ HTML структуры...')
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Заголовок и метаданные
            title = soup.find('title')
            analysis_results['content_analysis']['title'] = title.text.strip() if title else 'Не найден'
            
            meta_description = soup.find('meta', attrs={'name': 'description'})
            analysis_results['content_analysis']['description'] = (
                meta_description.get('content') if meta_description else 'Не найдена'
            )
            
            # Подсчет основных элементов
            ui_elements = {
                'tables': len(soup.find_all('table')),
                'forms': len(soup.find_all('form')),
                'buttons': len(soup.find_all('button')),
                'inputs': len(soup.find_all('input')),
                'select': len(soup.find_all('select')),
                'links': len(soup.find_all('a')),
                'images': len(soup.find_all('img')),
                'h1': len(soup.find_all('h1')),
                'h2': len(soup.find_all('h2')),
                'h3': len(soup.find_all('h3')),
            }
            analysis_results['ui_elements'] = ui_elements
            
            self.stdout.write(f'   📊 Таблицы: {ui_elements["tables"]}')
            self.stdout.write(f'   📝 Формы: {ui_elements["forms"]}')
            self.stdout.write(f'   🔘 Кнопки: {ui_elements["buttons"]}')
            self.stdout.write(f'   🔗 Ссылки: {ui_elements["links"]}')
            
            # 3. Анализируем технологии
            self.stdout.write('\n3️⃣ Анализ технологий...')
            tech_stack = {
                'has_jquery': bool(soup.find_all(text=lambda text: text and 'jquery' in text.lower())),
                'has_bootstrap': bool(soup.find_all('link', href=lambda x: x and 'bootstrap' in x)),
                'has_react': bool(soup.find_all(text=lambda text: text and 'react' in text.lower())),
                'has_angular': bool(soup.find_all(text=lambda text: text and 'angular' in text.lower())),
                'has_vue': bool(soup.find_all(text=lambda text: text and 'vue' in text.lower())),
                'external_scripts': [],
                'external_stylesheets': []
            }
            
            # Внешние скрипты
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src and src.startswith('http'):
                    tech_stack['external_scripts'].append(src)
            
            # Внешние стили
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href and href.startswith('http'):
                    tech_stack['external_stylesheets'].append(href)
            
            analysis_results['technical_stack'] = tech_stack
            
            frameworks_found = []
            if tech_stack['has_jquery']: frameworks_found.append('jQuery')
            if tech_stack['has_bootstrap']: frameworks_found.append('Bootstrap')
            if tech_stack['has_react']: frameworks_found.append('React')
            if tech_stack['has_angular']: frameworks_found.append('Angular')
            if tech_stack['has_vue']: frameworks_found.append('Vue.js')
            
            if frameworks_found:
                self.stdout.write(f'   🔧 Обнаружены: {", ".join(frameworks_found)}')
            else:
                self.stdout.write('   🔧 Основные фреймворки не обнаружены')
            
            # 4. Анализируем функциональность
            self.stdout.write('\n4️⃣ Анализ функциональности...')
            features = {
                'has_search': bool(soup.find_all('input', type='search') or 
                                 soup.find_all('input', placeholder=lambda x: x and 'поиск' in x.lower())),
                'has_filters': bool(soup.find_all('select') or 
                                  soup.find_all('input', type='checkbox')),
                'has_sorting': bool(soup.find_all('th') and 
                                  soup.find_all('a', href=lambda x: x and 'sort' in x)),
                'has_pagination': bool(soup.find_all('a', href=lambda x: x and 'page' in x)),
                'has_export': bool(soup.find_all('a', href=lambda x: x and ('export' in x or 'download' in x))),
                'data_tables': [],
                'interactive_elements': []
            }
            
            # Анализируем таблицы данных
            for table in soup.find_all('table'):
                headers = [th.get_text().strip() for th in table.find_all('th')]
                rows_count = len(table.find_all('tr')) - 1  # минус заголовок
                features['data_tables'].append({
                    'headers': headers,
                    'rows_count': rows_count,
                    'has_headers': len(headers) > 0
                })
            
            analysis_results['features'] = features
            
            feature_summary = []
            if features['has_search']: feature_summary.append('поиск')
            if features['has_filters']: feature_summary.append('фильтры')
            if features['has_sorting']: feature_summary.append('сортировка')
            if features['has_pagination']: feature_summary.append('пагинация')
            if features['has_export']: feature_summary.append('экспорт')
            
            if feature_summary:
                self.stdout.write(f'   ⚙️ Функции: {", ".join(feature_summary)}')
            
            if features['data_tables']:
                self.stdout.write(f'   📋 Таблиц данных: {len(features["data_tables"])}')
                for i, table in enumerate(features['data_tables'][:3]):  # показываем первые 3
                    self.stdout.write(f'      Таблица {i+1}: {table["rows_count"]} строк, {len(table["headers"])} колонок')
            
            # 5. Генерируем рекомендации
            self.stdout.write('\n5️⃣ Генерация рекомендаций...')
            recommendations = []
            
            # Производительность
            if analysis_results['accessibility']['response_time_ms'] > 2000:
                recommendations.append({
                    'type': 'performance',
                    'priority': 'high',
                    'issue': 'Медленная загрузка страницы',
                    'description': f'Время ответа {analysis_results["accessibility"]["response_time_ms"]:.0f}ms превышает рекомендуемые 2000ms',
                    'solution': 'Оптимизировать server response time, добавить кэширование'
                })
            
            # UI/UX
            if ui_elements['tables'] > 0 and not features['has_sorting']:
                recommendations.append({
                    'type': 'ux',
                    'priority': 'medium',
                    'issue': 'Отсутствует сортировка таблиц',
                    'description': 'Обнаружены таблицы без возможности сортировки',
                    'solution': 'Добавить интерактивную сортировку для улучшения пользовательского опыта'
                })
            
            # Функциональность
            if not features['has_export']:
                recommendations.append({
                    'type': 'functionality',
                    'priority': 'medium',
                    'issue': 'Отсутствует экспорт данных',
                    'description': 'Не найдены функции экспорта в научных форматах',
                    'solution': 'Добавить экспорт в CSV, FASTA, GenBank форматах'
                })
            
            # Технологии
            if not any([tech_stack['has_bootstrap'], tech_stack['has_react']]):
                recommendations.append({
                    'type': 'technology',
                    'priority': 'low',
                    'issue': 'Устаревший технологический стек',
                    'description': 'Не обнаружены современные UI фреймворки',
                    'solution': 'Рассмотреть использование Bootstrap 5+ или React.js для улучшения UI/UX'
                })
            
            analysis_results['recommendations'] = recommendations
            
            # Выводим рекомендации
            for i, rec in enumerate(recommendations[:5], 1):
                priority_color = {
                    'high': self.style.ERROR,
                    'medium': self.style.WARNING,
                    'low': self.style.NOTICE
                }[rec['priority']]
                
                self.stdout.write(f'   {i}. {priority_color(rec["issue"])} ({rec["priority"]})')
                self.stdout.write(f'      💡 {rec["solution"]}')
            
            # 6. Сохраняем результаты
            self.stdout.write('\n6️⃣ Сохранение результатов...')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2)
            
            self.stdout.write(f'   💾 Результаты сохранены в {output_file}')
            
        except requests.RequestException as e:
            analysis_results['error'] = str(e)
            self.stdout.write(self.style.ERROR(f'❌ Ошибка подключения: {e}'))
        
        except Exception as e:
            analysis_results['error'] = str(e)
            self.stdout.write(self.style.ERROR(f'❌ Ошибка анализа: {e}'))
        
        # Итоговая сводка
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📋 ИТОГОВАЯ СВОДКА'))
        self.stdout.write('='*60)
        
        if 'error' not in analysis_results:
            self.stdout.write(f'🌐 Сайт: {"✅ Доступен" if analysis_results["accessibility"]["accessible"] else "❌ Недоступен"}')
            self.stdout.write(f'⏱️ Производительность: {analysis_results["accessibility"]["response_time_ms"]:.0f}ms')
            self.stdout.write(f'📊 Таблиц: {analysis_results["ui_elements"]["tables"]}')
            self.stdout.write(f'⚙️ Функций: {len([f for f in analysis_results["features"].values() if f is True])}')
            self.stdout.write(f'⚠️ Рекомендаций: {len(analysis_results["recommendations"])}')
            
            # Приоритет следующих шагов
            self.stdout.write('\n🎯 СЛЕДУЮЩИЕ ШАГИ ДЛЯ СИФИБР:')
            next_steps = [
                '1. Анализировать найденные UI паттерны для адаптации',
                '2. Реализовать интерактивные таблицы с сортировкой',
                '3. Добавить экспорт в научных форматах (FASTA, GenBank)',
                '4. Оптимизировать производительность (<200ms target)',
                '5. Внедрить современный UI framework (Bootstrap 5/React)'
            ]
            
            for step in next_steps:
                self.stdout.write(f'   {step}')
        
        self.stdout.write('')
        self.stdout.write('✅ Анализ завершен!')
        
        return analysis_results 