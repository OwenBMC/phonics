import pronouncing

# -------------------------------------------------------------------------------------------------------------------------
"""Sources"""
# -------------------------------------------------------------------------------------------------------------------------
full_dictionary = pronouncing.cmudict.words()

# -------------------------------------------------------------------------------------------------------------------------
"""Rules"""
# -------------------------------------------------------------------------------------------------------------------------

com_rep_sounds = {
    'a': 'AE',
    'b': 'B',
    'c': 'K',
    'd': 'D',
    'e': 'EH',
    'f': 'F',
    'g': 'G',
    'h': 'HH',
    'i': 'IH',
    'j': 'JH',
    'k': 'K',
    'l': 'L',
    'm': 'M',
    'n': 'N',
    'o': ['AA', 'AO'],
    'p': 'P',
    'q': 'K W',
    'r': 'R',
    's': 'S',
    't': 'T',
    'u': 'AH',
    'v': 'V',
    'w': 'W',
    'x': 'K S',
    'y': 'Y',
    'z': 'Z'
}

double_letter_sounds = {
    'ff': 'F',
    'll': 'L',
    'ss': 'S',
    'tt': 'T',
    'zz': 'Z',
    'ck': 'K',
    'ch': 'CH',
    'sh': 'SH',
    'th': ['TH', 'DH'],
    'ng': 'NG',
    'ar': 'AA R',
    'qu': 'K W'
}

learned_words = [
    'i',
    'i\'m',
    'you',
    'me',
    'he',
    'she',
    'his',
    'her',

    'to',
    'too',
    'do',
    'as',
    'of',
    'was',
    'the',
    'all'
]

# -------------------------------------------------------------------------------------------------------------------------
"""Preperation"""
# -------------------------------------------------------------------------------------------------------------------------
equal_letter_and_sound_words = []
more_letter_than_sound_words = []
more_sound_than_letter_words = []

def sort_sounds_to_letter(word):
    """determines whether there are more sounds, letters, or the same amount of each"""
    for pronounciation in pronounciations:
        sounds = pronounciation.split(' ')
        if len(word) == len(sounds):
            equal_letter_and_sound_words.append(word)
        elif len(word) > len(sounds):
            more_letter_than_sound_words.append(word)
        else:
            more_sound_than_letter_words.append(word)

def cv_format(string):
    """determines which letters are vowels and which are constonants"""
    vowels = ['a','e','i','o','u']
    cvstring = ''
    for letter in string:
        if letter in vowels:
            cvstring = cvstring + "v"
        else:
            cvstring = cvstring + "c"
    return cvstring

# -------------------------------------------------------------------------------------------------------------------------
"""Logic"""
# -------------------------------------------------------------------------------------------------------------------------
# --------------
"""sound verifiers"""
# --------------
def verify_common_sounds(letter, sounds):
    """verifies that letters represent their most commonly represented sound"""

    global s
    global i

    if letter == 'x':
        loop = 'x'
        if sounds[s] == 'K':
            s += 1
            if sounds[s] == 'S':
                s+=1
                i+=1

    elif type(com_rep_sounds[letter]) is list:
        loop = 'listed sounds'
        for sound in com_rep_sounds[letter]:
            if sound == sounds[s][0:2]:
                s+=1
                i+=1
            else:
                continue

    elif len(com_rep_sounds[letter]) == 1:
        loop = 'common1'
        if com_rep_sounds[letter] == sounds[s]:
            s+=1
            i+=1

    else:
        loop = 'else'
        if com_rep_sounds[letter] == sounds[s][0:2]:
            s+=1
            i+=1

def verify_common_double_sounds(double_letter, sounds):
    global s
    global i

    if type(double_letter_sounds[double_letter]) is list:
        for sound in double_letter_sounds[double_letter]:
            if len(double_letter_sounds[double_letter]) == 1:
                if sounds[s] == sound:
                    s+=1
                    i+=2
                else:
                    continue
            elif len(double_letter_sounds[double_letter]) == 2:
                if sounds[s][0:2] == sound:
                    s+=1
                    i+=2
                else:

                    continue
            else:
                check = sound.split(' ')

                if (sounds[s] == check[0] or sounds[s][0:2] == check[0]) and sounds[s+1] == check[1]:
                    s+=2
                    i+=2
                else:

                    continue
    else:
        if len(double_letter_sounds[double_letter]) == 1:
            if sounds[s] == double_letter_sounds[double_letter]:
                s+=1
                i+=2

        elif len(double_letter_sounds[double_letter]) == 2:
            if sounds[s][0:2] == double_letter_sounds[double_letter]:
                s+=1
                i+=2

        else:
            check = double_letter_sounds[double_letter].split(' ')
            if (sounds[s] == check[0] or sounds[s][0:2] == check[0]) and sounds[s+1] == check[1]:
                s+=2
                i+=2

# --------------
"""word verifiers"""
# --------------

