import sys
import traceback
from http import HTTPStatus
from aiohttp import web

from botbuilder.core import BotFrameworkAdapterSettings, TurnContext
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import BotFrameworkHttpAdapter

from config import Config
from teams_bot import TeamsEchoBot


CONFIG = Config()

SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkHttpAdapter(SETTINGS)
BOT = TeamsEchoBot()


async def on_error(context: TurnContext, error: Exception):
    print(f"\n[on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    await context.send_activity("Ocorreu um erro no bot.")
    await context.send_activity("Por favor, tente novamente em instantes.")


ADAPTER.on_turn_error = on_error


async def messages(req: web.Request) -> web.Response:
    if "application/json" not in req.headers.get("Content-Type", ""):
        return web.Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    body = await req.json()
    auth_header = req.headers.get("Authorization", "")

    response = await ADAPTER.process_activity(body, auth_header, BOT.on_turn)
    if response:
        return web.json_response(data=response.body, status=response.status)

    return web.Response(status=HTTPStatus.OK)


def init_app():
    app = web.Application(middlewares=[aiohttp_error_middleware])
    app.router.add_post("/api/messages", messages)
    return app


if __name__ == "__main__":
    web.run_app(init_app(), host="0.0.0.0", port=CONFIG.PORT)
