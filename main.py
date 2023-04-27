from imported_files import *
# - ANSI Escape Codes
bright_blue = "\033[1;94m"
bright_green = "\033[1;92m"
white = "\033[1;37m"
bright_yellow = "\033[93m"

# -Messages
intro_message1 = f"{bright_blue}A long time ago, monsters came to the world through a foreign realm. They \n \
spilled out, and the peace of Sakino was broken. As the people struggled, heros were trained\n \
and fought against the monsters that destroyed\n(Enter or type skip to skip the storyline) \n"
intro_message2 = f"{bright_green}Soon enough, after countless battles, the heros forced the beasts\n, \
away. But they kept on coming non stop. Each hero retreated to a specific village \n \
where they could stay and defend the local land of Sakino.\n"

# Storyline
for char in intro_message1:
    print(char, end="", flush=True)
    sleep(0.02)
skip = input("\nType skip to skip the storyline:   ")


if skip == "skip":
    print("Skipping storyline. . .")
    sleep(2)
else:

    for char in intro_message2:
        print(char, end="", flush=True)
        sleep(0.02)
    input()


    sleep(2)

# Tutorial Starts
# ---Ghalad Messages


# Ghalad's Script
Ghalad1 = f"{white}Ghalad: Hey?! What are you doing there?!"
Ghalad2 = f"Ghalad: What is your {bright_blue} name? {white}"

# --Actual Speaking
for char in Ghalad1:
    print(char, end="", flush=True)
    sleep(0.01)

input()

for char in Ghalad2:
    print(char, end="", flush=True)
    sleep(0.01)

name = input("Your name: ")

# Ghalad's Script (Name)
Ghalad3 = f"Ghalad: Hello, {name}! I was just chasing some monsters that ran off with another hero. Have you seen {bright_yellow}Artimas{white}?"

Ghalad4 = f"Ghalad: Oh! There they are, those morbid little monsters! You are coming to chase them with me!"  # hashtag forceful

# --Actual Speaking 2 (Name)
for char in Ghalad3:
    print(char, end="", flush=True)
    sleep(0.01)
input()

for char in Ghalad4:
    print(char, end="", flush=True)
    sleep(0.01)
input()

print("LOL LOL LOL!! DEMO OVER XD! (THIS ISN't EVEN A DEMO LOL)")

