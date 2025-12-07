import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from typing import Tuple, Optional


def get_base64_image(image_path: str) -> str:
    """Convert image to base64 string for embedding in HTML."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Page configuration
st.set_page_config(
    page_title="POM Assistant | SAP Ariba",
    page_icon="sap-icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# SAP FIORI "MORNING HORIZON" THEME
# Strict adherence to SAP Fiori Design Guidelines
# ============================================================================

FIORI_HORIZON_CSS = """
<style>
    /* ========================================
       SAP FIORI HORIZON DESIGN TOKENS
       ======================================== */
    :root {
        /* Brand & Primary Colors */
        --sapBrandColor: #0070F2;
        --sapPrimaryColor: #0070F2;
        --sapSecondaryColor: #0040B0;
        
        /* Backgrounds */
        --sapBackgroundColor: #F5F6F7;
        --sapShellColor: #354A5F;
        --sapSurfaceColor: #FFFFFF;
        
        /* Text */
        --sapTextColor: #32363A;
        --sapContent_LabelColor: #6A6D70;
        --sapTitleColor: #32363A;
        --sapShell_TextColor: #FFFFFF;
        
        /* Semantic Colors */
        --sapNegativeColor: #BB0000;
        --sapCriticalColor: #E9730C;
        --sapPositiveColor: #107E3E;
        --sapInformationColor: #0070F2;
        --sapNeutralColor: #6A6D70;
        
        /* Components */
        --sapButton_Background: #0070F2;
        --sapButton_Hover_Background: #0064D9;
        --sapButton_Active_Background: #0058C0;
        --sapButton_TextColor: #FFFFFF;
        --sapButton_BorderRadius: 8px;
        --sapField_BorderColor: #89919A;
        --sapField_Hover_BorderColor: #0070F2;
        --sapField_Focus_BorderColor: #0070F2;
        --sapField_Background: #FFFFFF;
        
        /* Cards */
        --sapTile_Background: #FFFFFF;
        --sapTile_BorderRadius: 12px;
        --sapTile_BoxShadow: 0 0 2px rgba(0,0,0,0.1), 0 2px 8px rgba(0,0,0,0.1);
        
        /* Spacing & Layout */
        --sapContentPadding: 1rem;
        --sapElementGridSpacing: 0.5rem;
        --sapContent_MaxWidth: 1200px;
        
        /* Shell */
        --sapShell_Height: 48px;
    }

    /* ========================================
       TYPOGRAPHY - SAP 72 Font Stack
       ======================================== */
    * {
        font-family: "72", "72full", "72-Web", Helvetica, Arial, sans-serif;
    }
    
    /* ========================================
       GLOBAL RESET & APP BACKGROUND
       ======================================== */
    .stApp {
        background-color: var(--sapBackgroundColor) !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu, footer, header, 
    .stApp > header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    .block-container {
        padding-top: 0 !important;
        max-width: 100% !important;
    }

    /* ========================================
       SHELL BAR (Fixed Header)
       ======================================== */
    .fiori-shell {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: var(--sapShell_Height);
        background-color: var(--sapShellColor);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1rem;
        z-index: 9999;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    
    .shell-logo {
        display: flex;
        align-items: center;
    }
    
    .sap-logo {
        height: 40px;
        width: auto;
    }
    
    .shell-title {
        color: var(--sapShell_TextColor);
        font-size: 1rem;
        font-weight: 400;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .shell-user {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .shell-avatar {
        width: 32px;
        height: 32px;
        background-color: #5A7A94;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--sapShell_TextColor);
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* ========================================
       MAIN CONTENT CONTAINER
       ======================================== */
    .fiori-content {
        margin-top: calc(var(--sapShell_Height) + 1rem);
        max-width: var(--sapContent_MaxWidth);
        margin-left: auto;
        margin-right: auto;
        padding: 0 1.5rem 2rem 1.5rem;
    }

    /* ========================================
       PAGE HEADER
       ======================================== */
    .fiori-page-header {
        margin-bottom: 1.5rem;
    }
    
    .fiori-page-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--sapTitleColor);
        margin: 0 0 0.25rem 0;
    }
    
    .fiori-page-subtitle {
        font-size: 0.9375rem;
        color: var(--sapContent_LabelColor);
        margin: 0;
    }

    /* ========================================
       CARDS (Fiori Tiles)
       ======================================== */
    .fiori-card {
        background: var(--sapTile_Background);
        border-radius: var(--sapTile_BorderRadius);
        box-shadow: var(--sapTile_BoxShadow);
        padding: var(--sapContentPadding);
        margin-bottom: 1rem;
    }
    
    .fiori-card-header {
        border-bottom: 1px solid #E5E5E5;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .fiori-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--sapTitleColor);
        margin: 0;
    }
    
    .fiori-card-subtitle {
        font-size: 0.8125rem;
        color: var(--sapContent_LabelColor);
        margin: 0.25rem 0 0 0;
    }

    /* ========================================
       INFO TILES (Key-Value Display)
       ======================================== */
    .fiori-info-tile {
        background: var(--sapSurfaceColor);
        border-radius: var(--sapTile_BorderRadius);
        box-shadow: var(--sapTile_BoxShadow);
        padding: 1rem 1.25rem;
        height: 100%;
    }
    
    .fiori-info-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--sapContent_LabelColor);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    
    .fiori-info-value {
        font-size: 1rem;
        font-weight: 600;
        color: var(--sapTextColor);
        word-break: break-word;
    }

    /* ========================================
       NUMERIC TILES (KPIs)
       ======================================== */
    .fiori-numeric-tile {
        background: var(--sapSurfaceColor);
        border-radius: var(--sapTile_BorderRadius);
        box-shadow: var(--sapTile_BoxShadow);
        padding: 1.25rem;
        text-align: center;
    }
    
    .fiori-numeric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--sapBrandColor);
        line-height: 1.1;
    }
    
    .fiori-numeric-label {
        font-size: 0.8125rem;
        font-weight: 500;
        color: var(--sapContent_LabelColor);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* ========================================
       OBJECT STATUS / BADGES
       ======================================== */
    .fiori-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8125rem;
        font-weight: 600;
    }
    
    .fiori-status-info {
        background-color: rgba(0, 112, 242, 0.12);
        color: var(--sapInformationColor);
    }
    
    .fiori-status-success {
        background-color: rgba(16, 126, 62, 0.12);
        color: var(--sapPositiveColor);
    }
    
    .fiori-status-warning {
        background-color: rgba(233, 115, 12, 0.12);
        color: var(--sapCriticalColor);
    }
    
    .fiori-status-error {
        background-color: rgba(187, 0, 0, 0.12);
        color: var(--sapNegativeColor);
    }

    /* ========================================
       CODE DISPLAY (AQL Query)
       ======================================== */
    .fiori-code-card {
        background: var(--sapSurfaceColor);
        border-radius: var(--sapTile_BorderRadius);
        box-shadow: var(--sapTile_BoxShadow);
        overflow: hidden;
    }
    
    .fiori-code-header {
        background: #F5F6F7;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #E5E5E5;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .fiori-code-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--sapTitleColor);
        margin: 0;
    }
    
    .fiori-code-body {
        padding: 1rem;
        background: #FAFBFC;
        font-family: "Consolas", "Monaco", "Courier New", monospace;
        font-size: 0.8125rem;
        color: var(--sapTextColor);
        line-height: 1.6;
        overflow-x: auto;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }

    /* ========================================
       BUTTONS
       ======================================== */
    .stButton > button {
        background-color: var(--sapButton_Background) !important;
        color: var(--sapButton_TextColor) !important;
        border: none !important;
        border-radius: var(--sapButton_BorderRadius) !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: background-color 0.15s ease !important;
        box-shadow: none !important;
    }
    
    .stButton > button:hover {
        background-color: var(--sapButton_Hover_Background) !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    .stButton > button:active {
        background-color: var(--sapButton_Active_Background) !important;
    }
    
    /* Secondary button style */
    .fiori-btn-secondary {
        background-color: transparent !important;
        color: var(--sapBrandColor) !important;
        border: 1px solid var(--sapBrandColor) !important;
    }
    
    .fiori-btn-secondary:hover {
        background-color: rgba(0, 112, 242, 0.06) !important;
    }

    /* ========================================
       FILE UPLOADER
       ======================================== */
    .fiori-upload-card {
        background: var(--sapSurfaceColor);
        border-radius: var(--sapTile_BorderRadius);
        box-shadow: var(--sapTile_BoxShadow);
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"] {
        background: transparent;
    }
    
    [data-testid="stFileUploader"] > div {
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: var(--sapSurfaceColor) !important;
        border: 2px dashed var(--sapField_BorderColor) !important;
        border-radius: 8px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] section:hover {
        border-color: var(--sapBrandColor) !important;
        background: rgba(0, 112, 242, 0.02) !important;
    }

    /* ========================================
       SECTION HEADERS
       ======================================== */
    .fiori-section-header {
        font-size: 1rem;
        font-weight: 600;
        color: var(--sapTitleColor);
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E5E5E5;
    }
    
    /* Override Streamlit h3 */
    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--sapTitleColor) !important;
        margin: 1.5rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid #E5E5E5 !important;
    }

    /* ========================================
       CONTACT LIST
       ======================================== */
    .fiori-contact-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .fiori-contact-chip {
        display: inline-flex;
        align-items: center;
        background: #F0F1F2;
        border-radius: 16px;
        padding: 0.375rem 0.75rem;
        font-size: 0.8125rem;
        color: var(--sapTextColor);
    }


    /* ========================================
       EMPTY STATE
       ======================================== */
    .fiori-empty-state {
        background: var(--sapSurfaceColor);
        border-radius: var(--sapTile_BorderRadius);
        box-shadow: var(--sapTile_BoxShadow);
        padding: 4rem 2rem;
        text-align: center;
    }
    
    .fiori-empty-icon {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #E8F4FD 0%, #D6E9FA 100%);
        border-radius: 50%;
        margin: 0 auto 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .fiori-empty-icon svg {
        width: 28px;
        height: 28px;
        color: var(--sapBrandColor);
    }
    
    .fiori-empty-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--sapTitleColor);
        margin: 0 0 0.5rem 0;
    }
    
    .fiori-empty-text {
        font-size: 0.875rem;
        color: var(--sapContent_LabelColor);
        margin: 0;
    }

    /* ========================================
       EXPANDER / ACCORDION
       ======================================== */
    .streamlit-expanderHeader {
        background: var(--sapSurfaceColor) !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 8px !important;
        color: var(--sapTextColor) !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        border: 1px solid #E5E5E5 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ========================================
       DATA TABLE
       ======================================== */
    .stDataFrame {
        border-radius: 8px !important;
        overflow: hidden;
        box-shadow: var(--sapTile_BoxShadow);
    }
    
    [data-testid="stDataFrame"] > div {
        border-radius: 8px;
        overflow: hidden;
    }

    /* ========================================
       CODE BLOCK (Streamlit native)
       ======================================== */
    .stCodeBlock {
        border-radius: 8px !important;
        border: 1px solid #E5E5E5 !important;
    }
    
    pre {
        background: #FAFBFC !important;
        border-radius: 8px !important;
    }

    /* ========================================
       GRID LAYOUT HELPERS
       ======================================== */
    .fiori-grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }
    
    .fiori-grid-2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
    
    @media (max-width: 768px) {
        .fiori-grid-3, .fiori-grid-2 {
            grid-template-columns: 1fr;
        }
    }
