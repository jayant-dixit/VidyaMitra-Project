from supabase import create_client
from core.config import settings

supabase = create_client(
    str(settings.supabase_url),
    str(settings.supabase_service_role_key)
)