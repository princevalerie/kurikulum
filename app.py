import streamlit as st
import time
import asyncio
from typing import Dict, List, Any
import json
import requests
from datetime import datetime

# Simulasi import agents (dalam implementasi nyata, ini akan dari file terpisah)
class ReasoningAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def analyze_requirements(self, topic: str, level: str, duration: int, format_type: str) -> Dict[str, Any]:
        """Menganalisis kebutuhan kurikulum berdasarkan input pengguna"""
        # Simulasi pemrosesan dengan Gemini 2.0 Flash
        time.sleep(2)  # Simulasi API call
        
        competencies = {
            "pemula": ["Pemahaman dasar", "Pengenalan konsep", "Praktik sederhana"],
            "menengah": ["Penerapan teori", "Analisis kasus", "Project menengah"],
            "lanjutan": ["Analisis mendalam", "Optimisasi", "Project kompleks"]
        }
        
        return {
            "topic": topic,
            "level": level,
            "duration": duration,
            "format": format_type,
            "competencies": competencies.get(level, competencies["pemula"]),
            "learning_objectives": [
                f"Memahami konsep dasar {topic}",
                f"Mampu menerapkan {topic} dalam konteks {level}",
                f"Menguasai tools dan teknik {topic}"
            ],
            "recommended_modules": duration // 2 if duration > 4 else 2
        }

class YouTubeAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def search_videos(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mencari video YouTube yang relevan"""
        time.sleep(3)  # Simulasi API call
        
        # Simulasi hasil pencarian video
        topic = requirements['topic']
        level = requirements['level']
        
        videos = [
            {
                "title": f"Panduan {topic} untuk {level.title()}",
                "channel": "Tech Academy",
                "duration": "15:30",
                "views": "125K",
                "url": f"https://youtube.com/watch?v=example1_{topic.replace(' ', '_')}",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                "description": f"Video pembelajaran {topic} yang komprehensif untuk level {level}"
            },
            {
                "title": f"Tutorial {topic} - Step by Step",
                "channel": "Learn Hub",
                "duration": "22:45",
                "views": "89K",
                "url": f"https://youtube.com/watch?v=example2_{topic.replace(' ', '_')}",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                "description": f"Tutorial praktis {topic} dengan contoh nyata"
            },
            {
                "title": f"Masterclass {topic} - Advanced Techniques",
                "channel": "Pro Skills",
                "duration": "18:20",
                "views": "156K",
                "url": f"https://youtube.com/watch?v=example3_{topic.replace(' ', '_')}",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                "description": f"Teknik advanced untuk menguasai {topic}"
            }
        ]
        
        return videos

class WebAgent:
    def __init__(self):
        pass
    
    def scrape_references(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mengumpulkan referensi dari web"""
        time.sleep(2)  # Simulasi web scraping
        
        topic = requirements['topic']
        
        references = [
            {
                "title": f"Comprehensive Guide to {topic}",
                "url": f"https://example.com/guide-{topic.replace(' ', '-')}",
                "type": "Article",
                "summary": f"Panduan lengkap tentang {topic} dengan penjelasan mendalam dan contoh praktis."
            },
            {
                "title": f"{topic} Best Practices",
                "url": f"https://blog.example.com/{topic.replace(' ', '-')}-best-practices",
                "type": "Blog Post",
                "summary": f"Kumpulan best practices dan tips untuk mengoptimalkan penggunaan {topic}."
            },
            {
                "title": f"Documentation: {topic}",
                "url": f"https://docs.example.com/{topic.replace(' ', '-')}",
                "type": "Documentation",
                "summary": f"Dokumentasi resmi dan referensi teknis untuk {topic}."
            },
            {
                "title": f"Case Study: {topic} Implementation",
                "url": f"https://medium.com/case-study-{topic.replace(' ', '-')}",
                "type": "Case Study",
                "summary": f"Studi kasus implementasi {topic} di berbagai industri."
            }
        ]
        
        return references

class CurriculumComposer:
    def __init__(self):
        pass
    
    def compose_curriculum(self, requirements: Dict[str, Any], videos: List[Dict], references: List[Dict]) -> Dict[str, Any]:
        """Menyusun kurikulum final"""
        time.sleep(1)  # Simulasi composition
        
        topic = requirements['topic']
        level = requirements['level']
        duration = requirements['duration']
        
        description_para1 = f"""
        Kurikulum {topic} level {level} ini dirancang khusus untuk memberikan pemahaman komprehensif 
        dalam waktu {duration} jam pembelajaran. Program ini menggabungkan teori fundamental dengan 
        praktik langsung, memastikan peserta tidak hanya memahami konsep dasar tetapi juga mampu 
        menerapkannya dalam skenario nyata. Setiap modul telah dikurasi dengan cermat untuk memastikan 
        progres pembelajaran yang optimal.
        """
        
        description_para2 = f"""
        Melalui kombinasi video pembelajaran berkualitas tinggi dan referensi teks yang mendalam, 
        kurikulum ini memberikan pengalaman belajar multi-modal yang efektif. Peserta akan dibimbing 
        melalui {requirements['recommended_modules']} modul utama yang mencakup {', '.join(requirements['competencies'][:2])} 
        dan berbagai aspek praktis lainnya. Setiap sesi dirancang untuk membangun pemahaman secara 
        bertahap dan memberikan kesempatan untuk praktek langsung.
        """
        
        return {
            "title": f"Kurikulum {topic} - Level {level.title()}",
            "description": [description_para1.strip(), description_para2.strip()],
            "duration": f"{duration} jam",
            "level": level,
            "learning_objectives": requirements['learning_objectives'],
            "competencies": requirements['competencies'],
            "videos": videos,
            "references": references,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Streamlit App
def main():
    st.set_page_config(
        page_title="Curriculum Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("🎓 AI-Powered Curriculum Generator")
    st.markdown("*Powered by Gemini 2.0 Flash, LangChain & LangGraph*")
    
    # Sidebar untuk input
    with st.sidebar:
        st.header("⚙️ Konfigurasi Kurikulum")
        
        topic = st.text_input(
            "Topik Pembelajaran",
            placeholder="Contoh: Machine Learning, Web Development, Data Science"
        )
        
        level = st.selectbox(
            "Level Pembelajaran",
            ["pemula", "menengah", "lanjutan"]
        )
        
        duration = st.slider(
            "Durasi (jam)",
            min_value=2,
            max_value=40,
            value=8,
            step=2
        )
        
        format_type = st.multiselect(
            "Format Pembelajaran",
            ["video", "teks", "praktik", "quiz"],
            default=["video", "teks"]
        )
        
        st.markdown("---")
        
        # API Configuration (opsional untuk demo)
        with st.expander("🔧 API Configuration"):
            gemini_api_key = st.text_input("Gemini API Key", type="password")
            youtube_api_key = st.text_input("YouTube API Key", type="password")
            
        generate_button = st.button("🚀 Generate Curriculum", type="primary")
    
    # Main content area
    if generate_button and topic:
        # Initialize agents
        reasoning_agent = ReasoningAgent(gemini_api_key)
        youtube_agent = YouTubeAgent(youtube_api_key)
        web_agent = WebAgent()
        composer = CurriculumComposer()
        
        # Progress tracking
        progress_container = st.container()
        with progress_container:
            st.markdown("### 🔄 Proses Generasi Kurikulum")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Agent 1: Reasoning
            status_text.text("🧠 Agent 1: Menganalisis kebutuhan kurikulum...")
            requirements = reasoning_agent.analyze_requirements(topic, level, duration, format_type)
            progress_bar.progress(25)
            st.success("✅ Analisis kebutuhan selesai")
            
            # Agent 2: YouTube Search
            status_text.text("🎥 Agent 2: Mencari video pembelajaran...")
            videos = youtube_agent.search_videos(requirements)
            progress_bar.progress(50)
            st.success("✅ Video pembelajaran ditemukan")
            
            # Agent 3: Web Scraping
            status_text.text("🌐 Agent 3: Mengumpulkan referensi web...")
            references = web_agent.scrape_references(requirements)
            progress_bar.progress(75)
            st.success("✅ Referensi web terkumpul")
            
            # Agent 4: Composition
            status_text.text("📝 Agent 4: Menyusun kurikulum final...")
            curriculum = composer.compose_curriculum(requirements, videos, references)
            progress_bar.progress(100)
            st.success("✅ Kurikulum berhasil dibuat!")
            
            status_text.text("🎉 Selesai! Scroll ke bawah untuk melihat hasil.")
        
        st.markdown("---")
        
        # Display Results
        st.markdown("## 📋 Hasil Kurikulum")
        
        # Curriculum Overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {curriculum['title']}")
            st.markdown(f"**Durasi:** {curriculum['duration']} | **Level:** {curriculum['level'].title()}")
            
            st.markdown("#### 📝 Deskripsi Program")
            for i, para in enumerate(curriculum['description'], 1):
                st.markdown(f"**Paragraf {i}:**")
                st.markdown(para)
                st.markdown("")
        
        with col2:
            st.markdown("#### 🎯 Objektif Pembelajaran")
            for obj in curriculum['learning_objectives']:
                st.markdown(f"• {obj}")
            
            st.markdown("#### 💡 Kompetensi yang Dicapai")
            for comp in curriculum['competencies']:
                st.markdown(f"• {comp}")
        
        st.markdown("---")
        
        # Videos Section
        st.markdown("## 🎥 Video Pembelajaran")
        
        video_cols = st.columns(len(videos))
        for i, video in enumerate(videos):
            with video_cols[i]:
                st.markdown(f"### {video['title']}")
                st.image(video['thumbnail'], use_column_width=True)
                st.markdown(f"**Channel:** {video['channel']}")
                st.markdown(f"**Durasi:** {video['duration']}")
                st.markdown(f"**Views:** {video['views']}")
                st.markdown(f"**Deskripsi:** {video['description']}")
                st.markdown(f"[🔗 Tonton Video]({video['url']})")
        
        st.markdown("---")
        
        # References Section
        st.markdown("## 📚 Referensi Tambahan")
        
        ref_cols = st.columns(2)
        for i, ref in enumerate(references):
            with ref_cols[i % 2]:
                st.markdown(f"#### {ref['title']}")
                st.markdown(f"**Type:** {ref['type']}")
                st.markdown(f"**Summary:** {ref['summary']}")
                st.markdown(f"[🔗 Baca Selengkapnya]({ref['url']})")
                st.markdown("---")
        
        # Export Options
        st.markdown("## 💾 Export Kurikulum")
        
        export_cols = st.columns(3)
        
        with export_cols[0]:
            if st.button("📄 Export PDF"):
                st.info("Fitur export PDF akan segera tersedia!")
        
        with export_cols[1]:
            curriculum_json = json.dumps(curriculum, indent=2, ensure_ascii=False)
            st.download_button(
                label="📁 Download JSON",
                data=curriculum_json,
                file_name=f"curriculum_{topic.replace(' ', '_')}.json",
                mime="application/json"
            )
        
        with export_cols[2]:
            if st.button("📧 Kirim Email"):
                st.info("Fitur kirim email akan segera tersedia!")
    
    elif generate_button and not topic:
        st.error("⚠️ Silakan masukkan topik pembelajaran terlebih dahulu!")
    
    else:
        # Landing page
        st.markdown("""
        ## 🌟 Selamat Datang di Curriculum Generator!
        
        Aplikasi ini menggunakan teknologi AI terdepan untuk membuat kurikulum pembelajaran yang komprehensif dan personal.
        
        ### ✨ Fitur Utama:
        - **🧠 AI Reasoning**: Analisis kebutuhan pembelajaran dengan Gemini 2.0 Flash
        - **🎥 Video Curation**: Pencarian dan kurasi video YouTube terbaik
        - **🌐 Web Research**: Pengumpulan referensi dari berbagai sumber online
        - **📝 Smart Composition**: Penyusunan kurikulum yang terstruktur dan komprehensif
        
        ### 🚀 Cara Menggunakan:
        1. Masukkan topik pembelajaran di sidebar
        2. Pilih level dan durasi yang diinginkan
        3. Tentukan format pembelajaran
        4. Klik "Generate Curriculum"
        5. Tunggu proses AI bekerja
        6. Nikmati kurikulum yang telah dibuat!
        
        **Mulai dengan mengisi form di sidebar →**
        """)
        
        # Demo metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Kurikulum Dibuat", "1,234", "↗️ 12%")
        
        with col2:
            st.metric("Video Terkurasi", "5,678", "↗️ 8%")
        
        with col3:
            st.metric("Referensi Terkumpul", "12,345", "↗️ 15%")
        
        with col4:
            st.metric("Pengguna Aktif", "2,468", "↗️ 23%")

if __name__ == "__main__":
    main()
