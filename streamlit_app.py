import streamlit as st
import pandas as pd

# Load the predictions CSV
predictions = pd.read_csv('predictions.csv')

def show_machine_learning_page():
    st.title('Machine Learning Predictions')

    selected_region = st.selectbox('Select a Region', predictions['Region'].unique())

    # Convert Year and Month to string if they are not
    predictions['Year'] = predictions['Year'].astype(str)
    predictions['Month'] = predictions['Month'].astype(str)

    selected_year = st.selectbox('Select a Year', predictions[predictions['Region'] == selected_region]['Year'].unique())
    selected_month = st.selectbox('Select a Month', predictions[(predictions['Region'] == selected_region) & (predictions['Year'] == selected_year)]['Month'].unique())

    # Display the base map or the highlighted region map
    if selected_region:
        region_image_file = f"{selected_region.lower().replace(' ', '_')}_highlighted.webp"
        try:
            st.image(region_image_file, width=700)
        except FileNotFoundError:
            st.image("france_base.webp", width=700)
            st.warning(f"No highlighted map for {selected_region} available.")
    else:
        st.image("france_base.webp", width=700)

    if st.button('Predict'):
        
        # Retrieve the specific prediction
        specific_prediction = predictions[
            (predictions['Region'] == selected_region) &
            (predictions['Year'] == selected_year) &
            (predictions['Month'] == selected_month)
        ]
        
        if not specific_prediction.empty:
            avg_prediction = specific_prediction['AveragePrediction'].values[0]
            
            # Displaying the prediction method
            st.markdown('**Prediction made using pre-calculated data:**')
            st.markdown(f'<h2 style="font-weight:bold; color:blue;">Average Predicted Energy Consumption for {selected_region} in {selected_year} for the Month {selected_month} (MW):</h2>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="font-weight:bold; color:#FF4B4B;">{avg_prediction:.2f}</h1>', unsafe_allow_html=True)
            
            # Additional contextual information
            # Check if the prediction is for future dates
            if pd.to_datetime(f'{selected_year}-{selected_month}-01') > pd.to_datetime('2022-05-01'):
                st.write("Please note: The prediction for the selected period is based on projected trends, as the dataset available for analysis extends only up to May 2022. While this forecast is grounded in historical data patterns, it should be considered a reasoned estimate rather than a definitive figure.")
            else:
                st.write(f'Based on actual data points from {selected_year} in the Month {selected_month}.')
        else:
            st.error('No prediction data available for the selected combination of region, year, and month.')

def show_home_page():
    # Display the logo and introduction text
    st.image('transparent_bulb_logo.webp', width=150)  
    st.markdown(
        """
        # Welcome to the Energy Project
        
        The Energy Project is a data analyst initiative dedicated to the thorough exploration 
        and optimization of energy consumption. In the context of rapid technological 
        advancements and sustainable development challenges, our primary goal is to 
        intricately analyze national and departmental energy dynamics, focusing on risk 
        mitigation strategies for potential blackouts.
        
        Leveraging the comprehensive Open Data Energy Networks (ODRE) dataset since 2013, 
        we conduct in-depth departmental-level analyses, scrutinize production sectors, 
        and assess the geographical distribution of renewable energy sources.
        
        Explore our meticulous dataset overview, encompassing actual consumption, 
        production components, Energy Transfer Stations, and vital metrics such as TCO and TCH.
        
        For precise energy predictions, visit the Machine Learning page.
        
        Join us in shaping a sustainable and efficient future through data-driven insights 
        and informed decision-making.
        """
    )

def show_presentation_page():
    # Link to the file for downloading
    download_url = 'https://drive.google.com/uc?export=download&id=1_BUJULd8-MhvpxFt0FmHFERAO0aWagQR'
    link_text = 'Click here to download the presentation of the Energy Project'
    # Display the download link in blue
    st.markdown(f'<a href="{download_url}" download style="color: blue;">{link_text}</a>', unsafe_allow_html=True)

def show_authors_page():
    # Display authors and LinkedIn links
    st.title('Authors')
    st.markdown("""
    **Maryam Moradi**  
    [LinkedIn](https://www.linkedin.com/in/maryam-moradi-92b89771/)

    **Sara Cerreto**  
    [LinkedIn](https://www.linkedin.com/in/sara-cerreto/)

    **Leena Warunkar**  
    [LinkedIn](https://www.linkedin.com/in/leena-warunkar/)
    """)

# Set page configuration
st.set_page_config(page_title="Energy Consumption Predictions", page_icon="transparent_bulb_logo.webp", layout="wide")

if 'already_called' not in st.session_state:
    st.session_state['already_called'] = True
    st.session_state['current_page'] = 'Energy Project'

# Define a function to set the current page
def set_page(page_name):
    st.session_state['current_page'] = page_name

# Sidebar navigation with buttons
st.sidebar.title('Navigation')
if st.sidebar.button('Energy Project'):
    set_page('Energy Project')
if st.sidebar.button('Machine Learning'):
    set_page('Machine Learning')
if st.sidebar.button('Presentation'):
    set_page('Presentation')
if st.sidebar.button('Authors'):
    set_page('Authors')

# Display the selected page content
if st.session_state['current_page'] == 'Energy Project':
    show_home_page()
elif st.session_state['current_page'] == 'Machine Learning':
    show_machine_learning_page()  
elif st.session_state['current_page'] == 'Presentation':
    show_presentation_page()
elif st.session_state['current_page'] == 'Authors':
    show_authors_page()
