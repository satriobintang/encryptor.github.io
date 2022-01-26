from flask import Flask, send_from_directory, jsonify, request, render_template
import base64 as b64

app = Flask(__name__, static_folder='views')


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * *
# * * *  BERSIHKAN SPASI  * * *
# * * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

def line_break_to_space(my_string):
  string_list = list(my_string)
  for i in range(0, len(string_list)):
    if ord(string_list[i]) == 13:
      string_list[i] = " "
    if ord(string_list[i]) == 10:
      string_list[i] = ""
  return "".join(string_list)


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * *
# * * * * MENCARI SPASI * * * *
# * * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

def find_spaces(my_possible_strings, include_e_a, how_many):
  spaces_list = []
  for i in range(0, len(my_possible_strings)):
    spaces = 0
    for c in my_possible_strings[i]:
      if ord(c) == 32:
        spaces += 1
      if (include_e_a):
        if ord(c) == 101 or ord(c) == 97:
          spaces += 1
    spaces_list.append({"spaces": spaces, "index": i})
                 
  spaces_list = sorted(spaces_list, key=lambda k: k["spaces"], reverse=True)


  most_likely_indexes = []
  for i in range(0, how_many):
    most_likely_indexes.append(spaces_list[i]["index"])
                 
  return most_likely_indexes

# - - - - - - - - - - - - - - - -
# * * * * * * * * * * *
# * * *  ROUTES  * * *
# * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/")
def hello():
  return render_template('index.html')

@app.route("/about_us")
def about_us():
  return render_template('about_us.html')


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * *
# * * *  CAESAR CIPHER  * * *
# * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

def offset_encrypt(my_string, my_offset):
  clean_string = line_break_to_space(my_string)
  new_string = ""
  int_offset = int(my_offset)
  count = 0
  for c in clean_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error: Greater than 126"
    if int_c < 32:
      return "Error: Less than 32"
    new_int_c = int_c + int_offset
    if new_int_c > 126:
      new_int_c = new_int_c - 95
    new_char = chr(new_int_c)
    new_string += new_char
    count += 1
  return new_string
  
def offset_decrypt(my_encoded_string, my_offset):
  new_string = ""
  int_offset = int(my_offset)
  for c in my_encoded_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error"
    if int_c < 32:
      return "Error"
    new_int_c = int_c - int_offset
    if new_int_c < 32:
      new_int_c = new_int_c + 95
    new_char = chr(new_int_c)
    new_string += new_char
  return new_string

def offset_brute_force(my_encoded_string):
  new_strings = []
  # Do the following for each offest someone might have chosen
  for possible_offset in range(1, 95):
    # Test that offset on each character of the enrypted message
    new_string = offset_decrypt(my_encoded_string, possible_offset)
    new_strings.append(new_string)
  return new_strings


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * *
# * * * * * * RSA * * * * * *
# * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -
def shared_key_encrypt(my_string, my_key):
  clean_string = line_break_to_space(my_string)
  new_string = ""
  for c in my_key:
    if ord(c) > 126:
      return "Error"
  count = 0
  #direction = 0
  key_length = len(my_key)
  for c in clean_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error"
    if int_c < 32:
      return "Error"
    offset = ord(my_key[count])
    new_int_c = int_c + offset
    if new_int_c > 126:
      new_int_c = new_int_c - 95
      if new_int_c > 126:
        new_int_c = new_int_c - 95
    new_char = chr(new_int_c)
    new_string += new_char
    
    count += 1
    if count == key_length:
      count = 0
  return new_string

def shared_key_decrypt(my_encoded_string, my_key):
  new_string = ""
  for c in my_key:
    if ord(c) > 126:
      return "Error"
  count = 0
  key_length = len(my_key)
  for c in my_encoded_string:
    int_c = ord(c)
    if int_c > 126:
      return "Error"
    if int_c < 32:
      return "Error"
    offset = ord(my_key[count])
    new_int_c = int_c - offset
    if new_int_c < 32:
      new_int_c = new_int_c + 95
      if new_int_c < 32:
        new_int_c = new_int_c + 95
    new_char = chr(new_int_c)
    new_string += new_char
    
    count += 1
    if count == key_length:
      count = 0
  return new_string

def for_each_place(beginnings_of_keys):
  old_beginnings = beginnings_of_keys
  beginnings_of_keys = []
  for beginning in old_beginnings:
    for character in range(97, 123):
      beginnings_of_keys.append(beginning + chr(character))
  return beginnings_of_keys


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * *
# * * *  KUNCI PUBLIK * * *
# * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

