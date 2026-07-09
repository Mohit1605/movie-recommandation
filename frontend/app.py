import streamlit as st
import requests
import textwrap
from pathlib import Path
import streamlit.components.v1 as components

# ======================================================
# CONFIGURATION
# ======================================================

API_URL = "http://127.0.0.1:8000"

CONTENT_URL = f"{API_URL}/content/"
COLLAB_URL = f"{API_URL}/collabrative/"
HYBRID_URL = f"{API_URL}/Hybrid/"
HEALTH_URL = f"{API_URL}/health/"
MOVIE_SEARCH_URL = f"{API_URL}/movies/search"
USER_SEARCH_URL = f"{API_URL}/search_users/"
TYPEAHEAD_COMPONENT = components.declare_component(
    "api_typeahead",
    path=str(Path(__file__).parent / "typeahead_component"),
)

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.movie-card{
    background:#1C1F26;
    border-radius:18px;
    padding:22px;
    margin:18px 0;
    border:1px solid #2F3642;
    box-shadow:0 8px 20px rgba(0,0,0,.35);
    transition:.25s;
    min-height:560px;
    box-sizing:border-box;
    display:flex;
    flex-direction:column;
}

.movie-card:hover{
    transform:translateY(-4px);
    border-color:#ff4b4b;
    box-shadow:0 12px 28px rgba(255,75,75,.25);
}

.movie-title{
    font-size:26px;
    line-height:1.25;
    font-weight:700;
    color:white;
    min-height:64px;
    overflow:hidden;
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
}

.movie-id{
    color:#A8A8A8;
    font-size:15px;
    margin-top:8px;
    min-height:22px;
}

.movie-card hr{
    width:100%;
    margin:16px 0 4px;
}

.score-box{
    background:#262B35;
    border-radius:12px;
    padding:14px;
    text-align:center;
}

.score-title{
    color:#BBBBBB;
    font-size:14px;
}

.score-value{
    color:white;
    font-size:24px;
    font-weight:bold;
}
.poster{
    height:210px;
    flex:0 0 210px;
    background:#2B3140;
    border-radius:15px;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:90px;
    line-height:1;
    overflow:hidden;
    margin-bottom:16px;
}

.score-row{
    background:#262B35;
    padding:9px 8px;
    border-radius:10px;
    margin-top:8px;
    font-size:17px;
    line-height:1.25;
    text-align:center;
    color:white;
}

.score-list{
    margin-top:auto;
}

.sidebar-brand{
    background:#1C1F26;
    border:1px solid #2F3642;
    border-radius:14px;
    padding:18px;
    margin-bottom:16px;
}

.sidebar-brand-title{
    color:white;
    font-size:24px;
    font-weight:800;
    line-height:1.15;
}

.sidebar-brand-subtitle{
    color:#A8A8A8;
    font-size:13px;
    margin-top:8px;
}

.sidebar-status{
    border-radius:12px;
    padding:12px 14px;
    margin:12px 0 18px;
    font-weight:700;
}

.sidebar-status.online{
    background:rgba(34,197,94,.12);
    border:1px solid rgba(34,197,94,.45);
    color:#86EFAC;
}

.sidebar-status.offline{
    background:rgba(239,68,68,.12);
    border:1px solid rgba(239,68,68,.45);
    color:#FCA5A5;
}

.sidebar-section{
    background:#161A22;
    border:1px solid #2F3642;
    border-radius:12px;
    padding:14px;
    margin:14px 0;
}

.sidebar-section-title{
    color:white;
    font-size:15px;
    font-weight:800;
    margin-bottom:10px;
}

.mode-row{
    display:flex;
    gap:10px;
    align-items:flex-start;
    padding:9px 0;
    border-top:1px solid rgba(255,255,255,.07);
}

.mode-row:first-of-type{
    border-top:0;
}

.mode-icon{
    width:28px;
    height:28px;
    border-radius:8px;
    background:#262B35;
    display:flex;
    align-items:center;
    justify-content:center;
    flex:0 0 28px;
}

.mode-title{
    color:white;
    font-size:14px;
    font-weight:700;
}

.mode-text{
    color:#A8A8A8;
    font-size:12px;
    line-height:1.35;
    margin-top:2px;
}

.sidebar-footer{
    color:#777F8F;
    font-size:12px;
    text-align:center;
    margin-top:18px;
}

.recommendation-count-card{
    max-width:560px;
    margin:18px auto 2px;
    padding:0 4px;
}

.recommendation-count-title{
    color:white;
    font-size:15px;
    font-weight:800;
    letter-spacing:0;
}

