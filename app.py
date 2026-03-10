import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from huggingface_hub import InferenceClient
load_dotenv()
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Hugging Face Client

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    output = client.image_classification(
        path,
        model="linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
    )

    disease = output[0]["label"]
    confidence = round(output[0]["score"] * 100, 2)

    # Leaf condition indicator
    if confidence < 60:
        condition = "Poor"
    elif confidence < 85:
        condition = "Slightly Good"
    else:
        condition = "Very Good"

    return render_template(
        "index.html",
        disease=disease,
        confidence=confidence,
        condition=condition
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

