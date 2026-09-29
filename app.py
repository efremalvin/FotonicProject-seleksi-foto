from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
import streamlit as st

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Fotonic - Seleksi Foto",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. CSS STYLING (FIXED HEADER, BOTTOM CONFIRM, & ALL-ROUND CARDS) ---
st.markdown(
    """
<style>
    /* Sembunyikan elemen bawaan Streamlit */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Ruang kosong atas dan bawah agar konten foto tidak tertutup bar melayang */
    .block-container {
        padding-top: 140px !important;
        padding-bottom: 110px !important;
        max-width: 1200px !important;
    }

    /* 1. STICKY / FIXED TOP HEADER (MELAYANG TETAP DI ATAS) */
    .fixed-top-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        z-index: 99999 !important;
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 12px 24px !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
    }
    
    @media (prefers-color-scheme: dark) {
        .fixed-top-header {
            background: rgba(18, 18, 20, 0.96) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
        }
    }

    .header-inner {
        max-width: 1150px;
        margin: 0 auto;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .brand-sub {
        font-size: 0.75rem;
        color: #71717a;
    }
    .social-links a {
        text-decoration: none;
        color: #71717a;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 12px;
        transition: color 0.2s ease;
    }
    .social-links a:hover {
        color: #ff4b4b;
    }

    /* 2. SCROLL INTERAKTIF DI SISI KANAN (TEBAL & MUDAH DISERET) */
    ::-webkit-scrollbar {
        width: 12px !important;
        display: block !important;
    }
    ::-webkit-scrollbar-track {
        background: rgba(125, 125, 125, 0.08) !important;
        border-left: 1px solid rgba(125, 125, 125, 0.1) !important;
    }
    ::-webkit-scrollbar-thumb {
        background: #ff4b4b !important;
        border-radius: 8px !important;
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #dc2626 !important;
    }
    @media (prefers-color-scheme: dark) {
        ::-webkit-scrollbar-thumb {
            border: 2px solid rgba(18, 18, 20, 0.9) !important;
        }
    }

    /* 3. KARTU FOTO ALL-ROUND & MERAPATKAN CELAH NAMA + CHECKBOX */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(125, 125, 125, 0.2) !important;
        background: rgba(125, 125, 125, 0.03) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 16px !important;
        padding: 0 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 0px !important;
        gap: 0px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] img {
        border-radius: 16px 16px 0 0 !important;
        display: block !important;
        width: 100% !important;
        object-fit: cover !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {
        padding: 8px 12px !important;
        margin: 0px !important;
        border-top: 1px solid rgba(125, 125, 125, 0.12) !important;
        background: rgba(125, 125, 125, 0.04) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label {
        gap: 8px !important;
        display: flex !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] label p {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        margin: 0 !important;
    }

    /* 4. FIXED BOTTOM BAR (TOMBOL KONFIRMASI MELAYANG DI BAWAH) */
    div[data-testid="stAppViewContainer"] .stButton {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        z-index: 99998 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 12px 20px !important;
        border-top: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.05) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    @media (prefers-color-scheme: dark) {
        div[data-testid="stAppViewContainer"] .stButton {
            background: rgba(18, 18, 20, 0.95) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.35) !important;
        }
    }
    div[data-testid="stAppViewContainer"] .stButton > button {
        max-width: 600px !important;
        width: 100% !important;
        margin: 0 auto !important;
        height: 46px !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. PARAMETER URL ---
query_params = st.query_params.to_dict()
klien = query_params.get("klien", "Klien Fotonic")
folder_id = query_params.get("folder_id", None)

try:
  max_foto = int(query_params.get("max", 15))
except (ValueError, TypeError):
  max_foto = 15

if not folder_id:
  st.warning("⚠️ Tautan belum menyertakan `folder_id` Google Drive.")
  st.stop()


# --- 4. OTENTIKASI KE GOOGLE DRIVE & SHEETS ---
@st.cache_resource
def init_google_apis():
  creds_dict = st.secrets["gcp_service_account"]
  creds = service_account.Credentials.from_service_account_info(
      creds_dict,
      scopes=[
          "https://www.googleapis.com/auth/drive.readonly",
          "https://www.googleapis.com/auth/spreadsheets",
      ],
  )
  drive_service = build("drive", "v3", credentials=creds)
  gc = gspread.authorize(creds)
  return drive_service, gc


try:
  drive_service, gc = init_google_apis()
  sheet = gc.open("Rekap_Seleksi_Foto").sheet1
except Exception as e:
  st.error(f"Gagal menghubungkan sistem ke Google Sheets: {e}")
  st.stop()


# --- 5. AMBIL DATA FOTO DARI DRIVE ---
@st.cache_data(ttl=300)
def get_photos(f_id):
  query = f"'{f_id}' in parents and mimeType contains 'image/' and trashed = false"
  results = (
      drive_service.files()
      .list(
          q=query,
          fields="files(id, name)",
          pageSize=500,
          orderBy="name",
      )
      .execute()
  )
  return results.get("files", [])


photos = get_photos(folder_id)

if not photos:
  st.error("Folder foto kosong atau tidak ada foto yang ditemukan.")
  st.stop()

# --- 6. STATE DATA SELEKSI ---
if "terpilih" not in st.session_state:
  st.session_state.terpilih = set()

total_terpilih = len(st.session_state.terpilih)

# --- 7. STICKY TOP HEADER HTML (BRAND, SOSMED, & PROGRESS) ---
rasio = min(total_terpilih / max_foto, 1.0)
sisa = max_foto - total_terpilih
status_teks = (
    f"Sisa {sisa} foto lagi"
    if sisa > 0
    else "Kuota pas! Siap dikirim di bagian bawah."
)

st.markdown(
    f"""
<div class="fixed-top-header">
    <div class="header-inner">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div>
                <span class="brand-title">📷 Fotonic</span>
                <span class="brand-sub" style="margin-left:8px;">Photo & Video Project</span>
            </div>
            <div class="social-links">
                <a href="https://instagram.com/fotonicproject" target="_blank">Instagram ↗</a>
                <a href="https://wa.me/6281234567890" target="_blank">WhatsApp ↗</a>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <span style="font-size:0.85rem; font-weight:600;">Klien: {klien}</span>
            <span style="font-size:0.85rem; font-weight:700; color:{'#22c55e' if total_terpilih == max_foto else '#ff4b4b'};">
                {total_terpilih} / {max_foto} Foto
            </span>
        </div>
        <div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 5px; overflow: hidden;">
            <div style="width: {int(rasio * 100)}%; background-color: {'#22c55e' if total_terpilih == max_foto else '#ff4b4b'}; height: 100%; transition: width 0.3s ease;"></div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 8. GRID GALERI FOTO (ALL-ROUND CARDS) ---
kolom = st.columns(3)

for idx, photo in enumerate(photos):
  with kolom[idx % 3]:
    with st.container(border=True):
      img_url = f"https://lh3.googleusercontent.com/d/{photo['id']}"
      file_name = photo["name"]

      st.image(img_url, use_container_width=True)

      is_checked = file_name in st.session_state.terpilih
      is_disabled = (total_terpilih >= max_foto) and not is_checked

      cek = st.checkbox(
          f"{file_name}",
          value=is_checked,
          key=photo["id"],
          disabled=is_disabled,
      )

      if cek and file_name not in st.session_state.terpilih:
        st.session_state.terpilih.add(file_name)
        st.rerun()
      elif not cek and file_name in st.session_state.terpilih:
        st.session_state.terpilih.remove(file_name)
        st.rerun()

# --- 9. TOMBOL SUBMIT (FIXED BOTTOM BAR) ---
if st.button(
    f"Kunci & Kirim Pilihan ({total_terpilih}/{max_foto})",
    type="primary",
    use_container_width=True,
):
  if total_terpilih < max_foto:
    st.warning(
        f"Pilihan Anda belum lengkap. Silakan pilih {max_foto - total_terpilih}"
        " foto lagi."
    )
  else:
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    daftar_file_str = ",\n".join(sorted(list(st.session_state.terpilih)))

    try:
      sheet.append_row(
          [waktu, klien, "Selesai", total_terpilih, daftar_file_str]
      )
      st.success(
          f"Terima kasih {klien}! Pilihan {max_foto} foto berhasil dikirim ke"
          " Fotonic."
      )
      st.balloons()
      st.markdown("### Daftar Foto Terpilih:")
      st.code(daftar_file_str, language="text")
    except Exception as e:
      st.error(f"Gagal mencatat ke Google Sheets: {e}")
