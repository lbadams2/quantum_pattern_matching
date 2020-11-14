from pattern_match import run_match
import pprint

# expected: a list
def test(expected, input_string, pattern):
    result = run_match(input_string, pattern)
    pprint(result)
    # sort the results by count number
    # check if the expected list contains the same keys as the highest len(expected)
    #   values in the sorted counts

if __name__ == '__main__':
    run_match('0000', '0')
