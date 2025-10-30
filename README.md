# 🔒 bulkscrypt

**bulkscrypt** is a Python tool for recursive bulk encryption and decryption of files using the secure [scrypt](https://en.wikipedia.org/wiki/Scrypt) key derivation function.

---

## 🧠 How It Works

When run on a directory, **bulkscrypt** automatically:

1. Creates a new directory named:

   * `scrypt_encrypted/` — when encrypting, or
   * `scrypt_decrypted/` — when decrypting.
2. Recursively mirrors the original folder structure inside this new directory.
3. Encrypts or decrypts each file using the provided password via the `scrypt` package.

Your original files remain untouched — all operations happen within the generated output directory.

---

## ⚙️ Requirements

* **Python 3**
* Required libraries (install via `pip`):

  ```bash
  pip install -r requirements.txt
  ```

---

## 🚀 Usage

```bash
python3 scrypt.py {enc|dec} {PATH}
```

* `enc` → encrypt the contents of the specified directory
* `dec` → decrypt the contents of the specified directory
* `{PATH}` → path to the target directory

Example:

```bash
python3 scrypt.py enc ./my_folder
```
