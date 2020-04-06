import pickle


def get2Grams(payload_obj):
    '''Divides a string into 2-grams
    
    Example: input - payload: "<script>"
             output- ["<s","sc","cr","ri","ip","pt","t>"]
    '''
    payload = str(payload_obj)
    ngrams = []
    for i in range(0,len(payload)-2):
        ngrams.append(payload[i:i+2])
    return ngrams


filename = './finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))


def is_malicious(inputs):
    variables = inputs.split('&')
#     values = [ variable.split('=')[1] for variable in variables]
    values = variables
    return True if loaded_model['model'].predict(values).sum() > 0 else False


# print(is_malicious("val1=%3Cscript%3Ekiddie"))
# print(is_malicious("'OR 1=1 --"))
# print(is_malicious("blog-post"))