</style>
"""

st.markdown(FIORI_HORIZON_CSS, unsafe_allow_html=True)



def render_shell_bar():
    """Render the SAP Fiori Shell Bar (fixed header)."""
    # Get the SAP logo as base64
    logo_path = Path(__file__).parent / "saplogo.png"
    logo_base64 = get_base64_image(str(logo_path))
    
    shell_html = f"""
    <div class="fiori-shell">
        <div class="shell-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="SAP" class="sap-logo" />
        </div>
        <span class="shell-title">POM Assistant</span>
        <div class="shell-user">
            <div class="shell-avatar">PS</div>
        </div>
    </div>
    """
    st.markdown(shell_html, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str):
    """Render the page header section."""
    st.markdown(f"""
    <div class="fiori-page-header">
        <h1 class="fiori-page-title">{title}</h1>
        <p class="fiori-page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_info_tile(label: str, value: str):
    """Render a single info tile."""
    return f'<div class="fiori-info-tile"><div class="fiori-info-label">{label}</div><div class="fiori-info-value">{value}</div></div>'


def render_numeric_tile(value: str, label: str):
    """Render a numeric KPI tile."""
    return f"""
    <div class="fiori-numeric-tile">
        <div class="fiori-numeric-value">{value}</div>
        <div class="fiori-numeric-label">{label}</div>
    </div>
    """


