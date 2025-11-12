# 🚀 TMC CV Optimizer

**AI-Powered Professional CV Optimization System**

Advanced CV generation platform powered by Claude Sonnet 4.5, featuring intelligent matching analysis, OCR support, and specialized Morgan Stanley compliance mode.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.40+-red.svg)](https://streamlit.io)

---

## ✨ Core Features

### 📄 Universal Document Processing
- **Multi-format support**: PDF, DOCX, DOC, TXT
- **OCR technology**: Automatic text extraction from scanned PDFs using Tesseract
- **Smart text box extraction**: Captures content from Word text boxes and complex layouts
- **Bilingual optimization**: French & English CV generation with language-specific formatting

### 🤖 AI-Powered Intelligence
- **Claude Sonnet 4.5**: Latest Anthropic model for deep semantic analysis
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

### Render.com (Production)

1. **Fork** this repository to your GitHub account
2. **Create a new Web Service** on [Render](https://render.com)
3. **Connect** your GitHub repository
4. **Configure** build settings:
   ```bash
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
5. **Add environment variables**:
   - `ANTHROPIC_API_KEY`: Your Claude API key (from [console.anthropic.com](https://console.anthropic.com))
   - `APP_PASSWORD`: Login password for the app
   - `AIRTABLE_API_KEY`: (Optional) For usage analytics tracking
   - `TMC_TEMPLATE_PATH`: (Optional) Custom template directory path
6. **Deploy!** 🎉

### Local Development

```bash
# Clone repository
git clone https://github.com/abecassiskevin-dot/tmc-cv-optimizer.git
cd tmc-cv-optimizer

# Install dependencies
pip install -r requirements.txt

# Install OCR dependencies (for scanned PDFs)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra poppler-utils

# macOS:
brew install tesseract poppler

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
| `ANTHROPIC_API_KEY` | Claude API key from Anthropic | ✅ Yes | - |
| `APP_PASSWORD` | Password for app access | ✅ Yes | - |
| `AIRTABLE_API_KEY` | For usage analytics (optional) | ⚠️ Optional | - |
| `TMC_TEMPLATE_PATH` | Custom template directory | ⚠️ Optional | `./branding/templates/` |

---

## 🛠️ Tech Stack

### Backend
- **AI Engine**: Anthropic Claude Sonnet 4.5 (API version 0.25.9+)
- **Document Processing**: python-docx, docxtpl, PyPDF2, docxcompose
- **OCR**: pytesseract, pdf2image, Pillow
- **Template Engine**: Jinja2 with custom filters

### Frontend
- **Framework**: Streamlit 1.40+
- **UI Components**: Custom CSS, responsive design
- **Session Management**: Streamlit session state

### Infrastructure
- **Deployment**: Render.com, Docker support
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

### Example 2: Stack Mismatch (Score: 42/100)
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

**1. Template not found**
```bash
# Solution: Set custom template path
export TMC_TEMPLATE_PATH="/path/to/templates"
```

**2. OCR not working**
```bash
# Install Tesseract
sudo apt-get install tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng

# Verify installation
tesseract --version
```

**3. API timeout errors**
```
⏱️ Timeout - The system automatically retries up to 3 times.
If persistent, try with a shorter CV or contact support.
```

**4. JSON parsing errors**
```
🔧 Automatic correction - The system asks Claude to fix malformed JSON.
If it fails after 3 retries, check API logs.
```

---

## 👨‍💻 Author

**Kevin Abecassis**  
Business Manager & Automation Specialist @ TMC  
Founder of Ekinext (Automation Consulting)

**Technologies**: Power Automate, Airtable, Make.com, Streamlit, Claude AI, Python  
**Focus**: Business process automation, recruitment technology, AI-powered workflows

---

## 📝 Version History

| Version | Date | Key Features |
|---------|------|--------------|
| **v1.3.9** | 2025-01 | Ultra-strict scoring system, algorithmic consistency |
| **v1.3.4** | 2025-01 | Morgan Stanley 3-part mode, table width fixes |
| **v1.3.2** | 2024-12 | Anonymous mode + bilingual support |
| **v1.3.1** | 2024-12 | Two-step generation workflow |
| **v1.3.0** | 2024-11 | Client selector feature |
| **v1.0** | 2024-10 | Initial production release |

---

## 🔮 Roadmap

- [ ] Multi-language support (Spanish, German)
- [ ] Custom template builder UI
- [ ] Batch processing (multiple CVs)
- [ ] API endpoint for programmatic access
- [ ] Advanced analytics dashboard
- [ ] ATS compatibility checker

---

## 📄 License

**Internal TMC use only - All rights reserved**

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 🙏 Acknowledgments

- **Anthropic**: Claude Sonnet 4.5 API
- **TMC Recruitment Team**: Feature requirements and testing
- **Open Source Community**: python-docx, Streamlit, Tesseract OCR

---

**Made with ❤️ for TMC Recruiters**

*Need help? Contact Kevin Abecassis @ TMC Montreal*
