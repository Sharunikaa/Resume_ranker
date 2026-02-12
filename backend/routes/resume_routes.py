"""
Resume upload and processing; list candidates.
"""

from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.database import mongo
from backend.models.candidate_model import CandidateResponse
from backend.services import resume_service

router = APIRouter()


def _candidate_doc_to_response(doc: dict) -> CandidateResponse:
    from backend.models.candidate_model import (
        CareerInsights,
        Scores,
        StructuredResume,
    )
    resume = doc.get("structured_resume") or {}
    scores = doc.get("scores") or {}
    insights = doc.get("career_insights") or {}
    return CandidateResponse(
        candidate_id=doc["candidate_id"],
        job_id=doc["job_id"],
        name=doc.get("name", ""),
        email=doc.get("email", ""),
        structured_resume=StructuredResume(**resume) if isinstance(resume, dict) else resume,
        scores=Scores(**scores) if isinstance(scores, dict) else scores,
        career_insights=CareerInsights(**insights) if isinstance(insights, dict) else insights,
        rank=doc.get("rank"),
        explanation=doc.get("explanation", ""),
        skill_gaps=doc.get("skill_gaps", []),
        interview_questions=doc.get("interview_questions", []),
        created_at=doc.get("created_at"),
    )


@router.post("/jobs/{job_id}/resumes")
def upload_resumes(job_id: str, files: List[UploadFile] = File(...)):
    """Upload one or more PDF resumes; parse and extract; store candidates (parallel processing with batch size 3)."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    import time
    
    job = mongo.get_jobs_collection().find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not files:
        raise HTTPException(status_code=400, detail="At least one file required")
    
    print(f"\n{'='*60}")
    print(f"Starting parallel upload: {len(files)} files, batch size: 3")
    print(f"{'='*60}\n")
    start_time = time.time()
    
    def process_single_resume(file_data):
        """Process a single resume (runs in thread pool)."""
        filename, content = file_data
        try:
            print(f"[{filename}] Processing, size: {len(content)} bytes")
            text = resume_service.parse_resume(content)
            print(f"[{filename}] Extracted text length: {len(text)} chars")
            
            if not text.strip():
                print(f"[{filename}] ERROR: No text extracted")
                return {"success": False, "filename": filename, "error": "could not extract text (empty result)"}
            
            print(f"[{filename}] Calling LLM to extract structured data...")
            structured = resume_service.extract_structured_data(text)
            print(f"[{filename}] Structured data extracted: {structured.get('name', 'N/A')}")
            
            cid = resume_service.store_candidate(job_id, structured)
            print(f"[{filename}] ✓ Successfully processed -> {cid}")
            
            return {"success": True, "filename": filename, "candidate_id": cid}
        except Exception as e:
            error_msg = str(e)
            print(f"[{filename}] ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return {"success": False, "filename": filename, "error": error_msg}
    
    # Prepare file data (read all files first)
    file_data_list = []
    for f in files:
        if not f.filename or not f.filename.lower().endswith(".pdf"):
            file_data_list.append((f.filename or 'unknown', None, "not a PDF"))
            continue
        try:
            content = f.file.read()
            file_data_list.append((f.filename, content, None))
        except Exception as e:
            file_data_list.append((f.filename, None, str(e)))
    
    # Process in parallel batches of 3
    ids = []
    errors = []
    batch_size = 3
    
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        # Process files in batches
        for i in range(0, len(file_data_list), batch_size):
            batch = file_data_list[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(file_data_list) + batch_size - 1) // batch_size
            
            print(f"\n--- Processing Batch {batch_num}/{total_batches} ---")
            
            # Prepare batch for processing
            valid_batch = []
            for filename, content, error in batch:
                if error:
                    errors.append(f"{filename}: {error}")
                    continue
                valid_batch.append((filename, content))
            
            # Process batch in parallel
            if valid_batch:
                batch_start = time.time()
                results = list(executor.map(process_single_resume, valid_batch))
                batch_time = time.time() - batch_start
                print(f"Batch {batch_num} completed in {batch_time:.2f}s")
                
                # Collect results
                for result in results:
                    if result["success"]:
                        ids.append({"filename": result["filename"], "candidate_id": result["candidate_id"]})
                    else:
                        errors.append(f"{result['filename']}: {result['error']}")
    
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Upload completed in {total_time:.2f}s")
    print(f"Successful: {len(ids)}, Failed: {len(errors)}")
    print(f"{'='*60}\n")
    
    return {"uploaded": ids, "errors": errors}


@router.get("/jobs/{job_id}/candidates", response_model=List[CandidateResponse])
def list_candidates(job_id: str):
    """List all candidates for a job."""
    job = mongo.get_jobs_collection().find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    coll = mongo.get_candidates_collection()
    docs = list(coll.find({"job_id": job_id}))
    return [_candidate_doc_to_response(d) for d in docs]
