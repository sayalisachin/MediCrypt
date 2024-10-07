import streamlit as st
from search import patient_search_page
from analytics import analytics_dashboard
from report import generate_report

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Search", "Analytics", "Reports"])

    if page == "Search":
        patient_search_page()
    elif page == "Analytics":
        analytics_dashboard()
    elif page == "Reports":
        generate_report()

if __name__ == "__main__":
    main()
