import streamlit as st
import requests

# --- Sayfa ayarları ---
st.set_page_config(page_title="Kripto Çevirici", page_icon="🪙")
st.title("🪙 Kripto Para Çevirici")
st.write("Kraken Convert benzeri basit bir çevirici. Örnek: 50 ETH kaç BTC?")

# --- API'den verileri çekelim (senin kodundaki mantıkla aynı) ---
r = requests.get("https://api.coinlore.net/api/tickers/")
kod = r.status_code

if kod == 200:
    veri = r.json()
    veri = veri.get('data')

    # Coin isimlerini ve dolar fiyatlarını bir sözlükte tutalım
    # örnek: fiyatlar["ETH - Ethereum"] = 4600.50
    fiyatlar = {}
    semboller = {}

    for coin in veri:
        isim = coin.get('symbol') + " - " + coin.get('name')
        fiyat = float(coin.get('price_usd'))
        fiyatlar[isim] = fiyat
        semboller[isim] = coin.get('symbol')

    coin_listesi = list(fiyatlar.keys())

    # --- Kullanıcıdan girişleri alalım ---
    # st.columns(2) ekranı yan yana 2 kolona böler (Kraken'daki gibi)
    col1, col2 = st.columns(2)

    with col1:
        kaynak = st.selectbox("Bu coinden", coin_listesi, index=1)   # index=1 -> Ethereum
        miktar = st.number_input("Miktar", min_value=0.0, value=50.0)

    with col2:
        hedef = st.selectbox("Bu coine", coin_listesi, index=0)      # index=0 -> Bitcoin

    # --- Çevir butonu ---
    if st.button("Çevir 🔄"):
        kaynak_fiyat = fiyatlar[kaynak]   # 1 kaynak coin kaç dolar
        hedef_fiyat = fiyatlar[hedef]     # 1 hedef coin kaç dolar

        dolar_degeri = miktar * kaynak_fiyat
        sonuc = dolar_degeri / hedef_fiyat

        st.success(str(miktar) + " " + semboller[kaynak] + " = " + f"{sonuc:.8f}" + " " + semboller[hedef])
        st.info("Dolar karşılığı: $" + f"{dolar_degeri:,.2f}")

        # Birim kuru da gösterelim (Kraken'daki gibi)
        birim_kur = kaynak_fiyat / hedef_fiyat
        st.write("1", semboller[kaynak], "=", f"{birim_kur:.8f}", semboller[hedef])

else:
    st.error("API'ye ulaşılamadı, hata kodu: " + str(kod))