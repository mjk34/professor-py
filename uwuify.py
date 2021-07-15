import random
import discord

def do_uwu(message: discord.Message, prob: float):
    if random.random() < prob:
        return uwuify(message.content)

def uwuify(text: str):
    output_text = ''

    length = len(text)

    for i in range(length):
        c_char = text[i]
        p_char = text[i-1] if i > 0 else None

        if c_char == 'L' or c_char == 'R':
            output_text += 'W'
        elif c_char == 'l' or c_char == 'r':
            output_text += 'w'

        elif c_char == 'O' or c_char == 'o':
            check_list = ['N', 'n', 'M', 'm']
            if p_char in check_list:
                output_text += "yo"
            else:
                output_text += c_char
        else:
            output_text += c_char
    
    output_text += '\n\n(′ꈍωꈍ‵)'

    return output_text


if __name__ == "__main__":
    test1 = "The quick brown fox jumps over the lazy dog."
    test2 = "Oh! Nooo! I was late for work!"

    print(uwuify(test1))
    print(uwuify(test2))

    

