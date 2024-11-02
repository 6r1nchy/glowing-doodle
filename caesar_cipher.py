def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                shifted = ord(char) + shift_amount
                if shifted > ord("z"):
                    shifted -= 26
                result += chr(shifted)
            else:
                shifted = ord(char) + shift_amount
                if shifted > ord("Z"):
                    shifted -= 26
                result += chr(shifted)
        else:
            result += char
    return result

def main():
    text = input("Digite o texto a ser cifrado/descifrado: ")
    shift = int(input("Digite a quantidade de posições a ser deslocada: "))
    encrypted_text = caesar_cipher(text, shift)
    print("Texto cifrado/descifrado:", encrypted_text)

if __name__ == "__main__":
    main()
