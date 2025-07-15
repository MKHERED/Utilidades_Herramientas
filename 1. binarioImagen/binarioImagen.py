archivo = "logo.png"
destino = "logo.ico"
with open(archivo, "rb") as f:
    logo = f.read()
    
    with open(destino, "wb") as f_dest:
        f_dest.write(logo)
        
    #print(f"{logo}")