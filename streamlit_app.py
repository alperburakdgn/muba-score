import streamlit as st

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Lig ve Takım Yönetimi",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS Styles
enhanced_css = """
<style>
/* Genel arkaplan */
.stApp {
    background: linear-gradient(to bottom, #2a5298, #1e3c72);
    color: #ffffff;
    font-family: 'Poppins', sans-serif;
}

/* Başlıklar */
h1, h2 {
    color: #ffffff;
    text-align: center;
    font-weight: 600;
    margin-bottom: 20px;
}
h1 {
    font-size: 3rem;
}
h2 {
    font-size: 2rem;
}

/* Butonlar */
.stButton>button {
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #388e3c;
    transform: scale(1.1);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #212121;
    color: white;
    border-right: 2px solid #4caf50;
    padding: 10px;
}
section[data-testid="stSidebar"] h2 {
    color: #4caf50;
    font-size: 1.5rem;
}

/* Metin kutuları */
.stTextInput>div>div>input {
    background-color: #ffffff;
    border: 2px solid #4caf50;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    color: #000000;
}
</style>
"""

# Inject the CSS styles into the Streamlit app
st.markdown(enhanced_css, unsafe_allow_html=True)

# Original Streamlit app code below (without changes to logic)
import streamlit as st
import mysql.connector
from get_data import *
# Sayfa genişlik ayarı


