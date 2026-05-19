import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Имя файла для хранения данных
DB_FILE = "workout_data.json"

# Функция загрузки данных (с автоматическим апгрейдом под историю)
def load_data():
    defaults = {
        "athlete_name": "Enter ur name", # Изменено дефолтное имя
        "bw": 60.0,
        "pulls": 0,
        "weight_pulls": 0,
        "dips": 0,
        "weight_dips": 0,
        "tuck": 0,
        "advanced_tuck": 0,
        "semi_advanced_tuck": 0,
        "muscle_ups": 0,
        "slow_mu": 0,
        "tuck_fl": 0,         
        "adv_tuck_fl": 0,     
        "full_fl": 0          
    }
    
    history = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    for k, v in defaults.items():
                        if k not in data:
                            data[k] = v
                    data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    history = [data]
                elif isinstance(data, list):
                    history = data
                    if history:
                        for k, v in defaults.items():
                            if k not in history[-1]:
                                history[-1][k] = v
            except:
                pass
                
    if not history:
        defaults["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        history = [defaults]
        
    return history

def save_data(history_list):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(history_list, f, indent=4, ensure_ascii=False)

# Инициализация сессии
if "user_history" not in st.session_state:
    st.session_state.user_history = load_data()

current_data = st.session_state.user_history[-1].copy()

st.set_page_config(page_title="Apex Calisthenics Tracker", layout="wide")

# Ранги системы
RANKS = ["Gold (Pre-Int)", "Platinum", "Diamond", "Jade", "Master", "Grandmaster", "Nova", "Astra", "Celestial"]
RANK_COLORS = {
    "Gold (Pre-Int)": "🟨", "Platinum": "🔷", "Diamond": "💎", 
    "Jade": "🟢", "Master": "👑", "Grandmaster": "🔥", 
    "Nova": "🌌", "Astra": "⭐", "Celestial": "👁️"
}

# Метрики для рангов
GOALS = {
    "Pulls": [15, 20, 25, 30],       
    "Weight_Pull": [10, 20, 30, 40], 
    "Muscle_Ups": [1, 3, 5, 10],      
    "Slow_MU": [0, 0, 1, 3],          
    "Dips": [15, 20, 25, 30],        
    "Weight_Dips": [15, 30, 30, 40],   
    "tuck": [10, 15, 20, 25],          
    "advanced_tuck": [5, 8, 12, 15],   
    "semi_advanced_tuck": [5, 8, 12, 15],
    "tuck_fl": [10, 15, 20, 30],
    "adv_tuck_fl": [5, 10, 15, 20],
    "full_fl": [2, 5, 8, 12]
}

def get_rank_idx(val, thresholds):
    for i, t in enumerate(thresholds):
        if val < t:
            return i
    return len(thresholds)

st.title("👁️ APEX ATHLETICS: CALISTHENICS PRO")
st.write("---")

# --- САЙДБАР С КАТАЛОГАМИ РЕКОРДОВ ---
with st.sidebar:
    st.header("⚙️ Ввод данных")
    
    name = st.text_input("Name", value=current_data.get("athlete_name", "Enter ur name"))
    weight = st.number_input("Body Weight (kg)", value=float(current_data.get("bw", 60.0)), step=0.1, format="%.1f")
    
    st.markdown("---")
    st.markdown("### 🗂️ Рекорды")
    
    with st.expander("🔴 КАТАЛОГ: PULL (Тяга)", expanded=False):
        u_pulls = st.number_input("Max Pull-ups", value=int(current_data.get("pulls", 0)))
        u_weight_pull = st.number_input("Max Pull-up Weight (kg)", value=int(current_data.get("weight_pulls", 0)))
        u_muscle_ups = st.number_input("Max Muscle-ups", value=int(current_data.get("muscle_ups", 0)))
        u_mu = st.number_input("Slow Muscle-ups", value=int(current_data.get("slow_mu", 0)))
        
    with st.expander("🔵 КАТАЛОГ: PUSH (Жим)", expanded=False):
        u_dips = st.number_input("Max Dips", value=int(current_data.get("dips", 0)))
        u_weight_dips = st.number_input("Max Dip Weight (kg)", value=int(current_data.get("weight_dips", 0)))
        
    with st.expander("🟢 КАТАЛОГ: STATICS (Статика)", expanded=True):
        st.markdown("**Планш (Planche)**")
        u_tuck = st.number_input("Planche Tuck (sec)", value=int(current_data.get("tuck", 0)))
        u_advanced_tuck = st.number_input("Planche Advanced Tuck (sec)", value=int(current_data.get("advanced_tuck", 0)))
        u_semi_advanced_tuck = st.number_input("Planche Semi-Advanced Tuck (sec)", value=int(current_data.get("semi_advanced_tuck", 0)))
        
        st.markdown("**Передний вис (Front Lever)**")
        u_tuck_fl = st.number_input("Front Lever Tuck (sec)", value=int(current_data.get("tuck_fl", 0)))
        u_adv_tuck_fl = st.number_input("Front Lever Adv Tuck (sec)", value=int(current_data.get("adv_tuck_fl", 0)))
        u_full_fl = st.number_input("Full Front Lever (sec)", value=int(current_data.get("full_fl", 0)))
    
    st.write("")
    if st.button("💾 СОХРАНИТЬ РЕЗУЛЬТАТ", use_container_width=True):
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "athlete_name": name,
            "bw": weight,
            "pulls": u_pulls,
            "weight_pulls": u_weight_pull,
            "dips": u_dips,
            "weight_dips": u_weight_dips,
            "tuck": u_tuck,
            "advanced_tuck": u_advanced_tuck,
            "semi_advanced_tuck": u_semi_advanced_tuck,
            "muscle_ups": u_muscle_ups,
            "slow_mu": u_mu,
            "tuck_fl": u_tuck_fl,
            "adv_tuck_fl": u_adv_tuck_fl,
            "full_fl": u_full_fl
        }
        st.session_state.user_history.append(new_entry)
        save_data(st.session_state.user_history)
        st.success("Новый рекорд успешно записан в историю!")
        st.rerun()

    # СИСТЕМА БЕЙДЖЕЙ
    st.markdown("---")
    st.subheader("🏆 Достижения")
    badges_unlocked = False
    if current_data.get("advanced_tuck", 0) >= 6:
        st.success("⚖️ **Defying Gravity** (6+ сек Adv Tuck)")
        badges_unlocked = True
    if current_data.get("pulls", 0) >= 20:
        st.info("🦍 **Pull-up Beast** (20+ Подтягиваний)")
        badges_unlocked = True
    if current_data.get("muscle_ups", 0) >= 5:
        st.warning("🚀 **Explosive Power** (5+ Выходов)")
        badges_unlocked = True
    if current_data.get("full_fl", 0) >= 5:
        st.error("🦇 **Bat Mode** (5+ сек Full Front Lever)")
        badges_unlocked = True
        
    if not badges_unlocked:
        st.caption("Достигайте результатов, чтобы разблокировать бейджи.")

