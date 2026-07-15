# Script para configurar tareas programadas de MongoDB en Windows (Task Scheduler)
# Ejecutar como administrador

$projectPath = "c:\Users\majo1\Desktop\MiniAmigixV"
$pythonPath = "python"
$managePy = "$projectPath\manage.py"

Write-Host "=== Configurando tareas programadas de MongoDB ===" -ForegroundColor Green

# 1. Calcular estadísticas (diario a las 2:00 AM)
Write-Host "`n1. Configurando tarea: Calcular estadísticas (diario 2:00 AM)..." -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "$managePy calcular_estadisticas" -WorkingDirectory $projectPath
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "MiniAmigix MongoDB - Calcular Estadisticas" -Action $action -Trigger $trigger -Description "Calcula estadísticas agregadas de MongoDB diariamente" -Force
Write-Host "✓ Tarea configurada: Calcular estadísticas" -ForegroundColor Green

# 2. Verificar alertas (cada hora)
Write-Host "`n2. Configurando tarea: Verificar alertas (cada hora)..." -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "$managePy verificar_alertas" -WorkingDirectory $projectPath
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "MiniAmigix MongoDB - Verificar Alertas" -Action $action -Trigger $trigger -Description "Verifica métricas y envía alertas cada hora" -Force
Write-Host "✓ Tarea configurada: Verificar alertas" -ForegroundColor Green

# 3. Análisis de tendencias (semanal los domingos a las 3:00 AM)
Write-Host "`n3. Configurando tarea: Análisis de tendencias (semanal domingo 3:00 AM)..." -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "$managePy analisis_tendencias" -WorkingDirectory $projectPath
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3am
Register-ScheduledTask -TaskName "MiniAmigix MongoDB - Analisis Tendencias" -Action $action -Trigger $trigger -Description "Analiza tendencias de datos semanalmente" -Force
Write-Host "✓ Tarea configurada: Análisis de tendencias" -ForegroundColor Green

# 4. Retención de datos (mensual el día 1 a las 4:00 AM)
Write-Host "`n4. Configurando tarea: Retención de datos (mensual día 1 4:00 AM)..." -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "$managePy retencion_datos" -WorkingDirectory $projectPath
$trigger = New-ScheduledTaskTrigger -Monthly -Days 1 -At 4am
Register-ScheduledTask -TaskName "MiniAmigix MongoDB - Retencion Datos" -Action $action -Trigger $trigger -Description "Elimina datos antiguos mensualmente" -Force
Write-Host "✓ Tarea configurada: Retención de datos" -ForegroundColor Green

Write-Host "`n=== Configuración completada ===" -ForegroundColor Green
Write-Host "Las siguientes tareas han sido configuradas:" -ForegroundColor Cyan
Write-Host "1. MiniAmigix MongoDB - Calcular Estadisticas (diario 2:00 AM)" -ForegroundColor White
Write-Host "2. MiniAmigix MongoDB - Verificar Alertas (cada hora)" -ForegroundColor White
Write-Host "3. MiniAmigix MongoDB - Analisis Tendencias (semanal domingo 3:00 AM)" -ForegroundColor White
Write-Host "4. MiniAmigix MongoDB - Retencion Datos (mensual día 1 4:00 AM)" -ForegroundColor White
Write-Host "`nPara ver las tareas configuradas, ejecuta: Get-ScheduledTask | Where-Object {$_.TaskName -like '*MiniAmigix MongoDB*'}" -ForegroundColor Yellow
