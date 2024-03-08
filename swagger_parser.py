import json, os
# pip3 install colorama
from colorama import Fore, Back, Style

def count_verb(verb):
	count = verb_count.count(verb)
	return count
    
verb_count = []
endpoint_count = []

dir_path = r'.'

for file in os.listdir(dir_path):
	if file.endswith('.json'):
		f = open(file)
		data = json.load(f)
		print(Fore.GREEN)
		
		description = data["info"]["description"]
		print ("Scope description: {}".format(description))
		paths = description = data["paths"]
		for key, value in paths.items():
			endpoint = key
			endpoint_count.append(endpoint)
			for method in value:        
				print("Endpoint is: {} using method: {}".format(endpoint, method))
				verb_count.append(method)
		f.close()

print(Style.RESET_ALL)
print(Fore.RED)

print ("There are {} endpoints.".format(len(endpoint_count)))

print(Style.RESET_ALL)
print(Fore.BLUE)
print ("There are {} GET verbs being used.".format(count_verb("get")))
print ("There are {} POST verbs being used.".format(count_verb("post")))
print ("There are {} PUT verbs being used.".format(count_verb("put")))
print ("There are {} DELETE verbs being used.".format(count_verb("delete")))

calc_get = count_verb("get") * 1
calc_post = count_verb("post") * 2.2
calc_put = count_verb("put") * 2.2
calc_delete = count_verb("delete") * .5

total_scope = calc_get + calc_post + calc_put + calc_delete

print(Style.RESET_ALL)
print(Fore.GREEN)

print("Scope in days: {}".format(total_scope / 40))
    

