import json
import os
import time
from pathlib import Path
from typing import List, Optional

from docx import Document
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API ERROR: GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

# FULL Job Description restored
job_description = """ 
About American Express:  
At American Express, our culture is built on a 175-year history of innovation, shared values and 
Leadership Behaviors, and an unwavering commitment to back our customers, communities, and 
colleagues. As part of Team Amex, you’ll experience this powerful backing with comprehensive 
support for your holistic well-being and many opportunities to learn new skills, develop as a leader, and 
grow your career.  
Here, your voice and ideas matter, your work makes an impact, and together, you will help us define 
the future of American Express. 
Amex Flex: 
We back our colleagues with the support they need to thrive, professionally and personally. That’s why 
we have Amex Flex, our enterprise working model, that provides greater flexibility to colleagues while 
ensuring we preserve the important aspects of our unique in-person culture. Depending on role and 
business needs, colleagues will either work onsite, in a hybrid model (combination of in-office and virtual 
days) or fully virtual. 
Business Overview:  
Innovation is at the heart of everything we do. Every single day, our technologists enable our customers 
around the globe to achieve their goals. They design and deliver American Express infrastructure and 
applications across all markets and business units. To meet these demands, we’re looking for problem 
solvers who can get results through precise analysis and programming methodologies, individuals with 
a strong intellectual curiosity and a passion for innovation, and teammates who can convert their ideas 
into execution.  
Join the Engineering teams and make an impact right away:  
• Develop highly scalable and mission critical applications and platforms using modern Cloud 
Technologies and Programming Languages (e.g., Java, Golang, Python, JavaScript) 
• Function as core members of agile teams building products and solutions on a wide range of 
technology domains including Distributed Real-time Transaction Processing, Big Data and 
Analytics, AI/ML, omnichannel capabilities on native iOS, Android, Social Integration and 
Services/APIs. 
• Work in collaboration with highly talented engineers in day-to-day activities and help in reviewing 
design, coding, and the other Software Development Life Cycle tasks. 
• Be part of a culture of innovation and experimentation, constantly pursue and learn industry 
leading/innovative technologies and solutions and always be ready to try new concepts without 
fear of failure. 
We have the know-how, technology, and global reach to make nearly any idea a reality. All that’s missing 
is you! Do you have?  
• Passion for technology and strong desire to learn 
• Curious mind to explore new possibilities and act on them 
• Never-settle attitude and continuously looking for improvements  
• Customer-focus to think differently and deliver value to customers  
• Data-driven nature to drive decisions and results based on data 
Minimum Qualifications: 
• Strong technical skills, problem-solving, and analytical abilities. 
• Proficient programming and coding skills 
• Ability to work independently on complex problems. 
• Strong communication and critical thinking 
• Proficiency in partner collaboration and cross-functional teamwork. 
• Critical thinking with a business-first approach. 
• Ability to prioritize well, communicate clearly and compellingly 
• Demonstrate creativity and self-sufficiency along with strong interpersonal/ collaborative skills 
and experience working in global teams. 
Educational Requirements: 
• The candidate must earn bachelor's or master's degree in computer science, Computer 
Engineering, or other related technical discipline by June/July 2026. 
Job Location: Hybrid - Bengaluru (Karnataka), Gurugram (Haryana) or Chennai (Tamil Nadu) – 
depending on Business requirements 
American Express is an equal opportunity employer and makes employment decisions without regard to 
race, color, religion, sex, sexual orientation, gender identity, national origin, veteran status, disability 
status, age, or any other status protected by law. 
Offer of employment with American Express is conditioned upon the successful completion of a 
background verification check, subject to applicable laws and regulations. 
Campus Benefits 
We back you with benefits that support your holistic well-being so you can be and deliver your best. This 
means caring for you and your loved ones’ physical, financial and mental health, as well as providing the 
flexibility you need to thrive personally and professionally:  
• Competitive base salaries. 
• Flexible work arrangements and schedules with hybrid and virtual options with Amex Flex. 
• Free access to global on-site wellness centers staffed with nurses and doctors. (depending on 
location) 
• Free and confidential counselling support through our Healthy Minds program. 
• Career development and training opportunities.
"""

# Pydantic Schemas
class JobD(BaseModel):
    role: str
    required_skills: List[str]
    preferred_skills: List[str]
    minimum_experience: Optional[float] = None
    education_requirements: List[str]
    responsibilities: List[str]