# --- ГЛАВНЫЙ ЭКРАН: ТРИ ВКЛАДКИ ---
main_tab1, main_tab2, main_tab3 = st.tabs(["🏋️ Текущие показатели", "📈 Аналитика и История", "🌍 Лидерборд"])

with main_tab1:
    categories = {
        "🔴 PULL (Тяга)": {
            "Raw Pull: Подтягивания": {"val": current_data.get("pulls",0), "goals": GOALS["Pulls"], "desc": "Plat: 15 | Diam: 20 | Jade: 25 | Master: 30"},
            "Weighted Pull: Подтягивания с весом": {"val": current_data.get("weight_pulls",0), "goals": GOALS["Weight_Pull"], "desc": "Plat: 10 кг | Diam: 20 кг | Jade: 30 кг | Master: 40 кг"},
            "Dynamic Power: Muscle-up": {"val": current_data.get("muscle_ups",0), "goals": GOALS["Muscle_Ups"], "desc": "Plat: 1 | Diam: 3 | Jade: 5 | Master: 10+"},
            "Dynamic Power: Slow Muscle-up": {"val": current_data.get("slow_mu",0), "goals": GOALS["Slow_MU"], "desc": "Jade: 1 | Master: 3 / Идеал"}
        },
        "🔵 PUSH (Жим)": {
            "Raw Push: Брусья": {"val": current_data.get("dips",0), "goals": GOALS["Dips"], "desc": "Plat: 15 | Diam: 20 | Jade: 25 | Master: 30"},
            "Weighted Push: Брусья с весом": {"val": current_data.get("weight_dips",0), "goals": GOALS["Weight_Dips"], "desc": "Plat: 15 кг | Diam: 30 кг | Jade: 30 кг | Master: 40 кг"}
        },
        "🟢 STATICS (Статика)": {
            "Planche: Tuck": {"val": current_data.get("tuck",0), "goals": GOALS["tuck"], "desc": "Plat: 10с | Diam: 15с | Jade: 20с | Master: 25с+"},
            "Planche: Advanced Tuck": {"val": current_data.get("advanced_tuck",0), "goals": GOALS["advanced_tuck"], "desc": "Plat: 5с | Diam: 8с | Jade: 12с | Master: 15с+"},
            "Planche: Semi-Advanced Tuck": {"val": current_data.get("semi_advanced_tuck",0), "goals": GOALS["semi_advanced_tuck"], "desc": "Plat: 5с | Diam: 8с | Jade: 12с | Master: 15с+"},
            "Front Lever: Tuck": {"val": current_data.get("tuck_fl",0), "goals": GOALS["tuck_fl"], "desc": "Plat: 10с | Diam: 15с | Jade: 20с | Master: 30с+"},
            "Front Lever: Advanced Tuck": {"val": current_data.get("adv_tuck_fl",0), "goals": GOALS["adv_tuck_fl"], "desc": "Plat: 5с | Diam: 10с | Jade: 15с | Master: 20с+"},
            "Front Lever: Full": {"val": current_data.get("full_fl",0), "goals": GOALS["full_fl"], "desc": "Plat: 2с | Diam: 5с | Jade: 8с | Master: 12с+"}
        }
    }

    st.subheader(f"Профиль атлета: {name} ({weight} кг)")

    stat_tabs = st.tabs(list(categories.keys()))
    calculated_indices = []

    for tab, (cat_name, cat_stats) in zip(stat_tabs, categories.items()):
        with tab:
            cols = st.columns(2)  
            for item_idx, (title, data) in enumerate(cat_stats.items()):
                r_idx = get_rank_idx(data["val"], data["goals"])
                calculated_indices.append(r_idx) 
                r_name = RANKS[r_idx]
                
                with cols[item_idx % 2]:
                    st.markdown(f"### {title}")
                    st.markdown(f"**Текущий ранг:** {RANK_COLORS[r_name]} {r_name}")
                    st.caption(f"Требования: {data['desc']}")
                    
                    if r_idx < len(data["goals"]):
                        target = data["goals"][r_idx]
                        prog_val = min(data["val"] / target, 1.0) if target > 0 else 0.0
                        st.progress(prog_val)
                        remains = target - data["val"]
                        st.write(f"До ранга **{RANKS[r_idx+1]}**: **{remains}** ед.")
                    else:
                        st.progress(1.0)
                        st.success("Пиковый ранг!")
                    st.write("")

    st.write("---")
    if calculated_indices:
        overall_idx = min(calculated_indices)
        overall_rank_name = RANKS[overall_idx]
        st.markdown(f"## 🏆 Ваш общий ранг: {RANK_COLORS[overall_rank_name]} {overall_rank_name.upper()}")

