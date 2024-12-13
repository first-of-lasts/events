from fastapi import APIRouter, Depends, HTTPException
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.domain.exceptions.user import UserNotFoundError
from events.application.interactors import event_interactor
from events.main.authentication import get_user_email
from events.presentation.http.event.schemas import request as request_schemas
from events.presentation.http.event.schemas import response as response_schemas


event_router = APIRouter()