primes = [11, 13, 17, 19, 23, 29]

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1
  
def get_coprimes(prime_1, prime_2):
  larger_prime = prime_1
  if (prime_1 - prime_2) < 0:
    larger_prime = prime_2
  modulus = prime_1 * prime_2
  coprimes_of = (prime_1 - 1) * (prime_2 - 1)
  coprimes = []
  for n in range(larger_prime + 2, coprimes_of):
    if coprime(n, coprimes_of):
      if generate_keys(prime_1, prime_2, n):
        coprimes.append(n)
  return coprimes
  
def generate_keys(prime_1, prime_2, coprime):
  modulus = prime_1 * prime_2
  coprimes_of = (prime_1 - 1) * (prime_2 - 1)
  encrypt_exponent = coprime
  decrypt_exponent = 0
  public_keys = [encrypt_exponent, modulus]
  for n in range(2, coprimes_of):
    # Find largest decrypt_exponent:
    if (n * encrypt_exponent) % coprimes_of == 1:
      decrypt_exponent = n
  if decrypt_exponent  == 0:
    return False
  private_keys = [decrypt_exponent, modulus]
  if public_keys == private_keys:
    return False
  return {
    "public_keys": public_keys,
    "private_keys": private_keys
  }
  

def public_key_encrypt(plaintext_message, public_keys):
  clean_string = line_break_to_space(plaintext_message)
  newString = ""
  count = 0
  messageLength = len(clean_string)
  for c in clean_string:
    intC = ord(c)
    newIntC = ((intC**public_keys[0]) % public_keys[1])
    newString += str(newIntC)
    count += 1
    if count >= messageLength:
      pass
    else:
      newString += ", "
  return newString
  
def public_key_decrypt(encrypted_message, private_keys):
  encrypted_array = []
  decrypted_string = ""
  count = 0
  placeholder_string = ""
  for c in encrypted_message:
    if c != "," and c !=" ":
      placeholder_string += c
    else:
      if c == ",":
        encrypted_array.append(int(placeholder_string))
        placeholder_string = ""
      else:
        pass
  encrypted_array.append(int(placeholder_string))
  
  for i in encrypted_array:
    decrypted_int = (i ** private_keys[0] % private_keys[1])
    if decrypted_int > 126:
      decrypted_string = "Error: Invalid message"
      break;
    decrypted_string += chr(decrypted_int)
  return decrypted_string


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * *
# * * *  BASE 32  * * *
# * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/base32", strict_slashes=False)
def base32():  
  explanation = "Base32 encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "base32.html",
    explanation = explanation
  )

def base32_encrypt(my_string):
    clean_string = line_break_to_space(my_string)
    encode_string = clean_string.encode('utf-8')
    new_string = ""
    new_string_encrypt = b64.b32encode(encode_string)
    new_string = new_string_encrypt.decode('utf-8')
    return new_string
  
def base32_decrypt(my_encoded_string):
    new_string = ""
    new_string_encrypt= b64.b32decode(my_encoded_string)
    new_string = new_string_encrypt.decode('utf-8')
    return new_string

@app.route("/base32/encrypt", methods=["GET"], strict_slashes=False)
def base32_encrypt_get():
  explanation = "Base 32 encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "base32_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/base32/encrypt", methods=["POST"], strict_slashes=False)
def base32_encrypt_post():
  message = request.form.get("message")
  if message:
    encrypted_message = base32_encrypt(message)
    message = base32_decrypt(encrypted_message)
    return render_template(
      "base32_encrypt_post.html",
      message = message,
      encrypted_message = encrypted_message,
      encrypt = "active"
    )

@app.route("/base32/decrypt", methods=["GET"], strict_slashes=False)
def base32_decrypt_get():
  explanation = "Base 32 encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "base32_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )

@app.route("/base32/decrypt", methods=["POST"], strict_slashes=False)
def base32_decrypt_post():
  message = request.form.get("message")
  if message:
    decrypted_message = base32_decrypt(message)
    return render_template(
      "base32_decrypt_post.html",
      message = message,
      decrypted_message = decrypted_message,
      decrypt = "active"
    )


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * *
# * * *  BASE 64  * * *
# * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/base64", strict_slashes=False)
def base64():  
  explanation = "Base64 encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "base64.html",
    explanation = explanation
  )

def base64_encrypt(my_string):
    encode_string = my_string.encode('utf-8')
    new_string = ""
    new_string_encrypt = b64.b64encode(encode_string)
    new_string = new_string_encrypt.decode('utf-8')
    return new_string
  
