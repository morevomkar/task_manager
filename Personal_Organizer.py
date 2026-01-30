import streamlit as st
from datetime import datetime, date
import calendar
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Personal Organizer",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .event-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
    }
    .delete-button>button {
        background-color: #f44336;
        color: white;
    }
    .delete-button>button:hover {
        background-color: #da190b;
    }
    h1 {
        color: #2c3e50;
    }
    h2, h3 {
        color: #34495e;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing events
if 'events' not in st.session_state:
    st.session_state.events = []

# Function to validate if a year is a leap year
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Function to get maximum days in a month
def get_max_days(month, year):
    if month == 2:
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

# Function to add an event
def add_event(name, year, month, day):
    event = {
        'name': name,
        'year': year,
        'month': month,
        'day': day,
        'date': date(year, month, day)
    }
    st.session_state.events.append(event)
    st.session_state.events.sort(key=lambda x: x['date'])

# Function to delete an event
def delete_event(index):
    st.session_state.events.pop(index)

# Function to format date
def format_date(year, month, day):
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return f"{month_names[month - 1]} {day}, {year}"

# Main app header
st.title("📅 Personal Organizer")
st.markdown("### Organize your important events and dates")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

# Left column - Add Event Form
with col1:
    st.markdown("## ➕ Add New Event")
    
    with st.form(key="event_form", clear_on_submit=True):
        event_name = st.text_input(
            "Event Name",
            placeholder="e.g., Birthday Party, Meeting, Anniversary",
            help="Enter a descriptive name for your event"
        )
        
        col_year, col_month = st.columns(2)
        
        with col_year:
            current_year = datetime.now().year
            year = st.number_input(
                "Year",
                min_value=1900,
                max_value=2100,
                value=current_year,
                step=1
            )
        
        with col_month:
            month = st.selectbox(
                "Month",
                options=list(range(1, 13)),
                format_func=lambda x: calendar.month_name[x],
                index=datetime.now().month - 1
            )
        
        # Calculate max days for selected month and year
        max_days = get_max_days(month, year)
        
        day = st.number_input(
            "Day",
            min_value=1,
            max_value=max_days,
            value=1,
            step=1,
            help=f"Valid days for {calendar.month_name[month]}: 1-{max_days}"
        )
        
        submit_button = st.form_submit_button("Add Event")
        
        if submit_button:
            if event_name.strip():
                add_event(event_name, year, month, day)
                st.success(f"✅ Event '{event_name}' added successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please enter an event name!")

# Right column - Display Events
with col2:
    st.markdown("## 📋 Your Events")
    
    if st.session_state.events:
        # Display statistics
        total_events = len(st.session_state.events)
        upcoming_events = sum(1 for event in st.session_state.events if event['date'] >= date.today())
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Total Events", total_events)
        with metric_col2:
            st.metric("Upcoming Events", upcoming_events)
        
        st.markdown("---")
        
        # Display each event
        for idx, event in enumerate(st.session_state.events):
            with st.container():
                event_col1, event_col2 = st.columns([4, 1])
                
                with event_col1:
                    # Calculate days until event
                    days_until = (event['date'] - date.today()).days
                    
                    if days_until < 0:
                        status = f"🕒 {abs(days_until)} days ago"
                        status_color = "#95a5a6"
                    elif days_until == 0:
                        status = "🎉 TODAY!"
                        status_color = "#e74c3c"
                    elif days_until <= 7:
                        status = f"⚡ In {days_until} days"
                        status_color = "#f39c12"
                    else:
                        status = f"📅 In {days_until} days"
                        status_color = "#3498db"
                    
                    st.markdown(f"""
                    <div class="event-card">
                        <h3 style="margin-top: 0;">{event['name']}</h3>
                        <p style="font-size: 1.1em; margin: 0.5rem 0;">
                            📆 {format_date(event['year'], event['month'], event['day'])}
                        </p>
                        <p style="color: {status_color}; font-weight: bold; margin: 0;">
                            {status}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with event_col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️", key=f"delete_{idx}", help="Delete this event"):
                        delete_event(idx)
                        st.rerun()
        
        # Export options
        st.markdown("---")
        st.markdown("### 📤 Export Events")
        
        # Create DataFrame for export
        export_data = pd.DataFrame([
            {
                'Event': event['name'],
                'Date': format_date(event['year'], event['month'], event['day']),
                'Year': event['year'],
                'Month': event['month'],
                'Day': event['day']
            }
            for event in st.session_state.events
        ])
        
        col_csv, col_clear = st.columns(2)
        
        with col_csv:
            csv = export_data.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="personal_organizer_events.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_clear:
            if st.button("🗑️ Clear All Events", use_container_width=True):
                st.session_state.events = []
                st.rerun()
    else:
        st.info("📝 No events yet. Add your first event using the form on the left!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>Built with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)
