import random

def uwuify(text: str):
    uwu_emojis = [
        'ಇ( ꈍᴗꈍ)ಇ', '( ͡o ꒳ ͡o )', '(ó ꒳ ò✿)',
        '(ㅅꈍ ˘ ꈍ)', '(*ฅ́˘ฅ̀*)', ' (◡‿◡✿)',
        '(◠‿◠✿)', '(❦ ᴗ ❦ ✿)', '(ᅌ ˇ ᅌ✿)'
    ]

    output_text = '`*:･ﾟ✧ '

    if random.random() < 0.15:
        num = random.randint(0, 8)
        output_text += uwu_emojis[num] + ' '

    length = len(text)
    # rework the algorithm and glorify the weeb speak
    for i in range(length):
        c_char = text[i]
        p_char = text[i-1] if i > 0 else None

        if c_char == ' ':
            if random.random() < 0.15:
                num = random.randint(0, 8)
                output_text += ' ' + uwu_emojis[num] + ' '
            else: output_text += c_char
            continue

        if c_char == 'L'  and p_char != ' ' or c_char == 'R' and p_char != ' ':
            output_text += 'W'
        elif c_char == 'l'  and p_char != ' ' or c_char == 'r' and p_char != ' ':
            output_text += 'w'

        elif c_char == 'O' or c_char == 'o':
            check_list = ['N', 'n', 'K', 'k', 'G', 'g', 'M', 'm']
            if p_char in check_list:
                output_text += 'yo'
            else: output_text += c_char

        elif c_char == 'A' or c_char == 'a':
            check_list = ['N', 'n', 'K', 'k', 'G', 'g', 'M', 'm']
            if p_char in check_list:
                output_text += 'ya'
            else: output_text += c_char

        else:
            output_text += c_char
    
    output_text += ' ✧･ﾟ:*\n`'
    return output_text


if __name__ == "__main__":
    test1 = "The quick brown fox jumps over the lazy dog."
    test2 = "Oh! Nooo! I was late for work!"

    print(uwuify(test1).encode('utf-8').decode('ascii', 'ignore'))
    print(uwuify(test2).encode('utf-8').decode('ascii', 'ignore'))