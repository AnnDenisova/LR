import random
import sys
import gmpy2

def is_prime(number):
    return gmpy2.is_prime(number)

def generate_number(key_size):
    return random.randrange(2 ** (key_size - 1), 2 ** key_size)

def generate_prime_number(key_size):
    while True:
        number = generate_number(key_size)
        if is_prime(number):
            return number

# НОД и коэффициенты Безу
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def find_modular_inverse(number, module):
    gcd, x, y = extended_gcd(number, module)
    if gcd != 1:
        return None  # Обратного элемента не существует
    else:
        return x % module  # Возвращаем положительный остаток от деления

def generate_primitive_root(number):
    if number == 2: return 1
    while True:
        primitive_root = random.randrange(2, number - 1)
        if pow(primitive_root, number - 1, number) == 1 and pow(primitive_root, ((number - 1) // 2), number) != 1:
            return primitive_root

def xor_encrypt_decrypt(text, key):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    key_length = len(key_bytes)
    encrypted_text = bytearray()
    for i, char in enumerate(text):
        encrypted_text.append(char ^ key_bytes[i % key_length])
    return encrypted_text

def diffie_hellman(key_size, message):
    print(f"Протокол Диффи-Хелмана. Размерность ключа - {key_size} бит.")
    print("Генерация простого числа:")
    p = generate_prime_number(key_size)
    print(f"p = {p}")

    print("Генерация первообразного корня")
    g = generate_primitive_root(p)
    print(f"g = {g}")

    print("Генерация закрытых ключей:")
    private_key_A = random.randrange(2, p - 1)
    private_key_B = random.randrange(2, p - 1)
    print(f"X_A = {private_key_A}")
    print(f"Y_A = {private_key_B}")

    print("Генерация открытых ключей:")
    public_key_A = pow(g, private_key_A, p)
    public_key_B = pow(g, private_key_B, p)
    print(f"X_B = {public_key_A}")
    print(f"Y_B = {public_key_B}")

    print("Генерация сеансового ключа:")
    session_key_A = pow(public_key_B, private_key_A, p)
    session_key_B = pow(public_key_A, private_key_B, p)
    print(f"Z_AB = {session_key_A}")
    print(f"Z_AB = {session_key_B}")

    if session_key_A != session_key_B:
        print("Ошибка: сеансовые ключи не совпали")
        sys.exit(1)
    print("Сеансовые ключи совпали")

    print(f"Сообщение для шифрования: {message}")

    encrypted_message = xor_encrypt_decrypt(message.encode(), session_key_A)
    print(f"Зашифрованный текст: {encrypted_message.hex()}")

    decrypted_message = xor_encrypt_decrypt(encrypted_message, session_key_B).decode()
    print(f"Расшифрованный текст: {decrypted_message}")

def shamir_secret_sharing(key_size, message):
    return

def string_to_number(string):
    byte_array = string.encode('utf-8')
    return int.from_bytes(byte_array, 'big')

def number_to_string(number):
    byte_length = (number.bit_length() + 7) // 8
    byte_array = number.to_bytes(byte_length, 'big')
    return byte_array.decode('utf-8')

def el_gamal_encryption(key_size, message):
    print(f"Протокол Эль-Гамаля. Размерность ключа - {key_size} бит.")
    print("Генерация простого числа:")
    p = generate_prime_number(key_size)
    print(f"p = {p}")
    print("Генерация первообразного корня")
    g = generate_primitive_root(p)
    print(f"g = {g}")
    print("Генерация закрытого ключа:")
    private_key = random.randrange(2, p - 2)
    print(f"private_key = {private_key}")
    print("Генерация открытого ключа:")
    public_key = pow(g, private_key, p)
    print(f"public_key = {public_key}")

    print(f"Сообщение для шифрования: {message}")
    text_number = gmpy2.mpz(string_to_number(message))
    print(f"Текст в числовом представлении: {text_number}")

    print("Генерация случайного числа:")
    k = random.randrange(1, p - 2)
    print(f"k = {k}")

    print("Шифрование:")
    part1 = pow(g, k, p)
    part2 = (text_number * pow(public_key, k, p)) % p
    print(f"Зашифрованные данные: {part1}, {part2}")

    print("Дешифрование:")
    secret = pow(part1, private_key, p)
    reversed_secret = gmpy2.invert(secret, p)
    text_decryption = (part2 * reversed_secret) % p
    print(f"Расшифрованные данные: {text_decryption}")
    decrypted_message = number_to_string(text_decryption)
    print(f"Расшифрованные данные в текстовом представлении: {decrypted_message}")

if __name__ == "__main__":
    m_key_size = int(input("Введите размер ключа в битах (кратно степени 2 и больше 512): "))
    m_message = input("Введите сообщение для шифрования: ")

    if m_key_size <= 0 or m_key_size < 512 or (m_key_size & (m_key_size - 1)) != 0:
        print("Ошибка: размер ключа должен быть положительным, кратным степени 2 и больше 512.")
        sys.exit(1)

    # Добавить выбор алгоритма
    diffie_hellman(m_key_size, m_message)
    el_gamal_encryption(m_key_size, m_message)