from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Game, Score, Achievement, UserAchievement, GameSession, UserStats
from .serializers import (
    GameSerializer, ScoreSerializer, ScoreCreateSerializer,
    AchievementSerializer, UserAchievementSerializer,
    GameSessionSerializer, GameSessionCreateSerializer,
    UserStatsSerializer
)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para ver juegos disponibles"""
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    
    def get_queryset(self):
        queryset = Game.objects.filter(activo=True)
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        return queryset


class ScoreViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar puntuaciones"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ScoreCreateSerializer
        return ScoreSerializer
    
    def get_queryset(self):
        return Score.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Obtener tabla de líderes para un juego específico"""
        juego_id = request.query_params.get('juego_id')
        if not juego_id:
            return Response(
                {'error': 'Se requiere juego_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scores = Score.objects.filter(
            juego_id=juego_id
        ).order_by('-puntuacion')[:10]
        
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_best(self, request):
        """Obtener mejores puntuaciones del usuario"""
        scores = self.get_queryset().order_by('-puntuacion')[:5]
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para ver logros disponibles"""
    permission_classes = [IsAuthenticated]
    serializer_class = AchievementSerializer
    
    def get_queryset(self):
        queryset = Achievement.objects.filter(activo=True)
        juego_id = self.request.query_params.get('juego_id', None)
        if juego_id:
            queryset = queryset.filter(juego_id=juego_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Obtener logros desbloqueados por el usuario"""
        user_achievements = UserAchievement.objects.filter(
            usuario=request.user
        ).select_related('logro')
        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """Desbloquear un logro"""
        logro = self.get_object()
        
        # Verificar si ya está desbloqueado
        if UserAchievement.objects.filter(
            usuario=request.user,
            logro=logro
        ).exists():
            return Response(
                {'error': 'Logro ya desbloqueado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear logro desbloqueado
        UserAchievement.objects.create(
            usuario=request.user,
            logro=logro
        )
        
        # Agregar XP al usuario
        stats, created = UserStats.objects.get_or_create(
            usuario=request.user
        )
        stats.agregar_xp(logro.puntos_xp)
        
        return Response({
            'success': True,
            'message': f'Logro "{logro.nombre}" desbloqueado',
            'xp_ganado': logro.puntos_xp
        })


class GameSessionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar sesiones de juego"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GameSessionCreateSerializer
        return GameSessionSerializer
    
    def get_queryset(self):
        return GameSession.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        session = serializer.save(usuario=self.request.user)
        
        # Actualizar estadísticas del usuario
        stats, created = UserStats.objects.get_or_create(
            usuario=self.request.user
        )
        stats.actualizar_racha()
        
        if session.gano:
            stats.juegos_completados += 1
            stats.total_monedas += 10  # 10 monedas por ganar
            stats.save()
        
        return session
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """Finalizar una sesión de juego"""
        session = self.get_object()
        session.fin = timezone.now()
        puntuacion_final = request.data.get('puntuacion_final')
        gano = request.data.get('gano')
        
        if puntuacion_final is not None:
            session.puntuacion_final = puntuacion_final
        if gano is not None:
            session.gano = gano
        
        session.save()
        
        # Crear registro de puntuación si existe puntuación final
        if session.puntuacion_final:
            Score.objects.create(
                usuario=request.user,
                juego=session.juego,
                puntuacion=session.puntuacion_final,
                nivel=session.nivel_alcanzado,
                tiempo_jugado=int(session.duracion()) if session.duracion() else 0
            )
        
        return Response({'success': True})


class UserStatsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar estadísticas del usuario"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserStatsSerializer
    
    def get_queryset(self):
        return UserStats.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_stats(self, request):
        """Obtener estadísticas del usuario actual"""
        stats, created = UserStats.objects.get_or_create(
            usuario=request.user
        )
        serializer = self.get_serializer(stats)
        return Response(serializer.data)


class TicTacToeViewSet(viewsets.ViewSet):
    """ViewSet específico para el juego Tres en Raya"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def make_move(self, request):
        """Procesar un movimiento del jugador y devolver respuesta de la IA"""
        board = request.data.get('board', [])
        player_move = request.data.get('player_move')
        
        if not board or len(board) != 9:
            return Response(
                {'error': 'Tablero inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar movimiento del jugador
        if player_move < 0 or player_move > 8 or board[player_move] != '':
            return Response(
                {'error': 'Movimiento inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Aplicar movimiento del jugador (X)
        board[player_move] = 'X'
        
        # Verificar si el jugador ganó
        winner = self._check_winner(board)
        if winner == 'X':
            return Response({
                'board': board,
                'winner': 'X',
                'game_over': True,
                'ai_move': None
            })
        
        # Verificar empate
        if '' not in board:
            return Response({
                'board': board,
                'winner': 'draw',
                'game_over': True,
                'ai_move': None
            })
        
        # Movimiento de la IA (O) usando minimax
        ai_move = self._get_best_move(board)
        if ai_move is not None:
            board[ai_move] = 'O'
        
        # Verificar si la IA ganó
        winner = self._check_winner(board)
        if winner == 'O':
            return Response({
                'board': board,
                'winner': 'O',
                'game_over': True,
                'ai_move': ai_move
            })
        
        # Verificar empate después del movimiento de la IA
        if '' not in board:
            return Response({
                'board': board,
                'winner': 'draw',
                'game_over': True,
                'ai_move': ai_move
            })
        
        return Response({
            'board': board,
            'winner': None,
            'game_over': False,
            'ai_move': ai_move
        })
    
    def _check_winner(self, board):
        """Verificar si hay un ganador"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return board[combo[0]]
        
        return None
    
    def _get_best_move(self, board):
        """Obtener el mejor movimiento para la IA usando minimax"""
        best_score = float('-inf')
        best_move = None
        
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = self._minimax(board, 0, False)
                board[i] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing):
        """Algoritmo minimax para la IA"""
        winner = self._check_winner(board)
        
        if winner == 'O':
            return 10 - depth
        if winner == 'X':
            return depth - 10
        if '' not in board:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self._minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self._minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score
