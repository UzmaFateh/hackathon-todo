from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db import get_session
from models import Task, User
from routes.auth import get_current_user
import google.generativeai as genai
import os
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

class AnalyticsResponse(BaseModel):
    insight: str

@router.post("/", response_model=AnalyticsResponse)
async def generate_analytics(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Generate AI analytics/insights based on the user's tasks using Gemini.
    """
    # 1. Fetch user tasks
    # Handle current_user being a dict (from JWT) or an object (from DB/Pydantic/UserContext)
    if isinstance(current_user, dict):
        user_id = current_user.get("id") or current_user.get("sub") or current_user.get("user_id")
    else:
        user_id = getattr(current_user, "id", None) or getattr(current_user, "user_id", None)
        
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    if not tasks:
        return AnalyticsResponse(insight="You have no tasks yet! Create some tasks to get AI-powered insights.")

    # 2. Prepare prompt for Gemini
    task_descriptions = []
    for task in tasks:
        status_str = "Completed" if task.is_completed else "Pending"
        task_descriptions.append(f"- {task.title} (Priority: {task.priority}, Status: {status_str})")
    
    tasks_text = "\n".join(task_descriptions)
    
    prompt = f"""
    You are a productivity expert. Analyze the following to-do list and provide 3 short, actionable insights or observations about the user's workload, focus areas, or completion status. Be encouraging but practical. Keep the response under 100 words.
    
    Tasks:
    {tasks_text}
    """

    # 3. Call Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "CHANGE_ME" in api_key:
         # Fallback mock response if API key is not configured
         return AnalyticsResponse(insight="Gemini API Key is missing or invalid. Please configure GEMINI_API_KEY in your backend .env file to get real AI insights.")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return AnalyticsResponse(insight=response.text)
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini API Error: {error_msg}")
        
        # Check for invalid API key error often associated with 403 or 400
        if "403" in error_msg or "API key not valid" in error_msg or "404" in error_msg:
             mock_insight = (
                 "⚠️ **API Error (Using Mock Data):**\n"
                 "Your API key is invalid or the model is unavailable.\n\n"
                 "**Simulated Insight:**\n"
                 "You have a good mix of high and low priority tasks. Consider tackling the 'High' priority items first to reduce stress. Your completion rate is on track, but try to clear the pending tasks before adding new ones."
             )
             return AnalyticsResponse(insight=mock_insight)
        
        # Return a generic error message as an insight instead of crashing
        return AnalyticsResponse(insight=f"Unable to generate insights at the moment. (Error: {error_msg})")
