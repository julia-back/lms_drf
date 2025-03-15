from rest_framework.serializers import ValidationError


class YoutubeLinkValidator:
    """Валидатор для проверки источника ссылки. Допустимый источник - youtube.com"""
    def __init__(self, field=None):
        self.field = field

    def __call__(self, value):
        if self.field is None:
            if value is not None:
                if "youtube.com" not in value:
                    raise ValidationError("Поле должно содержать ссылку на youtube.com")
        else:
            value = value.get(self.field)
            if value is not None:
                if "youtube.com" not in value:
                    raise ValidationError("Поле должно содержать ссылку на youtube.com")
