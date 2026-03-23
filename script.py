import requests
import smtplib
from email.mime.text import MIMEText
import os

THRESHOLD = 0.5

def get_price():
    url = "https://api.exchangerate.host/latest?base=EUR&symbols=CNH"
    r = requests.get(url)
    data = r.json()
    if "rates" not in data or "CNH" not in data["rates"]:
        raise Exception(f"API Fehler: {data}")
    return data["rates"]["CNH"]

def send_email(change, price):
    try:
        msg = MIMEText(f"Kursänderung: {change:.2f}%\nNeuer Kurs: {price}")
        msg["Subject"] = "EUR/CNH ALERT"
        msg["From"] = os.environ["EMAIL_SENDER"]
        msg["To"] = os.environ["EMAIL_RECEIVER"]

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.environ["EMAIL_SENDER"], os.environ["EMAIL_PASSWORD"])
            server.send_message(msg)
        print("Email gesendet")
    except Exception as e:
        print("Email Fehler:", e)

def main():
    try:
        price = get_price()
        print("Preis:", price)
        try:
            with open("last_price.txt", "r") as f:
                last_price = float(f.read())
        except:
            last_price = price
        change = (price - last_price) / last_price * 100
        print("Änderung:", change)
        if abs(change) >= THRESHOLD:
            send_email(change, price)
        with open("last_price.txt", "w") as f:
            f.write(str(price))
    except Exception as e:
        print("FEHLER:", e)
        raise

if __name__ == "__main__":
    main()
