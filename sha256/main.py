# Functions for SHA-256 (NIST FIPS 180-4)
def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def rotr(x, n):
    return (x >> n) | (x << (32 - n))

def shr(x, n):
    return x >> n

def sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

def sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

def gamma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)

def gamma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)

def read_file_in_512_bit_blocks_with_padding(message):
    block_size = 64  # 512 bits = 64 bytes
    blocks = []

    # Calculate the length of the file in bits
    file_length_bits = len(message) * 8

    # Append a single '1' bit represented by 0x80 in hexadecimal
    message += b'\x80'

    # Append '0' bits until the message length is 448 modulo 512
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    # Append the original message length as a 64-bit big-endian integer
    message += file_length_bits.to_bytes(8, byteorder='big')

    # Partition the padded message into 512-bit blocks
    for i in range(0, len(message), block_size):
        blocks.append(message[i:i + block_size])

    return blocks

def sha_256(message):

    # Initial hash values for SHA-256 (NIST FIPS 180-4)
    H0 = 0x6a09e667
    H1 = 0xbb67ae85
    H2 = 0x3c6ef372
    H3 = 0xa54ff53a
    H4 = 0x510e527f
    H5 = 0x9b05688c
    H6 = 0x1f83d9ab
    H7 = 0x5be0cd19

    # Constants for SHA-256 (NIST FIPS 180-4)
    K = bytearray.fromhex('428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5'
                        'd807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174'
                        'e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da'
                        '983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967'
                        '27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85'
                        'a2bfe8a1 a81a664b c24b8b70 c76c51a3 d192e819 d6990624 f40e3585 106aa070'
                        '19a4c116 1e376c08 2748774c 34b0bcb5 391c0cb3 4ed8aa4a 5b9cca4f 682e6ff3'
                        '748f82ee 78a5636f 84c87814 8cc70208 90befffa a4506ceb bef9a3f7 c67178f2'.replace(" ", ""))


    def int_from_bytes(x: bytes) -> int:
        return int.from_bytes(x, 'big')


    K = [int_from_bytes(K[i*4:(i+1)*4]) for i in range(len(K) // 4)]
    blocks = read_file_in_512_bit_blocks_with_padding(message)

    for block in blocks:
        # Message schedule preparation
        # Break the current 512-bit block into 16 32-bit big-endian words
        words = []
        for i in range(0, len(block), 4):
            words.append(int.from_bytes(block[i:i + 4], byteorder='big'))

        # Extend the first 16 words into the remaining 48 words
        for i in range(16, 64):
            words.append((gamma1(words[i - 2]) + words[i - 7] + gamma0(words[i - 15]) + words[i - 16]) & 0xffffffff)

        
        # Initialize the eight working variables with the (i-1)st hash value
        a = H0
        b = H1
        c = H2
        d = H3
        e = H4
        f = H5
        g = H6
        h = H7

        # Compression function main loop
        for i in range(64):
            T1 = (h + sigma1(e) + ch(e, f, g) + K[i] + words[i]) & 0xffffffff
            T2 = (sigma0(a) + maj(a, b, c)) & 0xffffffff
            h = g
            g = f
            f = e
            e = (d + T1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xffffffff
        
        # Add the compressed chunk to the current hash value
        H0 = (H0 + a) & 0xffffffff
        H1 = (H1 + b) & 0xffffffff
        H2 = (H2 + c) & 0xffffffff
        H3 = (H3 + d) & 0xffffffff
        H4 = (H4 + e) & 0xffffffff
        H5 = (H5 + f) & 0xffffffff
        H6 = (H6 + g) & 0xffffffff
        H7 = (H7 + h) & 0xffffffff

    # Produce the final hash value (big-endian)
    return H0.to_bytes(4, byteorder='big') + H1.to_bytes(4, byteorder='big') + H2.to_bytes(4, byteorder='big') + \
              H3.to_bytes(4, byteorder='big') + H4.to_bytes(4, byteorder='big') + H5.to_bytes(4, byteorder='big') + \
                H6.to_bytes(4, byteorder='big') + H7.to_bytes(4, byteorder='big')


if __name__ == "__main__":

    # NIST FIPS 180-4 Secure Hash Standard

    # NIST CAVS 11.0 SHA-2 short message test vector 1
    message = b''
    expected_hash = bytearray.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    sha_256_hash = sha_256(message)

    assert (sha_256_hash == expected_hash)

    # NIST CAVS 11.0 SHA-2 long message test vector 1
    message = bytearray.fromhex('451101250ec6f26652249d59dc974b7361d571a8101cdfd36aba3b5854d3ae086b5fdd4597721b66e3c0dc'
                                '5d8c606d9657d0e323283a5217d1f53f2f284f57b85c8a61ac8924711f895c5ed90ef17745ed2d728abd22'
                                'a5f7a13479a462d71b56c19a74a40b655c58edfe0a188ad2cf46cbf30524f65d423c837dd1ff2bf462ac41'
                                '98007345bb44dbb7b1c861298cdf61982a833afc728fae1eda2f87aa2c9480858bec')

    expected_hash = bytearray.fromhex('3c593aa539fdcdae516cdf2f15000f6634185c88f505b39775fb9ab137a10aa2')

    sha_256_hash = sha_256(message)

    assert (sha_256_hash == expected_hash)

    print("All tests passed!")