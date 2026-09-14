"""aiohttp의 네트워크 대기 동안 다른 요청을 진행한다. 동시성과 병렬성을 구분한다."""
import argparse
import asyncio
import time
import aiohttp


# [코루틴 함수] fetch_url은 비동기 HTTP 작업의 실행 절차를 정의한다.
async def fetch_url(session, url, n):
    print(f'요청 {n} 시작')

    # [대기·양보] HTTP 응답을 기다리는 동안 다른 태스크가 진행할 수 있다.
    async with session.get(url) as response:

        # 400, 500 상태 코드 반환 시 예외 발생
        response.raise_for_status()

        # [대기·양보] 본문 수신을 기다릴 때 제어권을 넘기고,
        # 받은 JSON을 Python 값(dict)으로 바꾼다.
        data = await response.json()

        print(f'요청 {n} 완료: {response.status}')
        return data


# [코루틴 함수] main은 세 요청을 하나의 이벤트 루프에서 조율한다.
async def main(url):
    start = time.perf_counter()

    # 세 요청이 연결 풀을 공유하도록 하나의 비동기 세션을 사용한다.
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        # [코루틴 객체] 각 fetch_url(...) 호출은 실행 전 객체를 만든다.
        # [태스크·동시 실행] gather가 태스크로 예약하며, 결과는 입력 순서로 모인다.
        results = await asyncio.gather(
            *(fetch_url(session, url, i) for i in range(3))
            # fetch_url(session, url, 0),
            # fetch_url(session, url, 1),
            # fetch_url(session, url, 2)
        )

    print('응답 개수:', len(results))
    print(f'총 소요시간 {time.perf_counter() - start:.2f}초')

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://httpbin.org/delay/2')
    # [이벤트 루프] 새 루프에서 main 코루틴을 실행하고, 끝나면 루프를 정리한다.
    asyncio.run(main(parser.parse_args().url))