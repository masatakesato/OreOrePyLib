import os
import json
import traceback




if __name__ == '__main__':

    filepath_valid_json = 'valid.json'
    print( '#===================== Load VALID joson file %s =================#' % filepath_valid_json )

    try:
        # load json file
        with open( filepath_valid_json, 'r' ) as f:
            code_dict = json.load(f)

        # check contents
        print( code_dict['data']['Integer'] )
        print( code_dict['data']['String'] )
        print( code_dict['data']['Float'] )

    except:
        traceback.print_exc()



    filepath_non_json = 'ghdsh5wy53q.json'
    print( '#===================== Load NON-EXISTENT joson file %s =================#' % filepath_non_json )

    try:
        # load json file
        with open( filepath_non_json, 'r' ) as f:
            code_dict = json.load(f)

        # check contents
        print( code_dict['data']['Integer'] )
        print( code_dict['data']['String'] )
        print( code_dict['data']['Float'] )

    except:
        traceback.print_exc()




    filepath_invalid_json = 'invalid.json'
    print( '#===================== Load INVALID joson file %s =================#' % filepath_invalid_json )

    try:
        # load json file
        with open( filepath_invalid_json, 'r' ) as f:
            code_dict = json.load(f)

        # check contents
        print( code_dict['data']['Integer'] )
        print( code_dict['data']['String'] )
        print( code_dict['data']['Float'] )

    except:
        traceback.print_exc()