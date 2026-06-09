from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

AI_TOOLS = [
    {"name": "ChatGPT", "url": "https://chatgpt.com", "cat": "General", "desc": "Conversational AI."},
    {"name": "Claude", "url": "https://claude.ai", "cat": "Engineer", "desc": "Coding & analysis."},
    {"name": "Perplexity", "url": "https://perplexity.ai", "cat": "Student", "desc": "AI research engine."},
    {"name": "Canva", "url": "https://www.canva.com", "cat": "Teacher", "desc": "Design platform."},
    {"name": "Midjourney", "url": "https://www.midjourney.com", "cat": "General", "desc": "Image generation."},
    {"name": "GitHub Copilot", "url": "https://github.com/features/copilot", "cat": "Engineer", "desc": "AI coding."},
    {"name": "Gemini", "url": "https://gemini.google.com", "cat": "General", "desc": "Google AI assistant."},
    {"name": "Poe", "url": "https://poe.com", "cat": "General", "desc": "All-in-one AI chatbot."},
    {"name": "Adobe Premiere", "url": "https://adobe.com/premiere", "cat": "Editor", "desc": "Professional AI video editing."},
    {"name": "DaVinci Resolve", "url": "https://blackmagicdesign.com", "cat": "Editor", "desc": "AI color & post-production."},
    {"name": "Runway", "url": "https://runwayml.com", "cat": "Editor", "desc": "Generative AI for VFX."},
    {"name": "Descript", "url": "https://descript.com", "cat": "Editor", "desc": "Text-based video editing."},
    {"name": "Topaz Video", "url": "https://topazlabs.com", "cat": "Editor", "desc": "AI video upscaling."},
    {"name": "Grammarly", "url": "https://www.grammarly.com", "cat": "Student", "desc": "Writing assistant."},
    {"name": "Quillbot", "url": "https://quillbot.com", "cat": "Student", "desc": "Paraphrasing tool."},
    {"name": "Otter.ai", "url": "https://otter.ai", "cat": "Teacher", "desc": "Meeting transcription."},
    {"name": "Notion AI", "url": "https://notion.so", "cat": "General", "desc": "Productivity AI."},
    {"name": "DeepL", "url": "https://www.deepl.com", "cat": "Student", "desc": "Accurate translator."},
    {"name": "ElevenLabs", "url": "https://elevenlabs.io", "cat": "General", "desc": "Voice synthesis."},
    {"name": "Synthesia", "url": "https://www.synthesia.io", "cat": "Teacher", "desc": "AI avatars."},
    {"name": "Humata", "url": "https://www.humata.ai", "cat": "Student", "desc": "AI PDF reader."},
    {"name": "ChatPDF", "url": "https://www.chatpdf.com", "cat": "Student", "desc": "Talk to PDFs."},
    {"name": "Consensus", "url": "https://consensus.app", "cat": "Student", "desc": "AI research search."},
    {"name": "Elicit", "url": "https://elicit.com", "cat": "Student", "desc": "Literature review."},
    {"name": "Cursor", "url": "https://cursor.sh", "cat": "Engineer", "desc": "AI code editor."},
    {"name": "Tabnine", "url": "https://tabnine.com", "cat": "Engineer", "desc": "Code auto-complete."},
    {"name": "Replit AI", "url": "https://replit.com", "cat": "Engineer", "desc": "AI IDE."},
    {"name": "Codeium", "url": "https://codeium.com", "cat": "Engineer", "desc": "Fast code AI."},
    {"name": "DALL-E 3", "url": "https://openai.com/dall-e-3", "cat": "General", "desc": "Image AI."},
    {"name": "Leonardo.ai", "url": "https://leonardo.ai", "cat": "General", "desc": "Creative art."},
    {"name": "Stable Diffusion", "url": "https://stablediffusionweb.com", "cat": "General", "desc": "Open source AI."},
    {"name": "Adobe Firefly", "url": "https://firefly.adobe.com", "cat": "General", "desc": "Designer AI."},
    {"name": "Figma AI", "url": "https://figma.com", "cat": "Engineer", "desc": "UI/UX design AI."},
    {"name": "Uizard", "url": "https://uizard.io", "cat": "Engineer", "desc": "Wireframe AI."},
    {"name": "Medscape", "url": "https://medscape.com", "cat": "Doctor", "desc": "Clinical AI."},
    {"name": "Viz.ai", "url": "https://viz.ai", "cat": "Doctor", "desc": "Imaging AI."},
    {"name": "PathAI", "url": "https://pathai.com", "cat": "Doctor", "desc": "Pathology AI."},
    {"name": "Aidoc", "url": "https://aidoc.com", "cat": "Doctor", "desc": "Radiology AI."},
    {"name": "Zebra Medical", "url": "https://zebra-med.com", "cat": "Doctor", "desc": "Health AI."},
    {"name": "Babylon Health", "url": "https://babylonhealth.com", "cat": "Doctor", "desc": "Symptom checker."},
    {"name": "Google Scholar", "url": "https://scholar.google.com", "cat": "Student", "desc": "Research tool."},
    {"name": "WolframAlpha", "url": "https://wolframalpha.com", "cat": "Student", "desc": "Math AI."},
    {"name": "Photomath", "url": "https://photomath.com", "cat": "Student", "desc": "Math solver."},
    {"name": "Duolingo", "url": "https://duolingo.com", "cat": "Student", "desc": "Language AI."},
    {"name": "Socratic", "url": "https://socratic.org", "cat": "Student", "desc": "Homework helper."},
    {"name": "Brainly", "url": "https://brainly.com", "cat": "Student", "desc": "Learning AI."},
    {"name": "Khanmigo", "url": "https://khanacademy.org", "cat": "Student", "desc": "Tutor AI."},
    {"name": "Knewton", "url": "https://knewton.com", "cat": "Student", "desc": "Personalized learning."}
]

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617); min-height: 100vh; color: white; }
        .lux-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .blob { position: fixed; border-radius: 50%; filter: blur(100px); opacity: 0.4; animation: drift 20s infinite alternate; z-index: 0; }
        @keyframes drift { from { transform: translate(-50px, -50px); } to { transform: translate(50px, 50px); } }
    </style>
