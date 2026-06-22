from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from apps.mongodb.models import MetricasSistemaMongo, ChatMessageMongo, AnaliticaMongo
from collections import Counter

class Command(BaseCommand):
    help = 'Analiza tendencias de los datos en MongoDB'

    def handle(self, *args, **options):
        self.stdout.write('=== Análisis de Tendencias ===')
        
        # Análisis 1: Tendencia de actividad de usuarios
        self.stdout.write('\n1. Tendencia de actividad de usuarios (últimos 7 días)')
        self.analizar_tendencia_actividad()
        
        # Análisis 2: Tendencia de uso del chat
        self.stdout.write('\n2. Tendencia de uso del chat (últimos 7 días)')
        self.analizar_tendencia_chat()
        
        # Análisis 3: Tendencia de páginas más visitadas
        self.stdout.write('\n3. Tendencia de páginas más visitadas (últimos 7 días)')
        self.analizar_tendencia_paginas()
        
        # Análisis 4: Predicción simple de crecimiento
        self.stdout.write('\n4. Predicción simple de crecimiento')
        self.predecir_crecimiento()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Análisis de tendencias completado'))
    
    def analizar_tendencia_actividad(self):
        """Analiza la tendencia de actividad de usuarios"""
        hoy = datetime.now().date()
        datos_por_dia = []
        
        for i in range(7):
            fecha = hoy - timedelta(days=i)
            fecha_inicio = datetime.combine(fecha, datetime.min.time())
            fecha_fin = datetime.combine(fecha, datetime.max.time())
            
            # Contar usuarios activos ese día
            metricas = MetricasSistemaMongo.objects(fecha=fecha_inicio).first()
            if metricas:
                datos_por_dia.append({
                    'fecha': fecha.strftime('%d/%m'),
                    'usuarios': metricas.usuarios_activos
                })
        
        if datos_por_dia:
            datos_por_dia.reverse()
            promedio = sum(d['usuarios'] for d in datos_por_dia) / len(datos_por_dia)
            
            # Determinar tendencia
            if len(datos_por_dia) >= 2:
                primeros = datos_por_dia[:3]
                ultimos = datos_por_dia[-3:]
                promedio_primeros = sum(d['usuarios'] for d in primeros) / len(primeros)
                promedio_ultimos = sum(d['usuarios'] for d in ultimos) / len(ultimos)
                
                if promedio_ultimos > promedio_primeros * 1.2:
                    tendencia = "📈 Creciendo (+{:.1f}%)".format((promedio_ultimos - promedio_primeros) / promedio_primeros * 100)
                elif promedio_ultimos < promedio_primeros * 0.8:
                    tendencia = "📉 Decreciendo ({:.1f}%)".format((promedio_primeros - promedio_ultimos) / promedio_primeros * 100)
                else:
                    tendencia = "➡️ Estable"
            else:
                tendencia = "➡️ Estable"
            
            self.stdout.write(f'   Promedio diario: {promedio:.1f} usuarios')
            self.stdout.write(f'   Tendencia: {tendencia}')
            for dato in datos_por_dia:
                self.stdout.write(f'   {dato["fecha"]}: {dato["usuarios"]} usuarios')
    
    def analizar_tendencia_chat(self):
        """Analiza la tendencia de uso del chat"""
        hoy = datetime.now()
        fecha_limite = hoy - timedelta(days=7)
        
        chats_por_dia = {}
        chats = ChatMessageMongo.objects(fecha_creacion__gte=fecha_limite)
        
        for chat in chats:
            fecha = chat.fecha_creacion.date().strftime('%d/%m')
            chats_por_dia[fecha] = chats_por_dia.get(fecha, 0) + 1
        
        if chats_por_dia:
            total_chats = sum(chats_por_dia.values())
            promedio = total_chats / len(chats_por_dia)
            
            self.stdout.write(f'   Total chats (7 días): {total_chats}')
            self.stdout.write(f'   Promedio diario: {promedio:.1f} chats')
            self.stdout.write(f'   Día más activo: {max(chats_por_dia, key=chats_por_dia.get)} ({max(chats_por_dia.values())} chats)')
    
    def analizar_tendencia_paginas(self):
        """Analiza la tendencia de páginas más visitadas"""
        hoy = datetime.now()
        fecha_limite = hoy - timedelta(days=7)
        
        paginas = [a.pagina for a in AnaliticaMongo.objects(fecha_creacion__gte=fecha_limite)]
        paginas_contador = Counter(paginas)
        
        if paginas_contador:
            top_paginas = paginas_contador.most_common(5)
            self.stdout.write(f'   Top 5 páginas (últimos 7 días):')
            for i, (pagina, count) in enumerate(top_paginas, 1):
                self.stdout.write(f'   {i}. {pagina}: {count} visitas')
    
    def predecir_crecimiento(self):
        """Predicción simple de crecimiento basada en datos históricos"""
        hoy = datetime.now().date()
        metricas_recientes = []
        
        for i in range(7):
            fecha = hoy - timedelta(days=i)
            fecha_inicio = datetime.combine(fecha, datetime.min.time())
            metricas = MetricasSistemaMongo.objects(fecha=fecha_inicio).first()
            if metricas:
                metricas_recientes.append(metricas.usuarios_activos)
        
        if len(metricas_recientes) >= 3:
            # Cálculo simple de tendencia lineal
            crecimiento = metricas_recientes[-1] - metricas_recientes[0]
            tasa_crecimiento = crecimiento / metricas_recientes[0] * 100 if metricas_recientes[0] > 0 else 0
            
            prediccion_manana = metricas_recientes[-1] + (crecimiento / len(metricas_recientes))
            
            self.stdout.write(f'   Crecimiento últimos 7 días: {crecimiento:+d} usuarios ({tasa_crecimiento:+.1f}%)')
            self.stdout.write(f'   Predicción para mañana: {prediccion_manana:.0f} usuarios activos')
            
            if tasa_crecimiento > 10:
                self.stdout.write(f'   🚀 Tendencia positiva fuerte')
            elif tasa_crecimiento > 0:
                self.stdout.write(f'   📈 Tendencia positiva leve')
            elif tasa_crecimiento > -10:
                self.stdout.write(f'   📉 Tendencia negativa leve')
            else:
                self.stdout.write(f'   ⚠️ Tendencia negativa fuerte')
        else:
            self.stdout.write('   No hay suficientes datos para predicción')