with main_tab2:
    st.subheader("Визуализация прогресса 📈")
    # Фильтруем историю только для текущего выбранного пользователя
    user_history = [h for h in st.session_state.user_history if h.get("athlete_name") == name]
    
    if len(user_history) > 0:
        df = pd.DataFrame(user_history)
        
        st.markdown("**База (Динамика)**")
        base_cols = [c for c in ['pulls', 'dips', 'muscle_ups'] if c in df.columns]
        if base_cols:
            st.line_chart(df.set_index('date')[base_cols])
            
        st.markdown("**Статика (Планш и Передний вис)**")
        stat_cols = [c for c in ['advanced_tuck', 'adv_tuck_fl', 'full_fl'] if c in df.columns]
        if stat_cols:
            st.line_chart(df.set_index('date')[stat_cols])

        st.markdown("---")
        st.subheader("История записей 📝")
        st.dataframe(df, use_container_width=True)
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Скачать историю в CSV",
            data=csv_data,
            file_name=f"{name}_calisthenics_history.csv",
            mime="text/csv",
        )
    else:
        st.info("История этого атлета пока пуста. Сохраните первый результат!")

with main_tab3:
    st.subheader("Глобальный Лидерборд 🌍")
    st.write("Сравнение максимальных рекордов всех атлетов в базе данных.")
    
    if len(st.session_state.user_history) > 0:
        # Создаем датафрейм из всей истории
        df_all = pd.DataFrame(st.session_state.user_history)
        
        # Находим максимальные значения для каждого атлета
        best_stats = df_all.groupby('athlete_name').max().reset_index()
        
        # Функция подсчета очков (Apex Score) - сумма всех взятых рангов
        def calculate_apex_score(row):
            score = 0
            score += get_rank_idx(row.get("pulls", 0), GOALS["Pulls"])
            score += get_rank_idx(row.get("weight_pulls", 0), GOALS["Weight_Pull"])
            score += get_rank_idx(row.get("muscle_ups", 0), GOALS["Muscle_Ups"])
            score += get_rank_idx(row.get("slow_mu", 0), GOALS["Slow_MU"])
            score += get_rank_idx(row.get("dips", 0), GOALS["Dips"])
            score += get_rank_idx(row.get("weight_dips", 0), GOALS["Weight_Dips"])
            score += get_rank_idx(row.get("tuck", 0), GOALS["tuck"])
            score += get_rank_idx(row.get("advanced_tuck", 0), GOALS["advanced_tuck"])
            score += get_rank_idx(row.get("semi_advanced_tuck", 0), GOALS["semi_advanced_tuck"])
            score += get_rank_idx(row.get("tuck_fl", 0), GOALS["tuck_fl"])
            score += get_rank_idx(row.get("adv_tuck_fl", 0), GOALS["adv_tuck_fl"])
            score += get_rank_idx(row.get("full_fl", 0), GOALS["full_fl"])
            return score

        best_stats['Apex Score'] = best_stats.apply(calculate_apex_score, axis=1)
        
        # Сортируем по очкам от большего к меньшему
        leaderboard = best_stats.sort_values(by='Apex Score', ascending=False).reset_index(drop=True)
        
        # Оставляем только красивые столбцы для показа
        cols_to_show = {
            'athlete_name': 'Атлет',
            'Apex Score': 'Очки Системы',
            'pulls': 'Макс Подтягивания',
            'dips': 'Макс Брусья',
            'advanced_tuck': 'Adv Tuck (сек)',
            'full_fl': 'Full FL (сек)'
        }
        
        # Применяем фильтр колонок (только те, что есть в данных)
        valid_cols = {k: v for k, v in cols_to_show.items() if k in leaderboard.columns}
        display_df = leaderboard[list(valid_cols.keys())].rename(columns=valid_cols)
        
        # Индексация с 1 (для мест 1, 2, 3...)
        display_df.index = display_df.index + 1
        
        st.dataframe(display_df, use_container_width=True)
        
        st.caption("💡 **Apex Score (Очки Системы)** рассчитывается как сумма всех полученных рангов во всех упражнениях. Прокачивайте слабые стороны, чтобы подняться в топе!")
    else:
        st.info("База данных пока пуста.")