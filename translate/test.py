class Solution:
    def mySqrt(self, x: int) -> int:
        return self.compute(x, 0, x)

    def compute(self, x, start, end):
        middle = (end + start) // 2
        print(start,middle,end)
        if end - start <= 1:
            return start
        if middle * middle == x:
            return middle
        elif middle * middle > x:
            return self.compute(x, start, middle)
        else:
            return self.compute(x, middle, end)

if __name__ == "__main__":
    so = Solution()
    ans = so.mySqrt(1)
    print(ans)