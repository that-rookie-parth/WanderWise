import streamlit as st
from llm import askQuery

st.set_page_config(
        page_title="WanderWise",
        layout="centered",
    )

def show_page_one():

    st.header(" 🌍 WanderWise")
    st.caption("Crafting Unforgettable Journeys, One Itinerary at a Time")

    with st.form(key='my_form'):
        col1, col2 = st.columns(2)

        with col1:
            destination = st.selectbox(
                "What are your destination preferences?",
                [
                    "Tamil Nadu",
                    "Uttar Pradesh",
                    "Andhra Pradesh",
                    "Karnataka",
                    "Maharasthra"
                ]
            )

            interest = st.multiselect(
                "Interest & Activities",
                [
                    "Plains",
                    "Mountains",
                    "Beach",
                    "Historical Sites",
                    "Cultural Hubs",
                    "Urban Centers",
                    "Nature Reserves"
                ]
            )
        
        with col2:    
            transportation = st.multiselect(
                "Preferred Mode of Transportation at the destination",
                [
                    "Walking",
                    "Taxi / Cab",
                    "Two Wheelers",
                    "Auto Rickshaw",
                    "Metro",
                    "Boat / Ferry"
                ]
            )     

            extra = st.text_input("Additional Preferences")

        days = st.slider("Travel Duration (Days)", 0, 7, 2)
        st.write(str(days))

        submit_button = st.form_submit_button(label='Submit')

    # Process the form and redirect to page two on submission
    if submit_button:
        output = askQuery(
            destination,
            interest,
            transportation,
            extra,
            days
        )
        # Store the output using session_state
        st.session_state["form_output"] = output
        # Simulate page switch by setting current_page
        st.session_state["current_page"] = "page_two"

def show_page_two():

    st.header(" 🌍 WanderWise")
    st.caption("Crafting Unforgettable Journeys, One Itinerary at a Time")
    if "form_output" in st.session_state:
        output = st.session_state["form_output"]
        st.write(output)
    else:
        st.write("No results submitted yet.")

def main():
    with st.sidebar:
        st.title("🌍 WanderWise")
        st.markdown(
            """
            ## About
            WanderWise crafts bespoke travel itineraries, personalized just for you. Our AI-driven platform blends expert knowledge with your preferences to create seamless journeys that inspire and delight. Say goodbye to generic trips and hello to tailored adventures with WanderWise.
        """
        )

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "page_one"

    # Display content based on current page and redirect if needed
    current_page = st.session_state["current_page"]
    if current_page == "page_one":
        show_page_one()
    elif current_page == "page_two":
        show_page_two()
        # Reset current page to avoid infinite loop on refresh
        st.session_state["current_page"] = "page_one"
    
if __name__ == "__main__":
    main()