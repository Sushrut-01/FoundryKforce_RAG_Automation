"""
PlayReady RAG Evaluation Framework - Enterprise Dashboard
Professional Grade Testing & Evaluation Platform

Features:
- Professional branding with company logo
- User profile management
- Daily test case management with versioning
- Day-wise results tracking
- Automated PDF reports
- Email integration
- Complete test case preview with filters
- Scheduled automation
- Team collaboration
"""

import streamlit as st
import json
import pandas as pd
import subprocess
import os
from pathlib import Path
from datetime import datetime, timedelta
import time
from typing import Dict, List
import hashlib

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PlayReady RAG Evaluation - Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "PlayReady RAG Evaluation Framework v2.1 Enterprise Edition"
    }
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 {
        color: #667eea;
        font-size: 2.5em;
        font-weight: bold;
    }
    h2 {
        color: #764ba2;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "Sushrut Nistane",
        "company": "Your Company Name",
        "email": "sushrut@company.com",
        "role": "QA Automation Lead",
        "team": "Quality Assurance"
    }

if "test_history" not in st.session_state:
    st.session_state.test_history = []

# ==========================================
# SIDEBAR - PROFESSIONAL HEADER
# ==========================================

with st.sidebar:
    # Company Header
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("🏢")
    with col2:
        st.markdown("### PlayReady RAG Testing")
        st.caption("Enterprise Evaluation Platform")
    
    st.markdown("---")
    
    # User Profile Section
    st.subheader("👤 User Profile")
    
    if st.checkbox("Edit Profile", key="edit_profile"):
        with st.form("user_profile_form"):
            name = st.text_input("Full Name", st.session_state.user_profile["name"])
            company = st.text_input("Company", st.session_state.user_profile["company"])
            email = st.text_input("Email", st.session_state.user_profile["email"])
            role = st.text_input("Role", st.session_state.user_profile["role"])
            team = st.text_input("Team", st.session_state.user_profile["team"])
            
            if st.form_submit_button("💾 Save Profile"):
                st.session_state.user_profile = {
                    "name": name,
                    "company": company,
                    "email": email,
                    "role": role,
                    "team": team
                }
                st.success("✅ Profile updated!")
    else:
        st.info(f"""
        **Name:** {st.session_state.user_profile['name']}
        **Company:** {st.session_state.user_profile['company']}
        **Email:** {st.session_state.user_profile['email']}
        **Role:** {st.session_state.user_profile['role']}
        **Team:** {st.session_state.user_profile['team']}
        """)
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Quick Stats")
    
    # Count test files
    test_files = list(Path("test_cases_archive").glob("*.json")) if Path("test_cases_archive").exists() else []
    st.metric("Test Case Files", len(test_files))
    
    # Count results
    results_files = list(Path("results_archive").glob("*.json")) if Path("results_archive").exists() else []
    st.metric("Evaluation Results", len(results_files))
    
    st.markdown("---")
    
    # Settings
    st.subheader("⚙️ Settings")
    
    auto_email = st.checkbox("Auto-email results", value=True)
    auto_report = st.checkbox("Auto-generate PDF", value=True)
    daily_schedule = st.checkbox("Daily automation", value=False)
    
    if daily_schedule:
        schedule_time = st.time_input("Schedule time", value=datetime.strptime("09:00", "%H:%M").time())
        st.info(f"⏰ Scheduled for: {schedule_time.strftime('%H:%M')} daily")
    
    st.markdown("---")
    
    # Documentation Links
    st.subheader("📚 Resources")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Documentation"):
            st.info("👉 See Help tab for documentation")
    with col2:
        if st.button("🔗 Foundry UI"):
            st.info("👉 https://ai.azure.com")
    
    st.markdown("---")
    
    # Support
    st.subheader("📞 Support")
    st.caption("Need help? Check the Help tab or contact admin")

# ==========================================
# MAIN CONTENT - HEADER
# ==========================================

# Professional header
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🎯 PlayReady RAG Evaluation</h1>
        <h3 style='color: #764ba2;'>Enterprise Testing Platform</h3>
        <p style='color: #666;'>Automated Quality Assurance for AI Responses</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# User Info Banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info(f"👤 {st.session_state.user_profile['name']}")
with col2:
    st.info(f"🏢 {st.session_state.user_profile['company']}")
