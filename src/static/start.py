import emoji

greeting = f"Welcome, dear user {emoji.emojize(':white_heart:')}\n \n" \
           f"This bot will help you:\n" \
           f"- Determine the current weather {emoji.emojize(':cloud_with_lightning_and_rain:')}\n" \
           f"- Convert currency {emoji.emojize(':money_with_wings:')}\n" \
           f"- Send a random picture with a cute animal {emoji.emojize(':paw_prints:')}\n" \
           f"- Create polls and send them to a group chat {emoji.emojize(':hourglass_not_done:')}"

friends_gif = 'https://media.giphy.com/media/Vbtc9VG51NtzT1Qnv1/giphy.gif'

commands = [f"Show weather {emoji.emojize(':umbrella:')}",
             f"Convert currency {emoji.emojize(':money_with_wings:')}",
             f"Send cutie pic of animal {emoji.emojize(':paw_prints:')}",
             f"Create poll {emoji.emojize(':hourglass_not_done:')}"
             ]