def verify_basic_word(word):
    global s
    global i
    global sorted

    sorted = False
    
    for pronounciation in pronounciations:
        sounds = pronounciation.split(' ')
        s = 0
        i = 0
        for letter in word:
            try:
                verify_common_sounds(letter, sounds)
            
            except IndexError:
                # print(f'INDEX ERROR: {word} {letter} {i}')
                pass
        
        if i == len(word) and s == len(sounds):
            return True

def verify_word(word):
    global s
    global i

    success = False
    
    for pronounciation in pronounciations:
        if success:
            break
        sounds = pronounciation.split(' ')
        s = 0
        i = 0
        for letter in word:
            try:
                if i < len(word) -1 and letter + word[i+1] in double_letter_sounds:
                    double_letter = letter + word[i+1]

                    verify_common_double_sounds(double_letter, sounds)
                else:
                    verify_common_sounds(letter, sounds)
            
            except IndexError:
                # print(f'INDEX ERROR: {word} {letter} {i}')
                pass
        # print(f'{i}/{len(word)}\n{s}/{len(sounds)}')
        if i == len(word) and s == len(sounds):
            success = True
            return True
        

# --------------
"""stage verifiers"""
# --------------

equal_letter_and_sound_cvc = []
equal_letter_and_sound_single_syllable = []
equal_letter_and_sound_multisyllable = []

stage_one_words = []
stage_two_words = []
stage_three_words = []

learned_words_present = []
challenging_words = []
unknown_words = []

def verify_stage_one_to_three(word):
    global sorted
    global double_found
    if cv_format(word) == "cvc" or cv_format(word) == "cv" or cv_format(word) == "vc" or cv_format(word) == "vcc" or cv_format(word) == "v":
        equal_letter_and_sound_cvc.append(word)
        # print(word)
        if verify_basic_word(word):
            stage_one_words.append(word)
            sorted = True
        else:
            for double_letter in double_letter_sounds:
                if double_letter in word:
                    # print(double_letter)
                    verify_stage_four(word)
                    sorted = True
                    break

    elif syllables == 1:
        equal_letter_and_sound_single_syllable.append(word)
        if verify_basic_word(word):
            stage_two_words.append(word)
            sorted = True
        else:
            for double_letter in double_letter_sounds:
                if double_letter in word:
                    verify_stage_four(word)  
                    sorted = True
                    break


    else:
        equal_letter_and_sound_multisyllable.append(word)
        if verify_basic_word(word):
            stage_three_words.append(word)
            sorted = True
        else:
            if not double_found:
                for double_letter in double_letter_sounds:
                    if double_letter in word:
                        verify_stage_four(word)
                        sorted = True
                        break
            else:
                sorted = True
    if not sorted:
        # print(f'vs3: {word}')
        challenging_words.append(word)

stage_four_words = []

def verify_stage_four(word):
    global sorted
    sorted = False
    if verify_word(word):
        stage_four_words.append(word)
        sorted = True
    if not sorted:
        # print(f'vs4: {word}')
        challenging_words.append(word)
    


# --------------
"""prep"""
# --------------

def prepare_words(word):
    if word in learned_words:
        learned_words_present.append(word)
    else:
        # print('prep')
        word = ''.join(l for l in word if l.isalpha())
        global pronounciations
        global syllables
        global sorted
        global double_found

        sorted = False
        double_found = False
        pronounciations = pronouncing.phones_for_word(word)

        if not pronounciations:
            unknown_words.append(word)
        else:
            syllables = pronouncing.syllable_count(pronounciations[0])

            for pronounciation in pronounciations:
                sounds = pronounciation.split(' ')

                if len(sounds) != len(word):
                    if 'x' in word and len(sounds) == len(word)+1:
                        verify_stage_one_to_three(word)
                        sorted = True
                        break
                    if not double_found:
                        for double_letter in double_letter_sounds:
                            if double_letter in word:
                                # print(f'{word}, {double_letter}: through here')
                                verify_stage_four(word)
                                sorted = True
                                double_found = True
                                break
                else:
                    verify_stage_one_to_three(word)
                    sorted = True
                    break
            if not sorted:
                # print(f'prep: {word}')
                challenging_words.append(word)

def clear_lists():
    global stage_one_words
    global stage_two_words
    global stage_three_words
    global stage_four_words
    global challenging_words
    global learned_words_present
    global unknown_words

    stage_one_words=[]
    stage_two_words=[]
    stage_three_words=[]
    stage_four_words=[]
    challenging_words=[]
    learned_words_present=[]
    unknown_words = []

# -------------------------------------------------------------------------------------------------------------------------
"""Testing"""
# -------------------------------------------------------------------------------------------------------------------------

# for word in full_dictionary:
#     prepare_words(word)

#  prepare_words('during')

# print(list(dict.fromkeys(stage_one_words)))
# print('\n')
# print(list(dict.fromkeys(stage_two_words)))
# print('\n')
# print(list(dict.fromkeys(stage_three_words)))
# print('\n')
# print(list(dict.fromkeys(stage_four_words)))