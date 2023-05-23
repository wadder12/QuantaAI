import datetime
import nextcord
from nextcord.ext import commands
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.dates as mdates

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjdmZDJkYWQ2NDFiMjEyOTIiLCJpYXQiOjE2ODI5NzAwMDcsIm5iZiI6MTY4Mjk3MDAwNywiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjo3MDIzMjUifQ.WM5_voLQoe_aN7ekFe2g_TM6RSuKNsZ-REz1OH2SYWI"

    async def fetch_player_count_history(self, server_id: int):
        now = datetime.datetime.utcnow()
        start = now - datetime.timedelta(hours=24)

        url = f"https://api.battlemetrics.com/servers/{server_id}/player-count-history"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "start": start.isoformat() + "Z",
            "stop": now.isoformat() + "Z",
            "resolution": "30"
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            timestamps = []
            player_counts = []

            for item in data["data"]:
                timestamps.append(item["attributes"]["timestamp"])
                player_counts.append(item["attributes"]["value"])

            return timestamps, player_counts
        else:
            print(f"Error fetching player count history: {response.status_code} - {data.get('errors', 'Unknown error')}")
            return None, None

    async def generate_player_count_history_graph(self, server_id: int):
        timestamps, player_counts = await self.fetch_player_count_history(server_id)

        if timestamps and player_counts:
            fig, ax = plt.subplots()
            ax.plot(timestamps, player_counts, linestyle='-', marker='o', markersize=3, color='blue', linewidth=1)

            ax.set_xlabel("Time")
            ax.set_ylabel("Player Count")
            ax.set_title("Player Count History")
            ax.grid(True)

            # Format x-axis date and time labels
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
            fig.autofmt_xdate()

            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plt.close(fig)

            return buffer
        else:
            return None

    @nextcord.slash_command(name="serverinfo", description="Get server info for a given server ID on BattleMetrics")
    async def serverinfo(self, interaction: nextcord.Interaction, server_id: int):
        try:
            # Send a request to the BattleMetrics API
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"https://api.battlemetrics.com/servers/{server_id}"
            response = requests.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                # Extract server information
                server_name = data["data"]["attributes"]["name"]
                server_ip = data["data"]["attributes"]["ip"]
                server_port = data["data"]["attributes"]["port"]
                online_players = data["data"]["attributes"]["players"]
                max_players = data["data"]["attributes"]["maxPlayers"]

                # Generate and send player count history graph
                graph_buffer = await self.generate_player_count_history_graph(server_id)
                if graph_buffer:
                    graph_file = nextcord.File(graph_buffer, "player_count_history.png")

                    # Create embed message with server information and graph
                    embed = nextcord.Embed(title=f"Server info for {server_name}",
                                           description=f"IP: {server_ip}:{server_port}\n"
                                                       f"Online players: {online_players}/{max_players}",
                                           color=nextcord.Color.blue())

                    embed.set_image(url="attachment://player_count_history.png")
                    await interaction.response.send_message(embed=embed, file=graph_file)
                else:
                    # Create embed message with server information only
                    embed = nextcord.Embed(title=f"Server info for {server_name}",
                                           description=f"IP: {server_ip}:{server_port}\n"
                                                       f"Online players: {online_players}/{max_players}",
                                           color=nextcord.Color.blue())

                    await interaction.response.send_message(embed=embed)

            else:
                # Handle invalid server ID
                await interaction.response.send_message("Invalid server ID")
                
                
                

        except Exception as e:
            print(e)
            await interaction.response.send_message("An error occurred while fetching server information")

def setup(bot):
    bot.add_cog(ServerInfo(bot))