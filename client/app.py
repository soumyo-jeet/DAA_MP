import json
from typing import Dict, List, Optional

import requests
import streamlit as st

API_URL = "https://daa-mp.vercel.app/"


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #
def init_state():
    defaults = {
        "uploaded": False,
        "selected_courses": [],
        "completed_courses": [],
        "courses": {},
        "plan_a": None,
        "plan_b": None,
        "weights": {},
        "upload_message": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# --------------------------------------------------------------------------- #
# API helpers
# --------------------------------------------------------------------------- #
def call_api(endpoint: str, method: str = "GET", json_data: Optional[Dict] = None, files: Optional[Dict] = None):
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=12)
        else:
            response = requests.post(url, json=json_data, files=files, timeout=20)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as exc:
        return None, str(exc)
    except ValueError:
        return None, "Invalid JSON response from server."


def upload_dataset(uploaded_file) -> Optional[str]:
    if uploaded_file is None:
        return None
    file_bytes = uploaded_file.getvalue()
    files = {"file": (uploaded_file.name, file_bytes, "text/plain")}
    data, error = call_api("/upload", method="POST", files=files)
    if error:
        return f"Upload failed: {error}"
    if not data:
        return "Upload succeeded but server returned no data."
    return data.get("message", "File uploaded successfully.")


def load_courses():
    data, error = call_api("/courses", method="GET")
    if error:
        st.error(f"Unable to load course catalogue: {error}")
        return {}
    return data.get("courses", data.get("course", {}))


def request_plan_a(selected_courses: List[str], completed_courses: List[str]):
    data, error = call_api(
        "/plan_a",
        method="POST",
        json_data={"courses": selected_courses, "completed": completed_courses},
    )
    if error:
        st.error(f"Plan A request failed: {error}")
        return None
    return data


def request_plan_b(selected_courses: List[str], priorities: Dict[str, int]):
    data, error = call_api(
        "/plan_b",
        method="POST",
        json_data={"courses": selected_courses, "priorities": priorities},
    )
    if error:
        st.error(f"Plan B request failed: {error}")
        return None
    return data


# --------------------------------------------------------------------------- #
# Data normalization
# --------------------------------------------------------------------------- #
def normalize_time(value):
    if isinstance(value, list) and len(value) >= 2:
        return [int(value[0]), int(value[1])]
    if isinstance(value, str) and ":" in value:
        parts = value.split(":")
        try:
            return [int(parts[0]), int(parts[1])]
        except ValueError:
            return ["-", "-"]
    return ["-", "-"]


def normalize_course_data(course_data: dict) -> dict:
    if not course_data:
        return {}
    prereq = course_data.get("prereq") or course_data.get("Prerequisite") or []
    if isinstance(prereq, str) and prereq.strip():
        prereq = [p.strip() for p in prereq.split(";") if p.strip()]
    return {
        "name": course_data.get("name") or course_data.get("CourseName") or "Unknown",
        "department": course_data.get("department") or course_data.get("Department") or "-",
        "credits": course_data.get("credits") or course_data.get("Credits") or "-",
        "day": course_data.get("day") or course_data.get("Day") or "-",
        "start": normalize_time(course_data.get("start") or course_data.get("StartTime")),
        "end": normalize_time(course_data.get("end") or course_data.get("EndTime")),
        "prereq": prereq,
        "enrolled": course_data.get("enrolled") or course_data.get("CurrentEnrollment") or "-",
        "limit": course_data.get("limit") or course_data.get("EnrollmentLimit") or "-",
    }


def parse_required_courses(raw) -> Dict[str, List[str]]:
    """The API sometimes returns 'Required Course' as a JSON-encoded string
    mapping course -> list of prerequisites. Normalize it into a dict."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    return {}


# --------------------------------------------------------------------------- #
# Interaction
# --------------------------------------------------------------------------- #
def toggle_course(course_id: str):
    if course_id in st.session_state.selected_courses:
        st.session_state.selected_courses.remove(course_id)
    else:
        st.session_state.selected_courses.append(course_id)


def get_prereq_ok_courses(selected_courses: List[str], plan_a_data: Optional[dict], completed_courses: List[str]):
    """Split the selected courses into those with satisfied prerequisites
    (safe to include in Plan B) and those missing prerequisites (excluded),
    based on Plan A's eligibility data."""
    if not plan_a_data:
        return list(selected_courses), []

    eligibility = plan_a_data.get("eligibility", {})
    required = parse_required_courses(eligibility.get("Required Course"))
    completed = set(completed_courses)

    ok_courses = []
    excluded = []
    for course in selected_courses:
        reqs = required.get(course)
        if reqs:
            reqs_list = reqs if isinstance(reqs, list) else [reqs]
            missing = [p for p in reqs_list if p not in completed]
            if missing:
                excluded.append((course, missing))
                continue
        ok_courses.append(course)
    return ok_courses, excluded