def render_status_badge(text: str, status_type: str = "info"):
    """Render a status badge. status_type: info, success, warning, error"""
    return f'<span class="fiori-status fiori-status-{status_type}">{text}</span>'


def render_code_card(title: str, code: str):
    """Render a code display card."""
    return f"""
    <div class="fiori-code-card">
        <div class="fiori-code-header">
            <span class="fiori-code-title">{title}</span>
        </div>
        <div class="fiori-code-body">{code}</div>
    </div>
    """


def render_empty_state():
    """Render the empty state when no file is uploaded."""
    return """
    <div class="fiori-empty-state">
        <div class="fiori-empty-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#0070F2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 2V8H20" stroke="#0070F2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 18V12" stroke="#0070F2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 15L12 12L15 15" stroke="#0070F2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h2 class="fiori-empty-title">Upload Monitoring File</h2>
        <p class="fiori-empty-text">Drag and drop an Excel file or click to browse.<br/>Supports PO_Ordering and RC_Processing reports.</p>
    </div>
    """


def render_contact_chips(contacts: list):
    """Render contact email chips."""
    chips = "".join([f'<span class="fiori-contact-chip">{contact}</span>' for contact in contacts])
    return f'<div class="fiori-contact-list">{chips}</div>'


# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def extract_info_from_excel(df_info: pd.DataFrame) -> dict:
    """Extract metadata from the Info sheet."""
    info = {}
    
    for idx, row in df_info.iterrows():
        key = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        value = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        
        if key == "Realm":
            info["realm"] = value
        elif key == "Realms":
            info["realms"] = value
        elif key == "PSEE Consultant":
            info["product_specialist"] = value
        elif key == "Monitoring Contacts":
            info["customer_contacts"] = value
        elif key == "Monitoring":
            info["monitoring_type"] = value
        elif key == "Customer Account Name":
            info["customer_name"] = value
        elif key == "Data Center":
            info["data_center"] = value
    
    return info


