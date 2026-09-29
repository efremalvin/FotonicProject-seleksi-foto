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

# --- 2. CSS STYLING & FLOATING CONTROLS ---
st.markdown(
    """
<style>
    /* Hilangkan header default streamlit */
    header[data-testid="stHeader"] {display: none !important;}
    
    /* Beri ruang atas dan bawah agar konten tidak tertutup fixed bar */
    .block-container {
        padding-top: 5.5rem !important;
        padding-bottom: 7.5rem !important;
        max-width: 1200px;
    }

    /* Fixed Top Sticky Progress Bar */
    .fixed-top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 99999;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        padding: 10px 20px;
    }

    @media (prefers-color-scheme: dark) {
        .fixed-top-bar {
            background: rgba(14, 17, 23, 0.95);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }
    }

    .brand-title {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    
    .social-links a {
        text-decoration: none;
        color: #71717a;
        font-size: 0.8rem;
        margin-left: 10px;
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
        background: rgba(125, 125, 125, 0.06);
        padding: 8px 12px;
        border-radius: 0 0 8px 8px;
        margin-top: -3px !important;
        margin-bottom: 16px !important;
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

    /* Floating Navigation Scroll Buttons */
    .scroll-nav-container {
        position: fixed;
        bottom: 85px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        z-index: 99998;
    }
    .scroll-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 1.1rem;
        transition: transform 0.2s, background 0.2s;
    }
    .scroll-btn:hover {
        transform: scale(1.08);
        background: #ffffff;
    }
    @media (prefers-color-scheme: dark) {
        .scroll-btn {
            background: rgba(30, 35, 45, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
        }
        .scroll-btn:hover {
            background: rgba(45, 50, 65, 1);
        }
    }

    /* Floating Bottom Action Bar */
    .floating-bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 99997;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        padding: 12px 20px;
        display: flex;
        justify-content: center;
    }
    @media (prefers-color-scheme: dark) {
        .floating-bottom-bar {
            background: rgba(14, 17, 23, 0.95);
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
rasio = min(total_terpilih / max_foto, 1.0)
sisa = max_foto - total_terpilih
status_teks = (
    f"Sisa {sisa} foto lagi"
    if sisa > 0
    else "Kuota pas! Siap untuk dikonfirmasi."
)
color_accent = "#22c55e" if total_terpilih == max_foto else "#ff4b4b"

# --- 7. FIXED TOP STICKY BAR (PROGRES + IDENTITAS + SOSMED) ---
st.markdown(
    f"""
<div class="fixed-top-bar">
    <div style="max-width:1200px; margin:0 auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <div>
                <span class="brand-title">📷 Fotonic</span>
                <span style="font-size:0.75rem; color:#71717a; margin-left:6px;">| {klien}</span>
            </div>
            <div class="social-links">
                <a href="https://instagram.com/fotonicproject" target="_blank">Instagram ↗</a>
                <a href="https://wa.me/6281234567890" target="_blank">WhatsApp ↗</a>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem; font-weight:600; margin-bottom:4px;">
            <span style="color:#71717a; font-weight:500;">{status_teks}</span>
            <span style="color:{color_accent};">{total_terpilih} / {max_foto} Foto</span>
        </div>
        <div style="width: 100%; background-color: rgba(125,125,125,0.2); border-radius: 999px; height: 5px; overflow: hidden;">
            <div style="width: {int(rasio * 100)}%; background-color: {color_accent}; height: 100%; transition: width 0.3s ease;"></div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 8. FLOATING INTERACTIVE SCROLL BUTTONS (JAVASCRIPT) ---
components.html(
    """
    <div style="position: fixed; bottom: 85px; right: 20px; display: flex; flex-direction: column; gap: 8px; z-index: 999999;">
        <button onclick="window.parent.scrollTo({top: 0, behavior: 'smooth'});" 
                title="Gulir ke Atas"
                style="width: 42px; height: 42px; border-radius: 50%; background: #ffffff; border: 1px solid rgba(0,0,0,0.15); box-shadow: 0 4px 12px rgba(0,0,0,0.15); cursor: pointer; font-size: 1.1rem; display: flex; align-items: center; justify-content: center;">
            ▲
        </button>
        <button onclick="window.parent.scrollTo({top: window.parent.document.body.scrollHeight, behavior: 'smooth'});" 
                title="Gulir ke Tombol Konfirmasi"
                style="width: 42px; height: 42px; border-radius: 50%; background: #ffffff; border: 1px solid rgba(0,0,0,0.15); box-shadow: 0 4px 12px rgba(0,0,0,0.15); cursor: pointer; font-size: 1.1rem; display: flex; align-items: center; justify-content: center;">
            ▼
        </button>
    </div>
    """,
    height=0,
)

# --- 9. GRID GALERI FOTO ---
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

# --- 10. TOMBOL KONFIRMASI AKHIR ---
submit_clicked = st.button(
    f"Kunci & Kirim Pilihan ({total_terpilih}/{max_foto})",
    type="primary",
    use_container_width=True,
)

if submit_clicked:
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
