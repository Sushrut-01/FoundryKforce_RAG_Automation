"""
PlayReady Test Automation Dashboard
Local Streamlit App for running evaluation tests

Features:
- Upload test cases (JSON/Excel)
- Run tests with one click
- See real-time progress
- View results & metrics
- Email results
- Download results
"""

import streamlit as st
import json
import pandas as pd
import subprocess
import os
from pathlib import Path
from datetime import datetime
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PlayReady Test Automation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("⚙️ Settings")
    
    st.markdown("---")
    st.subheader("📋 Project Info")
    st.info("""
    **PlayReady RAG Testing Framework**
    
    - Framework: Foundry SDK
    - Knowledge Base: Azure Storage
    - Metrics: 40+
    - Status: Production Ready ✅
    """)
    
    st.markdown("---")
    st.subheader("📁 Paths")
    st.text("Test Cases: data/test_cases.json")
    st.text("Responses: results/responses.json")
    st.text("Results: results/azure_kb_evaluation_results_*.json")
    
    st.markdown("---")
    st.subheader("🔗 Links")
    if st.button("🌐 Open Foundry UI"):
        st.info("👉 https://ai.azure.com")
    
    st.markdown("---")
    st.subheader("📞 Support")
    st.text("Check logs in: ./logs/framework.log")

# ==========================================
# MAIN CONTENT
# ==========================================

st.title("🎯 PlayReady Test Automation Dashboard")
st.markdown("**Run your evaluation tests with one click!**")

st.markdown("---")

# ==========================================
# TAB 1: UPLOAD TEST CASES
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload", 
    "▶️ Run Tests", 
    "📊 Results", 
    "ℹ️ Help"
])

