# 🌐 Web Terminal Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud

### Option 1: One-Click Deploy
1. **Fork/Upload** this project to GitHub
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect** your GitHub repo
4. **Set main file** to `app.py`
5. **Deploy!** 🎉

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements_web.txt

# Run the web terminal
streamlit run app.py
```

## 🔧 Configuration

### API Key Setup (Optional)
For full Gemini AI functionality, add your API key to Streamlit secrets:

1. **Local development**: Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

2. **Streamlit Cloud**: Add in app settings:
```
GEMINI_API_KEY = "your_api_key_here"
```

## 🌟 Features in Web Version

### ✅ What Works
- **Natural Language Processing** - Both AI and fallback patterns
- **File Operations** - Create, list, delete files in session directory
- **Interactive Interface** - Click commands or type naturally
- **Session Management** - Each user gets isolated workspace
- **Real-time Updates** - Live terminal output display

### 🔒 Security Features
- **Sandboxed Environment** - Each session isolated in temp directory
- **Safe Commands Only** - Dangerous system commands blocked
- **Session Cleanup** - Temporary files auto-cleaned
- **No File System Access** - Can't access host system files

## 🎯 Demo URLs
Once deployed, share these examples with users:

**Natural Language Examples:**
- "create a file called hello.py"
- "how many files do we have"
- "show me all the files"
- "make a folder named project"

**Traditional Commands:**
- `ls` - List files
- `touch demo.txt` - Create file
- `count` - Count items
- `help` - Show all commands

## 📱 Mobile Friendly
The web terminal works great on:
- 💻 **Desktop** - Full functionality
- 📱 **Mobile** - Touch-friendly interface
- 📟 **Tablet** - Optimized layout

## 🚀 Sharing Your Terminal
Perfect for:
- **Portfolio demos** - Show off your AI terminal
- **Team collaboration** - Everyone can use it
- **Educational purposes** - Teach terminal commands
- **Hackathon judging** - Easy access for judges

---
**Built for CodeMate Hackathon 2025 - Now web accessible! 🏆**