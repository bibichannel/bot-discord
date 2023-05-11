import discord 
import my_secrets
import dictionaries
import notion
from notion import Notion

async def get_all_members(client, guild_id):
        guild = client.get_guild(guild_id)
        if guild is not None:
            # members = guild.members # get members online
            members = []
            async for member in guild.fetch_members(limit=None):
                members.append(member)
            print(f"{member.name}#{member.discriminator} ({member.id})")
            return members
        return None
            
async def get_userid(client, guild_id, username):
    members = await get_all_members(client, guild_id)

    if members is not None:
        for member in members:
            if member.name == username:
                print(member.id)
                return member.id
        return None
    return None

async def search_member_into_database_notion(user_notion):
    user_dict = dictionaries.user_dict
    for key in user_dict:
        if key == user_notion:
            return user_dict[key]
    return None

async def get_response_notion(object, query):
    response = object.post(query)
    if response is not None:
        return response
    return None

async def gen_message(client, object, response, ticket):

    if object.check_ticket_assgin(response, ticket):
        user_owner = await search_member_into_database_notion(object.owner)
        user_id = await get_userid(client, my_secrets.GUILD_ID_DISCORD, user_owner)
        print(user_id)
        print(object.owner)

        output_to_discord = f"{object.ticket}:\n owner: <@{user_id}>\n assign: {object.assign}\n {object.link}\n {object.note}"  # message send to discord

        print(output_to_discord)

        return output_to_discord
    return "error"

async def send_message(client, thread_id, ticket):
    noti = Notion(my_secrets.DATABASE_ID_NOTION, my_secrets.KEY_NOTION)
    response = await get_response_notion(noti, notion.query)

    if response is not None:
        messages = await gen_message(client, noti, response, ticket)
        try:
            thread = await client.fetch_channel(thread_id) 
            if thread is not None:
                await thread.send(messages)
            else:
                print("Thread not found")
        except Exception as e:
            print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

        await send_message(client, my_secrets.THREAD_ID_DISCORD, "AST-134")

    client.run(my_secrets.TOKEN_DISCORD)