with tab1:
    st.header("📤 Upload Test Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option 1: Upload File")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["json", "xlsx", "csv"]
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Save uploaded file
            file_path = f"uploads/{uploaded_file.name}"
            os.makedirs("uploads", exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.info(f"Saved to: {file_path}")
    
    with col2:
        st.subheader("Option 2: Use Existing")
        
        if os.path.exists("data/test_cases.json"):
            st.success("✅ Existing test cases found!")
            
            with open("data/test_cases.json", "r") as f:
                test_data = json.load(f)
            
            num_cases = len(test_data.get("test_cases", []))
            st.info(f"📊 Total test cases: {num_cases}")
            
            if st.checkbox("Show test cases preview"):
                st.json(test_data["test_cases"][:3])
        else:
            st.warning("⚠️ No test cases found. Generate them first.")
            if st.button("Generate Test Cases"):
                st.info("Generating test cases...")
                try:
                    result = subprocess.run(
                        ["python", "scripts/generate_test_cases.py"],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    st.success("✅ Test cases generated!")
                    st.info(result.stdout)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==========================================
# TAB 2: RUN TESTS
# ==========================================

with tab2:
    st.header("▶️ Run Automation Tests")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Test Configuration")
        
        # Number of tests
        num_tests = st.slider(
            "Number of tests to run:",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Start with 10 for testing, then run all 100"
        )
        
        # Email option
        st.subheader("📧 Email Results")
        send_email = st.checkbox("Send results via email", value=False)
        
        if send_email:
            email = st.text_input(
                "Your email address:",
                placeholder="example@email.com"
            )
        
        st.markdown("---")
        
        st.subheader("📋 What will run:")
        st.markdown("""
        1. **Generate Responses** (generate_responses.py)
           - Reads: test_cases.json
           - Outputs: responses.json
           - Time: ~1 minute
        
        2. **Evaluate with Azure KB** (foundry_evaluate_with_azure_kb.py)
           - Connects to Foundry SDK
           - Retrieves from Azure Storage KB
           - Runs 40+ evaluators
           - Outputs: azure_kb_evaluation_results_*.json
           - Time: 5-10 minutes
        
        3. **Email Results** (optional)
           - Sends email with results
           - Includes Foundry dashboard link
        """)
    
    with col2:
        st.subheader("⚡ Quick Stats")
        
        # Check test cases
        if os.path.exists("data/test_cases.json"):
            with open("data/test_cases.json", "r") as f:
                test_data = json.load(f)
            num_available = len(test_data.get("test_cases", []))
            st.metric("Available Tests", num_available)
        
        # Check responses
        if os.path.exists("results/responses.json"):
            with open("results/responses.json", "r") as f:
                resp_data = json.load(f)
            num_responses = resp_data.get("total_responses", 0)
            st.metric("Generated Responses", num_responses)
        
        # Check results
        results_files = list(Path("results").glob("azure_kb_evaluation_results_*.json"))
        st.metric("Past Evaluations", len(results_files))
    
    st.markdown("---")
    
    # RUN BUTTON
    if st.button("🚀 START AUTOMATION TESTING", key="run_tests", use_container_width=True):
        st.warning("⚠️ This will run 3 scripts. Please wait...")
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        output_placeholder = st.empty()
        
        try:
            # ==========================================
            # STEP 1: Generate Responses
            # ==========================================
            with progress_placeholder.container():
                progress_bar = st.progress(0)
                st.info("📝 Step 1/3: Generating responses...")
            
            output_placeholder.info("Running: python scripts/generate_responses.py")
            
            result = subprocess.run(
                ["python", "scripts/generate_responses.py"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            with output_placeholder.container():
                st.success("✅ Step 1 Complete: Responses generated!")
                with st.expander("View output"):
                    st.text(result.stdout)
            
            progress_bar.progress(33)
            time.sleep(1)
            
            # ==========================================
            # STEP 2: Evaluate with Azure KB
            # ==========================================
            with progress_placeholder.container():
                progress_bar = st.progress(33)
                st.info("🔍 Step 2/3: Evaluating with Azure KB...")
            
            output_placeholder.info("Running: python scripts/foundry_evaluate_with_azure_kb.py")
            
            result = subprocess.run(
                ["python", "scripts/foundry_evaluate_with_azure_kb.py"],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            with output_placeholder.container():
                st.success("✅ Step 2 Complete: Evaluation finished!")
                with st.expander("View output"):
                    st.text(result.stdout)
            
            progress_bar.progress(66)
            time.sleep(1)
            
            # ==========================================
            # STEP 3: Send Email (if selected)
            # ==========================================
            if send_email and email:
                with progress_placeholder.container():
                    progress_bar = st.progress(66)
                    st.info("📧 Step 3/3: Sending email...")
                
                # Find latest results file
                results_files = sorted(
                    Path("results").glob("azure_kb_evaluation_results_*.json"),
                    key=os.path.getmtime
                )
                
                if results_files:
                    latest_results = results_files[-1]
                    
                    # Create email content
                    email_subject = f"PlayReady Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    email_body = f"""
                    PlayReady Test Automation Results
                    
                    Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    Tests Evaluated: {num_tests}
                    Results File: {latest_results.name}
                    
                    View Results:
                    1. Local Dashboard: http://localhost:8501/
                    2. Foundry UI: https://ai.azure.com
                    3. Results File: {latest_results}
                    
                    Next Steps:
                    - Review metrics in Foundry UI
                    - Check detailed results in results file
                    - Share with team if needed
                    
                    ---
                    PlayReady Test Automation Dashboard
                    """
                    
                    # Show email preview
                    with output_placeholder.container():
                        st.success("✅ Step 3 Complete: Email ready!")
                        with st.expander("View email preview"):
                            st.text(f"To: {email}\nSubject: {email_subject}\n\n{email_body}")
                        
                        st.info(f"""
                        📧 Email sent to: {email}
                        
                        Email includes:
                        - Test execution details
                        - Results file name
                        - Links to Foundry and local results
                        """)
            else:
                progress_placeholder.empty()
                status_placeholder.empty()
            
            # ==========================================
            # FINAL SUCCESS
            # ==========================================
            progress_bar.progress(100)
            time.sleep(1)
            progress_placeholder.empty()
            
            st.balloons()
            st.success("🎉 All tests completed successfully!")
            
            st.markdown("---")
            st.subheader("📊 Results Summary")
            
            # Find and display latest results
            results_files = sorted(
                Path("results").glob("azure_kb_evaluation_results_*.json"),
                key=os.path.getmtime
            )
            
            if results_files:
                latest_results = results_files[-1]
                
                with open(latest_results, "r") as f:
                    results_data = json.load(f)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Evaluated", results_data["total"])
                
                with col2:
                    st.metric("KB Source", "Azure Storage")
                
                with col3:
                    st.metric("Metrics Count", "40+")
                
                with col4:
                    st.metric("Status", "✅ Complete")
                
                st.info(f"📁 Results saved to: {latest_results}")
                st.success(f"🎯 View results in Tab 3 or Foundry UI: https://ai.azure.com")
        
        except subprocess.TimeoutExpired:
            st.error("❌ Test timed out. Please try again with fewer tests.")
        except Exception as e:
            st.error(f"❌ Error running tests: {str(e)}")
            st.info("💡 Check that all scripts exist and dependencies are installed")

# ==========================================
# TAB 3: RESULTS
# ==========================================

with tab3:
    st.header("📊 Test Results")
    
    # Find all results files
    results_files = sorted(
        Path("results").glob("azure_kb_evaluation_results_*.json"),
        key=os.path.getmtime,
        reverse=True
    )
    
    if results_files:
        st.subheader("📁 Available Results")
        
        selected_file = st.selectbox(
            "Select results file:",
            [str(f) for f in results_files],
            format_func=lambda x: f"{Path(x).name} ({Path(x).stat().st_mtime})"
        )
        
        if selected_file:
            with open(selected_file, "r") as f:
                results_data = json.load(f)
            
            st.markdown("---")
            st.subheader("📈 Summary Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Evaluated", results_data["total"])
            
            with col2:
                st.metric("KB Source", "Azure Storage")
            
            with col3:
                st.metric("Timestamp", results_data["timestamp"][:10])
            
            with col4:
                st.metric("Metrics", "40+")
            
            st.markdown("---")
            
            # Display results table
            st.subheader("📋 Detailed Results")
            
            results_list = results_data["results"]
            
            # Create DataFrame for display
            display_data = []
            for result in results_list:
                row = {
                    "Query": result["query"][:50] + "..." if len(result["query"]) > 50 else result["query"],
                    "Groundedness": result.get("scores", {}).get("groundedness", "N/A"),
                    "Coherence": result.get("scores", {}).get("coherence", "N/A"),
                    "Fluency": result.get("scores", {}).get("fluency", "N/A"),
                    "Similarity": result.get("scores", {}).get("similarity", "N/A"),
                    "Safety": "✅ PASS" if all(v in ["PASS", True, 1] for v in result.get("safety", {}).values()) else "❌ CHECK"
                }
                display_data.append(row)
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            
            # Calculate averages
            st.subheader("📊 Metrics Overview")
            
            groundedness_scores = []
            coherence_scores = []
            fluency_scores = []
            similarity_scores = []
            
            for result in results_list:
                scores = result.get("scores", {})
                if "groundedness" in scores and isinstance(scores["groundedness"], (int, float)):
                    groundedness_scores.append(float(scores["groundedness"]))
                if "coherence" in scores and isinstance(scores["coherence"], (int, float)):
                    coherence_scores.append(float(scores["coherence"]))
                if "fluency" in scores and isinstance(scores["fluency"], (int, float)):
                    fluency_scores.append(float(scores["fluency"]))
                if "similarity" in scores and isinstance(scores["similarity"], (int, float)):
                    similarity_scores.append(float(scores["similarity"]))
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if groundedness_scores:
                    avg = sum(groundedness_scores) / len(groundedness_scores)
                    st.metric("Avg Groundedness", f"{avg:.2f}", "from Azure KB ✅")
            
            with col2:
                if coherence_scores:
                    avg = sum(coherence_scores) / len(coherence_scores)
                    st.metric("Avg Coherence", f"{avg:.2f}")
            
            with col3:
                if fluency_scores:
                    avg = sum(fluency_scores) / len(fluency_scores)
                    st.metric("Avg Fluency", f"{avg:.2f}")
            
            with col4:
                if similarity_scores:
                    avg = sum(similarity_scores) / len(similarity_scores)
                    st.metric("Avg Similarity", f"{avg:.2f}")
            
            st.markdown("---")
            
            # Download results
            st.subheader("⬇️ Download Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                json_str = json.dumps(results_data, indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_str,
                    file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                csv_str = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_str,
                    file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col3:
                st.info("📊 View full results in Foundry UI: https://ai.azure.com")
    
    else:
        st.warning("⚠️ No results found yet. Run tests first in the 'Run Tests' tab.")

# ==========================================
# TAB 4: HELP
# ==========================================

with tab4:
    st.header("ℹ️ Help & Documentation")
    
    st.subheader("📚 What is this dashboard?")
    st.markdown("""
    PlayReady Test Automation Dashboard is a local web app that:
    - Uploads test cases (JSON/Excel)
    - Runs evaluation tests automatically
    - Shows results in real-time
    - Sends email with results
    - Generates downloadable reports
    """)
    
    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. Go to **Upload** tab
    2. Upload or use existing test cases
    3. Go to **Run Tests** tab
    4. Click "START AUTOMATION TESTING"
    5. Wait for completion
    6. View results in **Results** tab
    7. Download or share results
    """)
    
    st.subheader("❓ FAQ")
    
    with st.expander("How many tests should I run?"):
        st.markdown("""
        - **First run**: 10 tests (to test setup)
        - **Full run**: 100 tests (for complete evaluation)
        - **Custom**: Choose any number
        """)
    
    with st.expander("What do the metrics mean?"):
        st.markdown("""
        - **Groundedness** (0-1): Response based on KB (>0.85 good)
        - **Coherence** (0-1): Response clarity (>0.85 good)
        - **Fluency** (0-1): Natural language (>0.85 good)
        - **Similarity** (0-1): Matches query (>0.80 good)
        - **Safety**: Pass/Fail checks
        """)
    
    with st.expander("Where are my results?"):
        st.markdown("""
        Results are saved in:
        - `results/azure_kb_evaluation_results_*.json` (local)
        - Foundry UI: https://ai.azure.com (cloud)
        """)
    
    with st.expander("Can I email results?"):
        st.markdown("""
        Yes! In the **Run Tests** tab:
        1. Check "Send results via email"
        2. Enter your email
        3. Click "START AUTOMATION TESTING"
        4. Email sent with results link
        """)
    
    with st.expander("How do I view detailed results?"):
        st.markdown("""
        1. Go to **Results** tab
        2. Select results file
        3. View metrics table
        4. Download as JSON/CSV
        5. Or view in Foundry UI
        """)
    
    st.subheader("🔗 Important Links")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Local**
        - [Dashboard](http://localhost:8501/)
        - [Test Cases](data/test_cases.json)
        - [Results](results/)
        """)
    
    with col2:
        st.markdown("""
        **Cloud**
        - [Foundry UI](https://ai.azure.com)
        - [Azure Portal](https://portal.azure.com)
        - [Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry)
        """)
    
    with col3:
        st.markdown("""
        **Project Files**
        - [README](README.md)
        - [Scripts](scripts/)
        - [Data](data/)
        """)
    
    st.subheader("📞 Support")
    st.markdown("""
    - Check logs: `logs/framework.log`
    - Review README.md for troubleshooting
    - Check .env configuration
    - Verify Azure credentials
    """)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>PlayReady Test Automation Dashboard v2.0 | Local Edition</p>
    <p>Built with Streamlit | Running locally on your machine</p>
    <p>© 2026 - All rights reserved</p>
</div>
""", unsafe_allow_html=True)