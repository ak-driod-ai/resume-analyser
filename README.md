# Resume Analyzer

An AI-powered resume analysis tool that compares candidate resumes against a job description and generates a technical match score, matched skills, missing skills, project-based matches, and an overall hiring-oriented assessment.

## 🚀 Features

* **AI-powered Job Description Analysis**

  * Extracts required skills
  * Extracts preferred skills
  * Extracts all relevant technical skills
  * Identifies responsibilities and educational requirements

* **Intelligent Resume Parsing**

  * Extracts candidate information
  * Identifies technical skills
  * Reads project descriptions
  * Extracts technologies used in projects
  * Analyzes work experience
  * Extracts certifications and education

* **Project-Based Skill Detection**

  * Skills are not limited to the resume's `Skills` section.
  * Technologies mentioned in projects are also considered.
  * For example, a project mentioning TCP/IP, TLS, QUIC, or PCAP can contribute those technologies to the candidate's skill profile.

* **Comprehensive JD Matching**

  * Compares the complete candidate skill set against the JD.
  * Identifies exact matches.
  * Identifies project-based matches.
  * Identifies experience-based matches.
  * Identifies partial/related matches.
  * Identifies missing important skills.

* **AI Match Score**

  * Generates an overall score from 0–100.
  * Considers technical skills, projects, experience, education, certifications, and job responsibilities.

* **Streaming AI Analysis**

  * Uses Groq streaming to progressively display the AI-generated matching analysis instead of waiting for the complete response.

* **Multiple Resume Evaluation**

  * Processes multiple PDF/DOCX resumes from the `resumes` directory.
  * Ranks candidates according to their match score.

## 🏗️ Architecture

```text
                    Job Description
                           │
                           ▼
                  ┌─────────────────┐
                  │   JD Parser     │
                  │     Groq        │
                  └────────┬────────┘
                           │
                           ▼
                   JD Skills & Data
                           │
                           │
Resume PDF/DOCX ───────────┤
                           ▼
                  ┌─────────────────┐
                  │ Resume Parser   │
                  │     Groq        │
                  └────────┬────────┘
                           │
                           ▼
                 Candidate Skill Set
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          Skills        Projects     Experience
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Skill Matching  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Match Scoring  │
                  └────────┬────────┘
                           │
                           ▼
               Final Candidate Analysis
```

## 🛠️ Tech Stack

* **Python**
* **Groq API**
* **OpenAI GPT OSS 120B via Groq**
* **Pydantic**
* **PyPDF**
* **python-docx**
* **python-dotenv**
* **uv** for Python dependency management

## 📁 Project Structure

```text
resume-analyser/
│
├── resume_parser.py       # Main resume analysis application
├── pyproject.toml         # Project dependencies/configuration
├── README.md              # Project documentation
├── .env                   # API key - kept local
│
├── resumes/
│   ├── resume1.pdf
│   ├── resume2.pdf
│   └── resume3.docx
│
└── .venv/                 # Local virtual environment
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ak-driod-ai/resume-analyser.git
cd resume-analyser
```

### 2. Install dependencies

Using `uv`:

```bash
uv sync
```

This creates the project's virtual environment and installs the required dependencies.

## 🔑 API Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

The application reads the API key using `python-dotenv`.

> **Important:** Never commit your `.env` file or expose your Groq API key publicly.

## 📄 Adding Resumes

Create or use the existing:

```text
resumes/
```

directory.

Add candidate resumes in:

* `.pdf`
* `.docx`

format.

Example:

```text
resumes/
├── candidate1.pdf
├── candidate2.pdf
└── candidate3.docx
```

The application processes all supported resumes inside this directory.

## ▶️ Running the Application

Run:

```bash
uv run python resume_parser.py
```

The application will:

1. Analyze the job description.
2. Extract JD requirements and skills.
3. Read each resume.
4. Extract candidate information.
5. Identify skills from the entire resume.
6. Extract technologies from projects.
7. Compare candidate skills against JD skills.
8. Generate a match score.
9. Display matching and missing skills.
10. Rank candidates based on their scores.

## 📊 Example Output

```text
============================================================
ANALYZING JOB DESCRIPTION
============================================================

✓ Job description analyzed

Required Skills:
Python, Java, Golang, JavaScript

All JD Skills:
Python, Java, Golang, JavaScript, AI/ML, APIs, Big Data

============================================================
PROCESSING: candidate.pdf
============================================================

🧠 Extracting resume information...

✓ Resume parsed
✓ Candidate: Candidate Name

Extracted Skills:
Python, C++, SQL, Git, APIs

Project Technologies:
Deep Packet Inspection: C++, TCP/IP, TLS, QUIC, PCAP

============================================================
🔍 MATCHING RESUME WITH JOB DESCRIPTION
============================================================

🤖 AI analysis:

...

Match Score: 82/100

Matching Skills:
✓ Python
✓ APIs

Project Matching Skills:
✓ TCP/IP
✓ TLS

Missing Important Skills:
✗ Java
✗ Golang
✗ AI/ML
```

## 🧠 How Skill Matching Works

The analyzer does not rely only on a candidate's dedicated Skills section.

The candidate's technical profile can be built from:

```text
Skills
  +
Projects
  +
Project Technologies
  +
Work Experience
  +
Internships
  +
Certifications
```

This is then compared against the complete technical skill set extracted from the job description.

### Example

If a resume contains:

```text
Project: Deep Packet Inspection

Built a packet analyzer using C++ and PCAP.
Parsed TCP, TLS and QUIC network traffic.
```

The analyzer can identify:

```text
C++
PCAP
TCP
TLS
QUIC
```

as relevant candidate technologies even if they were not separately listed under `Skills`.

## 📈 Candidate Ranking

When multiple resumes are present, candidates are sorted by their overall match score:

```text
1. Candidate A → 89/100
2. Candidate B → 82/100
3. Candidate C → 71/100
```

This makes the tool useful for initial resume screening and candidate prioritization.

## 🔐 Security

The following files should remain local and should **not** be committed:

```text
.env
.venv/
__pycache__/
*.pyc
```

The `.env` file contains the Groq API key and must never be uploaded to GitHub.

## 🔮 Future Improvements

Potential future improvements include:

* Web-based UI
* Resume and JD file upload
* Interactive match dashboard
* Skill-match visualizations
* Resume recommendations
* ATS compatibility analysis
* Custom scoring weights
* Multiple JD support
* Candidate filtering
* Exportable candidate reports
* Persistent candidate history

## 👨‍💻 Author

**Ak Droid AI**

Built as an AI-powered resume-to-job-description matching project using Python, Groq, Pydantic, and document parsing tools.

## ⭐ Project Goal

The goal of this project is to build an intelligent resume screening system that goes beyond keyword matching by analyzing the **context of skills across projects, experience, and the complete resume** and comparing them against the requirements of a job description.
