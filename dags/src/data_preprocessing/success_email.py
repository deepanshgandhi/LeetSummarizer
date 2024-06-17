from airflow.models import Variable
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template  

def send_success_email(**kwargs):
    sender_email = Variable.get('EMAIL_USER')
    receiver_email = "odedra.r@northeastern.edu"
    password = Variable.get('EMAIL_PASSWORD')

    # Define subject and body templates
    subject_template = 'Airflow Success: {{ dag.dag_id }} - {{ task.task_id }}'
    body_template = 'The task {{ task.task_id }} in DAG {{ dag.dag_id }} succeeded.'

    # Render templates using Jinja2 Template
    subject = Template(subject_template).render(dag=kwargs['dag'], task=kwargs['task'])
    body = Template(body_template).render(dag=kwargs['dag'], task=kwargs['task'])

    # Create the email headers and content
    email_message = MIMEText(body, 'html')
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = receiver_email

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()
