from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.audit_logs import GetAuditLogRequest, AuditLogEvents
from dippy.core.snowflake import Snowflake
from pytest import mark
from os import getenv


@mark.asyncio
async def test_rest_client():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(
            GetAuditLogRequest(Snowflake(getenv("GUILD_ID", 0)), limit=1)
        )
        assert len(resp["audit_log_entries"]) == 1
