# # app.py
# from __future__ import annotations
# import io
# import os
# import re
# import zipfile
# from datetime import datetime
# from typing import List

# import requests
# import streamlit as st
# from dotenv import load_dotenv

# from tools.image_search import UnsplashClient
# from tools.utils import extract_keywords, make_hashtags, enforce_platform_limit
# from crew.crew import build_crew
# from services.db import save_post, list_posts

# load_dotenv()
# st.set_page_config(page_title="CrewAI Social Post", page_icon="📣", layout="wide")

# # Sidebar — Settings
# with st.sidebar:
#     st.title("📣 CrewAI Social Post")
#     st.caption("Generate platform-ready captions + royalty-free images")


# platform = st.selectbox("Platform", ["instagram", "twitter", "linkedin"], index=0)
# tone = st.selectbox("Tone", ["Friendly", "Professional", "Playful", "Inspirational", "Bold"], index=0)
# include_hashtags = st.toggle("Include Hashtags", value=True)
# num_images = st.slider("Search images (count)", 1, 12, 6)
# st.title("AI Social Post Generator")

# col1, col2 = st.columns([2, 1]) 
# with col1: 
#     topic = st.text_input("Enter a topic", placeholder="e.g., benefits of drinking water") 
# with col2: 
#     st.write("") 
#     generate_btn = st.button("Generate Post", use_container_width=True)
#     status_placeholder = st.empty()

# with st.expander("🕘 Recent Posts"): posts = list_posts(limit=10) 
# if posts: 
#     for p in posts: st.markdown(f"[{p.platform.upper()}] {p.topic} — {p.created_at:%Y-%m-%d %H:%M}") 
#     st.text(p.caption) 
#     if p.image_url: st.image(p.image_url, use_column_width=True) 
#     st.divider()
# else: st.caption("No history yet. Generate your first post!")

# if generate_btn and not topic.strip(): st.warning("Please enter a topic.")
# if generate_btn and topic.strip(): 
#     try: 
#         status_placeholder.info("Assembling crew and crafting your caption…") 
#         crew = build_crew()
#         caption_task = crew.tasks[0]
# keyword_task = crew.tasks[1]

# caption_text = caption_task.execute(
# inputs={
# "topic": topic,
# "platform": platform,
# "tone": tone,
# "include_hashtags": include_hashtags,
# }
# ).raw

# # Optional hashtag pass if the LLM didn't include any
# if include_hashtags and ("#" not in caption_text):
#     kws = extract_keywords(caption_text)
# tags = make_hashtags(kws, limit=8)
# if tags:
#     caption_text = caption_text.strip() + "\n\n" + " ".join(tags)

# caption_text = enforce_platform_limit(caption_text, platform)

# status_placeholder.info("Extracting visual themes for image search…")
# keywords_csv = keyword_task.execute(inputs={"caption": caption_text}).raw
# keywords = [k.strip() for k in re.split(r",|\n|;", keywords_csv) if k.strip()]
# if not keywords:
#     keywords = extract_keywords(caption_text)

# status_placeholder.info("Searching Unsplash for a matching image…")
# client = UnsplashClient()
# best = client.best_image(keywords, fallback_query=topic)
# if not best:
#     best = client.best_image([topic])

# status_placeholder.empty()
# left, right = st.columns([1, 1])
# with left:
#     st.subheader("✍️ Caption")
# st.text_area("", caption_text, height=200)
# st.caption(f"Platform: {platform.capitalize()} · Tone: {tone}")
# with right:
#     st.subheader("🖼️ Image Preview")
# if best:
#     st.image(best.url, use_column_width=True, caption=(best.alt_description or ""))
# image_url = best.url
# credit = (best.author or "")
# if credit:
#     st.caption(f"Photo by {credit} on Unsplash")
# else:
#     st.info("No exact image found. Try adjusting the topic or tone.")
# image_url = ""

# st.divider()
# st.subheader("⬇️ Export")
# colA, colB = st.columns(2)
# with colA:
#     st.download_button(
# "Download Caption (.txt)",
# data=caption_text.encode("utf-8"),
# file_name=f"caption_{datetime.now():%Y%m%d_%H%M}.txt",
# )
# with colB:
#     mem = io.BytesIO()
# with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
#     status_placeholder.error(f"Something went wrong: {e}")

########################################################################################################################################
# app.py
from __future__ import annotations
import io
import os
import re
import zipfile
from datetime import datetime
from typing import List

import requests
import streamlit as st
from dotenv import load_dotenv

