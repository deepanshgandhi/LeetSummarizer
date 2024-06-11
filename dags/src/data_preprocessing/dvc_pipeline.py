import subprocess
import os


def fetch_and_track_data() -> None:
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable set successfully.")

        # Run fetch_data.py
        subprocess.run(["python", "fetch_data.py"], check=True)

        # Add data.json to DVC
        subprocess.run(["dvc", "add", "data.json"], check=True)

        # Push changes to DVC
        subprocess.run(["dvc", "push"], check=True)

        # Delete data.json
        os.remove("data.json")
        # Delete data.json.dvc
        os.remove("data.json.dvc")

        print("Data fetch and tracking completed successfully.")

    except subprocess.CalledProcessError as e:
        print("Error:", e)
    except FileNotFoundError as e:
        print("Error:", e)
    except Exception as e:
        print("Error setting GOOGLE_APPLICATION_CREDENTIALS:", e)
