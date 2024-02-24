import discord
from typing import Callable


class DiscordPagination(discord.ui.View):
    def __init__(self, context, get_page: Callable):
        self.context = context
        self.get_page = get_page
        self.total_pages = 20
        self.index = 0
        super().__init__(timeout=100)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.context.author:
            return True
        else:
            emb = discord.Embed(
                description=f"Only the author of the command can perform this action.",
                color=discord.Colour(0xE5E242),
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return False

    async def navigate(self):
        emb = await self.get_page(self.index)
        if self.total_pages == 1:
            await self.context.send(embed=emb)
        elif self.total_pages > 1:
            self.update_buttons()
            await self.context.send(embed=emb, view=self)

    async def edit_page(self, interaction: discord.Interaction):
        emb = await self.get_page(self.index)
        self.update_buttons()
        await interaction.response.edit_message(embed=emb, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.index == 0
        self.children[1].disabled = self.index == self.total_pages

    @discord.ui.button(emoji="◀️")
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1
        await self.edit_page(interaction)

    @discord.ui.button(emoji="▶️")
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1
        await self.edit_page(interaction)
