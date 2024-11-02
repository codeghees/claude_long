from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import time
import os
from typing import Optional, List
import json
from datetime import datetime
from pathlib import Path
import dotenv

dotenv.load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Initialize Claude client with better error handling
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
claude = anthropic.Anthropic(api_key=api_key)

# Store analysis states
analysis_sessions_dir = Path("analysis_sessions")
analysis_sessions_dir.mkdir(exist_ok=True)

# Create interactions directory if it doesn't exist
interactions_dir = Path('interactions')
interactions_dir.mkdir(exist_ok=True)

def log_claude_interaction(prompt, response, interaction_type=""):
    """Log Claude interactions to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = interactions_dir / f"claude_interaction_{timestamp}_{interaction_type}.json"
    
    interaction = {
        "timestamp": timestamp,
        "type": interaction_type,
        "input": prompt,
        "output": response
    }
    
    print(f"[{timestamp}] Logging {interaction_type} interaction:")
    print(f"Input: {prompt[:200]}...")
    print(f"Output: {response[:200]}...")
    
    with open(filename, 'w') as f:
        json.dump(interaction, f, indent=2)

class AnalysisRequest(BaseModel):
    task: str
    iteration_count: Optional[int] = 5

class SystemPromptUpdate(BaseModel):
    session_id: str
    new_prompt: str

def get_session_file(session_id: str) -> Path:
    return analysis_sessions_dir / f"{session_id}.json"

@app.post("/start_analysis")
async def start_analysis(request: AnalysisRequest):
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"[{session_id}] Starting new analysis session")
    print(f"Task: {request.task}")
    
    session_data = {
        "session_id": session_id,
        "task": request.task,
        "iterations": [],
        "start_time": datetime.now().isoformat(),
        "status": "in_progress"
    }
    
    # Save initial session data
    with open(get_session_file(session_id), 'w') as f:
        json.dump(session_data, f, indent=2)
    
    return {"session_id": session_id}

@app.get("/analysis_status/{session_id}")
async def get_analysis_status(session_id: str):
    try:
        with open(get_session_file(session_id), 'r') as f:
            data = json.load(f)
            print(f"[{session_id}] Retrieved analysis status")
            return data
    except FileNotFoundError:
        print(f"[{session_id}] Session not found")
        raise HTTPException(status_code=404, detail="Session not found")

@app.post("/update_system_prompt") 
async def update_system_prompt(update: SystemPromptUpdate):
    try:
        session_file = get_session_file(update.session_id)
        print(f"[{update.session_id}] Updating system prompt: {update.new_prompt}")
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        session_data["iterations"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "system_prompt_update",
            "content": update.new_prompt
        })
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
            
        return {"status": "success"}
    except FileNotFoundError:
        print(f"[{update.session_id}] Session not found")
        raise HTTPException(status_code=404, detail="Session not found")

# Background task processor
@app.post("/process_iteration/{session_id}")
async def process_iteration(session_id: str):
    try:
        print(f"[{session_id}] Processing next iteration")
        with open(get_session_file(session_id), 'r') as f:
            session_data = json.load(f)
            
        # Add 10s timeout between iterations
        print(f"[{session_id}] Waiting 10s before processing...")
        time.sleep(10)
        
        # Get previous iterations to provide context
        previous_iterations = [i["content"] for i in session_data["iterations"] if i["type"] == "analysis"]
        iteration_context = "\n\n".join(previous_iterations[-3:]) if previous_iterations else ""
        
        prompt = f"""Task: {session_data["task"]}

Previous Analysis Context:
{iteration_context}

Please continue analyzing this task. Take your time to think deeply. Consider:

1. What new insights or perspectives can you add?
2. What aspects need deeper investigation?
3. What patterns or connections are emerging?
4. You should think deeply and choose sub-tasks to investigate and keep doing this until you are confident that you have a good understanding of the task.
5. LIST NEXT STEPS to investigate the task.
6. Your job is to solve the task. You are a world class expert in your field. You are also a great problem solver. You are also a great thinker. You are also a great writer. You are also a great researcher. You are also a great analyst. You are also a great thinker. You are also a great writer. You are also a great researcher. You are also a great analyst. You are also a great thinker. You are also a great writer. You are also a great researcher. You are also a great analyst.
7. For any external collaboration or experiment you want to do, just assume how you would do it and what the results would be. You do not have access to the real world, but you can imagine how you would do it.
8. You can even write the code to simulate the experiment and see what the results would be.
9. Everytime you suggest a next step, ACTION ON IT and dig deeper and recursively. PICK ONLY ONE (MOST IMPORTANT) ACTION TO GO DEEPER ON.
Remember: This is a long-term analysis. You have months to complete this task. DO NOT rush. Take time to reflect carefully and build on previous insights."""

        print(f"[{session_id}] Sending request to Claude...")
        try:
            response = claude.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            print(f"[{session_id}] Claude API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")
            
        log_claude_interaction(prompt, response.content[0].text, "single_iteration_analysis")
        print(f"[{session_id}] Received response from Claude")
        
        # Update session with new iteration
        session_data["iterations"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "analysis",
            "content": response.content[0].text
        })
        
        with open(get_session_file(session_id), 'w') as f:
            json.dump(session_data, f, indent=2)
            
        print(f"[{session_id}] Iteration complete")
        return {"status": "success"}
    except FileNotFoundError:
        print(f"[{session_id}] Session not found")
        raise HTTPException(status_code=404, detail="Session not found")