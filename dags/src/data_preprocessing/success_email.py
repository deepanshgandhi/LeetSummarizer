from airflow.models import Variable
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template  
from email.mime.multipart import MIMEMultipart

def send_success_email(**kwargs):
    sender_email = Variable.get('EMAIL_USER')
    password = Variable.get('EMAIL_PASSWORD')
    receiver_emails = ["odedra.r@northeastern.edu","shah.sanke@northeastern.edu", 
                      "gandhi.dee@northeastern.edu","savaj.b@northeastern.edu","madani.r@northeastern.edu"]

    # Define subject and body templates
    subject_template = 'Airflow Success: {{ dag.dag_id }} - Data+Model Pipeline tasks succeeded'
    body_template = '''Hi team,
    The Data+Model Pipeline tasks in DAG {{ dag.dag_id }} succeeded.'''
    
    # Render templates using Jinja2 Template
    subject = Template(subject_template).render(dag=kwargs['dag'], task=kwargs['task'])
    body = Template(body_template).render(dag=kwargs['dag'], task=kwargs['task'])

    # Create the email headers and content
    email_message = MIMEMultipart()
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = ", ".join(receiver_emails)

    # Add body to email
    email_message.attach(MIMEText(body, 'plain'))

    try:
            # Set up the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            
            # Send email to each receiver
            for receiver_email in receiver_emails:
                email_message.replace_header('To', receiver_email)
                server.sendmail(sender_email, receiver_email, email_message.as_string())
                print(f"Success email sent successfully to {receiver_email}!")

    except Exception as e:
        print(f"Error sending success email: {e}")
    finally:
        server.quit()
