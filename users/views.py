import json
import bcrypt
import jwt
from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.views           import View

from users.models           import User, Gender
from users.validations      import Validation
from my_settings            import SECRET_KEY

class SignupView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            name         = data['name']
            birth_date   = data['birth_date']
            phone_number = data['phone_number']
            points       = 0
            gender       = data['gender']
#            gender       = 

#            if not Validation.validate_email(self, email):
#                return JsonResponse({'message': 'Error email'}, status=400)

#            if not Validation.validate_password(self, password):
#                return JsonResponse({'message': 'Error password'}, status=400)

#            if not Validation.validate_duplication(self, email, phone, nickname):
#                return JsonResponse({'message': 'Already exist'}, status=400)


            password = bcrypt.hashpw(
                    password.encode('utf-8'),
                    bcrypt.gensalt()
            ).decode('utf-8')
            User.objects.create(email=email, password=password, phone=phone, nickname=nickname)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'MESSAGE': 'NO_BODY'}, status=400)


class LoginView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            users = User.objects.filter(email=email)
            if not users:
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=401)

            user = users[0]
            if password != user.password:
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=401)
            
            access_token = jwt.encode(
                    {'user_id': user.id},
                    SECRET_KEY,
                    algorithm = 'HS256'
            ).decode('UTF-8')

            return JsonResponse({'MESSAGE': 'SUCCESS', 'ACCESS_TOKEN': access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'NO_BODY'}, status=400)
