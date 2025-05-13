from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import schedule
import time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def homeView():
    return render_template('home.html')

@app.route('/team')
def teamView():
    return render_template('team.html')

@app.route('/task')
def taskView():
    return render_template('task.html')


@app.route('/scrape', methods=['POST'])
def scrapeView():
    def job():
        url = request.form['url']
        app_password = "zndufskmcaokexqt"

        if not url.startswith('https://'):
            url = 'https://' + url

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        with open("information.txt", "w", encoding='utf-8') as info_file:
            for headline in soup.find_all('h2'):
                info_file.write(headline.get_text(strip=True) + "\n")

            for paragraph in soup.find_all('p'):
                info_file.write("Paragraph: " + paragraph.get_text(strip=True) + "\n")

        with open('information.txt', 'rb') as f:
            file_data = f.read()
            with open('emails.txt', 'r', encoding='utf-8') as email_file:
                for line in email_file:
                    user_email = line.strip()
                    if not user_email:
                        continue

                    msg = EmailMessage()
                    msg['Subject'] = 'Test Email from Flask app'
                    msg['From'] = 'ksourmi@gmail.com'
                    msg['To'] = user_email
                    msg.set_content('Hello! This is a test email sent from Flask app using Gmail.')
                    msg.add_attachment(file_data, maintype='text', subtype='plain', filename='information.txt')

                    try:
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login('lifesloadingscreen@gmail.com', app_password)
                            smtp.send_message(msg)
                        print(f"Email sent to {user_email}")
                    except Exception as e:
                        print(f"Failed to send email to {user_email}: {e}")

    schedule.every().day.at("08:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(300)



if __name__ == '__main__':
    app.run(debug=True)