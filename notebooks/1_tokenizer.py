import tiktoken

tokennizer = tiktoken.encoding_for_model(model_name='gpt-4')

result = tokennizer.encode('I am Abhik')
print (result)
result

print(tokennizer.decode([40, 1097, 3765, 71, 1605]))
