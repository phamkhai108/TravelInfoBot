import subprocess

def download_spacy_model():
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)

if __name__ == "__main__":
    download_spacy_model()
