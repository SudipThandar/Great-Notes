from supabase import create_client, Client
from app.config import settings


def get_supabase_client() -> Client:
    """Initialize and return Supabase client with service key."""
    return create_client(settings.supabase_url, settings.supabase_service_key)


def get_user_supabase_client(access_token: str) -> Client:
    """Initialize and return Supabase client with user's access token for RLS."""
    client = create_client(settings.supabase_url, settings.supabase_key)
    # Set the user's access token for RLS
    client.postgrest.auth(access_token)
    return client


def verify_connection() -> bool:
    """Verify Supabase connection is working."""
    try:
        client = get_supabase_client()
        # Simple query to test connection
        client.table("notes").select("id").limit(1).execute()
        return True
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        return False
