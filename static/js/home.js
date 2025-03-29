document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById('login-form');
  const resultDiv = document.getElementById('result');

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
      resultDiv.innerHTML = `
        <p>Token uzyskany:</p>
        <div class="token-box"><strong>Access:</strong><br/>${data.access}</div>
        <div class="token-box"><strong>Refresh:</strong><br/>${data.refresh}</div>
      `;
    } else {
      resultDiv.innerHTML = `<p style="color: red;">Błąd logowania: ${data.detail || 'Nieprawidłowe dane'}</p>`;
    }
  });
});
