import subprocess

def fetch_and_track_data():
    try:
        subprocess.run(["python", "fetch_data.py"], check=True)
        subprocess.run(["dvc", "add", "data.json"], check=True)
        subprocess.run(["git", "add", "data.json.dvc", ".gitignore"], check=True)
        subprocess.run(["git", "commit", "-m", "Update Firestore data"], check=True)
        subprocess.run(["dvc", "push"], check=True)
        
    except subprocess.CalledProcessError as e:
        print("Error:", e)

fetch_and_track_data()