.recommendation-count-subtitle{
    color:#A8A8A8;
    font-size:12px;
    margin-top:3px;
}

div[data-testid="stSlider"]{
    max-width:560px;
    margin:0 auto 18px;
    padding:2px 4px 0;
}

div[data-testid="stSlider"] label{
    display:none;
}

div[data-testid="stSlider"] [data-testid="stThumbValue"]{
    background:#ff4b4b;
    color:white;
    border-radius:999px;
    font-weight:800;
}

div[data-testid="stSlider"] [role="slider"]{
    background:#ff4b4b;
    border-color:white;
    box-shadow:0 0 0 4px rgba(255,75,75,.16);
}
</style>
""",unsafe_allow_html=True)

# ======================================================
# API FUNCTIONS
# ======================================================

def content_recommend(title,top_n):

    payload={
        "title":title,
        "top_n":top_n
    }

    response=requests.post(
        CONTENT_URL,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def collaborative_recommend(user_id,top_n):

    payload={
        "user_id":user_id,
        "top_n":top_n
    }

    response=requests.post(
        COLLAB_URL,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def hybrid_recommend(title,user_id,top_n):

    payload={
        "title":title,
        "user_id":user_id,
        "top_n":top_n
    }

    response=requests.post(
        HYBRID_URL,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def health_check():

    try:

        response=requests.get(
            HEALTH_URL,
            timeout=5
        )

        return response.status_code==200

    except:

        return False


def search_movie_titles(query, limit=10):

    query = query.strip()

    if not query:
        return []

    response = requests.get(
        MOVIE_SEARCH_URL,
        params={
            "q": query,
            "limit": limit,
        },
        timeout=5,
    )

    response.raise_for_status()

    return response.json().get("movies", [])


def search_user_ids(query, limit=10):

    query = query.strip()

    if not query:
        return []

    response = requests.get(
        USER_SEARCH_URL,
        params={
            "q": query,
            "limit": limit,
        },
        timeout=5,
    )

    response.raise_for_status()

    return response.json().get("users", [])


def api_typeahead(label, placeholder, options, state_key, component_key):

    current_value = st.session_state.get(state_key, "")

    typed_value = TYPEAHEAD_COMPONENT(
        label=label,
        placeholder=placeholder,
        options=options,
        value=current_value,
        key=component_key,
        default=current_value,
    )

    if typed_value is not None and typed_value != current_value:
        st.session_state[state_key] = typed_value
        st.rerun()

    return st.session_state.get(state_key, "")


def get_score(movie, *keys):

    for key in keys:

        value = movie.get(key)

        if value is not None:
            return float(value)

    return 0.0


def normalize_response(response):

    if isinstance(response, dict):
        raw_recommendations = response.get("recommendations", [])
    else:
        raw_recommendations = response

    recommendations = []

    for movie in raw_recommendations:

        recommendations.append(
            {
                "movieId": movie.get("movieId"),
                "title": movie.get("title", "Unknown Movie"),
                "content_score": get_score(movie, "content_score", "similarity"),
                "collabrative_score": get_score(
                    movie,
                    "collabrative_score",
                    "predicted_rating"
                ),
                "hybrid_score": get_score(movie, "hybrid_score"),
            }
        )

    return {"recommendations": recommendations}


# ======================================================
# ROUTER
# ======================================================

def get_recommendations(title,user_id,top_n):

    has_title=bool(title.strip())
    has_user=bool(user_id)

    if has_title and has_user:

        return (
            "Hybrid Recommendation",
            normalize_response(hybrid_recommend(
                title,
                int(user_id),
                top_n
            ))
        )

    elif has_title:

        return (
            "Content Based Recommendation",
            normalize_response(content_recommend(
                title,
                top_n
            ))
        )

    elif has_user:

        return (
            "Collaborative Recommendation",
            normalize_response(collaborative_recommend(
                int(user_id),
                top_n
            ))
        )

    else:

        raise Exception(
            "Please enter Movie Title or User ID."
        )
# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    backend_online = health_check()
    status_class = "online" if backend_online else "offline"
    status_text = "Backend connected" if backend_online else "Backend offline"
    status_icon = "&#128994;" if backend_online else "&#128308;"

    st.markdown(
        """
