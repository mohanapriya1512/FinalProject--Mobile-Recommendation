import streamlit as st
import pandas as pd
from langchain_community.llms import Cohere  # Corrected import
import cohere

# Load sentiment data
sentiment_data = pd.read_csv("Flipkart_mobile_reviews_Textblob_sentiment.csv")

# Initialize Cohere (Replace with your Cohere API Key)
cohere_api_key = '***********'  # Replace with your actual API key
co = cohere.Client(cohere_api_key)

# Function to recommend products based on user query
def recommend_products(query, sentiment_data):
    # Analyze the user's input using Cohere
    response = co.generate(prompt=query, model='command-xlarge-nightly')

    # Process response (you can also use a custom NLP method if needed)
    search_keywords = response.generations[0].text.strip().split()

    # Filter sentiment data based on query analysis (e.g., find related product names or positive reviews)
    recommendations = sentiment_data[sentiment_data['Reviews'].str.contains('|'.join(search_keywords))]

    # Sort products by sentiment score
    recommendations = recommendations.sort_values(by='Textblob_Polarity', ascending=False)

    # Select unique mobile names and return the top 5
    unique_recommendations = recommendations['Mobile Name'].drop_duplicates().head(3)

    # Convert to a list (optional) if you want to remove the index
    return {"Mobile Names": unique_recommendations.tolist()}
    #return unique_recommendations.tolist()

    # Return top 5 products
    #return recommendations['Mobile Name'].head(5)
    #return recommendations[['Mobile Name', 'Textblob_Polarity']].head(5)


# Streamlit App Interface Design
st.set_page_config(page_title="Mobile Recommendation Engine", page_icon="📱", layout="centered")
st.image("https://www.pngkey.com/png/detail/853-8531776_best-deals-on-smartphones-2017-mobile-phones-png.png", use_column_width=True)

# Title and description
st.title("📱 Mobile Recommendation Engine")
st.markdown("""
    Welcome to the **Mobile Recommendation Engine**!  
    Based on your preferences , we will recommend the best mobile phones for you.
""")

# Customizing input prompt
st.subheader("What are you looking for in a phone?")
st.markdown("Enter your preferences, such as *best camera phone*, *long battery life*, *budget-friendly*, etc.")

# Text input for user query
user_query = st.text_input("Your query here:", placeholder="Type something like 'best camera mobile'")


# Divider line for a cleaner look
st.markdown("---")
    
st.subheader("🔍 Recommendations based on your search")
    
if user_query:
        # Get top 5 product recommendations
        recommended_products = recommend_products(user_query, sentiment_data)

        if recommended_products['Mobile Names']:
            # Display the top mobile recommendations
            for idx, mobile in enumerate(recommended_products['Mobile Names'], start=1):
                st.write(f"**{idx}. {mobile}**")
        else:
            st.write("Sorry, no recommendations were found for your query. Please try a different one!")
else:
        st.write("Please enter a query to get recommendations.")

# Footer section
st.markdown("---")
# st.markdown("""
#     <style>
#     footer {visibility: hidden;}
#     .reportview-container .main footer {visibility: hidden;}
#     </style>
#     <div style='text-align:center'>
#         <p>Made with ❤️ by [Your Name]</p>
#     </div>
# """, unsafe_allow_html=True)
# streamlit run C:\Mobile_Recommendation\mobile_recommendation.py  -  COPY PASTE THIS IN TERMINAL TO RUN
