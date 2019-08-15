

UNSECURE_ERROR_MSGS = ['chartCloseOnly=True&token=']


# Returns true if error msg should not be shown to client
# IE it may contain a secret key
def filter_error_msg(msg):
    for error in UNSECURE_ERROR_MSGS:
        if error in msg:
            return True

    return False