class MatchResult(BaseModel):
    score: float
    details: dict

class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    skills_used: List[str] = []

class Resume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    total_experience_years: Optional[float] = None
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[str] = []
    projects: List[str] = []
    certifications: List[str] = []


# 1. Parse Job Description
jobd_schema = JobD.model_json_schema()

system_prompt = f"""
You are an expert HR assistant.
Analyze the provided job description and extract structured information into JSON matching this schema:
{jobd_schema}

Rules:
- Output valid JSON only.
- Extract all required and preferred skills mentioned in the job description.
- Set minimum_experience to null if no explicit number of years is stated.
- Fill all list fields properly. Do not return empty lists if information exists.
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Analyze this job description into JSON:\n{job_description}"}
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format={"type": "json_object"}
)

job_data = json.loads(response.choices[0].message.content)
job = JobD(**job_data)

print("Parsed Job Information:")
print("Required Skills:", job.required_skills)
print("Preferred Skills:", job.preferred_skills)
print("-" * 50)


def final_score(job: JobD, resume: Resume) -> MatchResult:
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
    You are an HR recruiter.
    Compare the candidate's parsed resume with the parsed job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dump_json(indent=2)}

    Output valid JSON strictly adhering to this schema:
    {match_schema}

    Ensure 'score' is an overall match percentage float from 0.0 to 100.0 based on how well the candidate's skills, education, and experience match the job requirements.
    Include 'candidate_name', 'matching_skills', 'missing_important_skills', and 'final_verdict' inside the 'details' JSON object.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    return MatchResult(**data)


def parse_resume(resume_text: str) -> Resume:
    resume_schema = Resume.model_json_schema()
    system_prompt = f"""
    You are an expert resume parser.
Extract candidate information into valid JSON matching this schema:
{resume_schema}

Important:
1. Output must be valid JSON format.
2. Extract candidate name accurately.
3. If multiple emails are present, extract only the primary email as a SINGLE string.
4. Extract all skills mentioned throughout the resume.
5. Do not invent information. If missing, return null or empty lists.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Parse this resume into JSON:\n{resume_text}"}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    return Resume(**data)


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def read_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"
    return text


def read_resume(file_path):
    file_path = Path(file_path)
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    else:
        return None


# Run script
resume_folder = Path("resumes")
all_results = []

if resume_folder.exists() and resume_folder.is_dir():
    for file_path in resume_folder.iterdir():
        if file_path.suffix.lower() not in [".pdf", ".docx"]:
            continue
            
        print("\nProcessing:", file_path.name)
        resume_text = read_resume(file_path)
        if not resume_text:
            continue
            
        parsed_resume = parse_resume(resume_text)
        time.sleep(2)
        
        result = final_score(job, parsed_resume)
        time.sleep(2)
        
        candidate_name = parsed_resume.name or file_path.stem
        
        all_results.append({
        "filename": file_path.name,
            "name": candidate_name,
            "score": result.score,
            "details": result.details
        })

    # Sort all candidates by score (highest to lowest)
    all_results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    # NEW: Print results for EVERY uploaded resume
    print("\n" + "=" * 60)
    print("           ALL EVALUATED RESUMES (SCORED)               ")
    print("=" * 60)
    for idx, candidate in enumerate(all_results, 1):
        print(f"\n[{idx}] File: {candidate['filename']}")
        print(f"    Candidate Name: {candidate['name']}")
        print(f"    Score: {candidate['score']}/100")
        print(f"    Details: {json.dumps(candidate['details'], indent=6)}")
        print("-" * 50)

    # Summary section for Top 2 and Worst 2
    top_2 = all_results[:2]
    worst_2 = all_results[-2:][::-1] if len(all_results) >= 2 else []

    print("\n" + "=" * 60)
    print("                SUMMARY HIGHLIGHTS                      ")
    print("=" * 60)

    print("\n🏆 TOP 2 CANDIDATES 🏆")
    print("-" * 60)
    for idx, candidate in enumerate(top_2, 1):
        print(f"{idx}. Name: {candidate['name']} ({candidate['filename']})")
        print(f"   Score: {candidate['score']}/100")

    print("\n⚠️ WORST 2 CANDIDATES ⚠️")
    print("-" * 60)
    for idx, candidate in enumerate(worst_2, 1):
        print(f"{idx}. Name: {candidate['name']} ({candidate['filename']})")
        print(f"   Score: {candidate['score']}/100")