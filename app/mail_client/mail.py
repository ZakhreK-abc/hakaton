import smtplib
from email.message import EmailMessage
from email.utils import formataddr

def send_email_mailru(
    sender_email: str,
    sender_password: str,      # ← Это будет "Пароль для внешних приложений"
    recipient_email: str,
    subject: str,
    body: str,
    sender_name: str = None
):
    msg = EmailMessage()
    
    if sender_name:
        msg['From'] = formataddr((sender_name, sender_email))
    else:
        msg['From'] = sender_email
        
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            
        print("✅ Письмо успешно отправлено через Mail.ru!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
if __name__ == "__main__":
    send_email_mailru(
        sender_email="sub.spase@mail.ru",
        sender_password="F8raHdnk0Y4VwaM2fRQG",
        recipient_email="nik_kent11@mail.ru",
        subject="Тест из Python",
        body="Привет! Это письмо отправлено через Mail.ru с помощью Python.",
        sender_name="Ваше Имя"
    )