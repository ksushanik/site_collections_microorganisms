# 📋 TODO: Обновления для Docker

## 1. Обновить settings.py для PostgreSQL
Добавить в settings.py:
```python
import dj_database_url
DATABASES = {'default': dj_database_url.config()}
```
