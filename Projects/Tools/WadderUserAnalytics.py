import nextcord
from nextcord.ext import commands
from nextcord import File
import os

# ** RFP ** SLash Commands

class UserAnalyticsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = {}
        self.channel_count = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        """Counts the number of messages sent by each user"""
        print(f"on_message called: {message.content}")
        if message.author.bot:
            return
        if message.guild.id not in self.message_count:
            self.message_count[message.guild.id] = {}
        if message.author.id not in self.message_count[message.guild.id]:
            self.message_count[message.guild.id][message.author.id] = 1
        else:
            self.message_count[message.guild.id][message.author.id] += 1

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Updates the message count when a message is deleted"""
        print(f"on_message_delete called: {message.content}")
        if message.author.bot:
            return
        if message.guild.id in self.message_count and message.author.id in self.message_count[message.guild.id]:
            self.message_count[message.guild.id][message.author.id] -= 1

    @nextcord.slash_command(name="useranalytics", description="Displays user analytics for the server")
    async def main (self, interaction: nextcord.Interaction):
        pass
    
    @main.subcommand(description="user analytics for the server")
    async def analytics(self, interaction: nextcord.Interaction, user: nextcord.User = None):
        """Displays user analytics for the server"""
        guild_id = interaction.guild.id

        if user:
            message_count = self.message_count.get(guild_id, {}).get(user.id, 0)
            message_count_embed = nextcord.Embed(title=f"Message Count for {user.display_name}")
            message_count_embed.add_field(name="Message Count", value=f"{message_count} \U0001F4AC")  # Emoji: 💬

            # Get the path to the GIF file in your project's directory
            gif_path = os.path.join(os.getcwd(), 'images', 'quanta.gif')

            print(f"GIF Path: {gif_path}")

            # Load and attach the GIF file
            gif = File(gif_path, filename='animated.gif')
            message_count_embed.set_image(url="attachment://animated.gif")

            await interaction.send(file=gif, embed=message_count_embed)
        else:
            message_count_embed = nextcord.Embed(title="Message Count")
            for user_id, count in self.message_count.get(guild_id, {}).items():
                user = self.bot.get_user(user_id)
                if user:
                    message_count_embed.add_field(name=user.display_name, value=f"{count} \U0001F4AC")  # Emoji: 💬

            # Get the path to the GIF file in your project's directory
            gif_path = os.path.join(os.getcwd(), 'images', 'quanta.gif')

            print(f"GIF Path: {gif_path}")

            # Load and attach the GIF file
            gif = File(gif_path, filename='animated.gif')
            message_count_embed.set_image(url="attachment://animated.gif")

            await interaction.send(file=gif, embed=message_count_embed)

def setup(bot):
    bot.add_cog(UserAnalyticsCog(bot))




