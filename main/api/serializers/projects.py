from main.api.serializers.common import StarredModelSerializer
from main.models import Project


class ProjectSerializer(StarredModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id", "title", "description", "tech_stack", "project_url", "project_image_url",
            "link", "created_at",
            "star_count", "is_starred", "starred_by_names",
        )
        read_only_fields = ("id",)

    def validate_title(self, value):
        return self.clean_text(value)

    def validate_description(self, value):
        return self.clean_text(value)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret.get("project_url") and instance.link:
            ret["project_url"] = instance.link
        if not ret.get("link") and instance.project_url:
            ret["link"] = instance.project_url
        return ret

    def create(self, validated_data):
        if "project_url" in validated_data and not validated_data.get("link"):
            validated_data["link"] = validated_data["project_url"]
        elif "link" in validated_data and not validated_data.get("project_url"):
            validated_data["project_url"] = validated_data["link"]
        return super().create(validated_data)
