"""Tool modules - auto-registers via @mcp.tool() decorators."""

from . import locations_location_id
from . import locations
from . import media_media_id_comments
from . import media_media_id
from . import media
from . import tags_tag_name
from . import tags
from . import users_self
from . import users_user_id
from . import users
from . import general

__all__ = ["locations_location_id", "locations", "media_media_id_comments", "media_media_id", "media", "tags_tag_name", "tags", "users_self", "users_user_id", "users", "general"]
