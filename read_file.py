try:
    with open("pi_digitss.txt") as file:
        lines = file.readlines()
        
    for line in lines:
        print(line.strip())
except FileNotFoundError:
    print("File not found.")
