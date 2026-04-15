from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import ChannelAccount


class TeamsEchoBot(TeamsActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = (turn_context.activity.text or "").strip()

        if text.lower() == "ping":
            await turn_context.send_activity("pong")
            return

        if text.lower() == "ajuda":
            await turn_context.send_activity("Comandos disponíveis: ping, ajuda")
            return

        await turn_context.send_activity(f"Você disse: {text}")

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Olá! Eu sou seu bot do Teams rodando em Python via Azure Bot Service."
                )
