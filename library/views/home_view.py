from django.http import HttpResponse

def home_view(request):
    html = """
    <html>
    <head>
        <title>Start - JWT Login</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            h1 { color: #333; }
            input, button {
                padding: 10px;
                margin: 5px 0;
                font-size: 16px;
                width: 300px;
            }
            .link { margin: 15px 0; }
            .token-box {
                background: #eee;
                padding: 10px;
                margin-top: 15px;
                word-break: break-word;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <h1>Strona startowa aplikacji</h1>

        <div class="link"><a href="/admin/">Panel administracyjny</a></div>
        <div class="link"><a href="/api/">REST API</a></div>
        <div class="link"><a href="/graphql/">GraphQL</a></div>
        <div class="link"><a href="/swagger/">Swagger</a></div>
        <div class="link"><a href="/redoc/">ReDoc</a></div>

        <hr/>
        <h2>Uzyskaj token JWT</h2>
        <form id="login-form">
            <input type="text" id="username" placeholder="Nazwa użytkownika" required /><br/>
            <input type="password" id="password" placeholder="Hasło" required /><br/>
            <button type="submit">Zaloguj się</button>
        </form>

        <div id="result"></div>

        <script>
            const form = document.getElementById('login-form');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;

                const response = await fetch('/api/token/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('result').innerHTML = `
                        <p>Token uzyskany:</p>
                        <div class="token-box"><strong>Access:</strong><br/>${data.access}</div>
                        <div class="token-box"><strong>Refresh:</strong><br/>${data.refresh}</div>
                    `;
                } else {
                    document.getElementById('result').innerHTML = `
                        <p style="color: red;">Błąd logowania: ${data.detail || 'Nieprawidłowe dane'}</p>
                    `;
                }
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)
