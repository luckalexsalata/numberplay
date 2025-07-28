from rest_framework import serializers
from .models import GameResult

class GamePlaySerializer(serializers.Serializer):
    number = serializers.IntegerField(
        min_value=1,
        max_value=9999,
        error_messages={
            'min_value': 'Number must be at least 1.',
            'max_value': 'Number cannot exceed 9999.',
            'invalid': 'Please enter a valid number.',
            'required': 'Number is required.'
        }
    )
    
    def validate_number(self, value):
        """Additional validation for number"""
        if value <= 0:
            raise serializers.ValidationError("Number must be positive.")
        return value

class GameResultSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    formatted_prize = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = GameResult
        fields = [
            'id', 'user_username', 'number', 'result', 
            'prize', 'formatted_prize', 'formatted_date', 'created_at'
        ]
        read_only_fields = ['id', 'user_username', 'result', 'prize', 'created_at']
    
    def get_formatted_prize(self, obj):
        """Format prize with currency symbol"""
        if obj.prize is not None:
            return f"${obj.prize:.2f}"
        return "No prize"
    
    def get_formatted_date(self, obj):
        """Format date in a readable format"""
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S") 