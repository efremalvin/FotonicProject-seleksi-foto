from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
import streamlit as st

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Fotonic - Seleksi Foto Klien",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. CSS STYLING (Sticky Header, Floating Bottom Bar, Minimalist Theme) ---
st.markdown(
    """
<style>
    /* Styling Header & Sosmed */
    .branding-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    .brand-title {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.85rem;
        color: #888;
        margin: 0;
    }
    .social-links a {
        color: #aaa;
        text-decoration: none;
        margin-left: 14px;
        font-size: 0.85rem;
        transition: color 0.2s;
    }
    .social-links a:hover {
        color: #ff4b4b;
    }

    /* Sticky Progress Bar di Atas saat Scroll */
    .sticky-progress-card {
        position: -webkit-sticky;
        position: sticky;
        top: 2.8rem;
        z-index: 999;
        background: rgba(14, 17, 23, 0.92);
        backdrop-filter: blur(10px);
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    
    .progress-text-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        margin-bottom: 0.4rem;
        font-weight: 500;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. AMBIL PARAMETER URL ---
query_params = st.query_params.to_dict()
klien = query_params.get("klien", "Klien Fotonic")
folder_id = query_params.get("folder_id", None)

try:
  max_foto = int(query_params.get("max", 15))
except (ValueError, TypeError):
  max_foto = 15

if not folder_id:
  st.error("⚠️ Tautan tidak lengkap. Parameter folder_id tidak ditemukan.")
  st.stop()


# --- 4. OTENTIKASI KE GOOGLE API ---
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
  st.error(f"Gagal menghubungkan ke database Google: {e}")
  st.stop()


# --- 5. LOAD FOTO DARI GOOGLE DRIVE ---
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
  st.warning(
      "Folder tidak ditemukan atau belum ada foto yang diunggah ke dalamnya."
  )
  st.stop()

# --- 6. LOGIKA DATA SELEKSI ---
if "terpilih" not in st.session_state:
  st.session_state.terpilih = set()

total_terpilih = len(st.session_state.terpilih)

# --- 7. TAMPILAN HEADER BRANDING & SOSMED ---
st.markdown(
    """
<div class="branding-container">
    <div>
        <h1 class="brand-title">FOTONIC</h1>
        <p class="brand-subtitle">PHOTO &amp; VIDEO PROJECT</p>
    </div>
    <div class="social-links">
        <a href="https://instagram.com/username_fotonic" target="_blank">Instagram</a>
        <a href="https://wa.me/6281234567890" target="_blank">WhatsApp</a>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 8. STICKY PROGRESS BAR (MELAYANG DI ATAS SAAT SCROLL) ---
rasio = min(total_terpilih / max_foto, 1.0)
persentase = int(rasio * 100)

st.markdown(
    f"""
<div class="sticky-progress-card">
    <div class="progress-text-row">
        <span>Klien: <b>{klien}</b></span>
        <span>Terpilih: <b>{total_terpilih}</b> / {max_foto} Foto ({persentase}%)</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
st.progress(rasio)

st.write("")  # Spasi pemisah

# --- 9. GALERI GRID RESPONSIF ---
COLS = 3
cols = st.columns(COLS)

for idx, photo in enumerate(photos):
  col = cols[idx % COLS]
  img_url = f"https://lh3.googleusercontent.com/d/{photo['id']}"
  file_name = photo["name"]

  with col:
    st.image(img_url, use_container_width=True)
    is_checked = file_name in st.session_state.terpilih
    is_disabled = (total_terpilih >= max_foto) and not is_checked

    cek = st.checkbox(
        file_name,
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

# --- 10. TOMBOL KONFIRMASI MELEBAR DI BAGIAN BAWAH ---
st.markdown("### Konfirmasi Seleksi")
if total_terpilih < max_foto:
  st.caption(
      f"Lengkapi pilihan Anda ({max_foto - total_terpilih} foto lagi) untuk"
      " mengaktifkan tombol simpan."
  )
else:
  st.caption(
      "Kuota pilihan Anda telah pas 15 foto. Silakan klik tombol di bawah untuk"
      " konfirmasi."
  )

tombol_kirim = st.button(
    "KUNCI & KIRIM PILIHAN FOTO",
    type="primary",
    use_container_width=True,
    disabled=(total_terpilih != max_foto),
)

if tombol_kirim:
  waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  daftar_file_str = ",\n".join(sorted(list(st.session_state.terpilih)))

  try:
    sheet.append_row([waktu, klien, "Selesai", total_terpilih, daftar_file_str])
    st.success(
        f"Terima kasih {klien}! Sebanyak {max_foto} foto pilihan Anda telah"
        " berhasil dikirim ke studio Fotonic."
    )
    st.balloons()
    st.code(daftar_file_str, language="text")
  except Exception as e:
    st.error(f"Gagal mencatat ke database: {e}")
