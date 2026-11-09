from main.api.serializers.common import StarredModelSerializer
from main.models import Education


class EducationSerializer(StarredModelSerializer):
    class Meta:
        model = Education
        fields = (
            "id",
            "institution",
            "program",
            "field",
            "started_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        )
        read_only_fields = ("id",)

    def validate_institution(self, value):
        return self.clean_text(value)

    def validate_program(self, value):
        return self.clean_text(value)

    def validate_field(self, value):
        return self.clean_text(value)
