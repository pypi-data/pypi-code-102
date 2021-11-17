import logging

from rest_framework import serializers

from ..models import Profile

logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    affiliation_home = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        read_only_fields = ("affiliation", "affiliation_id", "affiliation_home")
        fields = read_only_fields + (
            "display_name",
            "display_id",
        )

    def get_affiliation_home(self, obj: Profile):  # pylint: disable=no-self-use
        if obj.affiliation:
            return ",".join(
                sorted(
                    {aff.split("@")[1].strip() for aff in obj.affiliation.split(",")}
                )
            )
        return ""
