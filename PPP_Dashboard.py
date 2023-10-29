import webbrowser
import streamlit as st
import subprocess

# Configure the default settings of the page.
st.set_page_config(page_title='PhonePe Pulse - Home', page_icon="rupee.png", layout="wide")

right_arrow = "\u2192"

# Title
# Tried to replicate the Phonepe Pulse Site, which has the word Pulse with a little shinning and popping.
# You can skip this with just a single line of title.
# CSS for the combined shining and heartbeat popping effect
col1, col2, col3 = st.columns([1,7,3])

with col1:
   st.image("rupee1.png", width=150)

with col2:
  combined_css = """
  @keyframes shine {
    0%, 100% { color: white; text-shadow: none; }
    50% { color: #C0C0C0; text-shadow: 0 0 10px #FFFFFF; }
  }

  @keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    20%, 80% { transform: scale(1.1); }
  }

  .title-container {
    display: flex;
    text-align: left;
  }

  .pulse-text {
    animation: heartbeat 1s linear infinite, shine 1.5s linear infinite;
    transition: transform 0.3s;
  }

  .pulse-text:hover {
    transform: scale(1.1);
  }

  .title {
    font-size: 80px;
    font-weight: 700;
  }

  .column {
    display: flex;
    justify-content: space-between;
  }
  """

  # Apply the CSS to the title
  st.markdown(f'<style>{combined_css}</style>', unsafe_allow_html=True)

  # Display the title with the combined shining and popping effect on "Pulse," a vertical line, and "The Beat of Progress" on the same line
  st.markdown('<div class="title-container">'
              '<h1 class="title">PhonePe <span class="pulse-text">Pulse</span></h1>'
              '</div>', unsafe_allow_html=True)

with col3:
   if st.button("To see the ofiicial website of PhonePe"):
          webbrowser.open("https://www.phonepe.com/")
   if st.button("To see the ofiicial website of PhonePe Pulse"):
          webbrowser.open("https://www.phonepe.com/pulse/")     



st.subheader("Welcome to PhonePe Pulse")

st.write("""
    PhonePe Pulse is a feature-rich analytical platform offered by PhonePe, one of India's leading digital payment and financial services providers. This platform provides valuable insights and data-driven trends about digital payments, offering a comprehensive view of consumer behavior and financial transactions in India. PhonePe Pulse empowers businesses and individuals with real-time, actionable data to make informed decisions and stay ahead in the dynamic world of digital finance. It's a powerful tool for gaining a deep understanding of the digital payments landscape, enabling users to monitor trends, make strategic choices, and drive financial success.
    """)


col1, col2 = st.columns([2,2])

with col1:
    st.image("pulse-video.gif", width=600)
with col2:
    st.title("11,000+ Crore Transactions")
    st.write("Top trends accross India's digital payments ")
    if st.button("Explore trends in digital payments     " + right_arrow):
      subprocess.Popen(["streamlit", "run", "PPP_Payments_Dashboard.py"])
    st.title("PhonePe Pulse Conversations")
    if st.button("View All     " + right_arrow):
          webbrowser.open("https://www.phonepe.com/pulse/conversations/")
    col3, col4 = st.columns([1,1])
    with col3:
      st.image("insurance_thumbnail.png")
    with col4:
      st.write("""<h1 style='text-align: left;line-height: 0.5;'>Insurance</h1><h1 style='text-align: left;line-height: 0.5;'>in India</h1>""", unsafe_allow_html=True)
      st.write("Discover the latest trends & data-driven insights from the Indian Insurance Market")
      if st.button("Explore Now     " + right_arrow):
          webbrowser.open("https://www.phonepe.com/pulse/explore/insurance/2023/3/")

col5, col6 = st.columns([2,2])
with col5:
    st.title("Digital Payments in India: A US$10 Tn Opportunity")
    st.caption("Check out the new PhonePe Pulse - BCG Report on what the future holds for digital payments in India")
    if st.button("Download the report now -->"):
        webbrowser.open("https://www.phonepe.com/pulsestatic/736/pulse/static/83bc2c9e9038369af2eb9eb7d62cb49f/PhonePe_Pulse_BCG_report.pdf")

with col6:
    st.video("https://youtu.be/c_1H6vivsiA?si=cj7OTzRlk-QdDbXh")

# # Add more information
st.write("__________________________________________________________________________________________________________________________________________")
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
with col1:
    if st.button("About the Project", use_container_width=True):
        webbrowser.open("Phonepe Pulse Data Visualization and Exploration_ A User-Friendly Tool Using Streamlit and Plotly.pdf")
with col2:
    if st.button("PhonePe", use_container_width=True):
            webbrowser.open("https://www.phonepe.com/")
with col3:
    if st.button("PhonePe Pulse", use_container_width=True):
        webbrowser.open("https://www.phonepe.com/pulse/")
with col4:
    if st.button("GitHub", use_container_width=True):
        webbrowser.open("https://github.com/PhonePe/pulse#readme")
with col5:
    if st.button("Reports", use_container_width=True):
        webbrowser.open("https://www.phonepe.com/pulse/reports/")
with col6:
    if st.button("Insights - Articles", use_container_width=True):
        webbrowser.open("https://www.phonepe.com/pulse/articles/")
with col7:
    if st.button("FunFacts", use_container_width=True):
        webbrowser.open("https://www.phonepe.com/pulse/fun-facts/")
with col8:
    if st.button("Data API", use_container_width=True):
        webbrowser.open("https://www.phonepe.com/pulse/data-api/")

st.subheader("Credits")
st.write("Inspired by PhonePe Pulse.")