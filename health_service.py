import google.generativeai as genai

genai.configure(api_key="AIzaSyBxtwBpknlgIv-jtGs89IdeZ7S0Dc6jv0Q")

model = genai.GenerativeModel("gemini-2.5-flash")

def predict_health(data):
    prompt = f"""
    Analze the following blood test results:
    Blood Sugar: {data['blood_sugar']}
    Cholesterol: {data['cholesterol']}
    Hemoglobin: {data['hemoglobin']}

    Give a short health risk assessment.
    """
    response = model.generate_content(prompt)
    return response.text

