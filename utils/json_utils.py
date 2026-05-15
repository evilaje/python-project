import json

def sort_json(arr)-> None :
	for i in range(len(arr)):
		for j in range(i, len(arr)):
			if (arr[i]["grupo"] > arr[j]["grupo"]):
				aux = arr[i]
				arr[i] = arr[j]
				arr[j] = aux
	for i in range(len(arr)):
		for j in range(i, len(arr)):
			if (arr[i]["id"] > arr[j]["id"]):
				aux = arr[i]
				arr[i] = arr[j]
				arr[j] = aux
