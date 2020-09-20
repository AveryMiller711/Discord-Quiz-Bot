import os, discord, random, time, sys, asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '&test':
        response = 'Test was successful!'
        await message.channel.send(response)

    if message.content.lower() == '&quote_quiz':
        time.sleep(1)
        await message.channel.send('Starting **WHO SAID IT** Quiz...')
        time.sleep(1)
        lines = open('whosaidthat.txt').read().splitlines()
        run = True
        streak = 0
        while run:
            myline = random.choice(lines)
            response = myline
            name = ''
            quote = ''
            y = len(response)-1
            for i in range(len(response)):
                if response[y] == '|':
                    break
                name += response[y].upper()
                y -= 1
                
            for i in range(len(response)):
                if response[i] == '|':
                    break
                quote += response[i]

            await message.channel.send('**Who said:** ' + quote)

            def check(m):
                return m.content.upper() == name
            
            try:
                msg = await client.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('**Time\'s up! The correct answer was ' + name + '**')
                run = False
                time.sleep(1)
                await message.channel.send('**Your final streak:** ' + str(streak) + ' **!**')
            else:
                await message.channel.send('**That is correct!**')
                streak += 1
                time.sleep(1)
                await message.channel.send('**STREAK:** ' + str(streak))
                time.sleep(1)

                
client.run(TOKEN)






































