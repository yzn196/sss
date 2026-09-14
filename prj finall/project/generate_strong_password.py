import secrets
import string
from zxcvbn import zxcvbn

def generate_strong_password(length=16):
    # تجميع الأحرف والأرقام والرموز
    characters = string.ascii_letters.upper() + string.digits + string.punctuation + string.ascii_letters.lower()

    while True:
        # إنشاء كلمة سر قوية وتاخذ وقت طويل للكراكينق
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # اخلي المكتبه تتأكد من انه كلمة السر قويه
        if zxcvbn(password)['score'] == 4:
            return password





