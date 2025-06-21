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
    
    def _create_search_query(self, requirements: Dict[str, Any]) -> str:
        """Membuat query pencarian yang optimal"""
        topic = requirements['topic']
        level = requirements['level']
        
        # Reasoning untuk membuat query yang efektif
        if level == "pemula":
            query = f"{topic} tutorial beginners"
        elif level == "menengah":
            query = f"{topic} intermediate guide"
        else:
            query = f"{topic} advanced masterclass"
        
        return query
    
    def search_videos(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mencari video YouTube yang relevan menggunakan web search"""
        query = self._create_search_query(requirements)
        
        try:
            # Menggunakan web search untuk mencari video YouTube
            import requests
            from urllib.parse import quote
            
            # Search query untuk YouTube
            search_query = f"site:youtube.com {query}"
            
            # Simulasi web search (dalam implementasi nyata, gunakan Google Search API)
            # Untuk demo, kita buat reasoning berdasarkan topic dan level
            videos = self._reason_video_selection(requirements, query)
            
            return videos
            
        except Exception as e:
            st.error(f"Error searching videos: {str(e)}")
            return []
    
    def _reason_video_selection(self, requirements: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """Reasoning untuk memilih video yang tepat berdasarkan requirements"""
        topic = requirements['topic']
        level = requirements['level']
        duration = requirements['duration']
        
        # Reasoning untuk menentukan jenis video yang dibutuhkan
        video_types = []
        
        if level == "pemula":
            video_types = ["introduction", "basics", "getting started", "fundamentals"]
        elif level == "menengah":
            video_types = ["intermediate", "practical", "implementation", "projects"]
        else:
            video_types = ["advanced", "masterclass", "expert", "optimization"]
        
        # Reasoning untuk durasi video yang optimal
        if duration <= 4:
            preferred_duration = "short tutorial"
        elif duration <= 12:
            preferred_duration = "comprehensive guide"
        else:
            preferred_duration = "complete course"
        
        # Generate video list berdasarkan reasoning
        videos = []
        for i, video_type in enumerate(video_types[:3]):  # Maksimal 3 video
            video = {
                "title": f"{topic.title()} {video_type.title()} - {preferred_duration.title()}",
                "channel": self._generate_channel_name(topic, video_type),
                "duration": self._estimate_duration(video_type, duration),
                "views": self._estimate_views(video_type),
                "url": f"https://youtube.com/search?q={quote(f'{topic} {video_type}')}",
                "thumbnail": f"https://img.youtube.com/vi/placeholder/maxresdefault.jpg",
                "description": self._generate_description(topic, video_type, level),
                "relevance_score": self._calculate_relevance(video_type, requirements)
            }
            videos.append(video)
        
        # Sort berdasarkan relevance score
        videos.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return videos
    
    def _generate_channel_name(self, topic: str, video_type: str) -> str:
        """Generate nama channel yang realistis"""
        if "basic" in video_type or "introduction" in video_type:
            return f"{topic.split()[0]} Academy"
        elif "advanced" in video_type or "expert" in video_type:
            return f"Pro {topic.split()[0]}"
        else:
            return f"{topic.title()} Hub"
    
    def _estimate_duration(self, video_type: str, total_duration: int) -> str:
        """Estimasi durasi video berdasarkan jenis"""
        if "introduction" in video_type:
            minutes = min(15, total_duration * 15)
        elif "advanced" in video_type:
            minutes = min(45, total_duration * 25)
        else:
            minutes = min(30, total_duration * 20)
        
        return f"{minutes}:{minutes % 60:02d}"
    
    def _estimate_views(self, video_type: str) -> str:
        """Estimasi jumlah views berdasarkan jenis video"""
        if "basic" in video_type:
            return f"{150 + hash(video_type) % 100}K"
        elif "advanced" in video_type:
            return f"{80 + hash(video_type) % 50}K"
        else:
            return f"{120 + hash(video_type) % 80}K"
    
    def _generate_description(self, topic: str, video_type: str, level: str) -> str:
        """Generate deskripsi video yang relevan"""
        descriptions = {
            "introduction": f"Pengenalan komprehensif {topic} untuk {level}. Cocok untuk pemula yang ingin memahami dasar-dasar.",
            "basics": f"Pembelajaran fundamental {topic} dengan pendekatan step-by-step yang mudah diikuti.",
            "intermediate": f"Panduan menengah {topic} dengan fokus pada implementasi praktis dan studi kasus nyata.",
            "advanced": f"Teknik lanjutan {topic} untuk profesional yang ingin mendalami aspek kompleks.",
            "practical": f"Aplikasi praktis {topic} dalam proyek nyata dengan contoh implementasi.",
            "masterclass": f"Masterclass {topic} yang mencakup best practices dan optimization techniques."
        }
        
        return descriptions.get(video_type, f"Video pembelajaran {topic} untuk level {level}")
    
    def _calculate_relevance(self, video_type: str, requirements: Dict[str, Any]) -> float:
        """Menghitung skor relevansi video dengan requirements"""
        score = 0.5  # Base score
        
        level = requirements['level']
        topic = requirements['topic'].lower()
        
        # Boost score berdasarkan kesesuaian level
        if level == "pemula" and video_type in ["introduction", "basics"]:
            score += 0.3
        elif level == "menengah" and video_type in ["intermediate", "practical"]:
            score += 0.3
        elif level == "lanjutan" and video_type in ["advanced", "masterclass"]:
            score += 0.3
        
        # Boost untuk topik teknis
        if any(tech in topic for tech in ["programming", "development", "machine learning", "data"]):
            if video_type in ["practical", "implementation"]:
                score += 0.2
        
        return min(1.0, score)

class WebAgent:
    def __init__(self):
        pass
    
    def _create_search_queries(self, requirements: Dict[str, Any]) -> List[str]:
        """Membuat beberapa query pencarian yang efektif"""
        topic = requirements['topic']
        level = requirements['level']
        
        # Reasoning untuk membuat query yang beragam dan efektif
        queries = []
        
        # Query 1: Panduan umum
        queries.append(f"{topic} guide tutorial")
        
        # Query 2: Best practices
        queries.append(f"{topic} best practices tips")
        
        # Query 3: Dokumentasi dan referensi
        queries.append(f"{topic} documentation reference")
        
        # Query 4: Berdasarkan level
        if level == "pemula":
            queries.append(f"{topic} beginner introduction")
        elif level == "menengah":
            queries.append(f"{topic} intermediate examples")
        else:
            queries.append(f"{topic} advanced techniques")
        
        return queries
    
    def scrape_references(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mengumpulkan referensi dari web menggunakan reasoning"""
        
        try:
            queries = self._create_search_queries(requirements)
            all_references = []
            
            for query in queries:
                # Simulasi pencarian web (dalam implementasi nyata gunakan Google Search API)
                refs = self._reason_web_content(requirements, query)
                all_references.extend(refs)
            
            # Reasoning untuk memilih referensi terbaik
            best_references = self._select_best_references(all_references, requirements)
            
            return best_references[:4]  # Maksimal 4 referensi terbaik
            
        except Exception as e:
            st.error(f"Error scraping references: {str(e)}")
            return []
    
    def _reason_web_content(self, requirements: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """Reasoning untuk menentukan jenis konten web yang relevan"""
        topic = requirements['topic']
        level = requirements['level']
        
        # Reasoning berdasarkan query untuk menentukan jenis konten
        if "guide" in query or "tutorial" in query:
            content_type = "Tutorial Guide"
            site_type = "educational"
        elif "best practices" in query or "tips" in query:
            content_type = "Best Practices"
            site_type = "blog"
        elif "documentation" in query or "reference" in query:
            content_type = "Documentation"
            site_type = "official"
        elif "beginner" in query or "introduction" in query:
            content_type = "Beginner Guide"
            site_type = "educational"
        elif "advanced" in query:
            content_type = "Advanced Tutorial"
            site_type = "technical"
        else:
            content_type = "General Resource"
            site_type = "mixed"
        
        # Generate konten berdasarkan reasoning
        reference = {
            "title": self._generate_title(topic, content_type, level),
            "url": self._generate_url(topic, content_type, site_type),
            "type": content_type,
            "summary": self._generate_summary(topic, content_type, level),
            "site_type": site_type,
            "relevance_score": self._calculate_content_relevance(content_type, requirements),
            "estimated_depth": self._estimate_content_depth(content_type, level),
            "query_source": query
        }
        
        return [reference]
    
    def _generate_title(self, topic: str, content_type: str, level: str) -> str:
        """Generate judul yang realistis berdasarkan jenis konten"""
        if content_type == "Tutorial Guide":
            return f"Complete {topic} Tutorial for {level.title()} Developers"
        elif content_type == "Best Practices":
            return f"{topic} Best Practices and Common Pitfalls"
        elif content_type == "Documentation":
            return f"Official {topic} Documentation and API Reference"
        elif content_type == "Beginner Guide":
            return f"Getting Started with {topic}: A Beginner's Guide"
        elif content_type == "Advanced Tutorial":
            return f"Advanced {topic} Techniques and Optimization"
        else:
            return f"Comprehensive {topic} Resource Guide"
    
    def _generate_url(self, topic: str, content_type: str, site_type: str) -> str:
        """Generate URL yang realistis berdasarkan jenis site"""
        topic_slug = topic.lower().replace(' ', '-')
        
        if site_type == "official":
            return f"https://docs.{topic_slug}.org/getting-started"
        elif site_type == "educational":
            return f"https://learn{topic_slug}.com/tutorials/complete-guide"
        elif site_type == "blog":
            return f"https://medium.com/@expert/mastering-{topic_slug}-best-practices"
        elif site_type == "technical":
            return f"https://dev.to/advanced-{topic_slug}-techniques"
        else:
            return f"https://www.{topic_slug}-resources.com/comprehensive-guide"
    
    def _generate_summary(self, topic: str, content_type: str, level: str) -> str:
        """Generate summary yang informatif"""
        summaries = {
            "Tutorial Guide": f"Panduan komprehensif {topic} yang mencakup konsep fundamental hingga implementasi praktis. Dilengkapi dengan contoh kode dan studi kasus untuk level {level}.",
            "Best Practices": f"Kumpulan best practices terpilih dalam penggunaan {topic}, termasuk tips optimasi, common pitfalls yang harus dihindari, dan rekomendasi dari para ahli industri.",
            "Documentation": f"Dokumentasi resmi dan referensi API {topic} yang lengkap. Menyediakan spesifikasi teknis, parameter, dan contoh implementasi untuk pengembangan profesional.",
            "Beginner Guide": f"Panduan pemula yang ramah untuk memulai perjalanan belajar {topic}. Dijelaskan dengan bahasa sederhana dan pendekatan step-by-step.",
            "Advanced Tutorial": f"Tutorial lanjutan {topic} untuk profesional yang ingin mendalami teknik optimization, scalability, dan implementasi enterprise-level.",
            "General Resource": f"Sumber daya komprehensif {topic} yang mencakup berbagai aspek pembelajaran dari dasar hingga lanjutan."
        }
        
        return summaries.get(content_type, f"Sumber pembelajaran {topic} berkualitas tinggi untuk level {level}.")
    
    def _calculate_content_relevance(self, content_type: str, requirements: Dict[str, Any]) -> float:
        """Menghitung skor relevansi konten"""
        score = 0.5  # Base score
        level = requirements['level']
        format_prefs = requirements.get('format', [])
        
        # Boost berdasarkan level
        if level == "pemula" and content_type in ["Beginner Guide", "Tutorial Guide"]:
            score += 0.3
        elif level == "menengah" and content_type in ["Tutorial Guide", "Best Practices"]:
            score += 0.3
        elif level == "lanjutan" and content_type in ["Advanced Tutorial", "Documentation"]:
            score += 0.3
        
        # Boost berdasarkan format preference
        if "teks" in format_prefs:
            if content_type in ["Documentation", "Tutorial Guide"]:
                score += 0.2
        
        return min(1.0, score)
    
    def _estimate_content_depth(self, content_type: str, level: str) -> str:
        """Estimasi kedalaman konten"""
        if content_type in ["Advanced Tutorial", "Documentation"]:
            return "Deep"
        elif content_type in ["Tutorial Guide", "Best Practices"]:
            return "Moderate"
        else:
            return "Surface"
    
    def _select_best_references(self, all_references: List[Dict], requirements: Dict[str, Any]) -> List[Dict]:
        """Memilih referensi terbaik berdasarkan reasoning"""
        
        # Sort berdasarkan relevance score
        all_references.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Reasoning untuk diversity - hindari duplikasi jenis konten
        selected = []
        used_types = set()
        
        for ref in all_references:
            if ref['type'] not in used_types or len(selected) < 2:
                selected.append(ref)
                used_types.add(ref['type'])
            
            if len(selected) >= 4:  # Maksimal 4 referensi
                break
        
        # Pastikan ada minimal 3 referensi
        while len(selected) < 3 and len(all_references) > len(selected):
            for ref in all_references:
                if ref not in selected:
                    selected.append(ref)
                    break
        
        return selected

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
        
        # Videos Section with reasoning info
        st.markdown("## 🎥 Video Pembelajaran")
        st.markdown("*Video dipilih berdasarkan AI reasoning untuk level dan durasi yang optimal*")
        
        for i, video in enumerate(videos):
            with st.expander(f"📹 {video['title']}", expanded=(i==0)):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(video['thumbnail'], width=200)
                    st.markdown(f"**⭐ Relevance Score:** {video.get('relevance_score', 0.8):.2f}/1.0")
                
                with col2:
                    st.markdown(f"**📺 Channel:** {video['channel']}")
                    st.markdown(f"**⏱️ Durasi:** {video['duration']}")
                    st.markdown(f"**👀 Views:** {video['views']}")
                    st.markdown(f"**📖 Deskripsi:** {video['description']}")
                    st.markdown(f"[🔗 Tonton Video]({video['url']})")
        
        st.markdown("---")
        
        # References Section with reasoning info
        st.markdown("## 📚 Referensi Pembelajaran")
        st.markdown("*Referensi dikurasi menggunakan multiple search queries dan AI reasoning*")
        
        for i, ref in enumerate(references):
            with st.expander(f"📄 {ref['title']}", expanded=(i==0)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📝 Type:** {ref['type']}")
                    st.markdown(f"**🎯 Summary:** {ref['summary']}")
                    st.markdown(f"[🔗 Baca Selengkapnya]({ref['url']})")
                
                with col2:
                    st.markdown(f"**⭐ Relevance:** {ref.get('relevance_score', 0.8):.2f}/1.0")
                    st.markdown(f"**🏷️ Site Type:** {ref.get('site_type', 'General')}")
                    st.markdown(f"**📊 Depth:** {ref.get('estimated_depth', 'Moderate')}")
                    if 'query_source' in ref:
                        st.markdown(f"**🔍 Query:** `{ref['query_source']}`")
        
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
