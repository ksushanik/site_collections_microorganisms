# 🚀 Быстрый деплой СИФИБР на Render.com

## За 5 минут до живого сайта!

### Шаг 1: GitHub
```bash
# Убедитесь, что все файлы добавлены
git add .
git commit -m "feat: подготовка к деплою на Render"
git push origin main
```

**📁 Важные файлы для Render:**
- `render.yaml` - автоматическая конфигурация
- `Procfile` - команды запуска
- `runtime.txt` - версия Python
- `build.sh` - скрипт сборки
- `requirements.txt` - зависимости

### Шаг 2: Render.com
1. Откройте https://dashboard.render.com/
2. **New** → **Blueprint**
3. Подключите GitHub репозиторий
4. Render найдет `render.yaml` и создаст все сервисы автоматически

### Шаг 3: Ждите (~5-10 минут)
Render автоматически:
- Создаст PostgreSQL базу данных
- Развернет Django backend
- Соберет и развернет React frontend
- Выполнит миграции и создаст тестовые данные

### Шаг 4: Готово! 🎉

**Ваши URL адреса:**
- 🌐 **Сайт**: https://sifibr-frontend.onrender.com
- 🔧 **API**: https://sifibr-backend.onrender.com/api/
- ⚙️ **Админка**: https://sifibr-backend.onrender.com/admin/

**Админ доступ:**
- Логин: `admin`
- Пароль: `sifibr_admin_2025`

---

## Что получится:

✅ **Полнофункциональный сайт** коллекций микроорганизмов
✅ **5 научных коллекций** с тестовыми данными
✅ **7 штаммов байкальских микроорганизмов**
✅ **REST API** для разработчиков
✅ **Административная панель** для управления
✅ **PostgreSQL база данных** в облаке
✅ **Автоматические SSL сертификаты**
✅ **CDN для быстрой загрузки**

## Первое использование:

1. **Откройте сайт**: https://sifibr-frontend.onrender.com
2. **Просмотрите каталог** штаммов и коллекций
3. **Попробуйте поиск** и фильтрацию
4. **Зайдите в админку** для управления данными
5. **Проверьте API**: https://sifibr-backend.onrender.com/api/strains/

---

**Полная документация**: [docs/deployment/RENDER_DEPLOYMENT.md](docs/deployment/RENDER_DEPLOYMENT.md)

**Разработано для СИФИБР СО РАН** 🧬🦠🌊 