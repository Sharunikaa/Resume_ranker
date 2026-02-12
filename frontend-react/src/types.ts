export interface Job {
  job_id: string;
  title: string;
  description: string;
  extracted_requirements: {
    required_skills: string[];
    preferred_skills: string[];
    domain: string;
    experience_level: string;
  };
  weights: {
    project_weight: number;
    skill_weight: number;
    experience_match: number;
  };
  created_at: string;
}

export interface Candidate {
  candidate_id: string;
  job_id: string;
  name: string;
  email: string;
  structured_resume: {
    skills: string[];
    experience: Experience[];
    projects: Project[];
    education: Education[];
  };
  scores: {
    project_similarity: number;
    skill_match: number;
    experience_match: number;
    final_score: number;
  };
  rank: number | null;
  explanation: string;
  skill_gaps: string[];
  interview_questions: string[];
  career_insights: {
    learning_velocity: number;
    skill_evolution_rate: string;
    adaptability_score: number;
  };
}

export interface Experience {
  company: string;
  role: string;
  duration: string;
  description: string;
}

export interface Project {
  title: string;
  description: string;
  technologies: string[];
  impact?: string;
}

export interface Education {
  degree: string;
  institution: string;
  year: string;
}
