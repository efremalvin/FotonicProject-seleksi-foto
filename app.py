import base64
import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Fotonic - Seleksi Foto",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- FUNGSI BACA LOGO DARI GITHUB ---
def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return ""

b1 = get_b64("blacklogo1.png")
w1 = get_b64("whitelogo1.png")
b2 = get_b64("blacklogo2.png")
w2 = get_b64("whitelogo2.png")

# HTML Fallback jika logo tidak ditemukan
img1_light = f'<img src="{b1}" class="img-light logo1-size">' if b1 else '<div class="img-light fallback-logo">Fotonic<br><span>Photo & Video Project</span></div>'
img1_dark  = f'<img src="{w1}" class="img-dark logo1-size">' if w1 else '<div class="img-dark fallback-logo">Fotonic<br><span>Photo & Video Project</span></div>'
img2_light = f'<img src="{b2}" class="img-light logo2-size">' if b2 else '<span class="img-light" style="font-size:1.5rem;">📷</span>'
img2_dark  = f'<img src="{w2}" class="img-dark logo2-size">' if w2 else '<span class="img-dark" style="font-size:1.5rem;">📷</span>'

# --- 2. CSS STYLING ---
st.markdown(
    f"""
<style>
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    
    .block-container {{
        padding-top: 20px !important;
        padding-bottom: 120px !important;
        max-width: 1200px !important;
    }}

    /* SISTEM TEMA OTOMATIS */
    .img-dark {{ display: none !important; }}
    @media (prefers-color-scheme: dark) {{
        .img-light {{ display: none !important; }}
        .img-dark {{ display: block !important; }}
    }}

    .logo1-size {{ max-width: 250px; height: auto; display: block; margin: 0 auto; }}
    .logo2-size {{ width: 34px; height: 34px; border-radius: 50%; object-fit: cover; }}
    .fallback-logo {{ font-size: 2rem; font-weight: bold; text-align: center; line-height: 1.1; }}
    .fallback-logo span {{ font-size: 1rem; font-weight: normal; color: #71717a; }}
    
    /* LOGO 1 ATAS */
    .header-logo-1 {{
        text-align: center;
        padding-bottom: 24px;
        padding-top: 10px;
    }}

    /* HEADER STICKY (LENGKUNGAN 24PX) */
    .sticky-header {{
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 16px !important;
        z-index: 99990 !important;
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 16px 24px !important;
        border-radius: 24px !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 24px;
    }}
    @media (prefers-color-scheme: dark) {{
        .sticky-header {{
            background: rgba(18, 18, 20, 0.94) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
    }}
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {{ width: 8px !important; }}
    ::-webkit-scrollbar-thumb {{ background: #ff4b4b !important; border-radius: 8px !important; }}

    /* KARTU LUAR FOTO (LENGKUNGAN 24PX IDENTIK DENGAN HEADER) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 50px !important;
        padding: 12px !important;
        background: rgba(125, 125, 125, 0.04) !important;
        border: 1px solid rgba(125, 125, 125, 0.2) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 20px !important;
        overflow: hidden !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        padding: 0 !important;
        border-radius: 24px !important;
    }}

    /* KONTROL LENGKUNGAN FOTO DI DALAM (TARGET LENGKAP SEMUA LAPISAN) */
    div[data-testid="stImage"] {{
        border-radius: 12px !important;
        overflow: hidden !important;
        line-height: 0 !important;
    }}
    div[data-testid="stImage"] img,
    div[data-testid="stImage"] > div,
    div[data-testid="stImage"] picture {{
        border-radius: 12px !important;
        overflow: hidden !important;
        width: 100% !important;
        object-fit: cover !important;
        display: block !important;
    }}

    /* CHECKBOX & NAMA FILE */
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {{
        background: transparent !important;
        border: none !important;
        padding: 14px 8px 4px 8px !important;
        margin: 0 !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p {{
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }}

    /* TOMBOL KIRI SIMPEL (50% LAYAR) */
    div[data-testid="stButton"] {{
        position: fixed !important;
        z-index: 99998 !important;
        bottom: 24px !important;
        left: 24px !important;
        width: 50% !important;
        max-width: 400px !important;
    }}
    div[data-testid="stButton"] button {{
        width: 100% !important;
        height: 52px !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        box-shadow: 0 6px 16px rgba(255, 75, 75, 0.25) !important;
    }}
    
    /* EFEK TRANSISI LOGO 2 PADA HEADER */
    #logo2-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        opacity: 0;
        transform: translateX(-15px);
        visibility: hidden;
        transition: opacity 0.4s ease, transform 0.4s ease, visibility 0.4s;
    }}
    #logo2-container.show {{
        opacity: 1;
        transform: translateX(0);
        visibility: visible;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. PARAMETER & KONEKSI API ---
query_params = st.query_params.to_dict()
klien = query_params.get("klien", "Klien Fotonic")
folder_id = query_params.get("folder_id", None)

try:
    max_foto = int(query_params.get("max", 15))
except:
    max_foto = 15

if not folder_id:
    st.warning("⚠️ Tautan belum menyertakan `folder_id` Google Drive.")
    st.stop()

@st.cache_resource
def init_google_apis():
    creds_dict = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets"],
    )
    return build("drive", "v3", credentials=creds), gspread.authorize(creds)

try:
    drive_service, gc = init_google_apis()
    sheet = gc.open("Rekap_Seleksi_Foto").sheet1
except Exception as e:
    st.error(f"Gagal menghubungkan sistem ke Google: {e}")
    st.stop()

@st.cache_data(ttl=300)
def get_photos(f_id):
    query = f"'{f_id}' in parents and mimeType contains 'image/' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)", pageSize=500, orderBy="name").execute()
    return results.get("files", [])

photos = get_photos(folder_id)

if "terpilih" not in st.session_state:
    st.session_state.terpilih = set()

total_terpilih = len(st.session_state.terpilih)

# --- 4. TAMPILAN HEADER LOGO 1 ---
st.markdown(f'<div id="logo1-wrapper" class="header-logo-1">{img1_light}{img1_dark}</div>', unsafe_allow_html=True)

# --- 5. TAMPILAN STICKY HEADER ---
rasio = min(total_terpilih / max_foto, 1.0)
warna_progres = '#22c55e' if total_terpilih == max_foto else '#ff4b4b'
lebar_progres = int(rasio * 100)

html_header = f'<div class="sticky-header"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; height: 34px;"><div id="logo2-container"><div style="display:flex;">{img2_light}{img2_dark}</div><div><div style="font-size:1.1rem; font-weight:800; letter-spacing:-0.5px; line-height:1;">Fotonic</div></div></div><a href="https://instagram.com/fotonicproject" target="_blank" style="text-decoration:none; color:#71717a; font-size:0.85rem; font-weight:600; margin-left:auto;">Instagram ↗</a></div><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><span style="font-size:0.9rem; font-weight:600;">Klien: {klien}</span><span style="font-size:0.9rem; font-weight:800; color:{warna_progres};">{total_terpilih} / {max_foto} Foto</span></div><div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 6px;"><div style="width: {lebar_progres}%; background-color: {warna_progres}; height: 100%; border-radius: 999px; transition: width 0.4s ease;"></div></div></div>'
st.markdown(html_header, unsafe_allow_html=True)

# --- 6. GALERI KARTU FOTO ---
kolom = st.columns(3)
for idx, photo in enumerate(photos):
    with kolom[idx % 3]:
        with st.container(border=True):
            img_url = f"https://lh3.googleusercontent.com/d/{photo['id']}"
            file_name = photo["name"]
            st.image(img_url, use_container_width=True)
            
            is_checked = file_name in st.session_state.terpilih
            is_disabled = (total_terpilih >= max_foto) and not is_checked
            
            cek = st.checkbox(f"{file_name}", value=is_checked, key=photo["id"], disabled=is_disabled)
            if cek and file_name not in st.session_state.terpilih:
                st.session_state.terpilih.add(file_name)
                st.rerun()
            elif not cek and file_name in st.session_state.terpilih:
                st.session_state.terpilih.remove(file_name)
                st.rerun()

# --- 7. FOOTER KONFIRMASI ---
if st.button("Kunci & Kirim", type="primary", use_container_width=True):
    if total_terpilih < max_foto:
        st.warning(f"Pilihan belum lengkap. Kurang {max_foto - total_terpilih} foto lagi.")
    else:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        daftar_file_str = ",\n".join(sorted(list(st.session_state.terpilih)))
        try:
            sheet.append_row([waktu, klien, "Selesai", total_terpilih, daftar_file_str])
            st.success(f"Terima kasih {klien}! Pilihan berhasil dikirim.")
            st.balloons()
            st.code(daftar_file_str, language="text")
        except Exception as e:
            st.error(f"Gagal mencatat: {e}")

# --- 8. JAVASCRIPT: TRANSISI HEADER ---
components.html("""
<script>
    try {
        const parentDoc = window.parent.document;
        const logo1 = parentDoc.getElementById('logo1-wrapper');
        const logo2 = parentDoc.getElementById('logo2-container');
        
        if (logo1 && logo2) {
            const observer = new IntersectionObserver((entries) => {
                if(entries[0].isIntersecting) {
                    logo2.classList.remove('show');
                } else {
                    logo2.classList.add('show');
                }
            }, { threshold: 0 });
            observer.observe(logo1);
        }
    } catch (error) {
        console.log("Transisi JS gagal: ", error);
    }
</script>
""", height=0)
