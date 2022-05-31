# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string


### HELPER CODE ###
def load_words(file_name):
    """
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    #>>> is_word(load_words(word_list), 'bat')
    returns True
    #>>> is_word(load_words(word_list), 'asdf')
    returns False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        """
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        # assert text is string
        # assert self.shift in range(26)
        # self.shift = None
        self.message_text = text
        self.valid_words = load_words(file_name='words.txt')

    def get_message_text(self):
        """
        Used to safely access self.message_text outside the class

        Returns: self.message_text
        """
        return self.message_text

    def get_valid_words(self):
        """
        Used to safely access a copy of self.valid_words outside the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        """
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """
        # self.shift = shift
        l_case = string.ascii_lowercase
        u_case = string.ascii_uppercase

        l_cipher_dict = {}
        u_cipher_dict = {}

        for i in range(26):
            shift_to = (i + shift) % 26
            l_cipher_dict[l_case[i]] = l_cipher_dict.get(l_case[i], '') + l_case[shift_to]
            u_cipher_dict[u_case[i]] = u_cipher_dict.get(u_case[i], '') + u_case[shift_to]

        shift_dict = l_cipher_dict | u_cipher_dict

        return shift_dict

    def apply_shift(self, shift):
        """
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        """
        # self.shift = shift
        message = self.message_text
        shift_dict = self.build_shift_dict(shift)
        shifted_message = ''

        for char in message:
            if char in shift_dict:
                shifted_message += shift_dict[char]
            else:
                shifted_message += char

        return shifted_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        """
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        """
        Message.__init__(self, text)
        self.shift = shift
        # self.get_encryption_dict = Message.build_shift_dict(self, shift)
        # self.get_message_text_encrypted()

    def get_shift(self):
        """
        Used to safely access self.shift outside the class

        Returns: self.shift
        """
        return self.shift

    def get_encryption_dict(self):
        """
        Used to safely access a copy self.encryption_dict outside the class

        Returns: a COPY of self.encryption_dict
        """
        encryption_dict = Message.build_shift_dict(self, self.shift).copy()
        return encryption_dict

    def get_message_text_encrypted(self):
        """
        Used to safely access self.message_text_encrypted outside the class

        Returns: self.message_text_encrypted
        """
        encrypted_text = Message.apply_shift(self, self.shift)
        return encrypted_text

    def change_shift(self, shift):
        """
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        """
        self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        """
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        Message.__init__(self, text)
        self.message_text = text

    def decrypt_message(self):
        """
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """
        # (best_shift,decyrpted_message) = (0 ,'')

        # apply shift to message
        # count the number of valid words in shifted message (for each word in shifted message
        # see if it is a word) create a list of true/false for each word, the list of maximum trues is the
        # best

        word_list = self.valid_words
        trues_for_shift = {}
        shifted_message_dict = {}
        best_shift = 0
        decrypted_message = ''

        for s in range(26):
            number_of_trues = 0
            shifted_message = Message.apply_shift(self, 26 - s)
            for word in shifted_message.split():
                if is_word(word_list, word):
                    number_of_trues += 1
            trues_for_shift[26 - s] = trues_for_shift.get(26 - s, 0) + number_of_trues
            shifted_message_dict[26 - s] = shifted_message_dict.get(26 - s, '') + shifted_message

        for shift_number in trues_for_shift:
            if trues_for_shift[shift_number] == max(trues_for_shift.values()):
                best_shift = shift_number
                decrypted_message = shifted_message_dict[best_shift]


        # best_shift = max(trues_for_shift, key=trues_for_shift.get) from a google search

        return best_shift, decrypted_message

    def __str__(self):
        return self.message_text


if __name__ == '__main__':
    # #    #Example test case (PlaintextMessage)
    # plaintext = PlaintextMessage('hello', 2)
    # print('Expected Output: jgnnq')
    # print('Actual Output:', plaintext.get_message_text_encrypted())

    # #    #Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE
    plaintext = PlaintextMessage('Hello world! Nice to meet you all.', 2)
    print(f'Original Text: {plaintext.message_text}')
    print('Expected Output: Byffi qilfx! Hcwy ni gyyn sio uff')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print()
    plaintext.change_shift(3)
    print(plaintext.get_message_text_encrypted())

    # TODO: best shift value and unencrypted story
    # The best shift value is 12.
    # This is the decrypted story:
    # Jack Florey is a mythical character created on the spur of a moment to help cover an insufficiently planned hack.
    # He has been registered for classes at MIT twice before, but has reportedly never passed a class. It has been
    # the tradition of the residents of East Campus to become Jack Florey for a few nights each year to educate
    # incoming students in the ways, means, and ethics of hacking.

    story = CiphertextMessage(get_story_string())
    decrypted_story = story.decrypt_message()
    print(f'This is the unencrypted story: \n \t {story}')
    print()
    # print(f'The best shift value is {decrypted_story[0]}.')
    print(f'Using the best shift value of {decrypted_story[0]}, this is the decrypted story: \n \t {decrypted_story[1]}')
