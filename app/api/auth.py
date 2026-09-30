from fastapi import APIRouter, HTTPException, status

from google.oauth2 import id_token
from google.auth.transport import requests

from app.repositories.users_repository import UsersRepository
from app.data_schemas import (
    GoogleLoginRequest,
    UserResponseSchema,
    LoginInfoSchema,
    RegistrationInfoSchema,
)

router = APIRouter()




@router.post(
    "/google",
    response_model=UserResponseSchema,
)
async def google_login(
    payload: GoogleLoginRequest,
):

    try:
        google_info = id_token.verify_oauth2_token(
            payload.id_token,
            requests.Request(),
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google ID token",
        )

    google_id = google_info.get("sub")
    email = google_info.get("email")
    name = google_info.get("name")

    if not google_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account information is incomplete",
        )

    user = await UsersRepository.get_user_by_google_id(
        google_id
    )

    if user:
        return UserResponseSchema(
            user_id=int(user["user_id"]),
            username=user["username"],
            email_or_phone=user["email_or_phone"],
        )

    user = await UsersRepository.get_user_by_email(
        email
    )

    if user:

        user = await UsersRepository.link_google_account(
            user_id=int(user["user_id"]),
            google_id=google_id,
        )

        return UserResponseSchema(
            user_id=int(user["user_id"]),
            username=user["username"],
            email_or_phone=user["email_or_phone"],
        )


    username = name or email.split("@")[0]

    base_username = username[:50]
    username = base_username

    counter = 1

    while True:
        existing_user = await UsersRepository.get_user_by_username(
            username
        )

        if not existing_user:
            break

        suffix = f"_{counter}"

        username = (
            f"{base_username[:50 - len(suffix)]}{suffix}"
        )

        counter += 1

    user = await UsersRepository.create_google_user(
        username=username,
        email=email,
        google_id=google_id,
    )

    return UserResponseSchema(
        user_id=int(user["user_id"]),
        username=user["username"],
        email_or_phone=user["email_or_phone"],
    )


@router.post(
    "/register_user",
    response_model=UserResponseSchema,
)
async def register_user(
    payload: RegistrationInfoSchema,
):
    try:
        row = await UsersRepository.create_user(
            username=payload.username,
            email_or_phone=payload.email_or_phone,
            hashed_password=payload.password,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email/phone is already registered",
        )

    return UserResponseSchema(
        user_id=int(row["user_id"]),
        username=row["username"],
        email_or_phone=row["email_or_phone"],
    )


@router.post(
    "/login_user",
    response_model=UserResponseSchema,
)
async def login_user(
    payload: LoginInfoSchema,
):
    row = await UsersRepository.get_user_by_identifier(
        payload.email_or_phone,
        payload.password,
    )

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return UserResponseSchema(
        user_id=int(row["user_id"]),
        username=row["username"],
        email_or_phone=row["email_or_phone"],
    )