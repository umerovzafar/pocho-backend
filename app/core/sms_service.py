import requests
from app.core.config import settings


class SMSService:
    """Сервис для отправки SMS через API (точно как в примере)"""
    
    base_url = settings.SMS_API_URL

    def __get_token(self):
        """Получение токена авторизации для SMS API (точно как в примере)"""
        data = requests.post(
            url=f"{self.base_url}/auth/login/",
            data={
                "email": settings.SMS_AUTH_EMAIL,
                "password": settings.SMS_AUTH_SECRET_KEY,
            },
        )
        res = data.json()
        return res["data"]["token"]

    def send_message(self, phone_number, message):
        """Отправка SMS сообщения (точно как в примере)"""
        # Если это тестовый номер, пропускаем отправку
        if phone_number == settings.SMS_MAIN_PHONE_NUMBER:
            print(f"Test phone number {phone_number}, skipping SMS send")
            return
            
        token = self.__get_token()
        payload = {"mobile_phone": phone_number, "message": message, "from": settings.SMS_FROM_NUMBER}
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.post(
            url=f"{self.base_url}/message/sms/send", headers=headers, data=payload
        )
        print(res.json())

    def get_templates(self):
        """Получение шаблонов SMS (как в примере)"""
        token = self.__get_token()
        res = requests.get(
            f"{self.base_url}/users/templates",
            headers={"Authorization": f"Bearer {token}"},
        )
        print(res.json())
