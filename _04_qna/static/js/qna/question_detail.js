// DOM의 data 속성으로 Django가 만든 URL을 받는다. 응답 문자열은 HTML로 삽입하지 않는다.
const detail = document.querySelector('#question-detail');
// sessionid 쿠키가 로그인 사용자를 찾고, 폼에서 읽은 이 토큰은 POST의 CSRF 검사에 쓰인다.
const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

function requireLogin() {
    if (detail.dataset.authenticated === 'true') return true;
    if (confirm('로그인이 필요합니다. 로그인하시겠습니까?')) location.href = detail.dataset.loginUrl;
    return false;
}

document.answerCreateFrm.addEventListener('submit', (event) => {
    if (!requireLogin()) event.preventDefault();
});
document.querySelectorAll('.recommend').forEach((button) => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        if (!requireLogin()) return;
        try {
            button.disabled = true;
            // 추천할 객체는 URL에 담겨 있다. CSRF 토큰은 세션을 사용하는 POST를 보호한다.
            const response = await fetch(button.dataset.uri, {method: 'POST', headers: {'X-CSRFToken': csrf}});
            if (!response.ok) throw new Error('추천 요청을 처리하지 못했습니다.');
            // JSON 문자열을 객체로 읽어 서버의 최종 추천 수를 표시한다. 취소도 반영된다.
            const data = await response.json();
            button.querySelector('span').textContent = data.vote_count;
        } catch (error) {
            alert(error.message);
        } finally {
            button.disabled = false;
        }
    });
});
document.querySelectorAll('[data-answer-id]').forEach((button) => {
    button.addEventListener('click', () => {
        document.answerModifyFrm.action = button.dataset.modifyUrl;
        // textarea는 value로 갱신하여 모달을 여러 번 열어도 현재 내용을 보여 준다.
        document.querySelector('#content-modify').value = button.dataset.answerContent;
    });
});
