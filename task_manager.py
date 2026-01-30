import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Task Manager Pro",
    page_icon="✅",
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
        padding: 0.5rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .task-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .priority-1 { border-left: 5px solid #ff4444; }
    .priority-2 { border-left: 5px solid #ff8800; }
    .priority-3 { border-left: 5px solid #ffbb33; }
    .priority-4 { border-left: 5px solid #00C851; }
    .priority-5 { border-left: 5px solid #33b5e5; }
    .completed { background-color: #e8f5e9; }
    .pending { background-color: #fff3e0; }
    h1 {
        color: #2c3e50;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Priority mapping with emojis
PRIORITY_EMOJI = {
    1: "🔴",
    2: "🟠",
    3: "🟡",
    4: "🟢",
    5: "🔵"
}

PRIORITY_LABEL = {
    1: "Critical",
    2: "High",
    3: "Medium",
    4: "Low",
    5: "Very Low"
}

STATUS_EMOJI = {
    "Pending": "⏳",
    "Completed": "✅"
}

# Functions
def validate_priority(priority):
    """Validate priority is between 1 and 5"""
    return 1 <= priority <= 5

def validate_status(status):
    """Validate status is either Pending or Completed"""
    return status in ["Pending", "Completed"]

def add_task(name, priority, status):
    """Add a new task to the session state"""
    if name.strip():  # Check if task name is not empty
        task = {
            "id": len(st.session_state.tasks) + 1,
            "name": name,
            "priority": priority,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.tasks.append(task)
        return True
    return False

def delete_task(task_id):
    """Delete a task by ID"""
    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != task_id]

def update_task_status(task_id):
    """Toggle task status between Pending and Completed"""
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["status"] = "Completed" if task["status"] == "Pending" else "Pending"
            break

def get_statistics():
    """Calculate task statistics"""
    total = len(st.session_state.tasks)
    completed = sum(1 for task in st.session_state.tasks if task["status"] == "Completed")
    pending = total - completed
    return total, completed, pending

# Header
st.markdown("# 📋 Task Manager Pro")
st.markdown("### Organize your tasks efficiently and stay productive!")
st.markdown("---")

# Sidebar for adding new tasks
with st.sidebar:
    st.markdown("## ➕ Add New Task")
    
    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("📝 Task Name", placeholder="Enter your task...")
        
        task_priority = st.select_slider(
            "🎯 Priority Level",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: f"{PRIORITY_EMOJI[x]} {PRIORITY_LABEL[x]}"
        )
        
        task_status = st.selectbox(
            "📊 Status",
            options=["Pending", "Completed"],
            format_func=lambda x: f"{STATUS_EMOJI[x]} {x}"
        )
        
        submit_button = st.form_submit_button("➕ Add Task")
        
        if submit_button:
            if validate_priority(task_priority) and validate_status(task_status):
                if add_task(task_name, task_priority, task_status):
                    st.success("✅ Task added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Task name cannot be empty!")
            else:
                st.error("❌ Invalid input! Please check your entries.")
    
    st.markdown("---")
    
    # Filter options
    st.markdown("## 🔍 Filter Tasks")
    filter_status = st.multiselect(
        "Status",
        options=["Pending", "Completed"],
        default=["Pending", "Completed"]
    )
    
    filter_priority = st.multiselect(
        "Priority",
        options=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5],
        format_func=lambda x: f"{PRIORITY_EMOJI[x]} {PRIORITY_LABEL[x]}"
    )
    
    st.markdown("---")
    
    # Clear all tasks button
    if st.button("🗑️ Clear All Tasks", type="secondary"):
        if st.session_state.tasks:
            st.session_state.tasks = []
            st.success("All tasks cleared!")
            st.rerun()

# Main content area
col1, col2, col3 = st.columns(3)

total_tasks, completed_tasks, pending_tasks = get_statistics()

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h2>📊 {total_tasks}</h2>
            <p>Total Tasks</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <h2>✅ {completed_tasks}</h2>
            <p>Completed</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);">
            <h2>⏳ {pending_tasks}</h2>
            <p>Pending</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Display tasks
if st.session_state.tasks:
    st.markdown("## 📝 Your Tasks")
    
    # Filter tasks
    filtered_tasks = [
        task for task in st.session_state.tasks
        if task["status"] in filter_status and task["priority"] in filter_priority
    ]
    
    # Sort options
    sort_option = st.selectbox(
        "Sort by:",
        options=["Priority (High to Low)", "Priority (Low to High)", "Status", "Date Created"],
        index=0
    )
    
    if sort_option == "Priority (High to Low)":
        filtered_tasks.sort(key=lambda x: x["priority"])
    elif sort_option == "Priority (Low to High)":
        filtered_tasks.sort(key=lambda x: x["priority"], reverse=True)
    elif sort_option == "Status":
        filtered_tasks.sort(key=lambda x: x["status"], reverse=True)
    elif sort_option == "Date Created":
        filtered_tasks.sort(key=lambda x: x["created_at"], reverse=True)
    
    if filtered_tasks:
        for task in filtered_tasks:
            status_class = "completed" if task["status"] == "Completed" else "pending"
            priority_class = f"priority-{task['priority']}"
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"""
                        <div class="task-card {status_class} {priority_class}">
                            <h3>{STATUS_EMOJI[task['status']]} {task['name']}</h3>
                            <p><strong>{PRIORITY_EMOJI[task['priority']]} Priority:</strong> {PRIORITY_LABEL[task['priority']]}</p>
                            <p><strong>📅 Created:</strong> {task['created_at']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.write("")
                    st.write("")
                    if task["status"] == "Pending":
                        if st.button(f"✅ Complete", key=f"complete_{task['id']}"):
                            update_task_status(task['id'])
                            st.rerun()
                    else:
                        if st.button(f"↩️ Reopen", key=f"reopen_{task['id']}"):
                            update_task_status(task['id'])
                            st.rerun()
                
                with col3:
                    st.write("")
                    st.write("")
                    if st.button(f"🗑️ Delete", key=f"delete_{task['id']}", type="secondary"):
                        delete_task(task['id'])
                        st.rerun()
    else:
        st.info("🔍 No tasks match the current filters.")
    
    st.markdown("---")
    
    # Export tasks as CSV
    st.markdown("## 📥 Export Tasks")
    if st.button("💾 Download Tasks as CSV"):
        df = pd.DataFrame(st.session_state.tasks)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
else:
    st.info("👋 No tasks yet! Add your first task using the sidebar.")
    st.markdown("""
        ### 💡 Getting Started:
        1. Use the sidebar to add a new task
        2. Set the priority level (1-5)
        3. Choose the status (Pending/Completed)
        4. Click 'Add Task' to save
        
        ### ✨ Features:
        - ✅ Add, edit, and delete tasks
        - 🎯 Set priority levels with visual indicators
        - 📊 Track task statistics
        - 🔍 Filter and sort tasks
        - 💾 Export tasks to CSV
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>Made with ❤️ using Streamlit | Task Manager Pro v1.0</p>
    </div>
""", unsafe_allow_html=True)