def base64_decrypt(my_encoded_string):
    encode_string = my_encoded_string.encode('utf-8')
    new_string = ""
    new_string_encrypt= b64.b64decode(encode_string)
    new_string = new_string_encrypt.decode('utf-8')
    return new_string

@app.route("/base64/encrypt", methods=["GET"], strict_slashes=False)
def base64_encrypt_get():
  explanation = "Base 64 encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "base64_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/base64/encrypt", methods=["POST"], strict_slashes=False)
def base64_encrypt_post():
  message = request.form.get("message")
  if message:
    encrypted_message = base64_encrypt(message)
    message = base64_decrypt(encrypted_message)
    return render_template(
      "base64_encrypt_post.html",
      message = message,
      encrypted_message = encrypted_message,
      encrypt = "active"
    )

@app.route("/base64/decrypt", methods=["GET"], strict_slashes=False)
def base64_decrypt_get():
  explanation = "Base 64 encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "base64_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )

@app.route("/base64/decrypt", methods=["POST"], strict_slashes=False)
def base64_decrypt_post():
  message = request.form.get("message")
  if message:
    decrypted_message = base64_decrypt(message)
    return render_template(
      "base64_decrypt_post.html",
      message = message,
      decrypted_message = decrypted_message,
      decrypt = "active"
    )


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * *
# * * * * OFFSET* * * *
# * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/simple-offset/", methods=["GET"], strict_slashes=False)
def simple_offset_generator():
  return render_template(
    "simple_offset_generator.html"
  )


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * 
# * * * * OFFSET ENCRYPT* * * *
# * * * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

@app.route("/offset/encrypt", methods=["GET"], strict_slashes=False)
def offset_encrypt_get():
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/offset/encrypt", methods=["POST"], strict_slashes=False)
def offset_encrypt_post():
  message = request.form.get("message")
  offset = request.form.get("offset")
  if message and offset:
    encrypted_message = offset_encrypt(message, offset)
    message = offset_decrypt(encrypted_message, offset)
    return render_template(
      "offset_encrypt_post.html",
      offset = offset,
      message = message,
      encrypted_message = encrypted_message,
      encrypt = "active"
    )
  else:
    return render_template(
      "error.html",
      error = "" + str(message) + " -- " + str(offset)
    )
  

# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * 
# * * * * OFFSET DECRYPT* * * *
# * * * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

@app.route("/offset/decrypt", methods=["GET"], strict_slashes=False)
def offset_decrypt_get():
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )

@app.route("/offset/decrypt", methods=["POST"], strict_slashes=False)
def offset_decrypt_post():
  message = request.form.get("message")
  offset = request.form.get("offset")
  if message and offset:
    decrypted_message = offset_decrypt(message, offset)
    return render_template(
      "offset_decrypt_post.html",
      offset = offset,
      message = message,
      decrypted_message = decrypted_message,
      decrypt = "active"
    )
  else: 
    return render_template(
      "error.html",
      error = ""
    )
  

# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * 
# * * * * OFFSET INDEX* * * *
# * * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

@app.route("/offset", strict_slashes=False)
def offset():  
  explanation = "Offset encryption converts each character in your message to it's corresponding ASCII code. " 
  return render_template(
    "offset.html",
    explanation = explanation
  )


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * 
# * * * *SHARED KEY * * * *
# * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * * *
# * * * * SHARED KEY ENCRYPT* * * *
# * * * * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/shared-key/encrypt", methods=["GET"], strict_slashes=False)
def shared_key_encrypt_get():
  explanation = ""
  return render_template(
    "shared_key_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/shared-key/encrypt", methods=["POST"], strict_slashes=False)
def shared_key_encrypt_post():
  message = request.form.get("message")
  key_1 = request.form.get("key1").lower()
  key_2 = request.form.get("key2").lower()
  key_3 = request.form.get("key3").lower()
  key = key_1 + key_2 + key_3
  if message and key:
    encrypted_message = shared_key_encrypt(message, key)
    return render_template(
    "shared_key_encrypt_post.html",
    key = key,
    message = message,
    encrypted_message = encrypted_message,
    encrypt = "active"
    )
  else:
    return render_template("error.html")

  
# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * * *
# * * * * SHARED KEY DECRYPT* * * *
# * * * * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/shared-key/decrypt", methods=["GET"], strict_slashes=False)
def shared_key_decrypt_get():
  explanation = ""
  return render_template(
    "shared_key_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )  
  
@app.route("/shared-key/decrypt", methods=["POST"], strict_slashes=False)
def shared_key_decrypt_post():
  message = request.form.get("message")
  key_1 = request.form.get("key1").lower()
  key_2 = request.form.get("key2").lower()
  key_3 = request.form.get("key3").lower()
  key = key_1 + key_2 + key_3
  if message and key:
    decrypted_message = shared_key_decrypt(message, key)
    return render_template(
    "shared_key_decrypt_post.html",
    key = key,
    message = message,
    decrypted_message = decrypted_message,
    decrypt = "active"
    )
  else:
    return render_template("error.html")


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * * 
# * * * *SHARED KEY INDEX * * * *
# * * * * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -
  
@app.route("/shared-key", strict_slashes=False)
def shared_key():
  explanation = ""
  return render_template(
    "shared-key.html",
    explanation = explanation
  )


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * 
# * * * * PUBLIC KEY* * * *
# * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

@app.route("/public-key/generate-keys", methods=["GET"], strict_slashes=False)
def public_key_generate_keys_get():
  explanation = ""
  return render_template(
    "public_key_generate_keys_get.html",
    explanation = explanation,
    primes = primes,
    generate_keys = "active"
  )

@app.route("/public-key/primes", methods=["POST"], strict_slashes=False)
def available_coprimes():
  prime_1 = int(request.form.get("prime1"))
  prime_2 = int(request.form.get("prime2"))
  larger_prime = prime_1
  if (prime_1 - prime_2) < 0:
    larger_prime = prime_2
  modulus = prime_1 * prime_2
  coprimes_of = (prime_1 - 1) * (prime_2 - 1)
  coprimes = []
  for n in range(larger_prime + 2, coprimes_of):
    if coprime(n, coprimes_of):
      if generate_keys(prime_1, prime_2, n):
        coprimes.append(n)
  return jsonify(coprimes)

@app.route("/public-key/keys", methods=["POST"], strict_slashes=False)
def keys():
  prime_1 = int(request.form.get("prime1"))
  prime_2 = int(request.form.get("prime2"))
  coprime = int(request.form.get("coprime"))
  keys = generate_keys(prime_1, prime_2, coprime)
  if keys:
    return jsonify({"publicKeys": keys["public_keys"], "privateKeys": keys["private_keys"]})
  else:
    return jsonify({"error": "No keys found, select different numbers (probably higher numbers)."})  
  
  
# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * * *
# * * * * PUBLIC KEY ENCRYPT* * * *
# * * * * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/public-key/encrypt", methods=["GET"], strict_slashes=False)
def public_key_encrypt_get():
  explanation = ""
  return render_template(
    "public_key_encrypt_get.html",
    explanation = explanation,
    encrypt = "active"
  )

@app.route("/public-key/encrypt", methods=["POST"], strict_slashes=False)
def public_key_encrypt_post():
  public_key = []
  public_key.append(int(request.form.get("public-key-1")))
  public_key.append(int(request.form.get("public-key-2")))
  message = request.form.get("message")
  if public_key and message:
    return render_template(
      "public_key_encrypt_post.html",
      public_keys = public_key,
      message = message,
      encrypted_message = public_key_encrypt(message, public_key),
      encrypt = "active"
    )
  else:
    return render_template("error.html")


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * * *
# * * * * PUBLIC KEY DECRYPT* * * *
# * * * * * * * * * * * * * * * * *
# - - - - - - - - - - - - - - - -

@app.route("/public-key/decrypt", methods=["GET"], strict_slashes=False)
def public_key_decrypt_get():
  explanation = ""
  return render_template(
    "public_key_decrypt_get.html",
    explanation = explanation,
    decrypt = "active"
  )

@app.route("/public-key/decrypt", methods=["POST"], strict_slashes=False)
def public_key_decrypt_post():
  private_keys = []
  private_keys.append(int(request.form.get("private-key-1")))
  private_keys.append(int(request.form.get("private-key-2")))
  message = request.form.get("message")
  if private_keys and message:
    return render_template(
      "public_key_decrypt_post.html",
      private_keys = private_keys,
      encrypted_message = message,
      decrypted_message = public_key_decrypt(message, private_keys),
      decrypt = "active"
    )
  else:
    return render_template(
      "error.html"
    )


# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * * * * * * 
# * * * * PUBLIC KEY INDEX* * * *
# * * * * * * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

@app.route("/public-key", strict_slashes=False)
def public_key():
  explanation = ""
  return render_template(
    "public-key.html",
    explanation = explanation
  )

# - - - - - - - - - - - - - - - -
# * * * * * * * * * * * 
# * * * * PUBLIC* * * *
# * * * * * * * * * * * 
# - - - - - - - - - - - - - - - -

@app.route('/<path:path>', strict_slashes=False)
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()