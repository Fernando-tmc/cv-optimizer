# 🚀 TMC CV Optimizer

**AI-Powered Professional CV Optimization System**

Advanced CV generation platform featuring intelligent matching analysis, OCR support, and specialized Morgan Stanley compliance mode. Developed by TMC for TMC recruiters and business managers.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.37+-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

---

## ✨ Core Features

### 📄 Universal Document Processing
- **Multi-format support**: PDF, DOCX, DOC, TXT
- **OCR technology**: Automatic text extraction from scanned PDFs using Tesseract
- **Smart text box extraction**: Captures content from Word text boxes and complex layouts
- **Bilingual optimization**: French & English CV generation with language-specific formatting

### 🤖 AI-Powered Intelligence
- **Latest AI model**: Anthropic's most advanced language model for deep semantic analysis
- **Ultra-strict scoring system V1.3.9**: Algorithmic, reproducible matching analysis (0-100)
- **Weighted domain analysis**: Prioritizes critical skills based on job requirements
- **Two-step generation**: Separate analysis and enrichment for optimal results

### 🎯 Specialized Modes

#### Standard TMC Mode
- Professional TMC-branded DOCX templates
- Smart keyword bolding (3-5 critical technologies only)
- Categorized skills matrix with concise descriptions
- Anonymous mode for blind recruitment

#### Morgan Stanley Compliance Mode
- **3-part structure**: Cover page + Skills Matrix + Detailed content
- **Automatic table width correction**: Prevents formatting issues after merge
- **Margin alignment**: Ensures consistent page layout
- **Empty paragraph removal**: Professional spacing in merged documents

### 📊 Advanced Scoring System

**V1.3.9 Ultra-Strict Methodology**
- Algorithmic scoring (0-100 scale) for absolute consistency
- 5-8 weighted domains based on JD analysis
- Mathematical ponderation formula with JD frequency analysis
- Strict gap detection (stack incompatibilities scored at 0%)
- Comprehensive synthesis in English (80-120 words)

---

## 🏗️ Project Structure

```
tmc-cv-optimizer/
├── app.py                              # Streamlit web interface
├── tmc_cv_enricher.py                  # Core CV processing engine
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Docker container configuration
├── README.md                           # Documentation (you are here)
│
├── .streamlit/
│   └── config.toml                     # Streamlit configuration
│
├── .devcontainer/                      # VS Code Dev Container setup
├── .gitignore                          # Git ignore rules
│
├── branding/
│   └── templates/
│       ├── TMC_NA_template_FR.docx                    # French standard
│       ├── TMC_NA_template_FR_Anonymisé.docx         # French anonymous
│       ├── TMC_NA_template_EN.docx                    # English standard
│       ├── TMC_NA_template_EN_Anonymisé.docx         # English anonymous
│       ├── TMC_NA_template_EN_Anonymise_CoverPage.docx   # MS cover
│       └── TMC_NA_template_EN_Anonymise_Content.docx     # MS content
│
└── assets/
    ├── TMC big logo.png                # TMC logo (large)
    └── TMC mini logo.png               # TMC logo (small)
```

---

## 🚀 Deployment

### Option 1: Render.com with Docker (Production - Recommended)

**Prerequisites:**
- GitHub account
- Render.com account (free tier available)
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

**Steps:**

1. **Fork this repository** to your GitHub account or TMC organization

