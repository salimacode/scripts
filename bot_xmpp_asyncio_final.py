
import asyncio
from slixmpp import ClientXMPP
import aiohttp

class BotXMPP(ClientXMPP):
    def __init__(self, jid, password, webhook_url):
        super().__init__(jid, password)
        self.webhook_url = webhook_url
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(f"Mensaje recibido: {msg['body']}")
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json={"mensaje": msg['body']}) as resp:
                    response = await resp.json()
                    reply = response.get('message') or "No tengo respuesta."
                    msg.reply(reply).send()
                    print(f"Respuesta enviada: {reply}")

async def main():
    jid = "asistente@proyecto.asir2.lpdvg.es"
    password = "clave123"
    webhook = "https://n8n.proyecto.asir2.lpdvg.es/webhook-test/pregunta-ia"

    xmpp = BotXMPP(jid, password, webhook)
    await xmpp.connect()
    await xmpp.disconnected  # mantiene el bot corriendo hasta que se cierre la conexión

if __name__ == "__main__":
    asyncio.run(main())
