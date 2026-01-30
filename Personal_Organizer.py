import streamlit as st
from datetime import datetime, date, timedelta
import calendar
import pandas as pd
import json

# Page configuration
st.set_page_config(
    page_title="Personal Organizer Pro",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with animations and gradients
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Header Styles */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Card Container */
    .stContainer > div {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.6s ease-in-out;
    }
    
    /* Button Styles */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Event Card Styles */
    .event-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        animation: slideInRight 0.5s ease-in-out;
    }
    
    .event-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    .event-card-work {
        border-left-color: #3498db;
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
    }
    
    .event-card-personal {
        border-left-color: #e74c3c;
        background: linear-gradient(135deg, #ffe8e8 0%, #ffd4d4 100%);
    }
    
    .event-card-birthday {
        border-left-color: #f39c12;
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    }
    
    .event-card-holiday {
        border-left-color: #9b59b6;
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    }
    
    .event-card-other {
        border-left-color: #16a085;
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
    }
    
    /* Delete Button */
    .delete-button>button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        color: white;
        padding: 0.5rem 1rem !important;
        border-radius: 8px;
    }
    
    .delete-button>button:hover {
        background: linear-gradient(135deg, #c0392b 0%, #a93226 100%) !important;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 500;
    }
    
    .stMetric .metric-value {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Badge Styles */
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-work { background-color: #3498db; color: white; }
    .badge-personal { background-color: #e74c3c; color: white; }
    .badge-birthday { background-color: #f39c12; color: white; }
    .badge-holiday { background-color: #9b59b6; color: white; }
    .badge-other { background-color: #16a085; color: white; }
    
    /* Priority Badges */
    .priority-high { 
        background-color: #e74c3c; 
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .priority-medium { 
        background-color: #f39c12; 
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .priority-low { 
        background-color: #27ae60; 
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in-out;
    }
    
    /* Calendar Mini Card */
    .calendar-mini {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
    }
    
    .calendar-day {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .calendar-month {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
    }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }
    
    /* Search Box */
    .search-box {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing events
if 'events' not in st.session_state:
    st.session_state.events = []

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Category and Priority options
CATEGORIES = {
    "Work": "💼",
    "Personal": "👤",
    "Birthday": "🎂",
    "Holiday": "🎉",
    "Other": "📌"
}

PRIORITIES = ["Low", "Medium", "High"]

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
def add_event(name, year, month, day, category, priority, notes=""):
    event = {
        'name': name,
        'year': year,
        'month': month,
        'day': day,
        'date': date(year, month, day),
        'category': category,
        'priority': priority,
        'notes': notes,
        'created_at': datetime.now()
    }
    st.session_state.events.append(event)
    st.session_state.events.sort(key=lambda x: x['date'])

# Function to delete an event
def delete_event(index):
    st.session_state.events.pop(index)

# Function to edit an event
def edit_event(index, name, year, month, day, category, priority, notes):
    st.session_state.events[index] = {
        'name': name,
        'year': year,
        'month': month,
        'day': day,
        'date': date(year, month, day),
        'category': category,
        'priority': priority,
        'notes': notes,
        'created_at': st.session_state.events[index].get('created_at', datetime.now())
    }
    st.session_state.events.sort(key=lambda x: x['date'])

# Function to format date
def format_date(year, month, day):
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return f"{month_names[month - 1]} {day}, {year}"

# Function to get category badge
def get_category_badge(category):
    badge_classes = {
        "Work": "badge-work",
        "Personal": "badge-personal",
        "Birthday": "badge-birthday",
        "Holiday": "badge-holiday",
        "Other": "badge-other"
    }
    return f'<span class="category-badge {badge_classes[category]}">{CATEGORIES[category]} {category}</span>'

# Function to get priority badge
def get_priority_badge(priority):
    priority_classes = {
        "High": "priority-high",
        "Medium": "priority-medium",
        "Low": "priority-low"
    }
    return f'<span class="{priority_classes[priority]}">⚡ {priority}</span>'

# Function to get event card class
def get_event_card_class(category):
    card_classes = {
        "Work": "event-card-work",
        "Personal": "event-card-personal",
        "Birthday": "event-card-birthday",
        "Holiday": "event-card-holiday",
        "Other": "event-card-other"
    }
    return f"event-card {card_classes[category]}"

# Sidebar
with st.sidebar:
    st.markdown("# 🎯 Quick Stats")
    
    total_events = len(st.session_state.events)
    upcoming_events = sum(1 for event in st.session_state.events if event['date'] >= date.today())
    past_events = total_events - upcoming_events
    
    st.metric("📊 Total Events", total_events)
    st.metric("⏰ Upcoming", upcoming_events)
    st.metric("✅ Past Events", past_events)
    
    st.markdown("---")
    
   
    
    # Priority breakdown
    st.markdown("### 🎯 By Priority")
    if st.session_state.events:
        priority_counts = {}
        for event in st.session_state.events:
            pri = event['priority']
            priority_counts[pri] = priority_counts.get(pri, 0) + 1
        
        for priority in ["High", "Medium", "Low"]:
            count = priority_counts.get(priority, 0)
            st.markdown(f"⚡ **{priority}**: {count}")
    else:
        st.info("No events yet")
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    if st.button("📥 Import Sample Data", use_container_width=True):
        sample_events = [
            {"name": "Team Meeting", "year": 2026, "month": 2, "day": 5, "category": "Work", "priority": "High", "notes": "Quarterly review"},
            {"name": "Mom's Birthday", "year": 2026, "month": 3, "day": 15, "category": "Birthday", "priority": "High", "notes": "Don't forget the cake!"},
            {"name": "Vacation", "year": 2026, "month": 6, "day": 20, "category": "Holiday", "priority": "Medium", "notes": "Beach resort"},
        ]
        for event in sample_events:
            add_event(event['name'], event['year'], event['month'], event['day'], 
                     event['category'], event['priority'], event['notes'])
        st.rerun()

# Main app header
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0;'>📅 Personal Organizer Pro</h1>
        <p style='font-size: 1.2rem; color: #7f8c8d;'>Stay organized, stay productive!</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Manage Events", "📊 Analytics", "📅 Calendar View"])

# TAB 1: Manage Events
with tab1:
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    # Left column - Add Event Form
    with col1:
        st.markdown("## ➕ Add New Event")
        
        with st.form(key="event_form", clear_on_submit=True):
            event_name = st.text_input(
                "📌 Event Name",
                placeholder="e.g., Birthday Party, Meeting, Anniversary",
                help="Enter a descriptive name for your event"
            )
            
            # Category and Priority
            col_cat, col_pri = st.columns(2)
            with col_cat:
                category = st.selectbox(
                    "📁 Category",
                    options=list(CATEGORIES.keys()),
                    format_func=lambda x: f"{CATEGORIES[x]} {x}"
                )
            
            with col_pri:
                priority = st.selectbox(
                    "⚡ Priority",
                    options=PRIORITIES,
                    index=1
                )
            
            # Date inputs
            col_year, col_month = st.columns(2)
            
            with col_year:
                current_year = datetime.now().year
                year = st.number_input(
                    "📅 Year",
                    min_value=1900,
                    max_value=2100,
                    value=current_year,
                    step=1
                )
            
            with col_month:
                month = st.selectbox(
                    "📅 Month",
                    options=list(range(1, 13)),
                    format_func=lambda x: calendar.month_name[x],
                    index=datetime.now().month - 1
                )
            
            # Calculate max days for selected month and year
            max_days = get_max_days(month, year)
            
            day = st.number_input(
                "📅 Day",
                min_value=1,
                max_value=max_days,
                value=1,
                step=1,
                help=f"Valid days for {calendar.month_name[month]}: 1-{max_days}"
            )
            
            # Notes
            notes = st.text_area(
                "📝 Notes (Optional)",
                placeholder="Add any additional details...",
                height=100
            )
            
            submit_button = st.form_submit_button("✨ Add Event", use_container_width=True)
            
            if submit_button:
                if event_name.strip():
                    add_event(event_name, year, month, day, category, priority, notes)
                    st.success(f"✅ Event '{event_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please enter an event name!")
    
    # Right column - Display Events
    with col2:
        st.markdown("## 📋 Your Events")
        
        # Search and Filter
        search_col, filter_col = st.columns(2)
        
        with search_col:
            search_term = st.text_input("🔍 Search events", placeholder="Search by name...")
        
        with filter_col:
            filter_category = st.selectbox(
                "🎯 Filter by category",
                options=["All"] + list(CATEGORIES.keys())
            )
        
        # Filter events
        filtered_events = st.session_state.events
        
        if search_term:
            filtered_events = [e for e in filtered_events if search_term.lower() in e['name'].lower()]
        
        if filter_category != "All":
            filtered_events = [e for e in filtered_events if e['category'] == filter_category]
        
        if filtered_events:
            st.markdown(f"**Showing {len(filtered_events)} of {len(st.session_state.events)} events**")
            
            # Display each event
            for idx, event in enumerate(filtered_events):
                # Find original index
                original_idx = st.session_state.events.index(event)
                
                with st.container():
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
                    <div class="{get_event_card_class(event['category'])}">
                        <h3 style="margin-top: 0;">{event['name']}</h3>
                        <p style="margin: 0.5rem 0;">
                            {get_category_badge(event['category'])}
                            {get_priority_badge(event['priority'])}
                        </p>
                        <p style="font-size: 1.1em; margin: 0.5rem 0;">
                            📆 {format_date(event['year'], event['month'], event['day'])}
                        </p>
                        <p style="color: {status_color}; font-weight: bold; margin: 0.5rem 0;">
                            {status}
                        </p>
                        {f'<p style="margin: 0.5rem 0; font-style: italic; color: #7f8c8d;">📝 {event["notes"]}</p>' if event.get('notes') else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    action_col1, action_col2 = st.columns([1, 1])
                    with action_col1:
                        if st.button("✏️ Edit", key=f"edit_{original_idx}", use_container_width=True):
                            st.session_state[f'editing_{original_idx}'] = True
                            st.rerun()
                    
                    with action_col2:
                        if st.button("🗑️ Delete", key=f"delete_{original_idx}", use_container_width=True):
                            delete_event(original_idx)
                            st.rerun()
                    
                    # Edit form (shown when edit button clicked)
                    if st.session_state.get(f'editing_{original_idx}', False):
                        with st.form(key=f"edit_form_{original_idx}"):
                            st.markdown("### Edit Event")
                            
                            edit_name = st.text_input("Event Name", value=event['name'])
                            
                            edit_col1, edit_col2 = st.columns(2)
                            with edit_col1:
                                edit_category = st.selectbox(
                                    "Category",
                                    options=list(CATEGORIES.keys()),
                                    index=list(CATEGORIES.keys()).index(event['category'])
                                )
                            with edit_col2:
                                edit_priority = st.selectbox(
                                    "Priority",
                                    options=PRIORITIES,
                                    index=PRIORITIES.index(event['priority'])
                                )
                            
                            edit_col3, edit_col4 = st.columns(2)
                            with edit_col3:
                                edit_year = st.number_input("Year", value=event['year'], min_value=1900, max_value=2100)
                            with edit_col4:
                                edit_month = st.selectbox(
                                    "Month",
                                    options=list(range(1, 13)),
                                    index=event['month'] - 1,
                                    format_func=lambda x: calendar.month_name[x]
                                )
                            
                            edit_max_days = get_max_days(edit_month, edit_year)
                            edit_day = st.number_input("Day", value=event['day'], min_value=1, max_value=edit_max_days)
                            
                            edit_notes = st.text_area("Notes", value=event.get('notes', ''))
                            
                            save_col, cancel_col = st.columns(2)
                            with save_col:
                                if st.form_submit_button("💾 Save", use_container_width=True):
                                    edit_event(original_idx, edit_name, edit_year, edit_month, edit_day, 
                                             edit_category, edit_priority, edit_notes)
                                    st.session_state[f'editing_{original_idx}'] = False
                                    st.rerun()
                            
                            with cancel_col:
                                if st.form_submit_button("❌ Cancel", use_container_width=True):
                                    st.session_state[f'editing_{original_idx}'] = False
                                    st.rerun()
                    
                    st.markdown("---")
            
            # Export options
            st.markdown("### 📤 Export Options")
            
            col_csv, col_json, col_clear = st.columns(3)
            
            with col_csv:
                export_data = pd.DataFrame([
                    {
                        'Event': event['name'],
                        'Date': format_date(event['year'], event['month'], event['day']),
                        'Category': event['category'],
                        'Priority': event['priority'],
                        'Notes': event.get('notes', ''),
                        'Year': event['year'],
                        'Month': event['month'],
                        'Day': event['day']
                    }
                    for event in filtered_events
                ])
                
                csv = export_data.to_csv(index=False)
                st.download_button(
                    label="📥 CSV",
                    data=csv,
                    file_name="events.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_json:
                json_data = json.dumps([
                    {
                        'name': event['name'],
                        'date': format_date(event['year'], event['month'], event['day']),
                        'category': event['category'],
                        'priority': event['priority'],
                        'notes': event.get('notes', '')
                    }
                    for event in filtered_events
                ], indent=2)
                
                st.download_button(
                    label="📥 JSON",
                    data=json_data,
                    file_name="events.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col_clear:
                if st.button("🗑️ Clear All", use_container_width=True):
                    if st.session_state.get('confirm_clear', False):
                        st.session_state.events = []
                        st.session_state.confirm_clear = False
                        st.rerun()
                    else:
                        st.session_state.confirm_clear = True
                        st.warning("Click again to confirm")
        else:
            st.info("📝 No events match your search. Try adjusting your filters!")

# TAB 2: Analytics
with tab2:
    st.markdown("## 📊 Event Analytics")
    
    if st.session_state.events:
        # Overview metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric("Total Events", len(st.session_state.events))
        
        with metric_col2:
            upcoming = sum(1 for e in st.session_state.events if e['date'] >= date.today())
            st.metric("Upcoming", upcoming)
        
        with metric_col3:
            this_month = sum(1 for e in st.session_state.events 
                           if e['date'].month == date.today().month and e['date'].year == date.today().year)
            st.metric("This Month", this_month)
        
        with metric_col4:
            high_priority = sum(1 for e in st.session_state.events if e['priority'] == "High")
            st.metric("High Priority", high_priority)
        
        st.markdown("---")
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### 📁 Events by Category")
            category_data = {}
            for event in st.session_state.events:
                cat = event['category']
                category_data[cat] = category_data.get(cat, 0) + 1
            
            if category_data:
                cat_df = pd.DataFrame(list(category_data.items()), columns=['Category', 'Count'])
                st.bar_chart(cat_df.set_index('Category'))
        
        with col_chart2:
            st.markdown("### ⚡ Events by Priority")
            priority_data = {}
            for event in st.session_state.events:
                pri = event['priority']
                priority_data[pri] = priority_data.get(pri, 0) + 1
            
            if priority_data:
                pri_df = pd.DataFrame(list(priority_data.items()), columns=['Priority', 'Count'])
                st.bar_chart(pri_df.set_index('Priority'))
        
        st.markdown("---")
        
        # Upcoming events timeline
        st.markdown("### 📅 Upcoming Events Timeline")
        upcoming_events = [e for e in st.session_state.events if e['date'] >= date.today()][:5]
        
        if upcoming_events:
            for event in upcoming_events:
                days_until = (event['date'] - date.today()).days
                progress = max(0, min(100, 100 - (days_until * 2)))
                
                st.markdown(f"**{event['name']}** - {format_date(event['year'], event['month'], event['day'])}")
                st.progress(progress / 100)
                st.caption(f"In {days_until} days" if days_until > 0 else "Today!")
        else:
            st.info("No upcoming events")
    else:
        st.info("📊 Add some events to see analytics!")

# TAB 3: Calendar View
with tab3:
    st.markdown("## 📅 Calendar View")
    
    if st.session_state.events:
        # Month selector
        view_col1, view_col2 = st.columns(2)
        
        with view_col1:
            view_year = st.selectbox(
                "Select Year",
                options=sorted(list(set(e['year'] for e in st.session_state.events))),
                index=0
            )
        
        with view_col2:
            view_month = st.selectbox(
                "Select Month",
                options=list(range(1, 13)),
                format_func=lambda x: calendar.month_name[x],
                index=date.today().month - 1
            )
        
        # Get events for selected month
        month_events = [e for e in st.session_state.events 
                       if e['year'] == view_year and e['month'] == view_month]
        
        st.markdown(f"### {calendar.month_name[view_month]} {view_year}")
        st.markdown(f"**{len(month_events)} events this month**")
        
        # Display events
        if month_events:
            for event in month_events:
                days_until = (event['date'] - date.today()).days
                
                col1, col2, col3 = st.columns([1, 3, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="calendar-mini">
                        <div class="calendar-day">{event['day']}</div>
                        <div class="calendar-month">{calendar.month_abbr[event['month']]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{event['name']}**")
                    st.caption(f"{get_category_badge(event['category'])} {get_priority_badge(event['priority'])}", unsafe_allow_html=True)
                
                with col3:
                    if days_until >= 0:
                        st.info(f"In {days_until} days" if days_until > 0 else "Today!")
                    else:
                        st.warning(f"{abs(days_until)} days ago")
                
                st.markdown("---")
        else:
            st.info(f"No events in {calendar.month_name[view_month]} {view_year}")
    else:
        st.info("📅 Add events to see them in calendar view!")

# Footer
st.markdown("""
    <div class="footer">
        <p style='color: white; font-size: 0.9rem;'>
            ✨ Built with ❤️ using Streamlit | Personal Organizer Pro v2.0
        </p>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.8rem;'>
            Stay organized, stay productive, stay amazing! 🚀
        </p>
    </div>
""", unsafe_allow_html=True)
