"""
LLM prompt constants for job extraction, resume extraction, explanation, trajectory, interview.
"""

JOB_EXTRACTION_PROMPT = """
Extract the following from this job description. Return ONLY valid JSON with these exact keys.

- required_skills: list of required skill names (strings)
- preferred_skills: list of preferred/nice-to-have skill names (strings)
- domain: string, e.g. "Software Engineering", "Data Science"
- experience_level: one of "junior", "mid", "senior", "lead"

Job description:
---
{job_description}
---
"""

RESUME_EXTRACTION_PROMPT = """
Extract structured data from this resume text. Return ONLY valid JSON with these exact keys (use empty strings or empty arrays if not found):

- name: string (full name)
- email: string (email address)
- skills: array of strings (technical and soft skills)
- experience: array of objects, each with: company (string), role (string), duration (string), description (string)
- projects: array of objects, each with: title (string), description (string), technologies (array of strings), impact (string)
- education: array of objects, each with: degree (string), institution (string), year (string)

Resume text:
---
{resume_text}
---
"""

EXPLANATION_PROMPT = """
Given the following job requirements, candidate data, and scores, provide a structured response.

Job Requirements:
{requirements}

Candidate Projects (summary):
{projects}

Scores: project_similarity={project_similarity}, skill_match={skill_match}, experience_match={experience_match}, final_score={final_score}

Return ONLY valid JSON with these keys:
- summary: 2-3 sentence paragraph summarizing fit
- top_3_strengths: array of exactly 3 strings
- top_3_missing_skills: array of exactly 3 strings (or fewer if less than 3)
- recommendation: string, one of "strong_hire", "hire", "consider", "no_hire"
"""

TRAJECTORY_PROMPT = """
Analyze this career timeline (experience and projects) and return ONLY valid JSON with:

- learning_velocity: number 0-10 (rate of skill/role growth)
- skill_evolution_rate: one of "slow", "moderate", "fast"
- adaptability_score: number 0-100
- brief_narrative: 1-2 sentence summary of career progression

Experience list:
{experience_list}

Projects (if any):
{projects_list}
"""

INTERVIEW_QUESTIONS_PROMPT = """
Generate personalized interview questions based on this candidate's resume.

Candidate summary:
- Experience: {experience_summary}
- Projects: {projects_summary}
- Skill gaps for the role: {skill_gaps}

Return ONLY valid JSON with a single key "questions" whose value is an array of exactly 5 strings. Mix of:
1-2 technical questions from their projects
1-2 behavioral questions from their experience
1-2 questions that probe the skill gaps or verify claims
"""
