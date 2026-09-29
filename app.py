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

# --- 2. CSS STYLING (MINIMALIS & RESPONSIVE UX) ---
st.markdown(
    """
<style>
    /* Sembunyikan default header streamlit agar clean */
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 7rem !important;
    }

    /* Top Sticky Bar: Progress Seleksi */
    .sticky-progress-container {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(8px);
        padding: 12px 16px;
        margin-bottom: 20px;
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Support dark mode pada Streamlit */
    @media (prefers-color-scheme: dark) {
        .sticky-progress-container {
            background: rgba(14, 17, 23, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
    }

    .brand-title {
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }
    
    .social-links a {
        text-decoration: none;
        color: #71717a;
        font-size: 0.85rem;
        margin-right: 12px;
        transition: color 0.2s ease;
    }
    .social-links a:hover {
        color: #ff4b4b;
    }

    /* Rapatkan jarak antara gambar dan checkbox */
    div[data-testid="stImage"] {
        margin-bottom: 0px !important;
    }
    div[data-testid="stImage"] img {
        border-radius: 8px 8px 0 0;
        object-fit: cover;
    }
    div[data-testid="stCheckbox"] {
        background: rgba(125, 125, 125, 0.05);
        padding: 6px 10px;
        border-radius: 0 0 8px 8px;
        margin-top: -4px !important;
        margin-bottom: 18px !important;
        border-left: 1px solid rgba(125, 125, 125, 0.15);
        border-right: 1px solid rgba(125, 125, 125, 0.15);
        border-bottom: 1px solid rgba(125, 125, 125, 0.15);
    }
    div[data-testid="stCheckbox"] label p {
        font-size: 0.82rem !important;
        font-weight: 500;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }

    /* Floating Action Bar untuk tombol submit */
    .floating-submit-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 998;
        padding: 14px 20px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(8px);
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        display: flex;
        justify-content: center;
    }
    @media (prefers-color-scheme: dark) {
        .floating-submit-wrapper {
            background: rgba(14, 17, 23, 0.9);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. PARAMETER DARI URL ---
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


# --- 5. AMBIL DATA FOTO ---
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

# --- 7. HEADER BRAND & SOSMED ---
col_logo, col_social = st.columns([2, 1])
with col_logo:
  st.markdown(
      '<div class="brand-title">📷 Fotonic</div><div style="font-size:0.85rem;'
      ' color:#71717a;">Photo & Video Project</div>',
      unsafe_allow_html=True,
  )
with col_social:
  # Ubah tautan sesuai username Instagram & nomor WhatsApp Fotonic
  st.markdown(
      """
    <div class="social-links" style="text-align: right; margin-top: 6px;">
        <a href="https://instagram.com/fotonicproject" target="_blank">Instagram ↗</a>
        <a href="https://wa.me/6281234567890" target="_blank">WhatsApp ↗</a>
    </div>
    """,
      unsafe_allow_html=True,
  )

# --- 8. STICKY PROGRESS BAR ---
rasio = min(total_terpilih / max_foto, 1.0)
sisa = max_foto - total_terpilih
status_teks = (
    f"Sisa {sisa} foto lagi"
    if sisa > 0
    else "Kuota pas! Siap untuk dikonfirmasi."
)

st.markdown(
    f"""
<div class="sticky-progress-container">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span style="font-size:0.88rem; font-weight:600;">Seleksi untuk: {klien}</span>
        <span style="font-size:0.88rem; font-weight:700; color:{'#22c55e' if total_terpilih == max_foto else '#ff4b4b'};">
            {total_terpilih} / {max_foto} Foto
        </span>
    </div>
    <div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 6px; overflow: hidden;">
        <div style="width: {int(rasio * 100)}%; background-color: {'#22c55e' if total_terpilih == max_foto else '#ff4b4b'}; height: 100%; transition: width 0.3s ease;"></div>
    </div>
    <div style="font-size:0.75rem; color:#71717a; margin-top:4px;">{status_teks}</div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 9. GALERI FOTO (GRID 3 KOLOM DESKTOP, RESPONSIF DI HP) ---
kolom = st.columns(3)

for idx, photo in enumerate(photos):
  with kolom[idx % 3]:
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

st.divider()

# --- 10. TOMBOL SUBMIT / KONFIRMASI AKHIR ---
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
          f"Terima kasih {klien}! Pilihan {max_foto} foto berhasil dikonfirmasi"
          " dan dikirim."
      )
      st.balloons()
      st.markdown("### Daftar Foto Terpilih:")
      st.code(daftar_file_str, language="text")
    except Exception as e:
      st.error(f"Gagal mencatat ke sistem Sheets: {e}")