<div class="sidebar-brand">
    <div class="sidebar-brand-title">&#127916; Movie Recommender</div>
    <div class="sidebar-brand-subtitle">Personalized recommendations from content, users, or both.</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="sidebar-status {status_class}">{status_icon} {status_text}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="sidebar-section">
    <div class="sidebar-section-title">&#128204; Choose an engine</div>
    <div class="mode-row">
        <div class="mode-icon">&#127919;</div>
        <div>
            <div class="mode-title">Content based</div>
            <div class="mode-text">Enter only a movie title to find similar movies.</div>
        </div>
    </div>
    <div class="mode-row">
        <div class="mode-icon">&#128101;</div>
        <div>
            <div class="mode-title">Collaborative</div>
            <div class="mode-text">Enter only a user ID to use rating patterns.</div>
        </div>
    </div>
    <div class="mode-row">
        <div class="mode-icon">&#128640;</div>
        <div>
            <div class="mode-title">Hybrid</div>
            <div class="mode-text">Enter both title and user ID for blended ranking.</div>
        </div>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="sidebar-section">
    <div class="sidebar-section-title">&#9881; Quick tips</div>
    <div class="mode-text">Use exact movie names when possible.</div>
    <div class="mode-text" style="margin-top:8px;">Increase recommendation count when exploring.</div>
    <div class="mode-text" style="margin-top:8px;">If an API error occurs, it will appear in the main panel.</div>
</div>
<div class="sidebar-footer">FastAPI &bull; Streamlit &bull; Scikit-Learn &bull; Surprise<br>Version 1.0</div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# HEADER
# ======================================================

st.markdown(
    """
<div class="title">
🎬 Movie Recommendation System
</div>

<div class="subtitle">
Discover movies using Content-Based, Collaborative and Hybrid Recommendation.
</div>
""",
    unsafe_allow_html=True,
)

st.divider()


# ======================================================
# MOVIE CARD
# ======================================================