</head>
<body>
    <div class="blob" style="width: 400px; height: 400px; background: #3b82f6; top: 10%; left: 10%;"></div>
    <div class="blob" style="width: 400px; height: 400px; background: #8b5cf6; bottom: 10%; right: 10%;"></div>
    <div id="auth-wall" class="relative z-10 flex items-center justify-center min-h-screen">
        <div class="lux-card p-10 rounded-[2rem] shadow-2xl w-96 text-center">
            <h2 class="text-3xl font-bold mb-8 tracking-tight">Bhodi</h2>
            <input type="email" id="email" placeholder="Email" class="w-full p-4 bg-white/5 border-none rounded-2xl mb-4 focus:ring-2 focus:ring-blue-500 outline-none transition">
            <div class="relative mb-6">
                <input type="password" id="password" placeholder="Password" class="w-full p-4 bg-white/5 border-none rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition">
                <button onclick="togglePassword()" class="absolute right-4 top-4 opacity-50 hover:opacity-100"><i data-lucide="eye" id="eye-icon"></i></button>
            </div>
            <button onclick="auth('signup')" class="w-full text-sm py-3 mb-2 opacity-60 hover:opacity-100 transition">Create Account</button>
            <button onclick="auth('login')" class="w-full bg-blue-600 py-4 rounded-2xl font-semibold hover:bg-blue-500 transition shadow-lg shadow-blue-900/20">Login</button>
        </div>
    </div>
    <div id="main-content" class="hidden relative z-10 p-10">
        <div class="absolute top-10 right-10 flex items-center gap-4">
            <input type="text" id="search-input" onkeyup="searchTools()" placeholder="Search tools..." class="hidden p-3 bg-white/5 rounded-full border-none outline-none focus:ring-2 focus:ring-blue-500">
            <button onclick="toggleSearch()" class="p-3 bg-white/5 hover:bg-white/10 rounded-full transition"><i data-lucide="search"></i></button>
        </div>
        <h1 class="text-5xl font-light text-center mb-12 tracking-[0.2em] uppercase text-white/90">Bhodi</h1>
        <div class="flex flex-wrap justify-center gap-3 mb-12">
            <button onclick="filterTools('All')" class="filter-btn bg-blue-600 px-6 py-2.5 rounded-full font-medium transition">All</button>
            <button onclick="filterTools('Student')" class="filter-btn bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-full font-medium transition">Student</button>
            <button onclick="filterTools('Engineer')" class="filter-btn bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-full font-medium transition">Engineer</button>
            <button onclick="filterTools('Editor')" class="filter-btn bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-full font-medium transition">Editor</button>
            <button onclick="filterTools('Teacher')" class="filter-btn bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-full font-medium transition">Teacher</button>
            <button onclick="filterTools('Doctor')" class="filter-btn bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-full font-medium transition">Doctor</button>
        </div>
        <div id="tool-list" class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto"></div>
    </div>
    <script>
        const allTools = """ + str(AI_TOOLS).replace("'", '"') + """;
        const categoryConfig = { 'Student': {'color': 'blue', 'icon': 'book-open'}, 'Engineer': {'color': 'emerald', 'icon': 'code'}, 'Editor': {'color': 'violet', 'icon': 'film'}, 'Teacher': {'color': 'amber', 'icon': 'graduation-cap'}, 'Doctor': {'color': 'rose', 'icon': 'stethoscope'}, 'General': {'color': 'slate', 'icon': 'bot'} };
        function togglePassword() { const p = document.getElementById('password'); p.type = p.type === 'password' ? 'text' : 'password'; }
        function toggleSearch() { const input = document.getElementById('search-input'); input.classList.toggle('hidden'); input.focus(); }
        function searchTools() { const val = document.getElementById('search-input').value.toLowerCase(); render(allTools.filter(t => t.name.toLowerCase().includes(val))); }
        async function auth(type) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            if(!email || !password) return alert("Please enter credentials");
            const res = await fetch('/' + type, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({email, password}) });
            const data = await res.json();
            if (data.status === 'success') {
                if(type === 'signup') alert("Account created!");
                else { document.getElementById('auth-wall').classList.add('hidden'); document.getElementById('main-content').classList.remove('hidden'); render(allTools); }
            } else { alert(data.message); }
        }
        function filterTools(cat) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.className = btn.innerText === cat ? 'filter-btn bg-blue-600 px-6 py-2.5 rounded-full font-medium transition' : 'filter-btn bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-full font-medium transition');
            render(cat === 'All' ? allTools : allTools.filter(t => t.cat === cat));
        }
        function render(list) {
            document.getElementById('tool-list').innerHTML = list.map(t => {
                const config = categoryConfig[t.cat] || categoryConfig['General'];
                return `<div class="lux-card p-8 rounded-[2rem] border-l-4 border-${config.color}-500 hover:shadow-2xl hover:shadow-${config.color}-500/20 transition group">
                    <div class="mb-4 text-${config.color}-400"><i data-lucide="${config.icon}"></i></div>
                    <h3 class="font-bold text-xl mb-1">${t.name}</h3>
                    <p class="text-${config.color}-400 text-xs font-semibold uppercase tracking-widest mb-4">${t.cat}</p>
                    <p class="text-gray-400 text-sm mb-6">${t.desc}</p>
                    <button onclick="window.open('${t.url}', '_blank')" class="w-full py-3 bg-white/5 hover:bg-${config.color}-600 rounded-xl transition font-semibold">Visit Portal</button>
                </div>`;
            }).join('');
            lucide.createIcons();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return HTML_CODE

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(email=data['email']).first(): return jsonify({"status": "error", "message": "User exists"})
    db.session.add(User(email=data['email'], password=generate_password_hash(data['password'])))
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']): return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid"})

if __name__ == '__main__':
    app.run(debug=True)
