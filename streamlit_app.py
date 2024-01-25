import streamlit as st
import pandas as pd

# Load the predictions CSV
all_predictions = pd.read_csv('all_predictions_modified.csv')

def show_machine_learning_page():
    st.title('Machine Learning Predictions')
    
    selected_region = st.selectbox('Select a Region', all_predictions['Region'].unique())
    
    # Convert Year and Month to string if they are not
    all_predictions['Year'] = all_predictions['Year'].astype(str)
    all_predictions['Month'] = all_predictions['Month'].astype(str)
    
    selected_year = st.selectbox('Select a Year', all_predictions[all_predictions['Region'] == selected_region]['Year'].unique())
    selected_month = st.selectbox('Select a Month', all_predictions[(all_predictions['Region'] == selected_region) & (all_predictions['Year'] == selected_year)]['Month'].unique())
    
    if st.button('Predict'):
        # Retrieve the specific prediction
        specific_prediction = all_predictions[
            (all_predictions['Region'] == selected_region) &
            (all_predictions['Year'] == selected_year) &
            (all_predictions['Month'] == selected_month)
        ]
        
        if not specific_prediction.empty:
            avg_prediction = specific_prediction['AveragePrediction'].values[0]
            
            # Displaying the prediction method
            st.markdown('**Prediction made using pre-calculated data:**')
            st.markdown(f'<h2 style="font-weight:bold; color:blue;">Average Predicted Energy Consumption for {selected_region} in {selected_year} for the Month {selected_month} (MW):</h2>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="font-weight:bold; color:#FF4B4B;">{avg_prediction:.2f}</h1>', unsafe_allow_html=True)
            # Additional contextual information
            st.write(f'Based on 1488 data points from {selected_year} in the Month {selected_month}.')
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
st.set_page_config(page_title="Energy Consumption Predictions", page_icon=":zap:", layout="wide")

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
if st.sidebar.button('Authors'):
    set_page('Authors')

# Display the selected page content
if st.session_state['current_page'] == 'Energy Project':
    show_home_page()
elif st.session_state['current_page'] == 'Machine Learning':
    show_machine_learning_page()  
elif st.session_state['current_page'] == 'Authors':
    show_authors_page()
