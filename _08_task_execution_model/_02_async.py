"""비동기 실행: 기다리는 작업에서 제어권을 넘겨 다른 작업을 진행한다."""
import asyncio
import time


# [코루틴 함수] async def로 중간에 대기·재개할 수 있는 함수를 정의한다.
async def async_task(n):
    print(f'작업 {n} 시작')

    # [대기·양보] 1초 타이머를 기다리며 이벤트 루프에 제어권을 넘긴다.
    # await asyncio.sleep(1) # 1초 멈췄다가 끝나면 실행

    # [블로킹] 이벤트 루프 스레드가 멈춰 다른 태스크도 진행하지 못한다.
    time.sleep(1)

    print(f'작업 {n} 완료')
    return n


# [코루틴 함수] main도 이벤트 루프에서 실행될 코루틴 함수이다.
async def main():
    start = time.perf_counter()

    # [코루틴 객체] 각 async_task(i) 호출은 아직 실행되지 않은 객체를 만든다.
    # [태스크·동시 실행] gather가 태스크로 예약하며, 결과는 입력 순서로 모인다.
    results = await asyncio.gather(
        *(async_task(i) for i in range(3))
        # async_task(0),
        # async_task(1),
        # async_task(2)
    )
    print('반환값:', results)
    # 타이머 대기를 겹친 동시 실행이며 CPU 계산을 병렬 처리한 것은 아니다.
    print(f'총 소요시간 {time.perf_counter() - start:.2f}초')


if __name__ == '__main__':
    # [이벤트 루프] 새 루프에서 main 코루틴을 실행하고, 끝나면 루프를 정리한다.
    asyncio.run(main())