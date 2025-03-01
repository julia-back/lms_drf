from rest_framework.serializers import ValidationError


class YoutubeLinkValidator:

    def __init__(self, field=None):
        self.field = field

    def __call__(self, value):
        if self.field is None:
            if "youtube.com" not in value:
                raise ValidationError("Поле должно содержать ссылку на youtube.com")
            print(self.field)
        else:
            if "youtube.com" not in value.get(self.field):
                raise ValidationError("Поле должно содержать ссылку на youtube.com")
