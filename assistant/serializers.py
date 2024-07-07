from rest_framework import serializers


class VideoDataSerializer(serializers.Serializer):
    keywords = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=True
    )
    video_duration = serializers.CharField(max_length=50, required=True)
    video_scenes = serializers.CharField(max_length=500, required=False)
    video_type = serializers.CharField(max_length=100, required=True)
    video_genre = serializers.CharField(max_length=100, required=False)
    target_audience = serializers.CharField(max_length=255, required=False)
    purpose = serializers.CharField(max_length=255, required=True)
    cta = serializers.CharField(max_length=255, required=False)
    tone_and_style = serializers.CharField(max_length=255, required=False)
    setting_and_location = serializers.CharField(
        max_length=255, required=False)
    characters_and_roles = serializers.CharField(
        max_length=255, required=False)
    script_format = serializers.CharField(max_length=255, required=False)
    visual_elements = serializers.CharField(max_length=255, required=False)
    audio_elements = serializers.CharField(max_length=255, required=False)
    branding = serializers.CharField(max_length=255, required=False)
    additional_resources = serializers.CharField(
        max_length=500, required=False)

    def generate_content(self):
        """
        Generates content in the specified format using serializer fields.
        """
        content_format = "Now, I will share my keywords: {keywords}, video length: {video_duration}, video type: {video_type}, video purpose: {purpose}, with the goal of making a comprehensive and engaging video script for TikTok. The script should not include emojis."
        return content_format.format(
            keywords=self.validated_data.get('keywords', 'N/A'),
            video_duration=self.validated_data.get('video_duration', 'N/A'),
            video_type=self.validated_data.get('video_type', 'N/A'),
            purpose=self.validated_data.get('purpose', 'N/A')
        )
