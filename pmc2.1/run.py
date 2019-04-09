import sys, getopt
from random import randint
from postman2apiary import PostmanToApiary


def msg():
    """ Print application usage """
    print("""
    Tool for generating Blueprint API markup or the Apiary API
    from a Postman collection.
    Application takes three arguments. Use python3
    USAGE: python run.py [postman.json-file] [output-file.apid]\n
    postman.json-file: Json file exported from Postman collection
    output-file.apid: Name of your api markup file to be generated.\n\n""")
    return True


def main():
    if len(sys.argv) < 3:
        msg()
        exit(0)

    data = dict()
    data['postman_collection'] = sys.argv[1] if sys.argv[1] else 'postman_collection.json'
    data['output_file'] = sys.argv[2] if sys.argv[2] else 'apiary' + str(randint(0, 9)) + '.apid'
    data['verbose'] = False
    # default to newest collection version
    data['postman_collection_version'] = 'v2.1'
    data['api_version'] = '/api/v1'

    argument_list = sys.argv[3:]
    unix_options = 'c:av'
    gnu_options = ['coll-version=', 'api-version=', 'verbose']
    # set api-version/-a to 0 to omit version from the api route
    # not all api routes contain version number
    try:
        arguments, values = getopt.getopt(argument_list, unix_options, gnu_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ('-v', '--verbose'):
                data['verbose'] = True
            elif currentArgument in ('-c', '--coll-version'):
                if currentValue == 'v1':
                    print('Postman Collection v1 is deprecated')
                elif currentValue in ('v2', 'v2.1'):
                    data['postman_collection_version'] = currentValue
            elif currentArgument in ('-a', '--api-version'):
                if currentValue > 0:
                    data['api_version'] = currentValue
                else:
                    data['api_version'] = None
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        sys.exit(2)

    print(' * Generating api markup')
    app = PostmanToApiary(data)
    app.write()
    print(' * Done...:)')
    print(' * OUTPUT FILE: ' + data['output_file'])


if __name__ == '__main__':
    main()