def adjust_weight(course_id: str, delta: int):
    key = f"weight_{course_id}"
    current = st.session_state.get(key, 50)
    st.session_state[key] = max(0, min(100, current + delta))


# --------------------------------------------------------------------------- #
# Styling
# --------------------------------------------------------------------------- #
def inject_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

            .stApp {
                    /* Formal deep navy / slate gradient — professional, and keeps white panel text crisp */
                    background: linear-gradient(165deg, #0b1c33 0%, #16324f 45%, #274a6b 100%) !important;
            }

            .hero {
                padding: 28px 8px 8px 8px;
            }
            .hero h1 {
                color: #ffffff;
                font-weight: 800;
                font-size: 2.1rem;
                margin-bottom: 4px;
            }
            .hero p {
                color: #cbd5e1;
                font-size: 1rem;
                margin-top: 0;
            }

            .panel {
                background: #ffffff;
                border-radius: 18px;
                padding: 22px 24px;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
                border: 1px solid #eef1f5;
                margin-bottom: 22px;
            }

            .step-badge {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 26px;
                height: 26px;
                border-radius: 50%;
                background: #4f46e5;
                color: white;
                font-weight: 700;
                font-size: 0.8rem;
                margin-right: 10px;
            }
            .step-title {
                font-size: 1.15rem;
                font-weight: 700;
                color: #0f172a;
                display: flex;
                align-items: center;
                margin-bottom: 4px;
            }

            .course-card {
                background: #fbfcfe;
                border: 1px solid #e7ebf1;
                border-radius: 14px;
                padding: 16px 18px;
                transition: box-shadow 0.15s ease, transform 0.15s ease;
                height: 100%;
            }
            .course-card:hover {
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10);
                transform: translateY(-2px);
            }
            .course-card.selected {
                border: 1.5px solid #4f46e5;
                background: #f5f4ff;
            }
            .course-title {
                font-weight: 700;
                font-size: 1.02rem;
                color: #1e293b;
                margin-bottom: 8px;
            }
            .course-id-chip {
                display: inline-block;
                background: #eef2ff;
                color: #4338ca;
                font-weight: 700;
                font-size: 0.75rem;
                padding: 2px 8px;
                border-radius: 999px;
                margin-right: 6px;
            }
            .course-meta {
                font-size: 0.85rem;
                color: #475569;
                line-height: 1.6;
            }
            .course-meta b { color: #1e293b; }
            .prereq-chip {
                display: inline-block;
                background: #fef3c7;
                color: #92400e;
                font-size: 0.72rem;
                font-weight: 600;
                padding: 1px 7px;
                border-radius: 999px;
                margin: 2px 3px 0 0;
            }
            .prereq-none {
                color: #94a3b8;
                font-size: 0.82rem;
            }

            .chip-row { display: flex; flex-wrap: wrap; gap: 8px; }
            .selected-chip {
                background: #4f46e5;
                color: white;
                font-weight: 600;
                font-size: 0.82rem;
                padding: 5px 12px;
                border-radius: 999px;
            }

            .conflict-item {
                background: #fef2f2;
                border-left: 4px solid #ef4444;
                padding: 10px 14px;
                border-radius: 8px;
                margin-bottom: 8px;
                color: #7f1d1d;
                font-size: 0.9rem;
            }
            .no-conflict {
                background: #f0fdf4;
                border-left: 4px solid #22c55e;
                padding: 10px 14px;
                border-radius: 8px;
                color: #14532d;
                font-size: 0.9rem;
            }

            .eligible-badge {
                display: inline-block;
                padding: 5px 14px;
                border-radius: 999px;
                font-weight: 700;
                font-size: 0.85rem;
            }
            .eligible-yes { background: #dcfce7; color: #166534; }
            .eligible-no { background: #fee2e2; color: #991b1b; }

            .prereq-table-row {
                display: grid;
                grid-template-columns: 110px 1fr 90px;
                gap: 10px;
                padding: 8px 10px;
                border-bottom: 1px solid #eef1f5;
                font-size: 0.87rem;
                align-items: center;
            }
            .prereq-table-header {
                font-weight: 700;
                color: #64748b;
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.03em;
            }
            .status-met { color: #166534; font-weight: 700; }
            .status-missing { color: #991b1b; font-weight: 700; }

            .stButton>button {
                border-radius: 10px;
                font-weight: 600;
                border: 1px solid #e2e8f0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero():
    st.markdown(
        """
        <div class="hero">
            <h1>🎓 Course Scheduler</h1>
            <p>Upload your catalogue, pick courses, and get conflict-free or optimized schedule plans.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_start(step_num: str, title: str):
    st.markdown(
        f"""<div class="panel"><div class="step-title">
        <span class="step-badge">{step_num}</span>{title}</div>""",
        unsafe_allow_html=True,
    )


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def render_course_card(course_id: str, course_data: dict):
    if not course_data:
        st.warning(f"Course data missing for {course_id}")
        return

    data = normalize_course_data(course_data)
    start = ":".join(str(x).zfill(2) for x in data["start"])
    end = ":".join(str(x).zfill(2) for x in data["end"])
    prereq = data["prereq"]
    selected = course_id in st.session_state.selected_courses

    prereq_html = (
        "".join(f'<span class="prereq-chip">{p}</span>' for p in prereq)
        if prereq
        else '<span class="prereq-none">None</span>'
    )

    card_class = "course-card selected" if selected else "course-card"
    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="course-title">
                <span class="course-id-chip">{course_id}</span>{data['name']}
            </div>
            <div class="course-meta">
                <b>Dept:</b> {data['department']} &nbsp;·&nbsp; <b>Credits:</b> {data['credits']}<br/>
                <b>Schedule:</b> {data['day']} {start}–{end}<br/>
                <b>Enrollment:</b> {data['enrolled']}/{data['limit']}<br/>
                <b>Prerequisites:</b><br/>{prereq_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button(
        "✓ Selected — remove" if selected else "+ Select course",
        key=f"button_{course_id}",
        on_click=toggle_course,
        args=(course_id,),
        use_container_width=True,
        type="primary" if selected else "secondary",
    )


def render_selected_panel():
    if not st.session_state.selected_courses:
        st.info("No courses selected yet — use **+ Select course** on any card above.")
        return
    chips = "".join(f'<span class="selected-chip">{c}</span>' for c in st.session_state.selected_courses)
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)


def render_plan_a_results(plan_data: dict):
    if not plan_data:
        return

    recommended = plan_data.get("plan", [])
    conflicts = plan_data.get("conflicts", [])
    eligibility = plan_data.get("eligibility", {})

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**✅ Recommended courses**")
        if recommended:
            chips = "".join(f'<span class="selected-chip" style="background:#0f766e;">{c}</span>' for c in recommended)
            st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)
        else:
            st.info("No compatible courses found for the selected schedule.")

    with col2:
        st.markdown("**🕒 Schedule conflicts**")
        if conflicts:
            for message in conflicts:
                st.markdown(f'<div class="conflict-item">⚠️ {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-conflict">No schedule conflicts detected.</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("**📋 Prerequisite eligibility**")

    if eligibility:
        eligible = eligibility.get("Eligible", False)
        is_eligible = eligible in [True, "True", "true"]
        badge_class = "eligible-yes" if is_eligible else "eligible-no"
        badge_text = "Eligible to proceed" if is_eligible else "Missing prerequisites"
        st.markdown(f'<span class="eligible-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)

        required = parse_required_courses(eligibility.get("Required Course"))
        completed = set(st.session_state.completed_courses)

        if required:
            st.markdown("<br/>", unsafe_allow_html=True)
            rows = ['<div class="prereq-table-row prereq-table-header"><div>Course</div><div>Requires</div><div>Status</div></div>']
            for course, prereqs in required.items():
                prereqs_list = prereqs if isinstance(prereqs, list) else [prereqs]
                missing = [p for p in prereqs_list if p not in completed]
                status = (
                    '<span class="status-met">Met</span>'
                    if not missing
                    else f'<span class="status-missing">Missing: {", ".join(missing)}</span>'
                )
                prereq_text = ", ".join(prereqs_list) if prereqs_list else "None"
                rows.append(
                    f'<div class="prereq-table-row"><div><b>{course}</b></div>'
                    f'<div>{prereq_text}</div><div>{status}</div></div>'
                )
            st.markdown("".join(rows), unsafe_allow_html=True)
    else:
        st.info("No eligibility data returned.")

    with st.expander("Raw response (debug)"):
        st.json(plan_data)


def render_plan_b_results(plan_data: dict):
    if not plan_data:
        return

    plan_b = plan_data.get("plan", [])
    score = plan_data.get("score", None)

    st.markdown("**⚖️ Optimized courses**")
    if plan_b:
        chips = "".join(f'<span class="selected-chip" style="background:#7c3aed;">{c}</span>' for c in plan_b)
        st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)
    else:
        st.info("No weighted plan B courses produced for the given priorities.")

    if score is not None:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(f"**Weighted compatibility score:** {score:.2f}%")
        st.progress(min(max(int(score), 0), 100))


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    st.set_page_config(page_title="Course Scheduler Client", page_icon="🎓", layout="wide")
    init_state()
    inject_css()
    hero()

    # Step 1 — upload
    panel_start("1", "Upload your course file")
    uploaded_file = st.file_uploader("Upload `a.txt` containing course records", type=["txt"], label_visibility="collapsed")
    upload_col1, upload_col2 = st.columns([1, 3])
    with upload_col1:
        if uploaded_file is not None and st.button("Upload to server", type="primary"):
            upload_message = upload_dataset(uploaded_file)
            st.session_state.uploaded = upload_message is not None
            st.session_state.upload_message = upload_message
    with upload_col2:
        if st.session_state.upload_message:
            st.info(st.session_state.upload_message)
    panel_end()

    # Refresh trigger
    refresh_clicked = st.button("🔄 Refresh course catalogue from server")
    if st.session_state.uploaded or refresh_clicked:
        st.session_state.courses = load_courses()
        st.session_state.uploaded = False
        if st.session_state.courses:
            st.toast("Course catalogue loaded successfully.", icon="✅")

    if not st.session_state.courses:
        st.info("No course catalogue loaded yet. Upload `a.txt` above to begin, or refresh if it's already on the server.")
        st.markdown("---")
        st.caption("Make sure the server is running on localhost:5000 before using this client.")
        return

    # Step 2 — catalogue
    panel_start("2", "Browse & select courses")
    course_items = list(st.session_state.courses.items())
    cols_per_row = 3
    for i in range(0, len(course_items), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for col, (course_id, course_data) in zip(row_cols, course_items[i:i + cols_per_row]):
            with col:
                render_course_card(course_id, course_data)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("**Currently selected:**")
    render_selected_panel()
    panel_end()

    if not st.session_state.selected_courses:
        return

    # Step 3 — completed courses + Plan A
    panel_start("3", "Prerequisite check — Plan A")
    with st.form("completed_form"):
            all_courses = list(st.session_state.courses.keys())
            completed_options = [c for c in all_courses if c not in st.session_state.selected_courses]
            completed_default = [c for c in st.session_state.completed_courses if c in completed_options]

            completed = st.multiselect(
                "Choose courses you have already completed",
                options=completed_options,
                default=completed_default,
            )
            submit_completed = st.form_submit_button("Evaluate Plan A", type="primary")
            if submit_completed:
                st.session_state.completed_courses = completed
                st.session_state.plan_a = request_plan_a(
                    st.session_state.selected_courses, st.session_state.completed_courses
                )

    if st.session_state.plan_a is not None:
        st.markdown("<br/>", unsafe_allow_html=True)
        render_plan_a_results(st.session_state.plan_a)
    panel_end()

    if st.session_state.plan_a is None:
        return

    # Step 4 — weights + Plan B
    panel_start("4", "Weighted rearrangement — Plan B")
    st.caption("Give each eligible course a relative preference weight (0–100) to generate an optimized fallback plan.")

    ok_courses, excluded = get_prereq_ok_courses(
        st.session_state.selected_courses, st.session_state.plan_a, st.session_state.completed_courses
    )

    if excluded:
        excluded_text = "; ".join(f"{course} (missing {', '.join(missing)})" for course, missing in excluded)
        st.warning(f"Excluded from Plan B — missing prerequisites: {excluded_text}")

    if not ok_courses:
        st.info("No courses with satisfied prerequisites to build a Plan B from.")
        panel_end()
        st.markdown("---")
        st.caption("Make sure the server is running on localhost:5000 before using this client.")
        return

    # Initialize slider state before rendering so +/- buttons and dragging both work.
    for course_id in ok_courses:
        st.session_state.setdefault(f"weight_{course_id}", st.session_state.weights.get(course_id, 50))

    weight_cols = st.columns(3)
    for index, course_id in enumerate(ok_courses):
        with weight_cols[index % 3]:
            st.markdown(f"**{course_id}**")
            minus_col, slider_col, plus_col, value_col = st.columns([1, 5, 1, 1])
            with minus_col:
                st.button("−", key=f"minus_{course_id}", on_click=adjust_weight, args=(course_id, -5))
            with slider_col:
                st.slider(
                    course_id,
                    min_value=0,
                    max_value=100,
                    step=5,
                    key=f"weight_{course_id}",
                    label_visibility="collapsed",
                )
            with plus_col:
                st.button("+", key=f"plus_{course_id}", on_click=adjust_weight, args=(course_id, 5))
            with value_col:
                st.markdown(f"<div style='padding-top:8px;'>{st.session_state[f'weight_{course_id}']}</div>", unsafe_allow_html=True)

    if st.button("Generate Plan B", type="primary"):
        weights = {course_id: st.session_state[f"weight_{course_id}"] for course_id in ok_courses}
        st.session_state.weights = weights
        st.session_state.plan_b = request_plan_b(ok_courses, weights)

    if st.session_state.plan_b is not None:
        st.markdown("<br/>", unsafe_allow_html=True)
        render_plan_b_results(st.session_state.plan_b)
    panel_end()

    st.markdown("---")
    st.caption("Make sure the server is running on localhost:5000 before using this client.")


if __name__ == "__main__":
    main()