import re

from users.models import User

class Validation:
    def validate_email(self, mail):
        regex = re.compile('[a-zA-Z0-9\.\_\+\-]+\@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\.]+')
        if not regex.match(mail):
            return False
        return True

    def validate_password(self, password):
        regex = re.compile('[A-Za-z0-9]{8,}')
        if not regex.match(password):
            return False
        return True

    def validate_duplication(self, email, phone, nickname):
        if User.objects.filter(email=email):
            return False
        elif phone and User.objects.filter(phone=phone):
            return False
        elif nickname and User.objects.filter(nickname=nickname):
            return False
        return True

