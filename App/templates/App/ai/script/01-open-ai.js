<!-- JavaScript for handling chat -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('chat-form').addEventListener('submit', function(e) {
                e.preventDefault();

                var messageInput = document.querySelector('input[name="message"]');
                var message = messageInput.value;

                if (!message.trim()) return;  // 빈 메시지 전송 방지

                // 채팅창에 사용자의 메시지 추가
                var chatMessages = document.querySelector('.direct-chat-messages');
                chatMessages.innerHTML += `
                    <div class="direct-chat-msg right">
                        <div class="direct-chat-info clearfix">
                            <span class="direct-chat-name pull-right">ME</span>
                            <span class="direct-chat-timestamp pull-left">${new Date().toLocaleString()}</span>
                        </div>
                        <div class="direct-chat-text">
                            ${message}
                        </div>
                    </div>
                `;
                chatMessages.scrollTop = chatMessages.scrollHeight;  // 스크롤을 최신 메시지로 이동

                // AJAX 요청을 통해 서버로 메시지 전송
                fetch(`/openai/${encodeURIComponent(message)}`)
                    .then(response => response.json())
                    .then(data => {
                        // 서버에서 받은 ChatGPT의 응답을 채팅창에 추가
                        chatMessages.innerHTML += `
                            <div class="direct-chat-msg">
                                <div class="direct-chat-info clearfix">
                                    <span class="direct-chat-name pull-left">ChatGPT</span>
                                    <span class="direct-chat-timestamp pull-right">${new Date().toLocaleString()}</span>
                                </div>
                                <div class="direct-chat-text">
                                    ${data.message}
                                </div>
                            </div>
                        `;
                        chatMessages.scrollTop = chatMessages.scrollHeight;  // 스크롤을 최신 메시지로 이동
                    });

                // 입력 필드 초기화
                messageInput.value = '';
            });
        });
    </script>