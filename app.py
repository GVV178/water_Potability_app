from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("model.pkl")
user_data_path = "data/user_data.xlsx"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = [float(data.get(col, 0)) for col in [
            "ph", "Hardness", "Solids", "Chloramines", "Sulfate",
            "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"
        ]]
        prediction = model.predict([features])[0]
        df = pd.DataFrame([data])
        try:
            old = pd.read_excel(user_data_path)
            df = pd.concat([old, df], ignore_index=True)
        except:
            pass
        df.to_excel(user_data_path, index=False)
        return jsonify({"potability": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
