import io
import json
import nextcord
from nextcord.ext import commands
import os
from nextcord.ui import Button
import requests

class Developer1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @nextcord.slash_command(name="dev2")
    async def dev2(self, interaction: nextcord.Interaction):
       pass

   

    @dev2.subcommand(name="trivia2", description="Get a random trivia question")
    async def trivia2(self, interaction: nextcord.Interaction):
        try:
            url = "http://jservice.io/api/random"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data:
                question = data[0]["question"]
                category = data[0]["category"]["title"]
                answer = data[0]["answer"]

                embed = nextcord.Embed(title="Trivia Question", color=nextcord.Color.green())
                embed.add_field(name="Category", value=category, inline=False)
                embed.add_field(name="Question", value=question, inline=False)
                embed.add_field(name="Answer", value=answer, inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = nextcord.Embed(title="Trivia Question", color=nextcord.Color.red())
                embed.description = "No trivia question found."

                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the trivia question.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


    @dev2.subcommand(name="fbiwanted", description="Get the FBI's most wanted list")
    async def fbiwanted(self, interaction: nextcord.Interaction):
        try:
            url = "https://api.fbi.gov/wanted/v1/list"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data and "items" in data:
                wanted_list = data["items"]
                embed = nextcord.Embed(title="FBI's Most Wanted", color=nextcord.Color.red())

                for wanted in wanted_list:
                    title = wanted["title"]
                    description = wanted["description"]
                    image_url = wanted["images"][0]["large"]

                    embed.add_field(name=title, value=description, inline=False)
                    embed.set_image(url=image_url)

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = nextcord.Embed(title="FBI's Most Wanted", color=nextcord.Color.red())
                embed.description = "No wanted list found."
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the FBI's most wanted list.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev2.subcommand(name="federalregister", description="Get information about the latest document from the Federal Register")
    async def federalregister(self, interaction: nextcord.Interaction):
        try:
            url = "https://www.federalregister.gov/api/v1/documents?per_page=1&order=newest"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data and "results" in data:
                latest_document = data["results"][0]
                title = latest_document["title"]
                document_number = latest_document["document_number"]
                publication_date = latest_document["publication_date"]
                html_url = latest_document["html_url"]

                embed = nextcord.Embed(title=title, color=nextcord.Color.blue())
                embed.add_field(name="Document Number", value=document_number, inline=True)
                embed.add_field(name="Publication Date", value=publication_date, inline=True)
                embed.add_field(name="More Information", value=f"[Read More]({html_url})", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = nextcord.Embed(title="Federal Register Document", color=nextcord.Color.blue())
                embed.description = "No document found."
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching information from the Federal Register.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev2.subcommand(name="healthcare", description="Get information from the Healthcare.gov API")
    async def healthcare(self, interaction: nextcord.Interaction):
        try:
            url = "https://www.healthcare.gov/api/index.json"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            if data and "topics" in data:
                topics = data["topics"]
                topic_list = "\n".join(topics)

                embed = nextcord.Embed(title="Healthcare Topics", color=nextcord.Color.blue())
                embed.description = topic_list

                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = nextcord.Embed(title="Healthcare Topics", color=nextcord.Color.blue())
                embed.description = "No topics found."
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching information from the Healthcare.gov API.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="usaspending", description="Get information from the USAspending.gov API")
    async def agencies(self, interaction: nextcord.Interaction):
        try:
            url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Process the JSON data as needed
            # Example: Get a list of agency names
            agency_names = [agency["name"] for agency in data["results"]]

            # Create an embed to display the agency names
            embed = nextcord.Embed(title="Top-Tier Agencies", color=nextcord.Color.blue())
            embed.description = "\n".join(agency_names)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching information from the USAspending.gov API.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="dicebear", description="Generate a random pixel art image")
    async def dicebear(self, interaction: nextcord.Interaction):
        try:
            url = "https://api.dicebear.com/6.x/pixel-art/svg"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            svg_data = response.text

            # Create an embed with the SVG image as a file attachment
            embed = nextcord.Embed(title="Random Pixel Art", color=nextcord.Color.blue())

            # Create a file-like object from the SVG data
            file = io.BytesIO(svg_data.encode())

            # Set the file attachment in the embed
            embed.set_image(url="attachment://pixel_art.svg")

            await interaction.response.send_message(embed=embed, file=nextcord.File(file, "pixel_art.svg"), ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the pixel art image from the DiceBear API.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="housestock", description="Fetch house stock data")
    async def housestock(self, interaction: nextcord.Interaction):
        
        try:
            url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Limit the number of transactions to be displayed in the embed
            max_transactions = 5
            truncated_data = data[:max_transactions]

            # Create an embed to display the truncated data
            embed = nextcord.Embed(title="House Stock Data", color=nextcord.Color.green())

            # Add fields to the embed for each transaction
            for transaction in truncated_data:
                transaction_date = transaction["transaction_date"]
                ticker = transaction["ticker"]
                asset_description = transaction["asset_description"]
                transaction_type = transaction["type"]
                amount = transaction["amount"]
                representative = transaction["representative"]
                district = transaction["district"]
                state = transaction["state"]

                field_value = f"Ticker: {ticker}\nAsset Description: {asset_description}\nType: {transaction_type}\nAmount: {amount}\nRepresentative: {representative}\nDistrict: {district}\nState: {state}"
                embed.add_field(name=f"Transaction Date: {transaction_date}", value=field_value, inline=False)

            # Add a "Read More" button to view the full list of transactions
            if len(data) > max_transactions:
                embed.set_footer(text="Click 'Read More' to view the full list of transactions")
                button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Read More", url=url)
                view = nextcord.ui.View()
                view.add_item(button)
                await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the house stock data.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="carbonintensity", description="Fetch carbon intensity data")
    async def carbonintensity(self, interaction: nextcord.Interaction):
        try:
            url = "https://api.carbonintensity.org.uk/intensity/date"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Extract the data for the latest date
            latest_date_data = data["data"][0]

            # Get the date and intensity values
            date = latest_date_data["from"]
            intensity_forecast = latest_date_data["intensity"]["forecast"]
            intensity_actual = latest_date_data["intensity"]["actual"]

            # Create an embed to display the carbon intensity data
            embed = nextcord.Embed(title="Carbon Intensity Data", color=nextcord.Color.teal())
            embed.add_field(name="Date", value=date, inline=False)
            embed.add_field(name="Forecast Intensity", value=intensity_forecast, inline=True)
            embed.add_field(name="Actual Intensity", value=intensity_actual, inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the carbon intensity data.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="spacex", description="Fetch information about the latest SpaceX launch")
    async def spacex(self, interaction: nextcord.Interaction):
        try:
            url = "https://api.spacexdata.com/v5/launches/latest"
            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Extract relevant information from the response
            mission_name = data["name"]
            launch_date_utc = data["date_utc"]
            rocket_name = data["rocket"]
            details = data["details"]
            webcast_url = data["links"]["webcast"]
            wikipedia_url = data["links"]["wikipedia"]

            # Create an embed to display the launch information
            embed = nextcord.Embed(title="Latest SpaceX Launch", color=nextcord.Color.blue())
            embed.add_field(name=":rocket: Mission Name", value=mission_name, inline=False)
            embed.add_field(name=":calendar: Launch Date (UTC)", value=launch_date_utc, inline=False)
            embed.add_field(name=":rocket: Rocket", value=rocket_name, inline=False)
            embed.add_field(name=":clipboard: Details", value=details, inline=False)
            embed.set_footer(text="SpaceX", icon_url="https://i.imgur.com/2rWmEHm.png")

            # Add buttons for webcast and Wikipedia links
            buttons = [
                nextcord.Button(label="Webcast", style=nextcord.ButtonStyle.link, url=webcast_url),
                nextcord.Button(label="Wikipedia", style=nextcord.ButtonStyle.link, url=wikipedia_url)
            ]
            action_row = nextcord.ActionRow(*buttons)

            await interaction.response.send_message(embed=embed, components=action_row, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the SpaceX launch information.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Developer1(bot))