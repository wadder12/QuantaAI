import io
import json
import random
import nextcord
from nextcord.ext import commands
import os
from nextcord.ui import Button
import requests


def get_wind_emoji(direction):
        if direction == "N":
            return ":arrow_up:"
        elif direction == "NE":
            return ":arrow_upper_right:"
        elif direction == "E":
            return ":arrow_right:"
        elif direction == "SE":
            return ":arrow_lower_right:"
        elif direction == "S":
            return ":arrow_down:"
        elif direction == "SW":
            return ":arrow_lower_left:"
        elif direction == "W":
            return ":arrow_left:"
        elif direction == "NW":
            return ":arrow_upper_left:"
        else:
            return ""

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
            embed.add_field(name=":tv: Webcast", value=f"[Watch here]({webcast_url})")
            embed.add_field(name=":book: Wikipedia", value=f"[Read more]({wikipedia_url})")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the SpaceX launch information.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="space_agencies", description="Fetch information about space agencies")
    async def space_agencies(self, interaction: nextcord.Interaction):
        try:
            base_url = "https://ll.thespacedevs.com/2.2.0/agencies/"
            params = {
                "mode": "detailed",  # Use detailed mode to get more information
                "ordering": "featured"  # Order by featured
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()
            agencies = data.get("results")

            if not agencies:
                error_embed = nextcord.Embed(
                    title="No Agencies Found",
                    description="No space agencies found.",
                    color=nextcord.Color.red()
                )
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
                return

            total_agencies = len(agencies)
            split_index = total_agencies // 2

            # Split agencies into two separate lists
            agencies1 = agencies[:split_index]
            agencies2 = agencies[split_index:]

            # Create embeds to display the space agencies information
            embed1 = nextcord.Embed(title="Space Agencies - Part 1", color=nextcord.Color.blue())
            embed2 = nextcord.Embed(title="Space Agencies - Part 2", color=nextcord.Color.blue())

            # Add fields to the first embed
            for agency in agencies1:
                name = agency.get("name")
                country = agency.get("country_code")
                description = agency.get("description")

                if not name or not country or not description:
                    continue

                # Truncate the description if it exceeds the character limit
                if len(description) > 1024:
                    description = description[:1021] + "..."

                embed1.add_field(name=":star: Agency", value=name, inline=False)
                embed1.add_field(name=":earth_americas: Country", value=country, inline=False)
                embed1.add_field(name=":pencil: Description", value=description, inline=False)
                embed1.add_field(name="\u200b", value="\u200b", inline=False)  # Empty field for spacing

            # Add fields to the second embed
            for agency in agencies2:
                name = agency.get("name")
                country = agency.get("country_code")
                description = agency.get("description")

                if not name or not country or not description:
                    continue

                # Truncate the description if it exceeds the character limit
                if len(description) > 1024:
                    description = description[:1021] + "..."

                embed2.add_field(name=":star: Agency", value=name, inline=False)
                embed2.add_field(name=":earth_americas: Country", value=country, inline=False)
                embed2.add_field(name=":pencil: Description", value=description, inline=False)
                embed2.add_field(name="\u200b", value="\u200b", inline=False)  # Empty field for spacing

            await interaction.response.send_message(embed=embed1, ephemeral=True)
            await interaction.followup.send_message(embed=embed2, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the space agencies information.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev2.subcommand(name="xeno_canto_random", description="Fetch a random recording from Xeno-Canto API")
    async def xeno_canto_random(self, interaction: nextcord.Interaction):
        try:
            base_url = "https://xeno-canto.org/api/2/recordings"
            
            params = {
                "query": "q:A"
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data = response.json()
            
            recordings = data.get("recordings")
            
            if not recordings:
                error_embed = nextcord.Embed(
                    title="No Recordings Found",
                    description="No recordings found in the database.",
                    color=nextcord.Color.red()
                )
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
                return
            
            random_recording = random.choice(recordings)
            
            id = random_recording.get("id")
            genus = random_recording.get("gen")
            species = random_recording.get("sp")
            country = random_recording.get("cnt")
            location = random_recording.get("loc")
            
            if not id or not genus or not species or not country or not location:
                error_embed = nextcord.Embed(
                    title="Invalid Recording Data",
                    description="The selected recording has missing or invalid data.",
                    color=nextcord.Color.red()
                )
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
                return
            
            embed = nextcord.Embed(title="Xeno-Canto Random Recording", color=nextcord.Color.blue())
            embed.add_field(name=":sound: Recording", value=f"[{id}](https://xeno-canto.org/{id})", inline=False)
            embed.add_field(name=":bird: Species", value=f"{genus} {species}", inline=False)
            embed.add_field(name=":earth_americas: Country", value=country, inline=False)
            embed.add_field(name=":round_pushpin: Location", value=location, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching a random recording from Xeno-Canto.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)



    @dev2.subcommand(name="weather", description="Fetch weather information from 7Timer API")
    async def weather(self, interaction: nextcord.Interaction):
        try:
            url = "http://www.7timer.info/bin/api.pl"
            params = {
                "lon": "113.17",
                "lat": "23.09",
                "product": "astro",
                "output": "json"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Extract relevant weather information
            timepoint = data["dataseries"][0]["timepoint"]
            cloudcover = data["dataseries"][0]["cloudcover"]
            seeing = data["dataseries"][0]["seeing"]
            transparency = data["dataseries"][0]["transparency"]
            lifted_index = data["dataseries"][0]["lifted_index"]
            rh2m = data["dataseries"][0]["rh2m"]
            wind_direction = data["dataseries"][0]["wind10m"]["direction"]
            wind_speed = data["dataseries"][0]["wind10m"]["speed"]
            temp2m = data["dataseries"][0]["temp2m"]
            prec_type = data["dataseries"][0]["prec_type"]

            # Create an embed to display the weather information
            embed = nextcord.Embed(title="Weather Information", color=nextcord.Color.blue())
            embed.add_field(name=":clock1: Timepoint", value=str(timepoint), inline=False)
            embed.add_field(name=":cloud: Cloud Cover", value=str(cloudcover), inline=False)
            embed.add_field(name=":telescope: Seeing", value=str(seeing), inline=False)
            embed.add_field(name=":crystal_ball: Transparency", value=str(transparency), inline=False)
            embed.add_field(name=":arrow_double_down: Lifted Index", value=str(lifted_index), inline=False)
            embed.add_field(name=":droplet: Relative Humidity", value=str(rh2m), inline=False)
            embed.add_field(name=":dash: Wind",
                            value=f"Direction: {wind_direction} {get_wind_emoji(wind_direction)}\nSpeed: {wind_speed}",
                            inline=False)
            embed.add_field(name=":thermometer: Temperature", value=str(temp2m), inline=False)
            embed.add_field(name=":umbrella: Precipitation Type", value=str(prec_type), inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the weather information.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


        
    @dev2.subcommand(name="animeqts", description="Fetch anime quotes from AnimeChan API")
    async def quotesan(self, interaction: nextcord.Interaction):
        try:
            url = "https://animechan.vercel.app/api/quotes"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            quotes = response.json()

            # Create an embed to display the quotes
            embed = nextcord.Embed(title="Anime Quotes", color=nextcord.Color.blue())

            for quote in quotes:
                character = quote["character"]
                anime = quote["anime"]
                quote_text = quote["quote"]

                embed.add_field(name=f":bust_in_silhouette: Character - {character}", value=f":tv: Anime - {anime}\n:speech_balloon: Quote - {quote_text}", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the quotes.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
    @dev2.subcommand(name="characters", description="Fetch available characters from the AnimeChan API")
    async def characters(self, interaction: nextcord.Interaction):
        try:
            url = "https://animechan.vercel.app/api/available/character"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            characters = response.json()

            # Create an embed to display the available characters
            embed = nextcord.Embed(title="Available Anime Characters", color=nextcord.Color.blue())

            # Split characters into multiple fields
            chunk_size = 10  # Number of characters per field
            chunks = [characters[i:i + chunk_size] for i in range(0, len(characters), chunk_size)]

            for i, chunk in enumerate(chunks):
                field_name = f"Characters (Part {i+1})"
                character_list = ', '.join(chunk)
                embed.add_field(name=field_name, value=character_list, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the available characters.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @dev2.subcommand(description="Fetch waifu pictures from WAIFU.IM API")
    async def waifu(self, interaction: nextcord.Interaction, tags: str = "waifu"):
        try:
            url = "https://api.waifu.im/search"
            params = {
                "tags": tags
            }

            response = requests.get(url, params=params)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Extract image details from the response
            image = data["images"][0]
            image_url = image["url"]
            artist_name = image["artist"]["name"]
            source_url = image["source"]

            # Create an embed to display the waifu picture
            embed = nextcord.Embed(title="Waifu Picture", color=nextcord.Color.blue())
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Artist: {artist_name} | Source: {source_url}")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the waifu picture.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


    @dev2.subcommand(description="Fetch a random color from the ColourLovers API")
    async def random_color(self, interaction: nextcord.Interaction):
        try:
            url = "http://www.colourlovers.com/api/colors/random"

            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors

            data = response.json()

            # Extract color details from the response
            color_title = data[0]["title"]
            color_hex = data[0]["hex"]
            color_rgb = data[0]["rgb"]

            # Create an embed to display the random color
            embed = nextcord.Embed(title="Random Color", color=color_hex)
            embed.add_field(name="Title", value=color_title, inline=False)
            embed.add_field(name="Hex", value=color_hex, inline=False)
            embed.add_field(name="RGB", value=color_rgb, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(str(e))
            error_embed = nextcord.Embed(
                title="Error Occurred",
                description="An error occurred while fetching the random color.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Developer1(bot))