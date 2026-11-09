from rest_framework import serializers

from main.api.serializers.common import StarredModelSerializer
from main.models import Experience


class ExperienceSerializer(StarredModelSerializer):
    category_display = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "id",
            "title",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "started_at",
            "ended_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        )
        read_only_fields = ("id", "category_display")

    def validate_title(self, value):
        return self.clean_text(value)

    def validate_description(self, value):
        return self.clean_text(value)

    def get_category_display(self, obj):
        return obj.get_category_display()
