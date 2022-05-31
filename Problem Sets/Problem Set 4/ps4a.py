# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    """
    Enumerate all permutations of a given seq

    seq (seq): an arbitrary seq to permute. Assume that it is a
    non-empty seq.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of seq

    Example:
    >>> get_permutations('abc')
    ['abc', 'bac', 'bca', 'acb', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    """
    seq = str(sequence).lower()
    char0 = seq[0]  # the first character in the seq
    if len(seq) <= 1:  # if the input is a one character
        return [seq]  # return singleton seq

    # This set of steps is recursive
    # The if statement below reverses the order of a string with 2 elements
    # This 2-string we use to initialize a list of strings to iterate the characters over

    if len(seq) == 2:  # when the string is of length 2
        seq_in_list = [seq]  # add 2-string to list
        rev_seq = seq[::-1]  # reverse 2-string
        if seq[0] != seq[1]:  # guarantees only 1 output if string has two of the same character
            seq_in_list.append(''.join(rev_seq))  # append rev_seq to list
        return seq_in_list  # seq_in_list = [seq, rev_seq]

    # We take char0 and insert it into the string in all positions of the 2-string via lists
    # this returns a list of 3-strings, and we iterate the next char0 over these strings, store them,
    # and return the list of permuted 4-strings and repeat until finished

    else:
        permutations = []  # stores all permutations

        # recursively collects active permutations to iterate char0 over starting with 2-string
        active_permutations = get_permutations(seq[1:])
        for s in active_permutations:  # for each permutation to iterate over
            for i in range(len(seq)):  # and for each index of the current permutation to iterate over
                string_as_list = list(s)  # convert active permutation string to list
                string_as_list.insert(i, char0)  # insert char0 into each position of the list
                permuted_string = ''.join(string_as_list)  # list -> string
                if permuted_string not in permutations:  # guarantees no repeats appear (distinct permutations only)
                    permutations.append(permuted_string)  # append to list of all permutations

    return permutations


if __name__ == '__main__':
    #    #EXAMPLE
    #    example_input = 'abc'
    #    print('Input:', example_input)
    #    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    #    print('Actual Output:', get_permutations(example_input))

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    example_input = 'a'
    print('Input:', example_input)
    print('Expected Output:', ['a'])
    print('Actual Output:', get_permutations(example_input))
    print()

    example_input = 123
    print('Input:', example_input)
    print('Expected Output:', ['123', '213', '231', '132', '312', '321'])
    print('Actual Output:', get_permutations(example_input))
    print()

    example_input = 'too'
    print('Input:', example_input)
    print('Expected Output:', ['too', 'oto', 'oot'])
    print('Actual Output:', get_permutations(example_input))