def show_movie_card(movie, rank):

    st.markdown(
    f"""
    <div class="movie-card">
    <div class="movie-title">
            🎬 {rank}. {movie["title"]}
    </div>

    <div class="movie-id">
            Movie ID : {movie["movieId"]}
    </div>
    </div>
    """,
    unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        if movie.get("content_score") is not None:

            st.markdown(
            f"""
                <div class="score-box">
                    <div class="score-title">🎯 Content Score</div>
                    <div class="score-value">{movie["content_score"]:.3f}</div>
                </div>
            """,
            unsafe_allow_html=True,
            )

    with c2:

        if movie.get("collabrative_score") is not None:

            st.markdown(
                f"""
                <div class="score-box">
                    <div class="score-title">⭐ Predicted Rating</div>
                    <div class="score-value">{movie["collabrative_score"]:.3f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c3:

        if movie.get("hybrid_score") is not None:

            st.markdown(
                f"""
                <div class="score-box">
                    <div class="score-title">🏆 Hybrid Score</div>
                    <div class="score-value">{movie["hybrid_score"]:.3f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

# ======================================================
# RECOMMENDATION LIST
# ======================================================

# def display_recommendations(recommendation_type, response):

    st.success(recommendation_type)

    recommendations = response.get("recommendations", [])

    if not recommendations:
        st.warning("No recommendations found.")
        return

    st.subheader(f"🎬 Recommended Movies ({len(recommendations)})")


    posters = [
        "🎬", "🍿", "🎥", "📽️",
        "🎞️", "⭐", "🌟", "🎭",
        "🚀", "👑"
    ]


    cols = st.columns(4)


    for i, movie in enumerate(recommendations):

        with cols[i % 4]:

            icon = posters[i % len(posters)]


            st.markdown(
                textwrap.dedent(f"""
                <div class="movie-card">

                    <div class="poster">
                        {icon}
                    </div>


                    <div class="movie-title">
                        {movie["title"]}
                    </div>


                    <div class="movie-id">
                        Movie ID : {movie["movieId"]}
                    </div>


                    <hr>


                    <div class="score-row">
                        ⭐ Score :
                        {
                            movie.get("collabrative_score",
                            movie.get("predicted_rating",0))
                        :.3f}
                    </div>


                    <div class="score-row">
                        🎯 Similarity :
                        {
                            movie.get("content_score",
                            movie.get("similarity",0))
                        :.3f}
                    </div>


                    <div class="score-row">
                        🏆 Hybrid :
                        {
                            movie.get("hybrid_score",0)
                        :.3f}
                    </div>

                </div>
                """),
                unsafe_allow_html=True
            )
def format_score_row(label, value):

    if value is None:
        return ""

    return f'<div class="score-row">{label} : {float(value):.3f}</div>'


def display_recommendations(recommendation_type, response):

    st.success(recommendation_type)

    recommendations = response.get("recommendations", [])

    if not recommendations:
        st.warning("No recommendations found.")
        return

    st.subheader(f"Recommended Movies ({len(recommendations)})")

    posters = [
        "&#127916;",
        "&#127871;",
        "&#127909;",
        "&#128253;",
        "&#127902;",
        "&#11088;",
        "&#127775;",
        "&#127917;",
        "&#128640;",
        "&#128081;",
        "&#127912;",
        "&#127908;",
        "&#127926;",
        "&#127942;",
        "&#128293;",
        "&#10024;",
    ]
    cols = st.columns(4)

    for i, movie in enumerate(recommendations):

        with cols[i % 4]:

            score_rows = "".join(
                [
                    format_score_row(
                        "Score",
                        movie.get("collabrative_score")
                    ),
                    format_score_row(
                        "Similarity",
                        movie.get("content_score")
                    ),
                    format_score_row(
                        "Hybrid",
                        movie.get("hybrid_score")
                    ),
                ]
            )

            html = (
                '<div class="movie-card">'
                f'<div class="poster">{posters[i % len(posters)]}</div>'
                f'<div class="movie-title">{movie["title"]}</div>'
                f'<div class="movie-id">Movie ID : {movie["movieId"]}</div>'
                '<hr>'
                f'<div class="score-list">{score_rows}</div>'
                '</div>'
            )

            st.markdown(html, unsafe_allow_html=True)


# ======================================================
# INPUTS
# ======================================================

st.subheader("🔍 Get Movie Recommendations")

col1, col2 = st.columns(2)

movie_suggestions = []
user_suggestions = []
movie_query = st.session_state.get("movie_typeahead_value", "")
user_query = st.session_state.get("user_typeahead_value", "")

if movie_query.strip():

    try:
        movie_suggestions = search_movie_titles(movie_query, limit=10)
    except requests.exceptions.RequestException:
        movie_suggestions = []

if user_query.strip():

    try:
        user_suggestions = search_user_ids(user_query, limit=10)
    except requests.exceptions.RequestException:
        user_suggestions = []

with col1:

    title = api_typeahead(
        label="🎬 Movie Title (Optional)",
        placeholder="Start typing a movie name",
        options=[movie["title"] for movie in movie_suggestions],
        state_key="movie_typeahead_value",
        component_key="movie_typeahead",
    )

    if movie_query.strip() and not movie_suggestions:
        st.caption("No movie suggestions found.")

with col2:

    user_id = api_typeahead(
        label="👤 User ID (Optional)",
        placeholder="Start typing a user ID",
        options=[str(user_id) for user_id in user_suggestions],
        state_key="user_typeahead_value",
        component_key="user_typeahead",
    )

    if user_query.strip() and not user_suggestions:
        st.caption("No user ID suggestions found.")

st.markdown(
    """
<div class="recommendation-count-card">
    <div class="recommendation-count-title">Results to show</div>
    <div class="recommendation-count-subtitle">Pick a compact list or explore a wider set.</div>
</div>
    """,
    unsafe_allow_html=True,
)

top_n = st.slider(
    "Movies to show",
    min_value=1,
    max_value=20,
    value=10,
    label_visibility="collapsed"
)

submitted = st.button(
    "🚀 Get Recommendations",
    use_container_width=True
)

# ======================================================
# MAIN LOGIC
# ======================================================

def format_api_error(error_detail):

    if isinstance(error_detail, str):
        return error_detail

    if isinstance(error_detail, list):
        messages = []

        for item in error_detail:

            if isinstance(item, dict):
                location = " -> ".join(str(part) for part in item.get("loc", []))
                message = item.get("msg", str(item))

                if location:
                    messages.append(f"{location}: {message}")
                else:
                    messages.append(message)
            else:
                messages.append(str(item))

        return "\n".join(messages)

    if isinstance(error_detail, dict):
        return error_detail.get("message", str(error_detail))

    return str(error_detail)


def get_api_error_message(error):

    response = error.response

    if response is None:
        return str(error)

    try:
        body = response.json()
    except ValueError:
        return response.text or str(error)

    return format_api_error(body.get("detail", body))


if submitted:

    try:

        # Validate User ID
        if user_id.strip():

            if not user_id.isdigit():
                st.error("User ID must be an integer.")
                st.stop()

            user_id = int(user_id)

        else:
            user_id = None

        with st.spinner("Finding the best movies for you..."):

            recommendation_type, response = get_recommendations(
                title,
                user_id,
                top_n
            )

        st.divider()

        display_recommendations(
            recommendation_type,
            response
        )

    except requests.exceptions.HTTPError as e:
        st.error(get_api_error_message(e))

    except requests.exceptions.RequestException as e:
        st.error(f"Backend request failed: {e}")

    except Exception as e:
        st.error(str(e))

