"""requests는 응답을 기다리는 동안 호출한 스레드를 막는다."""
import argparse
import time
import requests


def main(url):
    start = time.perf_counter()
    # [순차 실행] 앞 요청이 끝난 뒤 다음 요청을 보낸다.
    for n in range(3):
        # [블로킹] requests.get은 응답을 기다리는 동안 현재 스레드를 멈춘다.
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print(f'작업 {n} 완료: {response.status_code}')
    # 세 요청의 블로킹 대기가 겹치지 않아 전체 시간에 차례로 누적된다.
    print(f'총 소요시간 {time.perf_counter() - start:.2f}초')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://httpbin.org/delay/2')

    main(parser.parse_args().url)