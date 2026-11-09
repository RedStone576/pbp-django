from main.api.serializers.common import StarredModelSerializer
from main.models import Project


class ProjectSerializer(StarredModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id", "title", "description", "link", "created_at",
            "star_count", "is_starred", "starred_by_names",
        )
        read_only_fields = ("id",)

    def validate_title(self, value):
        return self.clean_text(value)

    def validate_description(self, value):
        return self.clean_text(value)
