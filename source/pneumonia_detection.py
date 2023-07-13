import requests
from dotenv import load_dotenv
import os


def detect_pneumonia(file):
    load_dotenv()

    API_URL = "https://api-inference.huggingface.co/models/nickmuchi/vit-finetuned-chest-xray-pneumonia"
    API_TOKEN = os.environ["API_TOKEN"]

    # berisi header permintaan HTTP yang akan digunakan dalam permintaan API. Header Authorization akan berisi token API yang digunakan untuk otentikasi
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # melakukan permintaan ke API menggunakan metode POST. Fungsi ini menerima argumen file, yang merupakan path file gambar yang akan dikirim ke model

    data = file.read()

    response = requests.post(API_URL, headers=headers, data=data)

    normalScore = 0
    pneumoniaScore = 0

    if response.status_code == 200:
        output_json = response.json()

        for i, data in enumerate(output_json):
            if data["label"] == "NORMAL":
                normalScore = output_json[i]["score"]
            if data["label"] == "PNEUMONIA":
                pneumoniaScore = output_json[i]["score"]

    return [normalScore, pneumoniaScore]