# CSS: Modern görünüm için stiller
st.markdown("""
    <style>
    /* Genel arkaplan */
    .stApp {
        background: linear-gradient(to bottom right, #2c3e50, #4ca1af);
        color: white;
        font-family: 'Roboto', sans-serif;
    }

    /* Başlıklar */
    h1 {
        color: white;
        font-size: 2.8rem;
        text-align: center;
        font-weight: 700;
        margin-bottom: 20px;
    }
    h2 {
        color: #f8f9fa;
        font-size: 1.5rem;
        text-align: center;
        font-weight: 400;
    }

    /* Butonlar */
    .stButton>button {
        background-color: #4ca1af;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2c3e50;
        transform: scale(1.05);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #2c3e50;
        color: white;
    }
    section[data-testid="stSidebar"] h2 {
        color: white;
    }

    /* Metin kutuları */
    .stTextInput>div>div>input {
        background-color: #f8f9fa;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Ayarları
if "page" not in st.session_state:
    st.session_state.page = "home"

# Sidebar - Geri Butonu ve Ana Sayfaya Dön
# Sidebar - Takım Arama Özelliği
# Sidebar - Takım Arama Özelliği
# Sidebar - Geri Butonu, Ana Sayfaya Dön ve Oyuncu Arama
def sidebar_navigation():
    # Ana Sayfaya Dön Butonu
    if st.session_state.page != "home":
        if st.sidebar.button("Ana Sayfaya Dön"):
            st.session_state.page = "home"
            st.session_state.team_search_results = []  # Ana sayfaya dönüldüğünde sıfırla

    # Geri Butonu
    if st.session_state.page not in ["home", "league_selection", "team_search"]:
        if st.sidebar.button("Geri"):
            if st.session_state.page == "teams":
                st.session_state.page = "league_selection"
            elif st.session_state.page == "team_details":
                st.session_state.page = "teams"
            elif st.session_state.page in ["players", "fixtures"]:
                st.session_state.page = "team_details"
            st.session_state.team_search_results = []  # Geri gidildiğinde sıfırla

    # Oyuncu Arama Butonu
    if st.sidebar.button("Oyuncu Ara"):
        st.session_state.page = "player_search"

    # Takım Arama Butonu
    if st.sidebar.button("Takım Ara"):
        st.session_state.page = "team_search"
        st.session_state.team_search_results = []  # Yeni arama sayfasına geçerken sıfırla




# Sayfa Değiştirme
sidebar_navigation()

# Ana Sayfa
if st.session_state.page == "home":
    col1, col2, col3 = st.columns([1, 2, 1])  # Orta sütun için düzenleme
    with col2:
        st.markdown('<h1>🏆 Lig ve Takım Yönetimi</h1>', unsafe_allow_html=True)
        st.markdown('<h2>Ligleri, takımları ve oyuncuları keşfedin!</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 30px; text-align: center;">
            <p style="font-size: 1.2rem;">
            - Ligleri keşfedebilir,<br>
            - Takımları görüntüleyebilir,<br>
            - Oyuncuları arayabilirsiniz.<br><br>
            <strong>Başlamak için Lig Seç!</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Modern buton
        if st.button("Lig Seç", key="lig_sec"):
            st.session_state.page = "league_selection"

# Lig Seçim Sayfası
if st.session_state.page == "league_selection":
    st.markdown('<h1>🏆 Lig Seçimi</h1>', unsafe_allow_html=True)
    leagues = get_leagues()
    if leagues:
        st.write("<p style='text-align:center;'>Bir lig seçmek için aşağıdaki butonlara tıklayın:</p>", unsafe_allow_html=True)
        cols = st.columns(3)  # 3 sütun düzeni
        for i, league in enumerate(leagues):
            with cols[i % 3]:
                st.button(
                    league[1],
                    key=f"league_{league[0]}",
                    on_click=lambda league=league: select_league(league)
                )
    else:
        st.error("Lig verisi alınamadı. Veritabanı bağlantısını kontrol edin.")

def select_league(lig):
    st.session_state.page = "teams"
    st.session_state.selected_league = lig[0]
    st.session_state.selected_league_name = lig[1]

# Takım Seçim Sayfası
if st.session_state.page == "teams":
    st.markdown(f'<h1>{st.session_state.selected_league_name} Takımları</h1>', unsafe_allow_html=True)
    teams = get_teams_by_league(st.session_state.selected_league)
    if teams:
        st.write("<p>Bir takım seçmek için aşağıdaki butonlara tıklayın:</p>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, team in enumerate(teams):
            with cols[i % 3]:
                st.button(
                    team[1],
                    key=f"team_{team[0]}",
                    on_click=lambda team=team: select_team(team)
                )
    else:
        st.warning("Bu lige ait takım bilgisi bulunamadı.")

def select_team(team):
    st.session_state.page = "team_details"
    st.session_state.selected_team = team[0]
    st.session_state.selected_team_name = team[1]

# Takım Detay Sayfası
if st.session_state.page == "team_details":
    # Takım stadyum ve antrenör bilgilerini al
    team_details = get_team_details(st.session_state.selected_team)
    stadium_name, coach_name = team_details

    st.markdown(f'<h1>{st.session_state.selected_team_name} Takım Detayları</h1>', unsafe_allow_html=True)

    # Stadyum ve antrenör bilgilerini göster
    col1, col2 = st.columns(2)
    with col1:
        # Stadyum görünürlük durumunu kontrol et
        if "stadium_info_visible" not in st.session_state:
            st.session_state["stadium_info_visible"] = False

        # Stadyum butonuna tıklama ile görünürlük durumunu değiştir
        if st.button(f"🏟️ Stadyum: {stadium_name}", key="stadium_info"):
            st.session_state["stadium_info_visible"] = not st.session_state["stadium_info_visible"]

        # Eğer görünürlük durumu True ise kapasite ve konum bilgilerini göster
        if st.session_state["stadium_info_visible"]:
            stadium_details = get_stadium_details(st.session_state.selected_team)
            st.markdown("### Stadyum Detayları:")
            st.write(f"- **Kapasite**: {stadium_details[1]}")
            st.write(f"- **Konum**: {stadium_details[2]}")

    with col2:
        st.markdown(f"### 🧑‍🏫 Antrenör: {coach_name}")

    # Oyuncular ve fikstür butonları
    cols = st.columns(2)
    with cols[0]:
        if st.button("Oyuncular"):
            st.session_state.page = "players"
    with cols[1]:
        if st.button("Fikstür"):
            st.session_state.page = "fixtures"
            
    #gelen giden transfer
    cols = st.columns(2)
    with cols[0]:
        if st.button("Gelen Transfer"):
            st.session_state.page = "gelen_transfer"
    with cols[1]:
        if st.button("Giden Transfer"):
            st.session_state.page = "giden_transfer"





if st.session_state.page == "players":
    st.markdown(f'<h1>{st.session_state.selected_team_name} Oyuncu Kadrosu</h1>', unsafe_allow_html=True)
    players = get_players_by_team(st.session_state.selected_team)
    
    if players:
        for player in players:
            # Oyuncu bilgilerini göster
            st.subheader(f"{player[1]} {player[2]}")  # Ad ve Soyad
            st.write(f"Pozisyon: {player[3]}")  # Pozisyon
            st.write(f"Yaş: {player[4]}")  # Yaş
            st.write(f"Uyruğu: {player[5]}")  # Uyruğu

            # İstatistikler butonu
            if st.button(f"İstatistikler ({player[1]} {player[2]})", key=f"stats_{player[0]}"):
                # Oyuncu istatistiklerini çek
                statistics = get_player_statistics(player[0])  # player_id'yi kullanarak istatistikleri çek
                if statistics:
                    st.write(f"**{player[1]} {player[2]} İstatistikleri:**")
                    for stat in statistics:
                        st.write(f"Sezon: {stat[5]}")
                        st.write(f"Goller: {stat[0]}, Asistler: {stat[1]}, Sarı Kartlar: {stat[2]}, Kırmızı Kartlar: {stat[3]}")
                        st.write(f"Oynanan Dakika: {stat[4]}")
                        st.write("---")
                else:
                    st.warning(f"{player[1]} {player[2]} için istatistik bulunamadı.")
            st.write("---")
    else:
        st.warning("Bu takıma ait oyuncu bilgisi bulunamadı.")


if st.session_state.page == "player_search":
    st.markdown('<h1>Oyuncu Arama</h1>', unsafe_allow_html=True)

    # Girdileri ve sonuçları saklamak için session_state başlatma
    if "search_first_name" not in st.session_state:
        st.session_state.search_first_name = ""
    if "search_last_name" not in st.session_state:
        st.session_state.search_last_name = ""
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "expanded_stats" not in st.session_state:
        st.session_state.expanded_stats = {}  # Her oyuncu için istatistik durumu

    # Oyuncu adı ve soyadı giriş kutuları
    first_name = st.text_input("Oyuncunun Adı:", value=st.session_state.search_first_name)
    last_name = st.text_input("Oyuncunun Soyadı:", value=st.session_state.search_last_name)

    # Arama butonuna basıldığında girişleri ve sonuçları kaydet
    if st.button("Ara"):
        st.session_state.search_first_name = first_name
        st.session_state.search_last_name = last_name
        st.session_state.search_results = search_players_by_name(first_name, last_name)
        st.session_state.expanded_stats = {}  # Yeni bir aramada tüm istatistik durumlarını sıfırla

    # Arama sonuçlarını göster
    if st.session_state.search_results:
        st.write(f"**{len(st.session_state.search_results)} sonuç bulundu:**")
        for player in st.session_state.search_results:
            # Oyuncu bilgilerini göster
            st.subheader(f"{player[1]} {player[2]}")  # Ad ve Soyad
            st.write(f"Pozisyon: {player[3]}")
            st.write(f"Yaş: {player[4]}")
            st.write(f"Uyruğu: {player[5]}")
            st.write(f"Takım: {player[6] if player[6] else 'Takım bilgisi yok'}")

            # İstatistikler butonu
            if st.button(f"İstatistikler ({player[1]} {player[2]})", key=f"stats_button_{player[0]}"):
                # İstatistiklerin gösterim durumunu tersine çevir
                if player[0] in st.session_state.expanded_stats:
                    st.session_state.expanded_stats[player[0]] = not st.session_state.expanded_stats[player[0]]
                else:
                    st.session_state.expanded_stats[player[0]] = True

            # Eğer bu oyuncunun istatistikleri gösterilmek isteniyorsa
            if player[0] in st.session_state.expanded_stats and st.session_state.expanded_stats[player[0]]:
                statistics = get_player_statistics(player[0])  # İstatistikleri çek
                if statistics:
                    st.write(f"**{player[1]} {player[2]} İstatistikleri:**")
                    for stat in statistics:
                        st.write(f"Sezon: {stat[5]}")
                        st.write(f"Goller: {stat[0]}, Asistler: {stat[1]}, Sarı Kartlar: {stat[2]}, Kırmızı Kartlar: {stat[3]}")
                        st.write(f"Oynanan Dakika: {stat[4]}")
                        st.write("---")
                else:
                    st.warning(f"{player[1]} {player[2]} için istatistik bulunamadı.")
            st.write("---")
    else:
        st.warning("Hiçbir sonuç bulunamadı.")

# Takım Arama Sayfası
if st.session_state.page == "team_search":
    st.markdown('<h1>Takım Arama</h1>', unsafe_allow_html=True)

    # Kullanıcıdan takım adı alma
    team_name = st.text_input("Takım Adı:")
    if st.button("Ara"):
        if team_name:
            search_results = search_team_by_name(team_name)  # Veritabanı arama fonksiyonu
            if search_results:
                st.session_state.team_search_results = search_results
            else:
                st.session_state.team_search_results = []  # Sonuç bulunamazsa sıfırla
                st.warning("Aradığınız takıma ait sonuç bulunamadı.")

    # Takım arama sonuçlarını göster
    if "team_search_results" in st.session_state and st.session_state.team_search_results:
        st.markdown('<h2>Arama Sonuçları:</h2>', unsafe_allow_html=True)
        for team in st.session_state.team_search_results:
            if st.button(f"{team[1]}", key=f"team_{team[0]}"):
                st.session_state.page = "team_details"
                st.session_state.selected_team = team[0]
                st.session_state.selected_team_name = team[1]
    else:
        st.session_state.team_search_results = []  # Arama sonuçları sayfa terk edildiğinde sıfırlanır

if st.session_state.page == "gelen_transfer":
    st.markdown(f'<h1>{st.session_state.selected_team_name} Gelen Transferler</h1>', unsafe_allow_html=True)
    print("teamid : ", st.session_state.selected_team)
    gelen_transfer = get_gelen_transfers_by_team(st.session_state.selected_team)
    players = []
    print ("Gelen :", gelen_transfer) 
    for player in gelen_transfer:
        print ("Player:", player) 
        player_info = (get_player_information_by_player_id(player[1])+ [str(player[2]), str(player[3]), str(player[4]), str(player[5])])
        players.append(player_info)
    print ("Players:", players) 
    if players:
        for player in players:
            # Oyuncu bilgilerini göster
            st.subheader(f"{player[0][1]} {player[0][2]}")  # Ad ve Soyad
            st.write(f"Pozisyon: {player[0][3]}")  # Pozisyon
            st.write(f"Yaş: {player[0][4]}")  # Yaş
            st.write(f"Uyruğu: {player[0][5]}")  # Uyruğu
            st.write(f"Transfer Tarihi: {player[1]}")  
            st.write(f"Transfer Fee: {player[2]}")
            st.write(f"Transfer from: {player[3]}")
            st.write(f"Transfer to: {player[4]}")
            # İstatistikler butonu
            if st.button(f"İstatistikler ({player[0][1]} {player[0][2]})", key=f"stats_{player[0][0]}"):
                # Oyuncu istatistiklerini çek
                statistics = get_player_statistics(player[0][0])  # player_id'yi kullanarak istatistikleri çek
                if statistics:
                    st.write(f"**{player[0][1]} {player[0][2]} İstatistikleri:**")
                    for stat in statistics:
                        st.write(f"Sezon: {stat[5]}")
                        st.write(f"Goller: {stat[0]}, Asistler: {stat[1]}, Sarı Kartlar: {stat[2]}, Kırmızı Kartlar: {stat[3]}")
                        st.write(f"Oynanan Dakika: {stat[4]}")
                        st.write("---")
                else:
                    st.warning(f"{player[0][1]} {player[2]} için istatistik bulunamadı.")
            st.write("---")
    else:
        st.warning("Bu takıma ait oyuncu bilgisi bulunamadı.")
        
if st.session_state.page == "giden_transfer":
    st.markdown(f'<h1>{st.session_state.selected_team_name} Giden Transferler</h1>', unsafe_allow_html=True)
    print("teamid : ", st.session_state.selected_team)
    giden_transfer = get_giden_transfers_by_team(st.session_state.selected_team)
    players = []
    print ("giden :", giden_transfer) 
    for player in giden_transfer:
        print ("Player:", player) 
        player_info = (get_player_information_by_player_id(player[1])+ [str(player[2]), str(player[3]), str(player[4]), str(player[5])])
        players.append(player_info)

    print ("Players:", players) 
    if players:
        for player in players:
            # Oyuncu bilgilerini göster
            st.subheader(f"{player[0][1]} {player[0][2]}")  # Ad ve Soyad
            st.write(f"Pozisyon: {player[0][3]}")  # Pozisyon
            st.write(f"Yaş: {player[0][4]}")  # Yaş
            st.write(f"Uyruğu: {player[0][5]}")  # Uyruğu
            st.write(f"Transfer Tarihi: {player[1]}")  
            st.write(f"Transfer Fee: {player[2]}")
            st.write(f"Transfer from: {player[3]}")
            st.write(f"Transfer to: {player[4]}")
            # İstatistikler butonu
            if st.button(f"İstatistikler ({player[0][1]} {player[0][2]})", key=f"stats_{player[0][0]}"):
                # Oyuncu istatistiklerini çek
                statistics = get_player_statistics(player[0][0])  # player_id'yi kullanarak istatistikleri çek
                if statistics:
                    st.write(f"**{player[0][1]} {player[0][2]} İstatistikleri:**")
                    for stat in statistics:
                        st.write(f"Sezon: {stat[5]}")
                        st.write(f"Goller: {stat[0]}, Asistler: {stat[1]}, Sarı Kartlar: {stat[2]}, Kırmızı Kartlar: {stat[3]}")
                        st.write(f"Oynanan Dakika: {stat[4]}")
                        st.write("---")
                else:
                    st.warning(f"{player[0][1]} {player[2]} için istatistik bulunamadı.")
            st.write("---")
    else:
        st.warning("Bu takıma ait oyuncu bilgisi bulunamadı.")

