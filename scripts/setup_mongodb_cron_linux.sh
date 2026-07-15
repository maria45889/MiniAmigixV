#!/bin/bash
# Script para configurar cron jobs de MongoDB en Linux
# Ejecutar: chmod +x setup_mongodb_cron_linux.sh && ./setup_mongodb_cron_linux.sh

PROJECT_PATH="/path/to/MiniAmigixV"
PYTHON_CMD="python"
MANAGE_PY="$PROJECT_PATH/manage.py"

echo "=== Configurando cron jobs de MongoDB ==="

# Crear archivo temporal de cron
TEMP_CRON=$(mktemp)

# Exportar crontab actual
crontab -l > $TEMP_CRON 2>/dev/null || true

# 1. Calcular estadísticas (diario a las 2:00 AM)
echo "1. Configurando cron: Calcular estadísticas (diario 2:00 AM)..."
echo "0 2 * * * cd $PROJECT_PATH && $PYTHON_CMD $MANAGE_PY calcular_estadisticas >> /var/log/miniamigix_mongodb.log 2>&1" >> $TEMP_CRON

# 2. Verificar alertas (cada hora)
echo "2. Configurando cron: Verificar alertas (cada hora)..."
echo "0 * * * * cd $PROJECT_PATH && $PYTHON_CMD $MANAGE_PY verificar_alertas >> /var/log/miniamigix_mongodb.log 2>&1" >> $TEMP_CRON

# 3. Análisis de tendencias (semanal los domingos a las 3:00 AM)
echo "3. Configurando cron: Análisis de tendencias (semanal domingo 3:00 AM)..."
echo "0 3 * * 0 cd $PROJECT_PATH && $PYTHON_CMD $MANAGE_PY analisis_tendencias >> /var/log/miniamigix_mongodb.log 2>&1" >> $TEMP_CRON

# 4. Retención de datos (mensual el día 1 a las 4:00 AM)
echo "4. Configurando cron: Retención de datos (mensual día 1 4:00 AM)..."
echo "0 4 1 * * cd $PROJECT_PATH && $PYTHON_CMD $MANAGE_PY retencion_datos >> /var/log/miniamigix_mongodb.log 2>&1" >> $TEMP_CRON

# Instalar nuevo crontab
crontab $TEMP_CRON

# Limpiar archivo temporal
rm $TEMP_CRON

echo "=== Configuración completada ==="
echo "Los siguientes cron jobs han sido configurados:"
echo "1. Calcular estadísticas (diario 2:00 AM)"
echo "2. Verificar alertas (cada hora)"
echo "3. Análisis de tendencias (semanal domingo 3:00 AM)"
echo "4. Retención de datos (mensual día 1 4:00 AM)"
echo ""
echo "Para ver los cron jobs configurados, ejecuta: crontab -l"
