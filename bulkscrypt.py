import os
import sys
from getpass import getpass
from pathlib import Path
import scrypt
from concurrent.futures import ThreadPoolExecutor
import time


def copy_dirs(src, dst):
    for item in os.listdir(src):
        if item in ("scrypt_encrypted", "scrypt_decrypted"):
            continue
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            copy_dirs(s, d)


def encrypt_file(password, source_path, dest_path):
    with open(source_path, 'rb') as f:
        data = f.read()
    encrypted_data = scrypt.encrypt(data, password)
    with open(dest_path, 'wb') as f:
        f.write(encrypted_data)


def decrypt_file(password, source_path, dest_path):
    with open(source_path, 'rb') as f:
        encrypted_data = f.read()
    try:
        data = scrypt.decrypt(encrypted_data, password, encoding=None)
    except scrypt.error:
        print(f"Error: Incorrect password for file {source_path}")
        exit()
    except Exception as e:
        print(f"Error during decryption: {e}")
        exit()
    with open(dest_path, 'wb') as f:
        f.write(data)


def process_files_multithreaded(password, files, files_strip, destination, operation, max_threads=4):
    with ThreadPoolExecutor(max_threads) as executor:
        for i in range(0, len(files), max_threads):
            chunk = files[i:i + max_threads]
            chunk_strip = files_strip[i:i + max_threads]
            futures = []
            for x, file_path in enumerate(chunk):
                dest_path = os.path.join(
                    destination, f"{chunk_strip[x]}.enc" if operation == "encrypt" else chunk_strip[x].replace(".enc", "")
                )
                print(f"  {operation.title()} file {i + x + 1} of {len(files)}: {chunk_strip[x]}")
                if operation == "encrypt":
                    futures.append(executor.submit(encrypt_file, password, file_path, dest_path))
                elif operation == "decrypt":
                    futures.append(executor.submit(decrypt_file, password, file_path, dest_path))
            for future in futures:
                future.result()
            time.sleep(1)


def encrypt(password, files, files_strip, destination):
    process_files_multithreaded(password, files, files_strip, destination, "encrypt")
    print(f"Encrypted {len(files)} files.")


def decrypt(password, files, files_strip, destination):
    process_files_multithreaded(password, files, files_strip, destination, "decrypt")
    print(f"Decrypted {len(files)} files.")


def get_password(encdec):
    if encdec == 'enc':
        prompt = "Encryption password:"
    else:
        prompt = "Decryption password:"

    password = getpass(prompt=prompt)
    if encdec == 'enc':
        con_password = getpass(prompt='Confirm password:')
        if password != con_password:
            print("Passwords do not match!")
            exit()
    return password.encode()


def main(encdec, source):
    destination = os.path.join(source, "scrypt_encrypted" if encdec == 'enc' else "scrypt_decrypted")
    os.makedirs(destination, exist_ok=True)
    copy_dirs(source, destination)

    files = [
        os.path.join(root, f)
        for root, _, f_names in os.walk(source)
        for f in f_names if ".DS_Store" not in f
    ]

    files_strip = [os.path.relpath(file, source) for file in files]
    password = get_password(encdec)

    if encdec == 'enc':
        encrypt(password, files, files_strip, destination)
    elif encdec == 'dec':
        decrypt(password, files, files_strip, destination)
    else:
        print("Usage: python3 scrypt.py {enc|dec} {PATH}")
        exit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scrypt.py {enc|dec} {PATH}")
        exit()

    encdec = sys.argv[1]
    source = str(Path(sys.argv[2]).resolve())

    if encdec not in ("enc", "dec"):
        print("Usage: python3 scrypt.py {enc|dec} {PATH}")
        exit()

    main(encdec, source)
