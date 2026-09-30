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
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

logo1_b64 = get_image_base64("logo1.png")
logo2_b64 = get_image_base64("logo2.png")

# HTML untuk Logo (dengan Fallback teks jika gambar belum diupload)
html_logo1 = f'<img src="{logo1_b64}" class="logo1-img">' if logo1_b64 else '<div class="brand-title" style="font-size:2rem; text-align:center;">Fotonic<br><span style="font-size:1rem; color:#71717a;">Photo & Video Project</span></div>'
html_logo2 = f'<img src="{logo2_b64}" class="logo2-img">' if logo2_b64 else '📷'

# --- 2. CSS STYLING (LOGO, KARTU PRESISI, & TRANSISI TOMBOL) ---
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

    /* LOGO 1 AWAL */
    .header-logo-1 {{
        text-align: center;
        padding: 10px 0 30px 0;
    }}
    .logo1-img {{
        max-width: 250px;
        height: auto;
        display: block;
        margin: 0 auto;
    }}

    /* STICKY HEADER (LOGO 2) */
    .sticky-top-header {{
        position: sticky !important;
        top: 0 !important;
        z-index: 99990 !important;
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(12px) !important;
        padding: 14px 24px !important;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 24px;
    }}
    .logo2-img {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
    }}
    
    /* SCROLLBAR KANAN */
    ::-webkit-scrollbar {{ width: 10px !important; }}
    ::-webkit-scrollbar-thumb {{ background: #ff4b4b !important; border-radius: 8px !important; }}

    /* KARTU FOTO PRESISI (RADIUS LUAR LEBIH BESAR DARI DALAM) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 20px !important; /* Radius Luar Lebar */
        padding: 8px !important; /* Jarak bingkai */
        background: rgba(125, 125, 125, 0.04) !important;
        border: 1px solid rgba(125, 125, 125, 0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 16px !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] img {{
        border-radius: 14px !important; /* Radius Dalam Lebih Kecil (Presisi) */
        width: 100% !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {{
        background: transparent !important;
        border: none !important;
        padding: 10px 4px 2px 4px !important;
        margin: 0 !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p {{
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }}

    /* TOMBOL BUBBLE KE FULL (DIKENDALIKAN OLEH JS) */
    div[data-testid="stButton"] {{
        position: fixed !important;
        z-index: 99998 !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    /* State 1: Bubble Kiri Bawah */
    div[data-testid="stButton"].fab-mode {{
        bottom: 24px !important;
        left: 24px !important;
        width: 55px !important;
        height: 55px !important;
    }}
    div[data-testid="stButton"].fab-mode button {{
        width: 100% !important;
        height: 100% !important;
        border-radius: 50% !important;
        padding: 0 !important;
        color: transparent !important; /* Sembunyikan teks */
        box-shadow: 0 6px 16px rgba(255, 75, 75, 0.3) !important;
    }}
    div[data-testid="stButton"].fab-mode button::after {{
        content: "✓";
        position: absolute;
        color: white;
        font-size: 24px;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }}

    /* State 2: Full Lebar di Bawah (Saat Mentok Scroll) */
    div[data-testid="stButton"].full-mode {{
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        padding: 16px 20px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(12px) !important;
        border-top: 1px solid rgba(0,0,0,0.1) !important;
    }}
    div[data-testid="stButton"].full-mode button {{
        width: 100% !important;
        max-width: 600px !important;
        margin: 0 auto !important;
        height: 48px !important;
        border-radius: 12px !important;
        color: white !important; /* Tampilkan teks */
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25) !important;
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
st.markdown(f'<div class="header-logo-1">{html_logo1}</div>', unsafe_allow_html=True)

# --- 5. TAMPILAN STICKY HEADER LOGO 2 ---
rasio = min(total_terpilih / max_foto, 1.0)
st.markdown(
    f"""
<div class="sticky-top-header">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:10px;">
            {html_logo2}
            <div>
                <div style="font-size:1.05rem; font-weight:700;">Fotonic</div>
                <div style="font-size:0.75rem; color:#71717a; margin-top:-2px;">Photo & Video Project</div>
            </div>
        </div>
        <a href="https://instagram.com/fotonicproject" target="_blank" style="text-decoration:none; color:#71717a; font-size:0.8rem; font-weight:500;">Instagram ↗</a>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span style="font-size:0.85rem; font-weight:600;">Klien: {klien}</span>
        <span style="font-size:0.85rem; font-weight:700; color:{'#22c55e' if total_terpilih == max_foto else '#ff4b4b'};">
            {total_terpilih} / {max_foto} Foto
        </span>
    </div>
    <div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 5px;">
        <div style="width: {int(rasio * 100)}%; background-color: {'#22c55e' if total_terpilih == max_foto else '#ff4b4b'}; height: 100%; border-radius: 999px; transition: width 0.3s ease;"></div>
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

# --- 7. TOMBOL SUBMIT (BUBBLE TO FULL) ---
if st.button(f"Kunci & Kirim Pilihan ({total_terpilih}/{max_foto})", type="primary", use_container_width=True):
  if total_terpilih < max_foto:
    st.warning(f"Pilihan belum lengkap. Kurang {max_foto - total_terpilih} foto lagi.")
  else:
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    daftar_file_str = ",\n".join(sorted(list(st.session_state.terpilih)))
    try:
      sheet.append_row([waktu, klien, "Selesai", total_terpilih, daftar_file_str])
      st.success(f"Terima kasih {klien}! Pilihan berhasil dikirim ke Fotonic.")
      st.balloons()
      st.code(daftar_file_str, language="text")
    except Exception as e:
      st.error(f"Gagal mencatat: {e}")

# --- 8. JAVASCRIPT: TRANSISI TOMBOL BERDASARKAN SCROLL ---
components.html("""
<script>
    const parentDoc = window.parent.document;
    const viewContainer = parentDoc.querySelector('.stAppViewContainer');
    const buttonDiv = parentDoc.querySelector('div[data-testid="stButton"]');

    if (buttonDiv) {
        // Atur awal sebagai bubble
        buttonDiv.classList.add('fab-mode');

        function updateScroll() {
            const scrollPos = viewContainer.scrollTop;
            const maxScroll = viewContainer.scrollHeight - viewContainer.clientHeight;
            
            // Jika sisa scroll ke bawah kurang dari 120px (sudah mentok)
            if (maxScroll - scrollPos < 120) {
                buttonDiv.classList.add('full-mode');
                buttonDiv.classList.remove('fab-mode');
            } else {
                buttonDiv.classList.add('fab-mode');
                buttonDiv.classList.remove('full-mode');
            }
        }
        
        viewContainer.addEventListener('scroll', updateScroll);
        setTimeout(updateScroll, 500); // Trigger saat pertama dimuat
    }
</script>
""", height=0)
