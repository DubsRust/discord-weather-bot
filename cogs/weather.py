import discord
import requests
from discord import app_commands
from discord.ext import commands
import json

#Developed by Dubs#3101
#Source reference https://stackoverflow.com/questions/63486570/how-to-make-a-weather-command-using-discord-py-v1-4-1
#Updated to Discord.py 2.0 and as a slash command

intents = discord.Intents(members=True)

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open("config.json", "r") as f:
        config = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather Cog loaded!")

    @app_commands.command(name="weather", description="Gets your local weather!")
    @app_commands.guild_only()
    async def weather(self, interaction: discord.Interaction, zipcode: str):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = self.config['apikey']
        complete_url = base_url + "appid=" + api_key + "&q=" "&zip=" + zipcode
        response = requests.get(complete_url)
        data = json.loads(response.text)
        
        if 'main' not in data:
            await interaction.response.send_message("Unable to fetch weather information. Please check the provided zip code.", ephemeral=True)
            return
        
        y = data["main"]
        feelslike = y['feels_like']
        current_temperature = y["temp"]
        feels_like_celsius = str(round(feelslike - 273.15))
        feels_like_farenheit = str(round((9/5)* (feelslike - 273.15) + 32))
        current_temperature_celsius = str(round(current_temperature - 273.15))
        current_temperature_farenheit= str(round((9/5)* (current_temperature - 273.15) + 32))
        current_humidity = y["humidity"]
        z = data["weather"]
        city_name = data["name"]
        weather_description = z[0]["description"]

        embed = discord.Embed(title=f"Weather in {city_name}", color=int(self.config['color'], 16))
        embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
        embed.add_field(name="Temperature (C)", value=f"**{current_temperature_celsius}°C** - **{current_temperature_farenheit}°F**", inline=False)
        embed.add_field(name="Feels like", value=f"**{feels_like_celsius}°C** - **{feels_like_farenheit}°F**", inline=False)
        embed.add_field(name="Humidity (%)", value=f"**{current_humidity}%**", inline=False)
        embed.add_field(name="Information Requested by", value=f"{interaction.user.mention}", inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"Developed by Dubs#3101")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Weather(bot))
