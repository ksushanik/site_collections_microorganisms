# 🚀 Production Развертывание СИФИБР

## 📋 Требования к серверу

### Минимальные требования
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **CPU**: 4 vCPU (2 vCPU минимум)
- **RAM**: 8GB (4GB минимум)
- **Storage**: 50GB SSD (20GB минимум)
- **Network**: 100 Mbps (стабильное соединение)

### Рекомендуемые требования
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 8 vCPU
- **RAM**: 16GB
- **Storage**: 100GB SSD + backup storage
- **Network**: 1 Gbps
- **Monitoring**: Prometheus + Grafana

## 🔧 Подготовка сервера

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### 2. Установка Docker
```bash
# Удаление старых версий
sudo apt-get remove docker docker-engine docker.io containerd runc

# Установка зависимостей
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# Добавление официального GPG ключа Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавление репозитория
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установка Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Установка Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker --version
docker-compose --version
```

## 📁 Развертывание приложения

### 1. Клонирование репозитория
```bash
cd /opt
sudo git clone <repository-url> sifibr-collections
sudo chown -R $USER:$USER sifibr-collections
cd sifibr-collections
```

### 2. Настройка production окружения
```bash
# Создание production .env файла
cp docker/.env.example docker/.env.production

# Редактирование настроек
nano docker/.env.production
```

### 3. Production .env конфигурация
```bash
# Django настройки
DEBUG=False
SECRET_KEY=your-super-secret-production-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# База данных
DB_PASSWORD=super-secure-db-password-2025
DATABASE_URL=postgresql://sifibr:super-secure-db-password-2025@db:5432/sifibr_collections

# Redis
REDIS_PASSWORD=super-secure-redis-password-2025

# Email (для уведомлений)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Backup настройки
BACKUP_ENABLED=True
BACKUP_SCHEDULE=0 2 * * *  # Ежедневно в 2:00
```

### 4. SSL сертификаты (Let's Encrypt)
```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавить: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 5. Запуск production сервисов
```bash
# Запуск в production режиме
cd docker
docker-compose --env-file .env.production --profile prod up -d

# Проверка статуса
docker-compose ps
docker-compose logs -f
```

## 🔒 Безопасность

### 1. Firewall настройка (UFW)
```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Разрешенные порты
sudo ufw allow ssh
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS

# Опционально для мониторинга
sudo ufw allow 9090/tcp  # Prometheus
sudo ufw allow 3000/tcp  # Grafana

sudo ufw reload
```

### 2. Fail2Ban защита
```bash
sudo apt install fail2ban

# Создание конфигурации
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
```

### 3. Регулярные обновления безопасности
```bash
# Автоматические обновления
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# Еженедельная проверка
sudo nano /etc/cron.weekly/security-updates
```

## 📊 Мониторинг и логирование

### 1. Настройка логирования
```bash
# Создание директории для логов
sudo mkdir -p /var/log/sifibr
sudo chown $USER:$USER /var/log/sifibr

# Настройка ротации логов
sudo nano /etc/logrotate.d/sifibr
```

```
/var/log/sifibr/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 root root
}
```

### 2. Health check мониторинг
```bash
# Создание health check скрипта
nano /opt/sifibr-collections/scripts/health_check.sh
```

```bash
#!/bin/bash
HEALTH_URL="http://localhost:8001/api/health/"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $STATUS -eq 200 ]; then
    echo "✅ SIFIBR API: Healthy"
    exit 0
else
    echo "❌ SIFIBR API: Unhealthy (Status: $STATUS)"
    # Уведомление администратора
    echo "SIFIBR API down at $(date)" | mail -s "SIFIBR Alert" admin@your-domain.com
    exit 1
fi
```

```bash
chmod +x /opt/sifibr-collections/scripts/health_check.sh

# Добавление в cron для проверки каждые 5 минут
crontab -e
# */5 * * * * /opt/sifibr-collections/scripts/health_check.sh
```

## 💾 Резервное копирование

### 1. Автоматический backup БД
```bash
# Создание backup скрипта
nano /opt/sifibr-collections/scripts/backup_db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/sifibr"
DATE=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="sifibr_db"

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec $DB_CONTAINER pg_dump -U sifibr sifibr_collections | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup медиафайлов
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C /opt/sifibr-collections media/

# Удаление старых backup (старше 30 дней)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "✅ Backup completed: $DATE"
```

```bash
chmod +x /opt/sifibr-collections/scripts/backup_db.sh

# Ежедневный backup в 2:00
crontab -e
# 0 2 * * * /opt/sifibr-collections/scripts/backup_db.sh
```

### 2. Восстановление из backup
```bash
# Список доступных backup
ls -la /opt/backups/sifibr/

# Восстановление БД
zcat /opt/backups/sifibr/db_20241215_020000.sql.gz | docker exec -i sifibr_db psql -U sifibr -d sifibr_collections

# Восстановление медиафайлов
tar -xzf /opt/backups/sifibr/media_20241215_020000.tar.gz -C /opt/sifibr-collections/
```

## 🔄 Обновление приложения

### 1. Обновление кода
```bash
cd /opt/sifibr-collections

# Создание backup текущей версии
cp -r . ../sifibr-collections-backup-$(date +%Y%m%d)

# Получение обновлений
git fetch origin
git checkout main
git pull origin main
```

### 2. Применение обновлений
```bash
cd docker

# Остановка сервисов
docker-compose --env-file .env.production down

# Пересборка образов
docker-compose --env-file .env.production --profile prod build --no-cache

# Применение миграций БД
docker-compose --env-file .env.production run --rm backend python manage.py migrate

# Сбор статических файлов
docker-compose --env-file .env.production run --rm backend python manage.py collectstatic --noinput

# Запуск обновленных сервисов
docker-compose --env-file .env.production --profile prod up -d

# Проверка статуса
docker-compose ps
docker-compose logs -f --tail=50
```

## 🌐 Nginx reverse proxy (опционально)

### 1. Установка Nginx
```bash
sudo apt install nginx

# Создание конфигурации
sudo nano /etc/nginx/sites-available/sifibr
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/sifibr /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 📈 Производительность и оптимизация

### 1. Docker оптимизации
```bash
# Ограничение ресурсов в docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### 2. PostgreSQL оптимизации
```bash
# В docker/postgres/postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

## 🚨 Troubleshooting

### Общие проблемы и решения

1. **Контейнеры не запускаются**
```bash
docker-compose logs
docker system prune -a
```

2. **Ошибки подключения к БД**
```bash
docker exec -it sifibr_db psql -U sifibr -d sifibr_collections
# Проверка подключения
```

3. **Проблемы с SSL**
```bash
sudo certbot renew --dry-run
sudo nginx -t
```

4. **Высокое использование ресурсов**
```bash
docker stats
top
htop
```

## 📞 Поддержка

### Контакты технической поддержки
- **Email**: support@sifibr.irk.ru
- **Телефон**: +7 (3952) XX-XX-XX
- **Telegram**: @sifibr_support

### Логи для диагностики
```bash
# Логи приложения
docker-compose logs backend frontend

# Системные логи
journalctl -u docker
tail -f /var/log/nginx/error.log

# Health check
curl -v http://localhost:8001/api/health/
```

---

*Документ обновлен: Декабрь 2024* 