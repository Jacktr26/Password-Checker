import requests  # allows you to send HTTP requests using Python.
import hashlib  # lets you do hashing in python(hashes are a specific code for each combination of characters)
import sys

password = input("Enter your password ")
# it receives all the characters that were on separate lines and puts it into one string
password = password.splitlines()


def request_api_data(query_char):
    # link to the api + the password(query char hides the real password)
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    # we want a response of 400
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


# hashes make your passwords gibberish e.g. password123 will always be like CBFD40H...
# hashes = all the hashes, hash_to_check = our own password hash to check if it has been hacked
def get_password_leaks_count(hashes, hash_to_check):
    # line.split(':') will split it into the tail of the hash and the number of times it has been hacked
    # .text.splitlines makes it a list and splits at the end of each line instead of each value being its own list
    hashes = (line.split(':') for line in hashes.text.splitlines())
    # loops through hashes to check if ours has been hacked
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


# sha1 is the type of hash
def pwned_api_check(password):
    # converts to hexidecimal and capital letters
    # utf-8 is an encoding system for unicode
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()  # has to be encoded to utf-8 for hashing
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


# printing results
def main(args):
    # for password leaked add to count
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password!')
        else:
            print(f'{password} was NOT found. Carry on!')


main(password)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
