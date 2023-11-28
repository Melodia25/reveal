import os

from gotrue import User, Session, AuthResponse
from supabase import create_client, Client
from fastapi import Header, Depends

from entity import TokenAuthorization, ResponseModel, TokenHeaders

url: str = os.getenv("URL_SUPABASE")
key: str = os.getenv("KEY_SUPABASE")
supabase: Client = create_client(url, key)


def get_user_info(headers: TokenAuthorization = Depends()) -> User:
    user = supabase.auth.get_user(headers.Authorization)
    return user


def get_access_token(email: str, password: str) -> Session:
    supabase.auth.sign_in_with_password({"email": email, "password": password})
    res = supabase.auth.get_session()
    return res


def set_session_data(headers: TokenHeaders = Depends()) -> AuthResponse:
    res = supabase.auth.set_session(access_token=headers.Authorization, refresh_token=headers.Refresh)
    return res
