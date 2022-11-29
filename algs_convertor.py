finals = []
vstup = 1
while vstup != "0":
	vstup = input("Zadejte algoritmus")

	alg = vstup.split(" ")
	
	final = []
	for element in alg:		
		element = element.lower()
		element = element.strip()
		final.append(element)

	finals.append(final)

for element in finals:
	print(element)
