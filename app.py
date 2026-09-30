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

# --- FUNGSI BACA LOGO DARI GITHUB LOKAL ---
def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return ""

b1 = get_b64("blacklogo1.png")
w1 = get_b64("whitelogo1.png")
b2 = get_b64("blacklogo2.png")
w2 = get_b64("whitelogo2.png")

# HTML Fallback jika gambar belum terupload
img1_light = f'<img src="{b1}" class="img-light logo1-size">' if b1 else '<div class="img-light fallback-logo">Fotonic<br><span>Photo & Video Project</span></div>'
img1_dark  = f'<img src="{w1}" class="img-dark logo1-size">' if w1 else '<div class="img-dark fallback-logo">Fotonic<br><span>Photo & Video Project</span></div>'

img2_light = f'<img src="{b2}" class="img-light logo2-size">' if b2 else '<span class="img-light">📷</span>'
img2_dark  = f'<img src="{w2}" class="img-dark logo2-size">' if w2 else '<span class="img-dark">📷</span>'

# --- 2. CSS STYLING ---
st.markdown(
    f"""
<style>
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 110px !important;
        max-width: 1200px !important;
    }}

    /* SISTEM TEMA OTOMATIS (LIGHT/DARK) */
    .img-dark {{ display: none !important; }}
    @media (prefers-color-scheme: dark) {{
        .img-light {{ display: none !important; }}
        .img-dark {{ display: block !important; }}
    }}

    /* UKURAN LOGO */
    .logo1-size {{ max-width: 250px; height: auto; display: block; margin: 0 auto; }}
    .logo2-size {{ width: 34px; height: 34px; border-radius: 50%; object-fit: cover; }}
    .fallback-logo {{ font-size: 2rem; font-weight: bold; text-align: center; line-height: 1.1; }}
    .fallback-logo span {{ font-size: 1rem; font-weight: normal; color: #71717a; }}
    
    .header-logo-1 {{ padding: 10px 0 40px 0; }}

    /* STICKY HEADER */
    .sticky-top-header {{
        position: sticky !important;
        top: 0 !important;
        z-index: 99990 !important;
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 16px 24px !important;
        border-radius: 30px;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 24px;
    }}
    @media (prefers-color-scheme: dark) {{
        .sticky-top-header {{
            background: rgba(18, 18, 20, 0.94) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
    }}
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {{ width: 8px !important; }}
    ::-webkit-scrollbar-thumb {{ background: #ff4b4b !important; border-radius: 8px !important; }}

    /* KARTU FOTO EKSTREM (60px LUAR, 40px DALAM) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 60px !important; /* Radius Luar Ekstrem */
        padding: 14px !important; /* Jarak bingkai */
        background: rgba(125, 125, 125, 0.04) !important;
        border: 1px solid rgba(125, 125, 125, 0.1) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 16px !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] img {{
        border-radius: 40px !important; /* Radius Dalam */
        width: 100% !important;
        object-fit: cover !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {{
        background: transparent !important;
        border: none !important;
        padding: 16px 20px 4px 20px !important;
        margin: 0 !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p {{
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }}

    /* FOOTER KONFIRMASI (BUBBLE TO 1/3 KIRI) */
    div[data-testid="stButton"] {{
        position: fixed !important;
        z-index: 99998 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    /* State 1: Bubble Kiri Bawah */
    div[data-testid="stButton"].fab-mode {{
        bottom: 24px !important;
        left: 24px !important;
        width: 60px !important;
        height: 60px !important;
    }}
    div[data-testid="stButton"].fab-mode button {{
        width: 100% !important;
        height: 100% !important;
        border-radius: 50% !important;
        padding: 0 !important;
        color: transparent !important;
        box-shadow: 0 6px 16px rgba(255, 75, 75, 0.3) !important;
    }}
    div[data-testid="stButton"].fab-mode button::after {{
        content: "✓";
        position: absolute;
        color: white;
        font-size: 26px;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }}

    /* State 2: Full Mode (1/3 Kiri) */
    div[data-testid="stButton"].full-mode {{
        bottom: 24px !important;
        left: 24px !important;
        width: 33% !important; /* Lebar maksimal 1/3 layar */
        min-width: 280px !important; /* Agar tidak terlalu kecil di HP */
        max-width: 400px !important;
        background: transparent !important;
    }}
    div[data-testid="stButton"].full-mode button {{
        width: 100% !important;
        height: 52px !important;
        border-radius: 30px !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        box-shadow: 0 6px 16px rgba(255, 75, 75, 0.25) !important;
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

# --- 4. TAMPILAN HEADER LOGO 1 (TETAP DI ATAS) ---
st.markdown(f'<div class="header-logo-1">{img1_light}{img1_dark}</div>', unsafe_allow_html=True)

# --- 5. TAMPILAN STICKY HEADER ---
rasio = min(total_terpilih / max_foto, 1.0)
st.markdown(
    f"""
<div class="sticky-top-header">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <!-- Logo 2 dan Teks Header dengan transisi opacity -->
        <div id="logo2-container" style="display:flex; align-items:center; gap:12px; opacity:0; transition: opacity 0.4s ease, transform 0.4s ease; transform: translateY(8px);">
            <div style="display:flex;">
                {img2_light}
                {img2_dark}
            </div>
            <div>
                <div style="font-size:1.1rem; font-weight:800; letter-spacing:-0.5px; line-height:1;">Fotonic</div>
                <div style="font-size:0.75rem; color:#71717a; margin-top:2px;">Photo & Video Project</div>
            </div>
        </div>
        <a href="https://instagram.com/fotonicproject" target="_blank" style="text-decoration:none; color:#71717a; font-size:0.85rem; font-weight:600;">Instagram ↗</a>
    </div>
    
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-size:0.9rem; font-weight:600;">Klien: {klien}</span>
        <span style="font-size:0.9rem; font-weight:800; color:{'#22c55e' if total_terpilih == max_foto else '#ff4b4b'};">
            {total_terpilih} / {max_foto} Foto
        </span>
    </div>
    <div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 6px;">
        <div style="width: {int(rasio * 100)}%; background-color: {'#22c55e' if total_terpilih == max_foto else '#ff4b4b'}; height: 100%; border-radius: 999px; transition: width 0.4s ease;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

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
if st.button(f"Kunci & Kirim ({total_terpilih}/{max_foto})", type="primary", use_container_width=True):
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

# --- 8. JAVASCRIPT: TRANSISI HEADER & FOOTER ---
components.html("""
<script>
    const parentDoc = window.parent.document;
    const viewContainer = parentDoc.querySelector('.stAppViewContainer');
    
    function updateLayout() {
        if (!viewContainer) return;
        const scrollPos = viewContainer.scrollTop;
        const maxScroll = viewContainer.scrollHeight - viewContainer.clientHeight;
        
        // --- Transisi Header (Logo 2 Muncul) ---
        const logo2Container = parentDoc.getElementById('logo2-container');
        if (logo2Container) {
            // Jika digulir ke bawah lebih dari 80px, logo 2 muncul
            if (scrollPos > 80) {
                logo2Container.style.opacity = '1';
                logo2Container.style.transform = 'translateY(0)';
            } else {
                logo2Container.style.opacity = '0';
                logo2Container.style.transform = 'translateY(8px)';
            }
        }
        
        // --- Transisi Footer (Bubble -> 1/3 Kiri) ---
        const buttonDiv = parentDoc.querySelector('div[data-testid="stButton"]');
        if (buttonDiv) {
            // Jika sisa gulir kurang dari 120px, rentangkan tombol
            if (maxScroll - scrollPos < 120) {
                buttonDiv.classList.add('full-mode');
                buttonDiv.classList.remove('fab-mode');
            } else {
                buttonDiv.classList.add('fab-mode');
                buttonDiv.classList.remove('full-mode');
            }
        }
    }
    
    // Pasang listener pada scroll
    if(viewContainer) {
        viewContainer.addEventListener('scroll', updateLayout);
        // Panggil sekali saat dimuat
        setTimeout(updateLayout, 300);
    }
    
    // Monitor perubahan DOM jaga-jaga Streamlit refresh render UI
    const observer = new MutationObserver(updateLayout);
    observer.observe(parentDoc.body, { childList: true, subtree: true });
</script>
""", height=0)
