# # Copyright 2024 
#     Name : A V N S Bhavana (PhD Scholar)
#     Email Id : bhavana.akkiraju@research.iiit.ac.in
# # 
# # All rights reserved.

import re
import yaml
from num2words import num2words, CONVERTER_CLASSES
from google.transliteration import transliterate_text
import argparse

# Non-space joiners removal
def removing_nonspacejoiners(text, non_space_joiners_pattern):
    return non_space_joiners_pattern.sub('', text)

# --------------------------------------Punctuation Removal ---------------------------------

#Getting punctuation patterns from the congif file and compiling them
def create_punctuation_pattern(punctuations, lang):
    general_punctuations = ''.join(punctuations.get('general', [])) 
    hyphens = ''.join(punctuations.get('hyphens', []))
    punctuation_pattern = general_punctuations + hyphens
    if lang in ['ar', 'ur', 'fa']:
        arabic_punctuations = ''.join(punctuations.get('arabic', []))
        punctuation_pattern += arabic_punctuations
    return re.compile(f"[{punctuation_pattern}]")

#Removing punctuations
def remove_punctuations(text, punctuations, lang):
    punctuation_pattern = create_punctuation_pattern(punctuations, lang)
    return punctuation_pattern.sub('', text)


# Specific characters removal according to the text we have
def create_characters_pattern(characters):
    return re.compile(f"[{''.join(map(re.escape, characters))}]")

def remove_specific_characters(text, characters_pattern):
    return characters_pattern.sub('', text)
    
#-----------------------------------Transliteration and Translation -------------------------------------------------
# Convert English digits to PA languages
def get_supported_languages():
    return list(CONVERTER_CLASSES.keys())

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Translating numbers to words
def translate_num_to_words(match, target_lang):
    number_str = match.group()
    try:
        if is_number(number_str):
            number = float(number_str)
            return num2words(number, lang=target_lang)
        
        numeric_part = re.search(r'\d+', number_str)
        if numeric_part:
            number = int(numeric_part.group())
            word_part = number_str.replace(numeric_part.group(), '')
            translated_num = num2words(number, lang=target_lang)
            return f"{translated_num}{word_part}"
        
        for lang in get_supported_languages():
            try:
                parsed_number = num2words(number_str, to='cardinal', lang=lang)
                return num2words(float(parsed_number), lang=target_lang)
            except:
                continue
        
        return number_str
    except Exception as e:
        print(f"Error translating {number_str}: {e}")
        return number_str

# Transliterate
def transliterate_text_lang(text, lang):
    eng_pattern = re.compile(r'[A-Za-z]+')
    num_pattern = re.compile(r'\b(?:\d+(?:[.,]\d+)?|\w+(?:\s+\w+){0,2})\b')
    num_pattern_1 = re.compile(r'\b\d+(?:[.,]\d+)?\b')
    segments = text.split(' ')
    transliterated_segments = []
    for segment in segments:
        if eng_pattern.match(segment):
            try:
                transliterated_text = transliterate_text(segment, lang_code=lang)
                transliterated_segments.append(transliterated_text)
            except Exception as e:
                print(f"Error transliterating segment '{segment}' for language '{lang}': {e}")
                transliterated_segments.append(segment)  # Fallback to original text on error
        elif num_pattern.match(segment) or num_pattern_1.match(segment):
            translated_segment = num_pattern.sub(lambda m: translate_num_to_words(m, target_lang=lang), segment)
            translated_segment = num_pattern_1.sub(lambda m: translate_num_to_words(m, target_lang=lang), translated_segment)
            transliterated_segments.append(translated_segment)
        else:
            transliterated_segments.append(segment)
    
    return ' '.join(transliterated_segments)


#---------------------Checking the text is in the unicode range or not ----------------------------------------------------

#Getting the unicode-ranges for the specific languages and replacing the text which is not in that range
def create_unicode_ranges_pattern(unicode_ranges, lang):
    ranges = []
    for range_set in unicode_ranges.get(lang, []):
        ranges.append(range_set)
    # Combine all Unicode range patterns into a single regex pattern
    pattern = f"[{''.join(ranges)}]"
    return re.compile(pattern)

def remove_non_unicode_chars(text, unicode_ranges_pattern):
    filtered_chars = [char for char in text if unicode_ranges_pattern.match(char) or char.isspace()]
    return ''.join(filtered_chars)
    
#------------------------------------------Processing each line ------------------------------------------------------
'''
Function -Process line :
    1) Removing non space joiners
    2) Transliterating english text to required languages
    3) Translating numbers to words
    4) Removing punctuations
    5) Removing some specific charaacters present in the text file we have
    6) Removing text which is not in the range of unicode ranges
'''
def process_line(line, non_space_joiners_pattern, punctuations, lang, characters_pattern, unicode_ranges_pattern):
    if len(line.split('\t')) >= 2:
        id, text = line.strip().split('\t', 1)
        text = removing_nonspacejoiners(text, non_space_joiners_pattern)
        text = transliterate_text_lang(text, lang)
        text = remove_punctuations(text, punctuations, lang)
        text = remove_specific_characters(text, characters_pattern)
        text_1 = remove_non_unicode_chars(text, unicode_ranges_pattern)
        return f"{id}\t{text_1}\n"
    else:
        text = line.strip()
        text = removing_nonspacejoiners(text, non_space_joiners_pattern)
        text = transliterate_text_lang(text, lang)
        text = remove_punctuations(text, punctuations, lang)
        text = remove_specific_characters(text, characters_pattern)
        text_1 = remove_non_unicode_chars(text, unicode_ranges_pattern)
        return f"{text_1}\n"


#Reading the text file
def reading_ip_file(input_file, output_file, non_space_joiners_pattern, punctuations, lang, characters_pattern, unicode_ranges_pattern):
    with open(input_file, 'r', encoding='utf-8') as ip, open(output_file, 'w', encoding='utf-8') as op:
        lines = ip.readlines()
        for line in lines:
            result = process_line(line, non_space_joiners_pattern, punctuations, lang, characters_pattern, unicode_ranges_pattern)
            if result.strip():
                op.write(result)


def main(input_file, output_file, yaml_file, lang):
    #loading the config file
    with open(yaml_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    #Getting ranges from the config file
    non_space_joiners = config.get('non_space_joiners', [])
    unicode_ranges = config.get('unicode_ranges', {})
    punctuations = config.get('punctuations', {})
    characters = config.get('characters', [])

    
    non_space_joiners_pattern = re.compile(f"[{''.join(map(re.escape, non_space_joiners))}]")
    characters_pattern = create_characters_pattern(characters)
    unicode_ranges_pattern = create_unicode_ranges_pattern(unicode_ranges, lang)
    
    reading_ip_file(input_file, output_file, non_space_joiners_pattern, punctuations, lang, characters_pattern, unicode_ranges_pattern)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text preprocessing script.")
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    parser.add_argument('yaml_file', type=str, help='Path to the YAML configuration file')
    parser.add_argument('lang', type=str, help='Target language code for transliteration and translation')
    
    args = parser.parse_args()
    
    main(args.input_file, args.output_file, args.yaml_file, args.lang)
