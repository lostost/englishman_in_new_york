import re

text = '''Firefox

https://journojoshua.medium.com/too-many-americans-see-economics-as...

There’s a huge elephant in the room when talking about race or racism in America. We
avoid it, but regardless of race, class, gender, political ideology, religion, citizenship
status, etc., millions and millions of Americans believe in one incredibly powerful
logical fallacy: that minority progress, particularly the progress of black people, is, by
definition, achieved by taking things from white people.

We compartmentalize it differently, we reconcile it differently, we think it applies to
varying degrees, we address or dismiss it differently, but it’s there. That base
assumption is central to a vast variety of discourse—”blacks are lazy,” “Mexicans take
our jobs,” arguments against affirmative action, what people think of when they hear
words such as “diversity,” which immigrants we demonize, etc.

Стр. 1 из 1

25.04.2021, 20:13'''

length_text = len(text)


def tokenization(text):
    text = re.split('[^a-zа-яё]+', text, flags=re.IGNORECASE)
    return text


def remove_short_words(words):
    result = []
    for word in words:
        if len(word) > 3:
            result.append(word)
    return result


def word_processing(words):
    for i, word in enumerate(words):
        words[i] = words[i].lower()

    # words = set(words)
    return words


def remove_frequent(words):
    result = []
    most_common_words = []

    with open('static/most_common_words.txt', mode='r') as words_file:
        most_common_words = words_file.read().split()

    for word in words:
        if word not in most_common_words:
            result.append(word)
    return result


def sorted_dick(words):
    words_dict = {}
    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    sorted_keys = sorted(words_dict, key=words_dict.get, reverse=True)
    sorted_words_dict = {}
    for w in sorted_keys:
        sorted_words_dict[w] = words_dict[w]
    return sorted_words_dict


def remove_trash(words_dict):
    removed_koef = length_text // 200

    for key in words_dict:
        if words_dict[key] > removed_koef:
            del words_dict[key]
    return words_dict


def main(text):
    return list(remove_trash(sorted_dick(remove_short_words(remove_frequent(word_processing(tokenization(text)))))))


if __name__ == '__main__':
    print(main(text))
