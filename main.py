import streamlit as st

st.set_page_config(
        page_title="WanderWise",
        layout="centered",
    )

def main():
    with st.sidebar:
        st.title("🌍 WanderWise")
        st.markdown(
            """
            ## About
            WanderWise crafts bespoke travel itineraries, personalized just for you. Our AI-driven platform blends expert knowledge with your preferences to create seamless journeys that inspire and delight. Say goodbye to generic trips and hello to tailored adventures with WanderWise.
        """
        )

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

        age = st.slider("Travel Duration (Days)", 0, 7, 2)
        st.write(str(age))

        submit_button = st.form_submit_button(label='Submit')
    
if __name__ == "__main__":
    main()