2. **Create a new Web Service** on [Render](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Docker deployment**:
   - **Environment**: `Docker`
   - **Dockerfile path**: `./Dockerfile` (default)
   - **Instance type**: Choose based on usage (Free tier works for testing)

4. **Add environment variables** in Render dashboard:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxx        # Required - Your Anthropic API key
   APP_PASSWORD=your_secure_password      # Required - Login password for the app
   AIRTABLE_API_KEY=keyxxxxx             # Optional - For usage analytics
   TMC_TEMPLATE_PATH=/app/branding/templates/  # Optional - Custom path
   ```

5. **Deploy!** 
   - Render will automatically:
     - Build the Docker image
     - Install system dependencies (Tesseract OCR, poppler-utils)
     - Install Python packages
     - Start the Streamlit application
   
6. **Access your app** at `https://your-app-name.onrender.com`

**Important Notes:**
- ✅ Docker handles all dependencies automatically
- ✅ No need for `render.yaml`, `build.sh`, or `apt-packages` files
- ✅ Dockerfile installs Tesseract OCR for scanned PDF support
- ⚠️ Free tier: Apps sleep after 15 minutes of inactivity (30-60s cold start)

---

### Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- Docker (optional but recommended)

#### Method A: Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/YOUR_ORG/tmc-cv-optimizer.git
cd tmc-cv-optimizer

# Create .env file with your credentials
cat > .env << EOF
ANTHROPIC_API_KEY=your-api-key-here
APP_PASSWORD=your-password-here
EOF

# Build Docker image
docker build -t tmc-cv-optimizer .

# Run container
docker run -p 8501:8501 --env-file .env tmc-cv-optimizer

# Access app at http://localhost:8501
```

#### Method B: Native Python Installation

```bash
# Clone repository
git clone https://github.com/YOUR_ORG/tmc-cv-optimizer.git
cd tmc-cv-optimizer

# Install Python dependencies
pip install -r requirements.txt

# Install OCR dependencies (for scanned PDFs)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra poppler-utils

# macOS:
brew install tesseract poppler

# Windows:
# Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases

# Set environment variables
export ANTHROPIC_API_KEY="your-api-key"
export APP_PASSWORD="your-password"

# Run application
streamlit run app.py
```

---

## 🔐 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ANTHROPIC_API_KEY` | API key from Anthropic console | ✅ Yes | - |
| `APP_PASSWORD` | Password for app access | ✅ Yes | - |
| `AIRTABLE_API_KEY` | For usage analytics (optional) | ⚠️ Optional | - |
| `TMC_TEMPLATE_PATH` | Custom template directory | ⚠️ Optional | `./branding/templates/` |

**Getting your Anthropic API Key:**
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to "API Keys" section
4. Create a new key
5. Copy and save it securely (you won't see it again)

---

## 🛠️ Tech Stack

### Backend
- **AI Engine**: Anthropic API (Sonnet 4.5 model)
- **Document Processing**: python-docx, docxtpl, PyPDF2, docxcompose
- **OCR**: pytesseract, pdf2image, Pillow
- **Template Engine**: Jinja2 with custom filters

### Frontend
- **Framework**: Streamlit 1.37+
- **UI Components**: Custom CSS with TMC branding
- **Session Management**: Cookie-based authentication

### Infrastructure
- **Deployment**: Render.com with Docker
- **Container**: Python 3.11-slim base image
- **Analytics**: Airtable integration (optional)
- **Storage**: Ephemeral (in-memory processing, auto-cleanup)

---

## 📊 Feature Breakdown

### 1. Intelligent CV Parsing
- **Universal extraction**: Handles any CV format (PDF, Word, TXT)
- **OCR fallback**: Automatic detection of scanned PDFs with Tesseract processing
- **Structured data**: Extracts name, title, profile, skills, experiences, education, certifications
- **Language detection**: Identifies and adapts to French/English content

### 2. Ultra-Strict Matching Analysis (V1.3.9)
```
🎯 Scoring Philosophy:
- Algorithmic: Same CV + JD = Same score every time
- Strict: If you hesitate between scores → take the lower one
- Evidence-based: Every point must be justified by CV facts
- Reproducible: Acts like an algorithm, not a human

📊 Domain Identification:
1. Scan JD for all technical terms
2. Count exact frequency of each technology
3. Apply mathematical ponderation formula:
   Weight = (JD_Mentions × 10) + (Required_Level × 5) + Context_Bonus
4. Create 5-8 domains totaling exactly 100%

🎯 Scoring Grid (per domain):
- 0-15: Minimal/No competence
- 20-35: Junior level (0-1 years)
- 40-55: Intermediate (1-3 years)
- 60-75: Senior/Confirmed (3-7 years)
- 80-90: Expert (7-10+ years, industry recognition)
- 95-100: World-class (reserved for legends)

⚠️ Critical Rules:
- Stack mismatch (Java vs .NET) → 0 points (non-negotiable)
- No practical experience → max 30 points
- No metrics/quantified results → max 50 points
- Score_matching = exact sum of all domain scores
```

### 3. AI-Powered Enrichment
- **Smart rewriting**: Adapts experience bullets to match JD keywords
- **Professional titles**: Adjusts job titles for better alignment
- **Categorized skills**: Organizes competencies into 5-6 logical categories
- **Selective bolding**: Highlights only 3-5 critical technologies (not entire phrases)
- **Concise descriptions**: 2-3 lines max per skill (100-150 characters)

### 4. Morgan Stanley Mode (V1.3.4+)
```
3-Part Structure:
┌─────────────────────────────────┐
│  Part 1: Cover Page             │
│  - Photo placeholder            │
│  - Name (UPPERCASE)             │
│  - Professional title           │
│  - Location & Languages         │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│  Part 2: Skills Matrix          │
│  - Client-uploaded table        │
│  - Auto-corrected width         │
│  - Aligned margins              │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│  Part 3: Detailed Content       │
│  - Profile summary              │
│  - Categorized skills           │
│  - Work experience              │
│  - Education & certifications   │
└─────────────────────────────────┘

Technical Fixes Applied:
✅ Table width: Fixed → Auto (prevents horizontal shift)
✅ Empty paragraphs removed (clean spacing)
✅ Margins aligned across all sections
✅ Professional page breaks
```

### 5. Anonymous Mode
- **Privacy-first**: Removes name, contact information
- **Blind recruitment**: Complies with anti-discrimination requirements
- **Optional toggle**: Enable/disable per generation

### 6. Professional TMC Formatting
- **Brand compliance**: TMC logo, colors, fonts
- **Clean layout**: Recruiter-friendly, scannable design
- **RichText bolding**: Smart keyword highlighting with proper XML escaping
- **XML safety**: Handles special characters (®, &, <, >, etc.)

---

## 🔒 Privacy & Security

- ✅ **Ephemeral processing**: All data processed in-memory
- ✅ **No persistent storage**: Files auto-deleted after generation
- ✅ **Secure API**: TLS-encrypted communication with Anthropic
- ✅ **Password protection**: Authentication required for app access
- ✅ **Session isolation**: Multi-user support with isolated sessions
- ✅ **GDPR-friendly**: No personal data retention

---

## 📈 Usage Analytics (Optional)

When `AIRTABLE_API_KEY` is configured, the system tracks:

| Metric | Purpose |
|--------|---------|
| Candidate name | Identify unique profiles (anonymized if needed) |
| Matching score | Performance analytics (0-100) |
| Language selection | Usage patterns (French vs English) |
| Processing time | Performance monitoring |
| Token consumption | Cost analysis |
| User location | Geographic insights |
| Template used | Mode distribution (Standard vs MS) |

**Note**: Analytics are opt-in and can be disabled by removing the API key.

---

## 🎯 Scoring Examples

### Example 1: Strong Match (Score: 78/100)
```
JD: Senior .NET Developer (C#, Azure, SQL Server)
Candidate: 6 years .NET, 4 years Azure, proven leadership

Domain Breakdown:
├─ .NET Stack (40%): 32/40 ✅ (80% - senior level)
├─ Cloud Azure (25%): 18/25 ✅ (72% - confirmed)
├─ SQL Server (15%): 12/15 ✅ (80% - strong)
├─ DevOps/CI-CD (10%): 8/10 ✅ (80% - good)
└─ Agile/Scrum (10%): 8/10 ✅ (80% - experienced)

Total: 78/100 (GOOD MATCH)
```

### Example 2: Stack Mismatch (Score: 36/100)
```
JD: Senior .NET Developer (C#, Azure, SQL Server)
Candidate: 8 years Java, AWS expert, PostgreSQL

Domain Breakdown:
├─ .NET Stack (40%): 0/40 ❌ (incompatible - Java only)
├─ Cloud Azure (25%): 10/25 ⚠️ (AWS transferable)
├─ SQL Server (15%): 10/15 ✅ (SQL transferable)
├─ DevOps/CI-CD (10%): 8/10 ✅ (cloud-agnostic)
└─ Agile/Scrum (10%): 8/10 ✅ (experienced)

Total: 36/100 (WEAK MATCH - major reconversion needed)
Recommendation: PASS - critical stack incompatibility
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Docker build fails**
```bash
# Solution: Check Docker daemon is running
docker ps

# If not running:
# Windows/Mac: Start Docker Desktop
# Linux: sudo systemctl start docker
```

**2. Template not found errors**
```bash
# Solution: Verify template path in environment variables
# In Docker, templates are at: /app/branding/templates/
# Locally: ./branding/templates/

# Check if templates exist:
ls -la branding/templates/
```

**3. OCR not working on scanned PDFs**
```bash
# In Docker: Already installed automatically
# Locally, verify Tesseract installation:
tesseract --version

# If missing, install:
# Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-fra
# Mac: brew install tesseract
```

**4. API timeout errors**
```
⏱️ Timeout - The system automatically retries up to 3 times.
If persistent:
- Check your internet connection
- Verify API key is valid
- Try with a shorter CV (< 10 pages)
- Check Anthropic API status: status.anthropic.com
```

**5. Application won't start**
```bash
# Check environment variables are set:
docker exec -it <container-id> env | grep ANTHROPIC

# Check logs:
docker logs <container-id>

# On Render: Check "Logs" tab in dashboard
```

**6. JSON parsing errors**
```
🔧 Automatic correction - The system asks AI to fix malformed JSON.
If it fails after 3 retries:
- This is usually a temporary API issue
- Check Anthropic API status
- Retry the generation
```

---

## 🤝 Contributing

This is an internal TMC tool, but contributions from the team are welcome!

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- ✅ Test locally before pushing
- ✅ Update README if adding new features
- ✅ Follow existing code style (Python PEP 8)
- ✅ Add comments for complex logic
- ✅ Update version number in `app.py` header

### Reporting Issues

Found a bug or have a feature request?

1. Check existing issues on GitHub
2. Create a new issue with:
   - Clear title
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if relevant
   - Your environment (Docker/local, Render/local)

---

## 👨‍💻 Development Team

**Created by:**  
**Kevin Abecassis**  
Business Manager & Automation Specialist @ TMC  
Founder of Ekinext (Automation Consulting)

**Technologies**: Python, Streamlit, Docker, Anthropic API, Airtable  
**Focus**: Business process automation, recruitment technology, AI-powered workflows

**Contact**: [Your TMC email or Slack]

---

## 📝 Version History

| Version | Date | Key Features |
|---------|------|--------------|
| **v1.3.9** | Jan 2025 | Ultra-strict scoring system, algorithmic consistency |
| **v1.3.4** | Jan 2025 | Morgan Stanley 3-part mode, table width fixes, Docker deployment |
| **v1.3.2** | Dec 2024 | Anonymous mode + bilingual support |
| **v1.3.1** | Dec 2024 | Two-step generation workflow |
| **v1.3.0** | Nov 2024 | Client selector feature |
| **v1.0** | Oct 2024 | Initial production release |

---

## 🔮 Roadmap

### In Progress
- [ ] Performance optimizations (faster generation)
- [ ] Better error handling and user feedback

### Planned Features
- [ ] Multi-language support (Spanish, German)
- [ ] Custom template builder UI
- [ ] Batch processing (multiple CVs at once)
- [ ] API endpoint for programmatic access
- [ ] Advanced analytics dashboard
- [ ] ATS compatibility checker
- [ ] CV comparison tool (side-by-side)
- [ ] Skills gap analysis report

### Ideas (Vote with 👍)
- Integration with ATS systems
- Mobile app version
- Browser extension for LinkedIn
- Automated JD parsing from job boards

**Want to suggest a feature?** Open an issue with the "enhancement" label!

---

## 📄 License

**Internal TMC use only - All rights reserved**

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

For licensing inquiries, contact TMC management.

---

## 🙏 Acknowledgments

- **TMC Recruitment Team**: Feature requirements, testing, and feedback
- **Anthropic**: AI API and technical support
- **Open Source Community**: python-docx, Streamlit, Tesseract OCR, Docker

Special thanks to all TMC team members who provided feedback during development!

---

## 📞 Support

**Need help?**

1. 📖 Check this README first
2. 🔍 Search existing GitHub issues
3. 💬 Ask in TMC Slack channel: #cv-optimizer-support
4. 📧 Contact Kevin Abecassis @ TMC Montreal

**For urgent production issues:**
- Slack: @kevin.abecassis
- Email: [your-tmc-email]

---

**Made with ❤️ for TMC Recruiters by TMC**

*Empowering recruitment through AI automation*
