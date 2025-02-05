from .aes import oqs_mhy128_enc_c
from .magic import key_xorpad_table, aes_xorpad_table0, aes_xorpad_table1
from .mt import MT19937_64

def key_scramble(key: bytearray) -> bytes:
    round_keys = bytearray(11 * 16)
    for r in range(11):
        for i in range(16):
            for j in range(16):
                idx = (r << 8) + (i * 16) + j
                round_keys[r * 16 + i] ^= aes_xorpad_table1[idx] ^ aes_xorpad_table0[idx]

    chip = oqs_mhy128_enc_c(bytes(key), list(round_keys))
    return bytes(chip)

def get_decrypt_vector(final_key: bytes, data: bytes, output_size: int = 4096) -> bytes:
    if len(data) != 2048:
        raise ValueError(f'data must be 2048 bytes (got {len(data)})')

    val = 0xFFFFFFFFFFFFFFFF
    for i in range(0, len(data), 8):
        chunk = int.from_bytes(data[i:i+8], 'little')
        val ^= chunk
    key0 = int.from_bytes(final_key[:8], 'little')
    key1 = int.from_bytes(final_key[8:], 'little')
    seed = key1 ^ 0xCEAC3B5A867837AC ^ val ^ key0

    rng = MT19937_64(seed)
    out_bytes = bytearray()
    for _ in range(output_size // 8):
        num = rng()
        out_bytes.extend(num.to_bytes(8, 'little'))
    return bytes(out_bytes)

def derive(ec2b_data: bytes) -> bytes:
    if len(ec2b_data) != 2076:
        raise ValueError(f'ec2b_data must be 2076 bytes (got {len(ec2b_data)})')

    key = bytearray(ec2b_data[8:8+16])
    data = ec2b_data[28:28+2048]
    scrambled_key = key_scramble(key)
    final_key = bytes(s ^ k for s, k in zip(scrambled_key, key_xorpad_table))
    xorpad = get_decrypt_vector(final_key, data, 4096)
    return xorpad
