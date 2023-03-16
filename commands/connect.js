const { joinVoiceChannel,  } = require('@discordjs/voice');
const { SlashCommandBuilder, ChannelType } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('join')
		.setDescription('Join voice channel!')
        .addChannelOption((option) => option.setName('channel')
            .setDescription('Voice channel to join')
            .setRequired(true)
            .addChannelTypes(ChannelType.GuildVoice)),
	async execute(interaction) {
        const voiceChannel = interaction.options.getChannel('channel');
		joinVoiceChannel({  
            channelId : voiceChannel.id,
            guildId: interaction.guildId,
            adapterCreator: interaction.guild.voiceAdapterCreator,
        });
        await interaction.reply('Joined voice !' + voiceChannel);
	},
};
