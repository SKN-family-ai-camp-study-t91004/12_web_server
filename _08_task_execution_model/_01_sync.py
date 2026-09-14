"""동기 실행: 한 작업이 반환된 뒤 다음 작업을 호출한다."""
import time


def task_sync(n):
    print(f'작업 {n} 시작')
    # [블로킹] time.sleep은 현재 스레드를 멈춰 다음 작업도 기다리게 한다.
    time.sleep(1)
    print(f'작업 {n} 종료')


def main():
    start = time.perf_counter()
    # [동기 실행] 앞 작업이 끝난 뒤 다음 작업을 호출한다.
    for i in range(3):
        task_sync(i)
    # 세 번의 블로킹 대기가 겹치지 않아 전체 시간에 차례로 누적된다.
    print(f'총 소요시간 {time.perf_counter() - start:.2f}초')


if __name__ == '__main__':
    main()