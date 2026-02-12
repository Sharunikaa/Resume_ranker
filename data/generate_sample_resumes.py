"""
Generate sample resumes for testing the resume ranker.
Creates PDFs for both AI Engineer and Senior Python Developer roles.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from pathlib import Path

# AI Engineer Resumes (Most suited to least suited)
ai_engineer_resumes = [
    {
        "filename": "ai_engineer_excellent.pdf",
        "name": "Dr. Aisha Patel",
        "email": "aisha.patel@email.com",
        "phone": "+1-555-0101",
        "summary": "Senior AI Engineer with 8+ years of experience in ML/DL, LLMs, and production AI systems. PhD in Computer Science with focus on NLP. Expert in PyTorch, TensorFlow, and RAG architectures.",
        "skills": [
            "Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning",
            "LLMs (GPT, Gemini, LLaMA)", "Prompt Engineering", "RAG", "LangChain",
            "Vector Databases (FAISS, Pinecone, Chroma)", "FastAPI", "Docker",
            "Kubernetes", "MLOps", "SQL", "NoSQL", "AWS", "Fine-tuning LLMs",
            "Reinforcement Learning", "Hugging Face", "GPU Optimization"
        ],
        "experience": [
            {
                "title": "Senior AI Engineer",
                "company": "TechCorp AI Labs",
                "duration": "2020 - Present",
                "description": "Led development of production LLM systems serving 10M+ users. Built RAG pipelines with 95% accuracy. Fine-tuned LLaMA models for domain-specific tasks. Deployed models on AWS with Docker/Kubernetes. Implemented MLOps practices reducing deployment time by 60%."
            },
            {
                "title": "ML Engineer",
                "company": "DataSystems Inc",
                "duration": "2017 - 2020",
                "description": "Developed deep learning models for NLP tasks. Built data pipelines processing 1TB+ daily. Implemented transformer models achieving SOTA results. Created REST APIs with FastAPI serving 100K+ requests/day."
            },
            {
                "title": "Research Scientist Intern",
                "company": "AI Research Lab",
                "duration": "2016 - 2017",
                "description": "Published 3 papers on neural architecture search. Implemented novel attention mechanisms. Contributed to open-source ML frameworks."
            }
        ],
        "projects": [
            {
                "title": "Enterprise RAG System",
                "description": "Built production RAG system using LangChain, Chroma, and GPT-4. Implemented semantic search with 98% relevance. Deployed on AWS with auto-scaling. Reduced query latency to <100ms."
            },
            {
                "title": "LLM Fine-tuning Framework",
                "description": "Created framework for fine-tuning LLMs (LLaMA, Mistral) with LoRA/QLoRA. Achieved 40% improvement in domain-specific tasks. Open-sourced with 2K+ GitHub stars."
            }
        ],
        "education": [
            {
                "degree": "PhD in Computer Science (AI/ML)",
                "institution": "Stanford University",
                "year": "2016"
            },
            {
                "degree": "M.S. in Computer Science",
                "institution": "MIT",
                "year": "2012"
            }
        ]
    },
    {
        "filename": "ai_engineer_strong.pdf",
        "name": "Raj Kumar",
        "email": "raj.kumar@email.com",
        "phone": "+1-555-0102",
        "summary": "AI Engineer with 5 years of experience in ML, deep learning, and LLM applications. Strong background in PyTorch, RAG systems, and production deployment.",
        "skills": [
            "Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning",
            "LLMs (GPT, Gemini)", "RAG", "Vector Databases (FAISS, Chroma)",
            "FastAPI", "Docker", "SQL", "NoSQL", "AWS", "LangChain",
            "Prompt Engineering", "REST APIs", "Git"
        ],
        "experience": [
            {
                "title": "AI Engineer",
                "company": "AI Solutions Ltd",
                "duration": "2021 - Present",
                "description": "Developed LLM-powered chatbots using GPT-4 and RAG. Built vector search systems with Chroma. Created FastAPI services for ML inference. Deployed models on AWS EC2."
            },
            {
                "title": "ML Engineer",
                "company": "StartupAI",
                "duration": "2019 - 2021",
                "description": "Built CNN models for image classification. Implemented data pipelines with Python. Created REST APIs for model serving. Worked with PyTorch and TensorFlow."
            }
        ],
        "projects": [
            {
                "title": "Chatbot with RAG",
                "description": "Built intelligent chatbot using LangChain, OpenAI, and Pinecone. Implemented context-aware responses. Deployed with Docker on AWS."
            },
            {
                "title": "Image Classification System",
                "description": "Developed CNN model with 94% accuracy. Used PyTorch and transfer learning. Created REST API with FastAPI."
            }
        ],
        "education": [
            {
                "degree": "M.Tech in AI/ML",
                "institution": "IIT Delhi",
                "year": "2019"
            },
            {
                "degree": "B.Tech in Computer Science",
                "institution": "NIT Trichy",
                "year": "2017"
            }
        ]
    },
    {
        "filename": "ai_engineer_good.pdf",
        "name": "Emily Chen",
        "email": "emily.chen@email.com",
        "phone": "+1-555-0103",
        "summary": "ML Engineer with 3 years of experience in machine learning and Python development. Experience with PyTorch, scikit-learn, and building ML pipelines.",
        "skills": [
            "Python", "PyTorch", "scikit-learn", "Machine Learning",
            "Deep Learning", "Pandas", "NumPy", "FastAPI", "Docker",
            "SQL", "Git", "REST APIs", "Data Analysis"
        ],
        "experience": [
            {
                "title": "ML Engineer",
                "company": "DataTech Corp",
                "duration": "2022 - Present",
                "description": "Developed ML models for predictive analytics. Built data pipelines with Python. Created APIs with FastAPI. Worked with PyTorch for deep learning tasks."
            },
            {
                "title": "Data Scientist",
                "company": "Analytics Inc",
                "duration": "2021 - 2022",
                "description": "Analyzed large datasets using Pandas and NumPy. Built classification models with scikit-learn. Created visualizations with Matplotlib."
            }
        ],
        "projects": [
            {
                "title": "Predictive Analytics System",
                "description": "Built ML pipeline for sales forecasting. Used scikit-learn and XGBoost. Achieved 85% accuracy."
            },
            {
                "title": "Image Classifier",
                "description": "Developed CNN with PyTorch. Used transfer learning with ResNet. Deployed with Flask."
            }
        ],
        "education": [
            {
                "degree": "M.S. in Data Science",
                "institution": "UC Berkeley",
                "year": "2021"
            },
            {
                "degree": "B.S. in Computer Science",
                "institution": "UCLA",
                "year": "2019"
            }
        ]
    },
    {
        "filename": "ai_engineer_moderate.pdf",
        "name": "Michael Brown",
        "email": "michael.brown@email.com",
        "phone": "+1-555-0104",
        "summary": "Software Engineer with 2 years of experience and growing interest in AI/ML. Basic knowledge of Python, machine learning, and data analysis.",
        "skills": [
            "Python", "Java", "JavaScript", "Machine Learning (basics)",
            "scikit-learn", "Pandas", "NumPy", "SQL", "Git",
            "REST APIs", "Flask", "Django"
        ],
        "experience": [
            {
                "title": "Software Engineer",
                "company": "WebTech Solutions",
                "duration": "2022 - Present",
                "description": "Developed web applications with Django and Flask. Built REST APIs. Worked with SQL databases. Started learning ML with scikit-learn."
            },
            {
                "title": "Junior Developer",
                "company": "CodeCraft",
                "duration": "2021 - 2022",
                "description": "Built web applications with JavaScript and Python. Created CRUD APIs. Worked in agile teams."
            }
        ],
        "projects": [
            {
                "title": "ML Classification Project",
                "description": "Built simple classification model with scikit-learn. Used logistic regression. Personal learning project."
            },
            {
                "title": "Web Dashboard",
                "description": "Created analytics dashboard with Flask and Plotly. Integrated with PostgreSQL."
            }
        ],
        "education": [
            {
                "degree": "B.S. in Computer Science",
                "institution": "State University",
                "year": "2021"
            }
        ]
    },
    {
        "filename": "ai_engineer_weak.pdf",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1-555-0105",
        "summary": "Recent graduate with basic programming skills. Completed online courses in Python and machine learning. Looking to start career in tech.",
        "skills": [
            "Python (basic)", "Java", "C++", "HTML", "CSS",
            "SQL (basic)", "Git", "Microsoft Office"
        ],
        "experience": [
            {
                "title": "Intern",
                "company": "Local Tech Startup",
                "duration": "Summer 2023",
                "description": "Assisted with web development tasks. Fixed bugs in Python scripts. Learned about software development process."
            }
        ],
        "projects": [
            {
                "title": "Personal Website",
                "description": "Created portfolio website with HTML, CSS, and JavaScript."
            },
            {
                "title": "Simple Calculator",
                "description": "Built calculator application in Python. Learning project from online course."
            }
        ],
        "education": [
            {
                "degree": "B.S. in Information Technology",
                "institution": "Community College",
                "year": "2023"
            }
        ]
    }
]

# Senior Python Developer Resumes (Most suited to least suited)
python_developer_resumes = [
    {
        "filename": "python_dev_excellent.pdf",
        "name": "David Martinez",
        "email": "david.martinez@email.com",
        "phone": "+1-555-0201",
        "summary": "Senior Python Developer with 10+ years of experience in backend systems, APIs, and scalable architectures. Expert in FastAPI, Django, Flask, microservices, and cloud platforms. Strong knowledge of databases, Docker, Kubernetes, and system design.",
        "skills": [
            "Python", "FastAPI", "Django", "Flask", "REST APIs", "GraphQL",
            "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes",
            "AWS", "GCP", "Microservices", "System Design", "CI/CD",
            "Git", "RabbitMQ", "Celery", "SQLAlchemy", "Pytest",
            "Data Structures & Algorithms", "Design Patterns", "Asyncio"
        ],
        "experience": [
            {
                "title": "Senior Python Developer",
                "company": "Enterprise Solutions Inc",
                "duration": "2019 - Present",
                "description": "Architected and built scalable backend systems serving 50M+ users. Designed microservices with FastAPI and Docker. Optimized database queries reducing latency by 70%. Led team of 8 developers. Implemented CI/CD pipelines with GitHub Actions."
            },
            {
                "title": "Python Developer",
                "company": "CloudTech Corp",
                "duration": "2016 - 2019",
                "description": "Developed REST APIs with Django and Flask. Built data pipelines processing 10TB+ daily. Implemented caching with Redis. Deployed on AWS with auto-scaling. Mentored junior developers."
            },
            {
                "title": "Backend Developer",
                "company": "StartupHub",
                "duration": "2014 - 2016",
                "description": "Built backend services with Python and PostgreSQL. Created RESTful APIs. Implemented authentication and authorization. Worked with message queues (RabbitMQ)."
            }
        ],
        "projects": [
            {
                "title": "High-Performance API Gateway",
                "description": "Built API gateway handling 1M+ requests/day with FastAPI. Implemented rate limiting, caching, and authentication. Deployed on Kubernetes with auto-scaling. Achieved 99.99% uptime."
            },
            {
                "title": "Real-time Data Pipeline",
                "description": "Created data pipeline with Python, Kafka, and PostgreSQL. Processed 100K+ events/second. Implemented monitoring with Prometheus and Grafana."
            }
        ],
        "education": [
            {
                "degree": "M.S. in Computer Science",
                "institution": "Carnegie Mellon University",
                "year": "2014"
            },
            {
                "degree": "B.S. in Software Engineering",
                "institution": "University of Michigan",
                "year": "2012"
            }
        ]
    },
    {
        "filename": "python_dev_strong.pdf",
        "name": "Priya Sharma",
        "email": "priya.sharma@email.com",
        "phone": "+1-555-0202",
        "summary": "Python Developer with 6 years of experience in backend development, APIs, and databases. Proficient in Django, Flask, FastAPI, PostgreSQL, and Docker. Experience with cloud deployment and microservices.",
        "skills": [
            "Python", "Django", "Flask", "FastAPI", "REST APIs",
            "PostgreSQL", "MongoDB", "MySQL", "Docker", "AWS",
            "Git", "Redis", "Celery", "SQLAlchemy", "Pytest",
            "Linux", "Nginx", "CI/CD", "Data Structures"
        ],
        "experience": [
            {
                "title": "Python Developer",
                "company": "WebServices Ltd",
                "duration": "2020 - Present",
                "description": "Developed backend APIs with FastAPI and Django. Built microservices with Docker. Optimized database queries. Deployed on AWS EC2. Implemented caching with Redis."
            },
            {
                "title": "Backend Developer",
                "company": "TechStart",
                "duration": "2018 - 2020",
                "description": "Created REST APIs with Flask. Worked with PostgreSQL and MongoDB. Built authentication systems. Implemented background tasks with Celery."
            }
        ],
        "projects": [
            {
                "title": "E-commerce Backend",
                "description": "Built scalable backend for e-commerce platform with Django. Handled 10K+ daily transactions. Integrated payment gateways. Deployed on AWS."
            },
            {
                "title": "API Service",
                "description": "Created RESTful API with FastAPI. Implemented JWT authentication. Used PostgreSQL and Redis. Dockerized for deployment."
            }
        ],
        "education": [
            {
                "degree": "B.Tech in Computer Science",
                "institution": "IIT Bombay",
                "year": "2018"
            }
        ]
    },
    {
        "filename": "python_dev_good.pdf",
        "name": "Alex Thompson",
        "email": "alex.thompson@email.com",
        "phone": "+1-555-0203",
        "summary": "Python Developer with 3 years of experience in web development and APIs. Experience with Flask, Django, PostgreSQL, and basic DevOps practices.",
        "skills": [
            "Python", "Flask", "Django", "REST APIs", "PostgreSQL",
            "MySQL", "Git", "Docker (basic)", "HTML", "CSS",
            "JavaScript", "SQLAlchemy", "Linux"
        ],
        "experience": [
            {
                "title": "Python Developer",
                "company": "WebDev Agency",
                "duration": "2022 - Present",
                "description": "Developed web applications with Django and Flask. Created REST APIs. Worked with PostgreSQL databases. Implemented user authentication."
            },
            {
                "title": "Junior Developer",
                "company": "CodeFactory",
                "duration": "2021 - 2022",
                "description": "Built web features with Python and JavaScript. Fixed bugs. Wrote unit tests. Learned about API development."
            }
        ],
        "projects": [
            {
                "title": "Blog Platform",
                "description": "Created blogging platform with Django. Implemented CRUD operations. Used PostgreSQL. Deployed on Heroku."
            },
            {
                "title": "REST API",
                "description": "Built simple REST API with Flask. Implemented authentication. Used SQLite database."
            }
        ],
        "education": [
            {
                "degree": "B.S. in Computer Science",
                "institution": "Boston University",
                "year": "2021"
            }
        ]
    },
    {
        "filename": "python_dev_moderate.pdf",
        "name": "Lisa Wang",
        "email": "lisa.wang@email.com",
        "phone": "+1-555-0204",
        "summary": "Junior developer with 1 year of Python experience. Basic knowledge of web frameworks and databases. Eager to learn and grow.",
        "skills": [
            "Python", "Flask (basic)", "SQL", "Git",
            "HTML", "CSS", "JavaScript (basic)", "Linux (basic)"
        ],
        "experience": [
            {
                "title": "Junior Python Developer",
                "company": "Small Tech Firm",
                "duration": "2023 - Present",
                "description": "Writing Python scripts for automation. Learning Flask for web development. Working with MySQL databases. Fixing bugs and writing tests."
            }
        ],
        "projects": [
            {
                "title": "Task Manager",
                "description": "Built simple task management app with Flask. Used SQLite. Learning project."
            },
            {
                "title": "Web Scraper",
                "description": "Created web scraper with Python and BeautifulSoup. Stored data in CSV files."
            }
        ],
        "education": [
            {
                "degree": "B.S. in Information Systems",
                "institution": "State College",
                "year": "2023"
            }
        ]
    },
    {
        "filename": "python_dev_weak.pdf",
        "name": "Tom Anderson",
        "email": "tom.anderson@email.com",
        "phone": "+1-555-0205",
        "summary": "Recent bootcamp graduate with basic Python knowledge. Completed online courses. Looking for entry-level position.",
        "skills": [
            "Python (basic)", "HTML", "CSS", "Git (basic)",
            "SQL (basic)", "Microsoft Office"
        ],
        "experience": [
            {
                "title": "Freelance",
                "company": "Self-employed",
                "duration": "2023",
                "description": "Completed small Python projects for local businesses. Created simple scripts for data processing."
            }
        ],
        "projects": [
            {
                "title": "Calculator App",
                "description": "Built calculator with Python Tkinter. Bootcamp final project."
            },
            {
                "title": "Todo List",
                "description": "Created command-line todo list application. Learning project."
            }
        ],
        "education": [
            {
                "degree": "Coding Bootcamp Certificate",
                "institution": "Online Bootcamp",
                "year": "2023"
            }
        ]
    }
]

def create_resume_pdf(resume_data, output_path):
    """Create a PDF resume from resume data."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2C3E50',
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#34495E',
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#16A085',
        spaceAfter=6,
        spaceBefore=12,
        borderWidth=0,
        borderColor='#16A085',
        borderPadding=0,
        leftIndent=0
    )
    
    # Name
    story.append(Paragraph(resume_data['name'], title_style))
    
    # Contact info
    contact = f"{resume_data['email']} | {resume_data['phone']}"
    story.append(Paragraph(contact, contact_style))
    
    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    story.append(Paragraph(resume_data['summary'], styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_text = " • ".join(resume_data['skills'])
    story.append(Paragraph(skills_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
    for exp in resume_data['experience']:
        job_title = f"<b>{exp['title']}</b> | {exp['company']}"
        story.append(Paragraph(job_title, styles['Normal']))
        story.append(Paragraph(f"<i>{exp['duration']}</i>", styles['Normal']))
        story.append(Paragraph(exp['description'], styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    # Projects
    if resume_data.get('projects'):
        story.append(Paragraph("KEY PROJECTS", heading_style))
        for proj in resume_data['projects']:
            proj_title = f"<b>{proj['title']}</b>"
            story.append(Paragraph(proj_title, styles['Normal']))
            story.append(Paragraph(proj['description'], styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    for edu in resume_data['education']:
        edu_text = f"<b>{edu['degree']}</b> | {edu['institution']} | {edu['year']}"
        story.append(Paragraph(edu_text, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    
    doc.build(story)
    print(f"✓ Created: {output_path}")

# Generate AI Engineer resumes
print("\n=== Generating AI Engineer Resumes ===")
ai_dir = Path("/Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker/data/ai_engineer")
for resume in ai_engineer_resumes:
    output_path = ai_dir / resume['filename']
    create_resume_pdf(resume, output_path)

# Generate Python Developer resumes
print("\n=== Generating Python Developer Resumes ===")
python_dir = Path("/Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker/data/python_developer")
for resume in python_developer_resumes:
    output_path = python_dir / resume['filename']
    create_resume_pdf(resume, output_path)

print("\n✓ All resumes generated successfully!")
print(f"\nAI Engineer resumes: {ai_dir}")
print(f"Python Developer resumes: {python_dir}")
