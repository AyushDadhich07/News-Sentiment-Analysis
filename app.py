from imports import*
from data_preprocessing import*
from web_scrapper import*

def delete_files():
    files_to_delete = ['label_encoder.pkl', 'logreg_model.pkl', 'max_length.pkl', 'tokenizer.pkl']
    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"Deleted {file}")
        except FileNotFoundError:
            print(f"{file} not found")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

# Delete the files before training the model
delete_files()

subprocess.run(["python", "model.py"])

logreg = joblib.load('logreg_model.pkl')
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('max_length.pkl', 'rb') as handle:
    max_length = pickle.load(handle)
with open('label_encoder.pkl', 'rb') as handle:
    label_encoder = pickle.load(handle)


st.set_page_config(page_title="News Sentiment Analysis")
st.title("News Sentiment Analysis")

url = st.text_input("Link for the website page")
if url:
    titles, links = scrape(url, driver_path='geckodriver.exe')

    # Clean and preprocess titles
    cleaned_titles = [clean(title) for title in titles]
    padded_titles = preprocess_texts(cleaned_titles, tokenizer, max_length)

    # Make predictions
    predictions = logreg.predict(padded_titles)
    predicted_labels = label_encoder.inverse_transform(predictions)

    # Display results
    for title, link, sentiment in zip(titles, links, predicted_labels):
        st.write(f"Title: {title}")
        st.write(f"Link: {link}")
        st.write(f"Predicted Sentiment: {sentiment}")
        st.write("-----")