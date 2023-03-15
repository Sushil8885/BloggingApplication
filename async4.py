import asyncio
import time


async def count3():
    print("five")
    await asyncio.sleep(1)
    print("six")


async def count2():
    print("three")
    await asyncio.sleep(1)
    print("four")


async def count1():
    print("one")
    await asyncio.sleep(1)
    print("two")


async def main():
    await asyncio.gather(count1(), count2(), count3())


if __name__ == "__main__":
    print(f"started at {time.strftime('%X')}")
    asyncio.run(main())
    print(f"finished at {time.strftime('%X')}")