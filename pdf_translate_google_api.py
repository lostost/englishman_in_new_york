import os
import six
from google.cloud import translate_v2 as translate


def go_translate(text, target):

    credential_path = "euler-hermes-199615-02d2b6a07be2.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    text_to_translate = text #u'Вадим прекрати издевать над нами мы итак еле подсоединились к этому Гуглу, так ещ что-то дальше делать :)'
    # The target language
    target = target

    # Translates some text into Russian
    translation = translate_client.translate(
        text_to_translate,
        target_language=target)
    return translation['translatedText']
    #print(u'Text: {}'.format(text))
    #print(u'Translation: {}'.format(translation['translatedText']))