def detect_monitoring_type(excel_file) -> Tuple[str, Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Detect the monitoring type from the Excel file."""
    xl = pd.ExcelFile(excel_file)
    sheet_names = xl.sheet_names
    
    df_info = None
    df_data = None
    monitoring_type = None
    
    if "Info" in sheet_names:
        df_info = pd.read_excel(xl, sheet_name="Info")
    
    # Check for known query types first
    if "PO_Ordering" in sheet_names:
        df_data = pd.read_excel(xl, sheet_name="PO_Ordering")
        monitoring_type = "PO_Ordering"
    elif "RC_Processing" in sheet_names:
        df_data = pd.read_excel(xl, sheet_name="RC_Processing")
        monitoring_type = "RC_Processing"
    else:
        # For other types, find the data sheet (any sheet that's not "Info")
        data_sheets = [s for s in sheet_names if s != "Info"]
        if data_sheets:
            data_sheet_name = data_sheets[0]
            df_data = pd.read_excel(xl, sheet_name=data_sheet_name)
            monitoring_type = data_sheet_name  # Use the sheet name as the type
    
    return monitoring_type, df_info, df_data


def has_query_support(monitoring_type: str) -> bool:
    """Check if the monitoring type has AQL query support."""
    return monitoring_type in ["PO_Ordering", "RC_Processing"]


def generate_po_ordering_query(unique_names: list) -> str:
    """Generate AQL query for PO Ordering."""
    names_str = ", ".join([f"'{name}'" for name in unique_names])
    
    query = f"""SELECT
UniqueName "PO ID Ariba",
OrderID "Order ID SAP",
Name "PO Title",
StatusString "Status",
"Active" "Active",
TimeCreated,
TimeUpdated,
Recipients.OrderingMethod "Ordering Method",
Recipients.State "Recipient State",
Recipients.FailureReason "Failure Reason",
Recipients.TimeCreated "Recipient TimeCreated",
Recipients.TimeUpdated "Recipient TimeUpdated",
Supplier.Name as "Supplier Name",
Supplier.UniqueName as "Supplier ID",
SupplierLocation.PreferredOrderingMethod as SupplierOrderingMethod,
SupplierLocation.EmailAddress as EmailAddress,
SupplierLocation.AribaNetworkId as AribaNetworkId,
this
FROM ariba.purchasing.core.PurchaseOrder
WHERE UniqueName IN ({names_str})
ORDER BY StatusString, UniqueName, TimeCreated, Recipients.OrderingMethod"""
    
    return query


def generate_rc_processing_query(unique_names: list) -> str:
    """Generate AQL query for RC Processing."""
    names_str = ", ".join([f"'{name}'" for name in unique_names])
    
    query = f"""SELECT DISTINCT UniqueName as "Id",
UniqueName,
StatusString,
CreateDate,
ApprovedDate,
'Awaiting processing' ProcessedStateString
FROM ariba.receiving.core.Receipt
WHERE StatusString = 'Approved'
AND ProcessedState = 1
AND UniqueName IN ({names_str})
ORDER BY ApprovedDate DESC"""
    
    return query


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Render Shell Bar
    render_shell_bar()
    
    # Main content wrapper
    st.markdown('<div class="fiori-content">', unsafe_allow_html=True)
    
    # Page Header
    render_page_header(
        "AQL Query Generator",
        "Generate AQL queries from SAP Ariba monitoring reports"
    )
    
    # File Upload Card
    st.markdown('<div class="fiori-upload-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Select Excel File",
        type=["xlsx", "xls"],
        help="Upload a PO_Ordering or RC_Processing monitoring Excel file",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Detect type and extract data
            monitoring_type, df_info, df_data = detect_monitoring_type(uploaded_file)
            
            if monitoring_type is None:
                st.error("Could not detect monitoring type. Please ensure the file contains a valid data sheet.")
                return
            
            # Extract info
            info = {}
            if df_info is not None:
                info = extract_info_from_excel(df_info)
            
            # Status Badge - different styles for different types
            if monitoring_type == "PO_Ordering":
                st.markdown(render_status_badge("PO Ordering", "info"), unsafe_allow_html=True)
            elif monitoring_type == "RC_Processing":
                st.markdown(render_status_badge("RC Processing", "success"), unsafe_allow_html=True)
            else:
                # Format the monitoring type name nicely (replace underscores with spaces)
                display_name = monitoring_type.replace("_", " ")
                st.markdown(render_status_badge(display_name, "warning"), unsafe_allow_html=True)
            
            # Report Information Section
            st.markdown("### Report Information")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(render_info_tile("Realm", info.get('realm', 'N/A')), unsafe_allow_html=True)
            
            with col2:
                st.markdown(render_info_tile("Product Specialist", info.get('product_specialist', 'N/A')), unsafe_allow_html=True)
            
            with col3:
                st.markdown(render_info_tile("Data Center", info.get('data_center', 'N/A')), unsafe_allow_html=True)
            
            # Customer Contacts
            contacts = info.get('customer_contacts', '')
            if contacts and contacts != 'N/A':
                st.markdown("### Customer Contacts")
                contact_list = [c.strip() for c in contacts.split(',')]
                st.markdown(f'<div class="fiori-card">{render_contact_chips(contact_list)}</div>', unsafe_allow_html=True)
            
            # Process Data
            if df_data is not None:
                # Summary KPIs
                st.markdown("### Summary")
                
                # Check if UniqueName column exists for record counting
                if "UniqueName" in df_data.columns:
                    unique_names = df_data["UniqueName"].dropna().unique().tolist()
                    record_count = len(unique_names)
                else:
                    record_count = len(df_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(render_numeric_tile(str(record_count), "Total Records"), unsafe_allow_html=True)
                
                with col2:
                    # Show monitoring type abbreviation
                    if monitoring_type == "PO_Ordering":
                        type_label = "PO"
                    elif monitoring_type == "RC_Processing":
                        type_label = "RC"
                    else:
                        type_label = monitoring_type[:3].upper() if len(monitoring_type) >= 3 else monitoring_type.upper()
                    st.markdown(render_numeric_tile(type_label, "Record Type"), unsafe_allow_html=True)
                
                # Generate Query - only for supported types
                if has_query_support(monitoring_type) and "UniqueName" in df_data.columns:
                    st.markdown("### Generated AQL Query")
                    
                    if monitoring_type == "PO_Ordering":
                        query = generate_po_ordering_query(unique_names)
                    else:
                        query = generate_rc_processing_query(unique_names)
                    
                    # Copyable code block
                    st.code(query, language="sql")
                
                # Data Preview
                st.markdown("### Raw Data")
                with st.expander("View uploaded data", expanded=not has_query_support(monitoring_type)):
                    st.dataframe(df_data, use_container_width=True)
                
            else:
                st.error("Could not find data in the uploaded file.")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        # Empty State
        st.markdown(render_empty_state(), unsafe_allow_html=True)
    
    # Close content wrapper
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