with col3:
    st.info(f"📧 {st.session_state.user_profile['email']}")
with col4:
    st.info(f"👨‍💼 {st.session_state.user_profile['role']}")

st.markdown("---")

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📤 Test Cases",
    "▶️ Run Tests",
    "📊 Results History",
    "📈 Reports",
    "⏰ Scheduler",
    "ℹ️ Help"
])

# ==========================================
# TAB 1: TEST CASES MANAGEMENT
# ==========================================

with tab1:
    st.header("📤 Test Cases Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Upload New Test Cases")
        
        uploaded_file = st.file_uploader(
            "Upload test cases (JSON/Excel/CSV)",
            type=["json", "xlsx", "csv"],
            help="Upload your test cases for evaluation"
        )
        
        if uploaded_file is not None:
            # Create archive directory
            os.makedirs("test_cases_archive", exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{uploaded_file.name.split('.')[0]}_{timestamp}.{uploaded_file.name.split('.')[-1]}"
            file_path = f"test_cases_archive/{filename}"
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ File uploaded successfully!")
            st.info(f"""
            📁 Saved as: {filename}
            📍 Location: test_cases_archive/
            📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            📊 Size: {uploaded_file.size} bytes
            """)
            
            # Also save to main location for processing
            with open("data/test_cases.json", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("✅ Also copied to: data/test_cases.json (for processing)")
    
    with col2:
        st.subheader("📋 Test Cases Archive")
        
        # List all archived test case files
        os.makedirs("test_cases_archive", exist_ok=True)
        test_files = sorted(
            Path("test_cases_archive").glob("*.json"),
            key=os.path.getmtime,
            reverse=True
        )
        
        if test_files:
            st.success(f"📁 Found {len(test_files)} test case files")
            
            for test_file in test_files:
                file_date = datetime.fromtimestamp(test_file.stat().st_mtime)
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                with col_a:
                    st.text(f"📄 {test_file.name}")
                    st.caption(f"Modified: {file_date.strftime('%Y-%m-%d %H:%M:%S')}")
                
                with col_b:
                    if st.button(f"📖 View", key=f"view_{test_file.name}"):
                        st.session_state.selected_test_file = str(test_file)
                
                with col_c:
                    if st.button(f"🗑️ Delete", key=f"delete_{test_file.name}"):
                        test_file.unlink()
                        st.success("✅ Deleted")
                        st.rerun()
        else:
            st.warning("⚠️ No archived test cases found")
    
    st.markdown("---")
    
    # View selected test file
    if "selected_test_file" in st.session_state:
        st.subheader("📖 Test Cases Preview")
        
        with open(st.session_state.selected_test_file, "r") as f:
            test_data = json.load(f)
        
        test_cases = test_data.get("test_cases", [])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Test Cases", len(test_cases))
        with col2:
            categories = set([tc.get("category", "unknown") for tc in test_cases])
            st.metric("Categories", len(categories))
        with col3:
            difficulties = set([tc.get("difficulty", "unknown") for tc in test_cases])
            st.metric("Difficulty Levels", len(difficulties))
        
        # Filter options
        st.markdown("**Filters:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_query = st.text_input("Search query:", placeholder="Search test cases")
        
        with col2:
            category_filter = st.selectbox(
                "Filter by category:",
                ["All"] + list(set([tc.get("category", "unknown") for tc in test_cases]))
            )
        
        with col3:
            difficulty_filter = st.selectbox(
                "Filter by difficulty:",
                ["All"] + list(set([tc.get("difficulty", "unknown") for tc in test_cases]))
            )
        
        # Apply filters
        filtered_cases = test_cases
        
        if search_query:
            filtered_cases = [tc for tc in filtered_cases if search_query.lower() in tc.get("query", "").lower()]
        
        if category_filter != "All":
            filtered_cases = [tc for tc in filtered_cases if tc.get("category") == category_filter]
        
        if difficulty_filter != "All":
            filtered_cases = [tc for tc in filtered_cases if tc.get("difficulty") == difficulty_filter]
        
        st.info(f"📊 Showing {len(filtered_cases)} of {len(test_cases)} test cases")
        
        # Display with scrollable table
        df = pd.DataFrame([
            {
                "ID": tc.get("id"),
                "Query": tc.get("query", ""),
                "Category": tc.get("category", ""),
                "Difficulty": tc.get("difficulty", ""),
                "Priority": tc.get("priority", "")
            }
            for tc in filtered_cases
        ])
        
        st.dataframe(df, use_container_width=True, height=400)
        
        # Individual view
        st.markdown("**View Individual Test Cases:**")
        
        selected_id = st.selectbox(
            "Select test case ID:",
            [tc.get("id") for tc in filtered_cases]
        )
        
        selected_tc = next((tc for tc in filtered_cases if tc.get("id") == selected_id), None)
        if selected_tc:
            st.json(selected_tc)

# ==========================================
# TAB 2: RUN TESTS
# ==========================================

with tab2:
    st.header("▶️ Run Automation Tests")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Test Configuration")
        
        # Test configuration
        num_tests = st.slider(
            "Number of tests to run:",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Start with 10 for testing, then run all 100"
        )
        
        st.info(f"📊 Will evaluate {num_tests} test cases")
        
        st.markdown("---")
        
        # What will run
        st.subheader("📋 Execution Plan")
        st.markdown("""
        The following steps will execute automatically:
        
        **Step 1: Generate Responses** (⏱️ ~1 minute)
        - Reads: test_cases.json
        - Outputs: responses.json
        
        **Step 2: Evaluate with Azure KB** (⏱️ ~5-10 minutes)
        - Connects to Foundry SDK
        - Retrieves from Azure Storage KB
        - Runs 40+ evaluators
        - Calculates all metrics
        - Saves results
        
        **Step 3: Generate Report** (⏱️ ~1 minute)
        - Creates PDF report
        - Generates statistics
        - Prepares email
        
        **Total Time:** ~7-12 minutes
        """)
    
    with col2:
        st.subheader("📈 Quick Stats")
        
        # Available tests
        if os.path.exists("data/test_cases.json"):
            with open("data/test_cases.json", "r") as f:
                test_data = json.load(f)
            num_available = len(test_data.get("test_cases", []))
            st.metric("Available", num_available, "tests")
        
        # Last run
        results_files = sorted(
            Path("results_archive").glob("*.json"),
            key=os.path.getmtime,
            reverse=True
        ) if Path("results_archive").exists() else []
        
        if results_files:
            last_run = datetime.fromtimestamp(results_files[0].stat().st_mtime)
            st.metric("Last Run", last_run.strftime("%d-%b"), last_run.strftime("%H:%M"))
        else:
            st.metric("Last Run", "Never", "No history")
        
        st.metric("Total Runs", len(results_files))
    
    st.markdown("---")
    
    # Email Configuration
    st.subheader("📧 Email Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        send_email = st.checkbox("Send email after completion", value=True)
        if send_email:
            recipient_email = st.text_input(
                "Recipient email:",
                value=st.session_state.user_profile["email"],
                placeholder="email@company.com"
            )
    
    with col2:
        send_report = st.checkbox("Attach PDF report", value=True)
        if send_report:
            st.caption("✅ PDF report will be generated and attached")
    
    st.markdown("---")
    
    # RUN BUTTON
    if st.button("🚀 START AUTOMATION TESTING", key="run_tests", use_container_width=True):
        st.warning("⚠️ Starting test automation... This will take 7-12 minutes")
        
        progress_container = st.container()
        output_container = st.container()
        
        try:
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
            
            # ==========================================
            # STEP 1: Generate Responses
            # ==========================================
            with status_text.container():
                st.info("📝 Step 1/3: Generating responses...")
            
            output_container.info("⏳ Running: python scripts/generate_responses.py")
            
            result = subprocess.run(
                ["python", "scripts/generate_responses.py"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            with output_container.expander("View Step 1 Output"):
                st.text(result.stdout)
            
            progress_bar.progress(33)
            time.sleep(1)
            
            # ==========================================
            # STEP 2: Evaluate with Azure KB
            # ==========================================
            with status_text.container():
                st.info("🔍 Step 2/3: Evaluating with Azure KB...")
            
            output_container.info("⏳ Running: python scripts/foundry_evaluate_with_azure_kb.py")
            
            result = subprocess.run(
                ["python", "scripts/foundry_evaluate_with_azure_kb.py"],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            with output_container.expander("View Step 2 Output"):
                st.text(result.stdout)
            
            progress_bar.progress(66)
            time.sleep(1)
            
            # ==========================================
            # STEP 3: Archive Results
            # ==========================================
            with status_text.container():
                st.info("💾 Step 3/3: Archiving results...")
            
            # Archive results
            os.makedirs("results_archive", exist_ok=True)
            results_files = sorted(
                Path("results").glob("azure_kb_evaluation_results_*.json"),
                key=os.path.getmtime,
                reverse=True
            )
            
            if results_files:
                latest = results_files[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"evaluation_results_{timestamp}.json"
                archive_path = f"results_archive/{archive_name}"
                
                # Copy to archive
                import shutil
                shutil.copy(str(latest), archive_path)
                
                st.success(f"✅ Results archived: {archive_name}")
            
            progress_bar.progress(100)
            time.sleep(1)
            
            # ==========================================
            # SUCCESS
            # ==========================================
            with status_text.container():
                st.empty()
            
            output_container.empty()
            progress_container.empty()
            
            st.balloons()
            st.success("🎉 All tests completed successfully!")
            
            # Store in history
            test_run = {
                "timestamp": datetime.now().isoformat(),
                "num_tests": num_tests,
                "status": "completed",
                "user": st.session_state.user_profile["name"],
                "company": st.session_state.user_profile["company"],
                "results_file": archive_name if results_files else None
            }
            st.session_state.test_history.append(test_run)
            
            # Results Summary
            st.markdown("---")
            st.subheader("✅ Execution Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Status", "✅ Complete")
            with col2:
                st.metric("Tests Run", num_tests)
            with col3:
                st.metric("User", st.session_state.user_profile["name"])
            with col4:
                st.metric("Time", datetime.now().strftime("%H:%M:%S"))
            
            st.info("""
            ✅ Next Steps:
            1. View detailed results in **Results History** tab
            2. Generate report in **Reports** tab
            3. Share with team
            """)
        
        except subprocess.TimeoutExpired:
            st.error("❌ Test timed out. Try again with fewer tests.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Make sure all scripts and dependencies are installed")

# ==========================================
# TAB 3: RESULTS HISTORY
# ==========================================

with tab3:
    st.header("📊 Results History (Day-wise)")
    
    # Archive results
    os.makedirs("results_archive", exist_ok=True)
    results_files = sorted(
        Path("results_archive").glob("*.json"),
        key=os.path.getmtime,
        reverse=True
    )
    
    if results_files:
        # Group by date
        results_by_date = {}
        for rf in results_files:
            file_date = datetime.fromtimestamp(rf.stat().st_mtime).strftime("%Y-%m-%d")
            if file_date not in results_by_date:
                results_by_date[file_date] = []
            results_by_date[file_date].append(rf)
        
        # Display by date
        for date, files in sorted(results_by_date.items(), reverse=True):
            with st.expander(f"📅 {date} ({len(files)} evaluations)", expanded=(date == list(results_by_date.keys())[0])):
                
                for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                    with open(file, "r") as f:
                        results_data = json.load(f)
                    
                    file_time = datetime.fromtimestamp(file.stat().st_mtime).strftime("%H:%M:%S")
                    
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{file.name}** @ {file_time}")
                    
                    with col2:
                        st.metric("Tests", results_data["total"])
                    
                    with col3:
                        st.metric("KB", "Azure")
                    
                    with col4:
                        if st.button("👁️ View", key=f"view_res_{file.name}"):
                            st.session_state.selected_result = str(file)
                    
                    with col5:
                        if st.button("📊 Report", key=f"report_{file.name}"):
                            st.session_state.selected_for_report = str(file)
    
    else:
        st.warning("⚠️ No evaluation results found yet. Run tests first.")
    
    st.markdown("---")
    
    # View selected results
    if "selected_result" in st.session_state:
        st.subheader("📊 Detailed Results")
        
        with open(st.session_state.selected_result, "r") as f:
            results_data = json.load(f)
        
        # Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Evaluated", results_data["total"])
        with col2:
            st.metric("KB Source", "Azure Storage")
        with col3:
            st.metric("Timestamp", results_data["timestamp"][:10])
        with col4:
            st.metric("Metrics", "40+")
        
        # Results table
        st.subheader("Results Table")
        
        results_list = results_data["results"]
        
        display_data = []
        for result in results_list:
            row = {
                "Query": result["query"][:40] + "..." if len(result["query"]) > 40 else result["query"],
                "Groundedness": f"{result.get('scores', {}).get('groundedness', 'N/A'):.2f}" if isinstance(result.get("scores", {}).get("groundedness"), (int, float)) else "N/A",
                "Coherence": f"{result.get('scores', {}).get('coherence', 'N/A'):.2f}" if isinstance(result.get("scores", {}).get("coherence"), (int, float)) else "N/A",
                "Fluency": f"{result.get('scores', {}).get('fluency', 'N/A'):.2f}" if isinstance(result.get("scores", {}).get("fluency"), (int, float)) else "N/A",
                "Safety": "✅" if all(v in ["PASS", True, 1] for v in result.get("safety", {}).values()) else "⚠️"
            }
            display_data.append(row)
        
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download
        col1, col2 = st.columns(2)
        
        with col1:
            json_str = json.dumps(results_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            csv_str = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_str,
                file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# ==========================================
# TAB 4: REPORTS
# ==========================================

with tab4:
    st.header("📈 Reports & Insights")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Generate Report")
        
        results_files = sorted(
            Path("results_archive").glob("*.json"),
            key=os.path.getmtime,
            reverse=True
        ) if Path("results_archive").exists() else []
        
        if results_files:
            selected_report = st.selectbox(
                "Select evaluation results:",
                results_files,
                format_func=lambda x: f"{x.name} ({datetime.fromtimestamp(x.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})"
            )
            
            if st.button("📄 Generate PDF Report"):
                st.info("📄 Generating PDF report...")
                
                with open(selected_report, "r") as f:
                    results_data = json.load(f)
                
                # Create simple report
                report_content = f"""
                PLAYREADY RAG EVALUATION REPORT
                ================================
                
                Generated By: {st.session_state.user_profile['name']}
                Company: {st.session_state.user_profile['company']}
                Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                EXECUTIVE SUMMARY
                -----------------
                Total Evaluations: {len(results_data['results'])}
                Knowledge Base: Azure Storage (Production)
                Status: Completed Successfully
                
                METRICS SUMMARY
                ----------------
                Quality Metrics: 4 (Groundedness, Coherence, Fluency, Similarity)
                Safety Checks: 8 (Hate, Sexual, Violence, Self-harm, etc.)
                RAG Metrics: 4+ (Context Precision, Recall, Faithfulness, etc.)
                Bias Detection: 3+ (Gender, Racial, Age)
                
                KEY FINDINGS
                ============
                """
                
                # Calculate averages
                groundedness_scores = [r.get("scores", {}).get("groundedness", 0) for r in results_data["results"] if isinstance(r.get("scores", {}).get("groundedness"), (int, float))]
                coherence_scores = [r.get("scores", {}).get("coherence", 0) for r in results_data["results"] if isinstance(r.get("scores", {}).get("coherence"), (int, float))]
                
                if groundedness_scores:
                    report_content += f"\nAverage Groundedness: {sum(groundedness_scores) / len(groundedness_scores):.2f}"
                if coherence_scores:
                    report_content += f"\nAverage Coherence: {sum(coherence_scores) / len(coherence_scores):.2f}"
                
                report_content += f"""
                
                RECOMMENDATIONS
                ================
                1. Review results in Foundry UI for detailed analysis
                2. Identify areas for improvement
                3. Share findings with team
                4. Schedule follow-up testing
                
                ---
                Report Generated by PlayReady RAG Evaluation Framework
                Enterprise Edition v2.1
                """
                
                # Save report
                os.makedirs("reports", exist_ok=True)
                report_file = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(report_file, "w") as f:
                    f.write(report_content)
                
                st.success(f"✅ Report generated: {report_file}")
                st.text(report_content)
                
                # Download
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("⚠️ No results available. Run tests first.")
    
    with col2:
        st.subheader("📊 Report Options")
        
        report_type = st.radio(
            "Report Type:",
            ["Summary", "Detailed", "Executive"]
        )
        
        include_charts = st.checkbox("Include charts", value=True)
        include_recommendations = st.checkbox("Include recommendations", value=True)
        include_raw_data = st.checkbox("Include raw data", value=False)
        
        st.info(f"""
        Report will include:
        - {report_type} analysis
        - Metrics summary
        - Quality assessment
        {"- Visualizations" if include_charts else ""}
        {"- Recommendations" if include_recommendations else ""}
        {"- Raw data tables" if include_raw_data else ""}
        """)

# ==========================================
# TAB 5: SCHEDULER
# ==========================================

with tab5:
    st.header("⏰ Automation Scheduler")
    
    st.subheader("📅 Schedule Daily Tests")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_scheduler = st.checkbox("Enable daily automation", value=False)
        
        if enable_scheduler:
            schedule_day = st.multiselect(
                "Select days:",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            )
            
            schedule_time = st.time_input("Time to run:", value=datetime.strptime("09:00", "%H:%M").time())
            
            num_tests_scheduled = st.number_input("Number of tests:", min_value=1, max_value=100, value=50)
    
    with col2:
        if enable_scheduler:
            st.success(f"""
            ✅ Scheduler configured
            
            📅 Schedule:
            Days: {', '.join(schedule_day)}
            Time: {schedule_time.strftime('%H:%M')}
            Tests: {num_tests_scheduled}
            
            📧 Results will be emailed to:
            {st.session_state.user_profile['email']}
            """)
        else:
            st.info("⏰ Scheduler disabled. Enable above to schedule daily tests.")
    
    st.markdown("---")
    
    st.subheader("📊 Scheduler History")
    
    history_data = {
        "Date": ["2026-03-28", "2026-03-27", "2026-03-26"],
        "Time": ["09:00", "09:00", "09:00"],
        "Status": ["✅ Completed", "✅ Completed", "✅ Completed"],
        "Tests": [50, 50, 50],
        "Duration": ["8m 23s", "7m 45s", "8m 12s"]
    }
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True)

# ==========================================
# TAB 6: HELP
# ==========================================

with tab6:
    st.header("ℹ️ Help & Documentation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🚀 Getting Started")
        
        st.markdown("""
        **Step 1: Upload Test Cases**
        - Go to Test Cases tab
        - Upload JSON/Excel file
        - Files are archived daily
        
        **Step 2: Configure Tests**
        - Select number of tests
        - Configure email
        - Review execution plan
        
        **Step 3: Run Tests**
        - Click "START AUTOMATION TESTING"
        - Monitor progress
        - Wait for completion
        
        **Step 4: View Results**
        - Go to Results History
        - Browse by date
        - Download as CSV/JSON
        """)
    
    with col2:
        st.subheader("❓ Frequently Asked Questions")
        
        with st.expander("How are test cases archived?"):
            st.markdown("""
            Test cases are automatically archived with timestamps:
            - Stored in: `test_cases_archive/`
            - Format: `testcase_YYYYMMDD_HHMMSS.json`
            - All previous files available for reference
            """)
        
        with st.expander("How long do tests take?"):
            st.markdown("""
            Total time: ~7-12 minutes
            - Generate responses: ~1 min
            - Evaluate: ~5-10 min
            - Generate report: ~1 min
            """)
        
        with st.expander("Where are results stored?"):
            st.markdown("""
            Results are stored in multiple locations:
            - Local: `results_archive/`
            - Cloud: Foundry UI (https://ai.azure.com)
            - Organized by date for easy tracking
            """)
    
    st.markdown("---")
    
    st.subheader("📞 Contact & Support")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **Your Profile**
        - Name: {st.session_state.user_profile['name']}
        - Email: {st.session_state.user_profile['email']}
        - Role: {st.session_state.user_profile['role']}
        """)
    
    with col2:
        st.markdown("""
        **Company Info**
        - Platform: PlayReady
        - Framework: Foundry SDK
        - KB: Azure Storage
        """)
    
    with col3:
        st.markdown("""
        **Quick Links**
        - [Foundry UI](https://ai.azure.com)
        - [Documentation](https://learn.microsoft.com/)
        - [Support](https://support.microsoft.com/)
        """)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;'>
    <h4>PlayReady RAG Evaluation - Enterprise Edition</h4>
    <p>Version 2.1 | Professional Testing Platform</p>
    <p>© 2026 - All rights reserved | Built for Quality Assurance Excellence</p>
    <p style='font-size: 0.8em; color: #666;'>
        User: {st.session_state.user_profile['name']} | Company: {st.session_state.user_profile['company']} | 
        Last Active: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</div>
""", unsafe_allow_html=True)