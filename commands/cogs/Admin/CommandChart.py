import heapq
import typing
from io import BytesIO
import nextcord
from nextcord.ext import commands
import matplotlib.pyplot as plt
import numpy as np

class CommandChart(commands.Cog):
    """Shows the commands most used in a certain channel within the last so-and-so messages"""

    def __init__(self, bot):
        self.bot = bot

    async def command_from_message(self, m: nextcord.Message):
        message_context = await self.bot.get_context(m)
        if not message_context.valid:
            return None

        maybe_command = message_context.command
        command = maybe_command
        while isinstance(maybe_command, commands.Group):
            message_context.view.skip_ws()
            possible = message_context.view.get_word()
            maybe_command = maybe_command.all_commands.get(possible, None)
            if maybe_command:
                command = maybe_command

        return command

    def create_chart(self, top, others, channel):
        plt.clf()

        # Set a custom color map
        cmap = plt.get_cmap("nipy_spectral")
        colors = cmap(np.linspace(0, 1, len(top)))

        # Set figure and axis properties
        fig, ax = plt.subplots(figsize=(8, 8), dpi=80)
        ax.axis("equal")

        # Generate the pie chart
        wedges, texts, autotexts = ax.pie(
            [x[1] for x in top] + [others],
            labels=["{} ({:.1f}%)".format(x[0], x[1]) for x in top] + ["Others ({:.1f}%)".format(others)],
            colors=colors,
            autopct="%1.1f%%",
            startangle=0,
            wedgeprops=dict(width=0.3),
            textprops={"color": "w", "fontweight": "bold"},
        )

        # Set font properties for the text inside the wedges
        plt.setp(autotexts, size=10, weight="bold")

        # Add a title
        title = plt.title("Stats in #{}".format(channel.name), color="white", fontsize=16)
        title.set_va("top")
        title.set_ha("center")

        # Add a shadow effect to the wedges
        for wedge in wedges:
            wedge.set_edgecolor("k")
            wedge.set_linewidth(1)
            wedge.set_alpha(0.8)

        # Remove unnecessary spines and ticks
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="both", which="both", bottom=False, top=False, left=False, right=False)

        # Save the chart to an image buffer
        image_object = BytesIO()
        plt.savefig(image_object, format="PNG", facecolor="#36393E", bbox_inches="tight", pad_inches=0)
        image_object.seek(0)
        return image_object

    @commands.guild_only()
    @nextcord.slash_command()
    async def commandchart(
        self, interaction: nextcord.Interaction, channel: typing.Optional[nextcord.TextChannel] = None, number: int = 5000,
    ):
        """See the used commands in a certain channel within a certain amount of messages."""
        e = nextcord.Embed(description="Loading...", color=0x000099)
        e.set_thumbnail(url="https://cdn.discordapp.com/emojis/544517783224975387.gif?v=1")
        em = await interaction.send(embed=e)

        if not channel:
            channel = interaction.channel
        if not channel.permissions_for(interaction.user).read_messages:
            await em.delete()
            return await interaction.send("You do not have the proper permissions to access that channel.")

        message_list = []
        try:
            async for msg in channel.history(limit=number):
                com = await self.command_from_message(msg)
                if com is not None:
                    message_list.append(com.qualified_name)
        except nextcord.errors.Forbidden:
            await em.delete()
            return await interaction.send("I do not have permission to look at that channel.")

        msg_data = {"total count": 0, "commands": {}}
        for msg in message_list:
            if len(msg) >= 20:
                short_name = "{}...".format(msg[:20])
            else:
                short_name = msg
            if short_name in msg_data["commands"]:
                msg_data["commands"][short_name]["count"] += 1
                msg_data["total count"] += 1
            else:
                msg_data["commands"][short_name] = {}
                msg_data["commands"][short_name]["count"] = 1
                msg_data["total count"] += 1

        if not msg_data["commands"]:
            await em.delete()
            return await interaction.send("No commands have been run in that channel.")

        for command in msg_data["commands"]:
            pd = float(msg_data["commands"][command]["count"]) / float(msg_data["total count"])
            msg_data["commands"][command]["percent"] = round(pd * 100, 1)

        top_ten = heapq.nlargest(
            20,
            [
                (x, msg_data["commands"][x][y])
                for x in msg_data["commands"]
                for y in msg_data["commands"][x]
                if y == "percent"
            ],
            key=lambda x: x[1],
        )
        others = 100 - sum(x[1] for x in top_ten)

        img = self.create_chart(top_ten, others, channel)
        await em.delete()
        await interaction.channel.send(file=nextcord.File(img, "chart.png"))


def setup(bot):
    bot.add_cog(CommandChart(bot))

