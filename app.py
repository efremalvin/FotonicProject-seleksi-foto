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

# HTML Fallback 
img1_light = f'<img src="{b1}" class="img-light logo1-size">' if b1 else '<div class="img-light fallback-logo">Fotonic</div>'
img1_dark  = f'<img src="{w1}" class="img-dark logo1-size">' if w1 else '<div class="img-dark fallback-logo">Fotonic</div>'
img2_light = f'<img src="{b2}" class="img-light logo2-size">' if b2 else '<span class="img-light" style="font-size:1.5rem;">📷</span>'
img2_dark  = f'<img src="{w2}" class="img-dark logo2-size">' if w2 else '<span class="img-dark" style="font-size:1.5rem;">📷</span>'

# --- 2. CSS STYLING ---
st.markdown(
    f"""
<style>
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    
    .block-container {{
        padding-top: 10px !important;
        padding-bottom: 90px !important;
        max-width: 1200px !important;
    }}

    /* SISTEM TEMA OTOMATIS */
    .img-dark {{ display: none !important; }}
    @media (prefers-color-scheme: dark) {{
        .img-light {{ display: none !important; }}
        .img-dark {{ display: block !important; }}
    }}

    /* LOGO 1 DIPERKECIL 60% (max 100px) & IG LINK */
    .logo1-size {{ max-width: 100px; height: auto; display: block; margin: 0 auto; }}
    .fallback-logo {{ font-size: 1.5rem; font-weight: bold; text-align: center; }}
    .header-logo-1 {{
        text-align: center;
        padding-bottom: 24px;
        padding-top: 10px;
    }}
    .ig-link-top {{
        display: block;
        margin-top: 8px;
        font-size: 0.75rem;
        color: #71717a;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s;
    }}
    .ig-link-top:hover {{ color: #ff4b4b; }}

    /* LOGO 2 */
    .logo2-size {{ width: 28px; height: 28px; border-radius: 50%; object-fit: cover; }}
    
    /* TRIK MEMAKSA STICKY */
    div[data-testid="stVerticalBlock"] > div:has(.sticky-header) {{
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 12px !important;
        z-index: 99990 !important;
    }}

    /* HEADER STICKY (TIPIS & MINIMALIS) */
    .sticky-header {{
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 12px !important;
        z-index: 99990 !important;
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 12px 16px !important;
        border-radius: 18px !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
    }}
    @media (prefers-color-scheme: dark) {{
        .sticky-header {{
            background: rgba(18, 18, 20, 0.94) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
    }}
    
    /* TRANSISI HEADER: LOGO 2 MUNCUL, BAR PROGRES MENYEMPIT */
    #logo2-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        width: 0px; 
        opacity: 0;
        overflow: hidden;
        white-space: nowrap;
        transition: all 0.4s ease;
    }}
    #logo2-container.show {{
        width: 145px; /* Lebar optimal untuk logo + teks */
        opacity: 1;
        margin-right: 12px;
    }}
    #progress-container {{
        flex: 1; /* Otomatis melebar di awal, menyempit saat logo 2 muncul */
        transition: all 0.4s ease;
    }}

    /* SCROLLBAR */
    ::-webkit-scrollbar {{ width: 8px !important; }}
    ::-webkit-scrollbar-thumb {{ background: #ff4b4b !important; border-radius: 8px !important; }}

    /* KARTU FOTO FULL-FRAME (TANPA NAMA, CHECKBOX MELAYANG DI FOTO) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 20px !important;
        padding: 0px !important; /* Hapus celah dalam */
        background: transparent !important;
        border: 1px solid rgba(125, 125, 125, 0.15) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 16px !important;
        position: relative !important; /* Wadah acuan absolute */
        overflow: hidden !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{ padding: 0 !important; }}
    div[data-testid="stVerticalBlockBorderWrapper"] img {{
        border-radius: 20px !important;
        width: 100% !important;
        object-fit: cover !important;
        display: block !important;
    }}

    /* CHECKBOX POJOK KIRI ATAS */
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {{
        position: absolute !important;
        top: 8px !important;
        left: 8px !important;
        background: rgba(0, 0, 0, 0.45) !important;
        backdrop-filter: blur(4px) !important;
        border-radius: 8px !important;
        padding: 6px !important;
        margin: 0 !important;
        z-index: 10 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    /* Sembunyikan label nama file */
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label {{
        gap: 0 !important;
        min-height: 0 !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p {{
        display: none !important;
    }}

    /* FOOTER TOMBOL KIRI (MINIMALIS & COMPACT) */
    div[data-testid="stButton"] {{
        position: fixed !important;
        z-index: 99998 !important;
        bottom: 12px !important; /* Sangat mepet bawah */
        left: 12px !important;   /* Sangat mepet kiri */
        width: auto !important;  /* Menyesuaikan ukuran teks */
    }}
    div[data-testid="stButton"] button {{
        width: auto !important;
        height: 44px !important;
        padding: 0 20px !important; /* Jarak pas untuk teks */
        border-radius: 12px !important;
        color: white !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3) !important;
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

# --- 4. TAMPILAN HEADER LOGO 1 (MUNGIL & IG LINK) ---
html_logo1 = f"""
<div id="logo1-wrapper" class="header-logo-1">
    {img1_light}{img1_dark}
    <a href="https://instagram.com/fotonicproject" target="_blank" class="ig-link-top">Instagram ↗</a>
</div>
"""
st.markdown(html_logo1, unsafe_allow_html=True)

# --- 5. TAMPILAN STICKY HEADER DINAMIS (BAR PROGRES SAJA -> + LOGO 2) ---
rasio = min(total_terpilih / max_foto, 1.0)
warna_progres = '#22c55e' if total_terpilih == max_foto else '#ff4b4b'
lebar_progres = int(rasio * 100)

html_header = f"""
<div class="sticky-header">
    <div id="logo2-container">
        <div style="display:flex;">{img2_light}{img2_dark}</div>
        <div style="display:flex; flex-direction:column; justify-content:center;">
            <div style="font-size:0.95rem; font-weight:800; letter-spacing:-0.5px; line-height:1;">Fotonic</div>
            <div style="font-size:0.65rem; color:#71717a; margin-top:2px; line-height:1;">Photo & Video</div>
        </div>
    </div>
    <div id="progress-container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:0.85rem; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:60%;">{klien}</span>
            <span style="font-size:0.85rem; font-weight:800; color:{warna_progres}; white-space:nowrap;">{total_terpilih} / {max_foto}</span>
        </div>
        <div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 5px;">
            <div style="width: {lebar_progres}%; background-color: {warna_progres}; height: 100%; border-radius: 999px; transition: width 0.4s ease;"></div>
        </div>
    </div>
</div>
"""
st.markdown(html_header, unsafe_allow_html=True)

# --- 6. GALERI KARTU FOTO (FULL FRAME) ---
kolom = st.columns(3)
for idx, photo in enumerate(photos):
    with kolom[idx % 3]:
        with st.container(border=True):
            img_url = f"https://lh3.googleusercontent.com/d/{photo['id']}"
            file_name = photo["name"]
            
            # Urutan Streamlit: Gambar digambar lebih dulu, baru Checkbox menimpanya dari atas kiri
            st.image(img_url, use_container_width=True)
            
            is_checked = file_name in st.session_state.terpilih
            is_disabled = (total_terpilih >= max_foto) and not is_checked
            
            # Label kosong " " karena teksnya sudah disembunyikan via CSS
            cek = st.checkbox(" ", value=is_checked, key=photo["id"], disabled=is_disabled)
            
            if cek and file_name not in st.session_state.terpilih:
                st.session_state.terpilih.add(file_name)
                st.rerun()
            elif not cek and file_name in st.session_state.terpilih:
                st.session_state.terpilih.remove(file_name)
                st.rerun()

# --- 7. FOOTER KONFIRMASI (TOMBOL KIRI KECIL) ---
if st.button("Kunci & Kirim", type="primary"):
    if total_terpilih < max_foto:
        st.warning(f"Kurang {max_foto - total_terpilih} foto.")
    else:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        daftar_file_str = ",\n".join(sorted(list(st.session_state.terpilih)))
        try:
            sheet.append_row([waktu, klien, "Selesai", total_terpilih, daftar_file_str])
            st.success(f"Terima kasih! Terkirim.")
            st.balloons()
            st.code(daftar_file_str, language="text")
        except Exception as e:
            st.error(f"Gagal mencatat: {e}")

# --- 8. JAVASCRIPT: TRANSISI EKSPANSI HEADER ---
components.html("""
<script>
    try {
        const parentDoc = window.parent.document;
        const logo1 = parentDoc.getElementById('logo1-wrapper');
        const logo2 = parentDoc.getElementById('logo2-container');
        
        if (logo1 && logo2) {
            const observer = new IntersectionObserver((entries) => {
                if(entries[0].isIntersecting) {
                    // Logo 1 terlihat -> Logo 2 disembunyikan, Bar Progress melebar penuh
                    logo2.classList.remove('show');
                } else {
                    // Digulir ke bawah -> Logo 2 muncul, Bar Progress menyempit ke kanan
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
