"""
Conversation management API routes.

This module implements endpoints for managing conversations:
- List all conversations for a user
- Get messages for a specific conversation
- Delete a conversation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from pydantic import BaseModel
from datetime import datetime
import uuid

from dependencies import validate_user_id_path
from db import get_session
from models import Conversation, Message, User


# Response models
class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime


# Create router
router = APIRouter(prefix="/api", tags=["conversations"])


@router.get("/{user_id}/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    user_id: str = Depends(validate_user_id_path),
    session: Session = Depends(get_session)
) -> List[ConversationResponse]:
    """
    List all conversations for a user, ordered by most recent first.
    
    Args:
        user_id: The ID of the authenticated user
        session: Database session
        
    Returns:
        List of conversations with message counts
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get all conversations for the user
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).all()
        
        # Build response with message counts
        result = []
        for conv in conversations:
            # Count messages in this conversation
            message_count = session.exec(
                select(Message)
                .where(Message.conversation_id == conv.id)
            ).all()
            
            result.append(ConversationResponse(
                id=str(conv.id),
                title=conv.title or "New Conversation",
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=len(message_count)
            ))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    user_id: str = Depends(validate_user_id_path),
    session: Session = Depends(get_session)
) -> List[MessageResponse]:
    """
    Get all messages for a specific conversation.
    
    Args:
        conversation_id: The conversation ID
        user_id: The ID of the authenticated user
        session: Database session
        
    Returns:
        List of messages in chronological order
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        # Validate conversation_id format
        try:
            conv_uuid = uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )
        
        # Verify conversation exists and belongs to user
        conv = session.get(Conversation, conv_uuid)
        if not conv or conv.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get all messages for this conversation
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conv_uuid)
            .order_by(Message.sequence_number.asc())
        ).all()
        
        return [
            MessageResponse(
                id=str(msg.id),
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.delete("/{user_id}/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(validate_user_id_path),
    session: Session = Depends(get_session)
):
    """
    Delete a conversation and all its messages.
    
    Args:
        conversation_id: The conversation ID to delete
        user_id: The ID of the authenticated user
        session: Database session
        
    Returns:
        Success message
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        # Validate conversation_id format
        try:
            conv_uuid = uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )
        
        # Verify conversation exists and belongs to user
        conv = session.get(Conversation, conv_uuid)
        if not conv or conv.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Delete the conversation (messages will be cascade deleted)
        session.delete(conv)
        session.commit()
        
        return {"success": True, "message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
