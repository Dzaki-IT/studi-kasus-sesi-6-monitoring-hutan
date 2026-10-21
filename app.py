import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

st.set_page_config(page_title="Forest Change Monitor", page_icon="🌳", layout="wide")
DATA = Path(__file__).parent / "data" / "land_change_samples.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

df = load_data()
st.title("🌳 Forest Change Monitor")
st.caption("Demo klasifikasi indikasi perubahan tutupan lahan dari fitur numerik.")
st.warning("Dataset ini sintetis untuk pembelajaran. Ini bukan citra satelit asli, bukan laporan deforestasi resmi, dan bukan bukti penyebab pembukaan lahan.")

with st.sidebar:
    st.header("Filter eksplorasi")
    zones = st.multiselect("Pilih zona", sorted(df["zone"].unique()), default=sorted(df["zone"].unique()))
    drop_threshold = st.slider("Penurunan NDVI minimum", 0.0, 0.4, 0.10, 0.01)

filtered = df[(df["zone"].isin(zones)) & (df["ndvi_drop"] >= drop_threshold)]
c1, c2, c3 = st.columns(3)
c1.metric("Sampel terpilih", len(filtered))
c2.metric("Indikasi perubahan", int((filtered["label"] == "Pembukaan lahan").sum()))
c3.metric("Rata-rata penurunan NDVI", f"{filtered['ndvi_drop'].mean():.2f}" if len(filtered) else "—")

left, right = st.columns(2)
with left:
    st.subheader("NDVI sebelum dan sesudah")
    plot_df = filtered.melt(id_vars=["tile_id","zone"], value_vars=["ndvi_before","ndvi_after"],
                            var_name="periode", value_name="ndvi")
    fig = px.box(plot_df, x="periode", y="ndvi", color="periode", points="all",
                 hover_data=["tile_id","zone"], labels={"periode":"Periode","ndvi":"Nilai NDVI"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Sampel berdasarkan zona")
    zone_counts = filtered.groupby(["zone","label"]).size().reset_index(name="jumlah")
    fig2 = px.bar(zone_counts, x="zone", y="jumlah", color="label", barmode="group",
                  labels={"zone":"Zona","jumlah":"Jumlah sampel","label":"Label contoh"})
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Titik sampel (koordinat contoh)")
if len(filtered):
    map_fig = px.scatter_mapbox(filtered, lat="latitude", lon="longitude", color="label",
                                hover_name="tile_id", hover_data=["zone","ndvi_drop"],
                                zoom=7, height=420)
    map_fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(map_fig, use_container_width=True)
else:
    st.info("Tidak ada sampel yang sesuai filter.")

st.subheader("Model klasifikasi demonstrasi")
features = ["ndvi_before","ndvi_after","ndvi_drop","bare_soil_change","burn_index_change"]
X, y = df[features], df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
st.write(f"**Akurasi pada test split:** {accuracy_score(y_test, pred):.2f}")
st.caption("Angka evaluasi hanya menggambarkan dataset sintetis kecil ini. Jangan menganggapnya sebagai akurasi model untuk hutan nyata.")
cm = confusion_matrix(y_test, pred, labels=["Stabil","Pembukaan lahan"])
cm_df = pd.DataFrame(cm, index=["Aktual: Stabil","Aktual: Pembukaan lahan"],
                     columns=["Prediksi: Stabil","Prediksi: Pembukaan lahan"])
st.dataframe(cm_df, use_container_width=True)
with st.expander("Lihat classification report"):
    st.code(classification_report(y_test, pred, zero_division=0))

st.subheader("Data hasil filter")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Unduh sampel hasil filter (CSV)", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="sampel_perubahan_lahan.csv", mime="text/csv")
st.markdown("""
### Catatan interpretasi
- Penurunan NDVI dapat menjadi sinyal perubahan vegetasi, tetapi juga bisa dipengaruhi musim, awan, kualitas citra, atau kondisi tanah.
- Klasifikasi harus divalidasi dengan citra asli, data referensi berlabel, peninjauan ahli, dan bila memungkinkan verifikasi lapangan.
- Model tidak menetapkan siapa yang bertanggung jawab atau penyebab langsung perubahan lahan.
""")
