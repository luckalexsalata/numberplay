from django.contrib import admin
from django.db.models import Count, Avg, Sum
from django.utils.html import format_html
from .models import GameResult

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'result', 'prize', 'created_at', 'get_result_color')
    list_filter = ('result', 'created_at', 'user')
    search_fields = ('user__username', 'user__email', 'number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Game Info', {'fields': ('user', 'number', 'result', 'prize')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def get_result_color(self, obj):
        if obj.result == 'win':
            return format_html('<span style="color: green; font-weight: bold;">WIN</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">LOSE</span>')
    get_result_color.short_description = 'Result'
    
    def changelist_view(self, request, extra_context=None):
        # Add statistics to the changelist view
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Calculate statistics
        total_games = qs.count()
        wins = qs.filter(result='win').count()
        losses = qs.filter(result='lose').count()
        total_prize = qs.filter(result='win').aggregate(total=Sum('prize'))['total'] or 0
        avg_prize = qs.filter(result='win').aggregate(avg=Avg('prize'))['avg'] or 0
        
        # Add to context
        response.context_data['stats'] = {
            'total_games': total_games,
            'wins': wins,
            'losses': losses,
            'win_rate': round((wins / total_games * 100) if total_games > 0 else 0, 1),
            'total_prize': round(total_prize, 2),
            'avg_prize': round(avg_prize, 2),
        }
        
        return response
