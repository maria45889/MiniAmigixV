from django.core.cache import cache

# Ejemplo básico de uso de caché
cache.set('key', 'value', 60)
valor = cache.get('key')

print(f"Valor recuperado: {valor}")