from tools.image_search import UnsplashClient
from tools.utils import extract_keywords, make_hashtags, enforce_platform_limit
from crew.crew import build_crew
from services.db import save_post, list_posts

# --- Page Config & Initialization ---
load_dotenv()
st.set_page_config(page_title="CrewAI Social Post", page_icon="📣", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("📣 CrewAI Social Post")
    st.caption("Generate platform-ready captions + royalty-free images.")
    
    st.header("Settings")
    platform = st.selectbox("Platform", ["instagram", "twitter", "linkedin"], index=0)
    tone = st.selectbox("Tone", ["Friendly", "Professional", "Playful", "Inspirational", "Bold"], index=0)
    include_hashtags = st.toggle("Include Hashtags", value=True)
    # The image slider was removed as the logic only ever fetched one "best" image.

# --- Main Page ---
st.title("AI Social Post Generator")

# Use a form to prevent reruns on every widget change
with st.form(key="post_form"):
    topic = st.text_input("Enter a topic", placeholder="e.g., benefits of drinking water")
    generate_btn = st.form_submit_button("Generate Post", use_container_width=True)

status_placeholder = st.empty()

# --- Main Logic ---
if generate_btn and topic.strip():
    try:
        # 1. KICKOFF THE CREW
        status_placeholder.info("🤖 Assembling crew and starting the mission...")
        crew = build_crew()
        inputs = {
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "include_hashtags": include_hashtags,
        }
        # The modern way to run CrewAI is with kickoff(), which returns the final result.
        result = crew.kickoff(inputs=inputs)
        
        # The result from the crew should be a single, finalized string.
        caption_text = result

        # 2. ENFORCE PLATFORM LIMITS
        caption_text = enforce_platform_limit(caption_text, platform)
        
        # 3. SEARCH FOR IMAGE
        status_placeholder.info("🖼️ Searching for the perfect image...")
        # We can still use the keywords from the final caption for a better image search
        keywords = extract_keywords(caption_text)
        if not keywords:
            keywords = [topic] # Fallback to the original topic
            
        client = UnsplashClient()
        best_image = client.best_image(keywords, fallback_query=topic)
        
        status_placeholder.success("🚀 Post Generated Successfully!")

        # 4. DISPLAY RESULTS
        left, right = st.columns([1, 1])
        with left:
            st.subheader("✍️ Caption")
            st.text_area("", caption_text, height=250)
            st.caption(f"Platform: {platform.capitalize()} · Tone: {tone}")
        
        image_url = ""
        with right:
            st.subheader("🖼️ Image Preview")
            if best_image:
                st.image(best_image.url, use_column_width=True, caption=(best_image.alt_description or ""))
                image_url = best_image.url
                credit = best_image.author or ""
                if credit:
                    st.caption(f"Photo by {credit} on Unsplash")
            else:
                st.warning("No suitable image found. You can still use the caption!")
        
        # 5. SAVE & EXPORT
        # Save to database (optional, but good practice)
        save_post(topic, caption_text, image_url, platform, tone)
        
        st.divider()
        st.subheader("⬇️ Export")
        colA, colB = st.columns(2)

        with colA:
            st.download_button(
                "Download Caption (.txt)",
                data=caption_text.encode("utf-8"),
                file_name=f"caption_{datetime.now():%Y%m%d_%H%M}.txt",
            )
            
        if image_url:
            with colB:
                # Download image data for zipping
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    image_bytes = response.content
                    
                    # Create zip in memory
                    mem_zip = io.BytesIO()
                    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                        zf.writestr("caption.txt", caption_text)
                        zf.writestr("image.jpg", image_bytes)
                    
                    st.download_button(
                        "Download Post (.zip)",
                        data=mem_zip.getvalue(),
                        file_name=f"post_{datetime.now():%Y%m%d_%H%M}.zip",
                        mime="application/zip",
                    )

    except Exception as e:
        status_placeholder.error(f"An error occurred: {e}")

# --- Recent Posts Display ---
with st.expander("🕘 View Recent Posts"):
    posts = list_posts(limit=10)
    if posts:
        for p in posts:
            st.markdown(f"**[{p.platform.upper()}]** {p.topic}")
            st.text_area("", value=p.caption, height=150, key=f"caption_{p.id}", disabled=True)
            if p.image_url:
                st.image(p.image_url, use_column_width=True)
            st.caption(f"Generated on {p.created_at:%Y-%m-%d %H:%M}")
            st.divider()
    else:
        st.caption("No history yet. Generate your first post!")


