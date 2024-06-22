import requests

notebook_url = 'https://colab.research.google.com/drive/1N2i6rtYi4lp9CruU7qeHeLDCIj-get-F'
print('Run starts')
response = requests.post(notebook_url)
print(response.content)
print('Run ends')