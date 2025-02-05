class MT19937_64:
    NN = 312
    MM = 156
    MATRIX_A = 0xB5026F5AA96619E9
    UM = 0xFFFFFFFF80000000
    LM = 0x7FFFFFFF

    def __init__(self, seed: int):
        self.MT = [0] * self.NN
        self.index = self.NN
        self.MT[0] = seed & 0xFFFFFFFFFFFFFFFF
        for i in range(1, self.NN):
            self.MT[i] = (6364136223846793005 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 62)) + i) & 0xFFFFFFFFFFFFFFFF

    def twist(self):
        for i in range(self.NN):
            x = (self.MT[i] & self.UM) + (self.MT[(i + 1) % self.NN] & self.LM)
            xA = x >> 1
            if x & 1:
                xA ^= self.MATRIX_A
            self.MT[i] = self.MT[(i + self.MM) % self.NN] ^ xA
        self.index = 0

    def extract_number(self) -> int:
        if self.index >= self.NN:
            self.twist()
        y = self.MT[self.index]
        self.index += 1
        y ^= (y >> 29) & 0x5555555555555555
        y ^= (y << 17) & 0x71D67FFFEDA60000
        y ^= (y << 37) & 0xFFF7EEE000000000
        y ^= y >> 43
        return y & 0xFFFFFFFFFFFFFFFF

    def __call__(self) -> int:
        return self.extract_number()
