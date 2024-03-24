import requests
import streamlit as st

# Workflow: Image ==> AI Model for generate semainsets information ==> AI Model for generate caption

SEMAINTICS_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
CAPTION_GENERATION_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

# def generate_semaintics(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     response = requests.post(SEMAINTICS_API_URL, headers=headers, data=data)
#     return response.json()

# output = query("./images/cat.png")
# output = generate_semaintics("./images/01.jpg")
# print(output[0]['generated_text'])
# print(output)


def generate_semaintics(file):
    response = requests.post(SEMAINTICS_API_URL, headers=headers, data=file)
    return response.json()


def generate_captions(payload):
    response = requests.post(CAPTION_GENERATION_API_URL,
                             headers=headers, json=payload)
    return response.json()


st.title("Image Captioning")
file = st.file_uploader(label="Upload an Image", type=['jpg', 'jpeg', 'png'])

if file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(image=file, use_column_width=True)
    with col2:
        with st.spinner("Generating Semaintics..."):
            semaintics = generate_semaintics(file)
        #     st.subheader(body="Semaintics")
        #     st.write(semaintics[0]['generated_text'].capitalize())
        #     st.write(semaintics[0]['generated_text'])

        with st.spinner("Generating Captions..."):
            prompt_dic = {
                "inputs": f"Question:Covert the following image semaintics '{semaintics}' to an instagram caption Make sure to add hash tags and emojis. Answer: "}
            raw_caption = generate_captions(payload=prompt_dic)
            caption = raw_caption[0]['generated_text'].split("Answer: ")[1]
            st.subheader(body="Caption")
            # st.write(caption)
            style = """
                    <style>
                        .fancy-text {
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #ccc;
                            box-shadow: 5px 5px 15px #aaa;
                        }
                    </style>
                    """

            fancy_text = f"{style}<div class='fancy-text'>{caption}</div>"
            st.markdown(body=fancy_text, unsafe_allow_html=True)
