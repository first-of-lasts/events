from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from events.presentation.http.dependencies.authentication import get_user_email


event_router = APIRouter()
