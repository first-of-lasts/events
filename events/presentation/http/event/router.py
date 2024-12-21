from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

# from events.application.interactors import event_interactor
from events.presentation.http.dependencies.authentication import get_user_email


event_router = APIRouter()


@event_router.get("/me")
@inject
async def get_user(
        # interactor: FromDishka[event_interactor.GetUserInteractor],
        user_email: str = Depends(get_user_email),
):
    return
    # try:
    #     user = await interactor(user_email)
    #     return response_schemas.UserResponse(
    #        email=user.email,
    #        username=user.username,
    #        bio=user.bio,
    #     )
    # except UserNotFoundError:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="User not found",
    #     )
