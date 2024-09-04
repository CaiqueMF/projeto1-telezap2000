<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { token, user } from '../../store';
  
    let username = '';
    let password = '';
    let error = null;
  
    async function handleLogin() {
      error = null;
      const res = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });
       if (res.ok) {
        const data = await res.json();
        token.set(data.access_token);
        user.set({
          isAuthenticated: true,
          username: username,
          role: data.role
        });
        if (data.role == 'admin'){
            goto('/turmas');
        }else {
            goto('/cadeiras')
        }
      } else {
        error = 'Invalid username or password';
      }
    }
    onMount(() => {
        const currentUser = $user;
        if (currentUser.isAuthenticated) {
            if (currentUser.role === 'admin') {
                goto('/turmas');
            } else {
                goto('/cadeiras');
            }
        }
    }); 
</script>
  
  <main>
    <form on:submit|preventDefault={handleLogin}>
        <div class="return">
            <i class="fa-solid fa-x"></i>
        </div>
        {#if error}
            <p style="color: red;">{error}</p>
        {/if}
        <div class="inputs">
            <h1>Login</h1>
            <label for="username">Usuário:</label>
            <input type="text" id="username" bind:value={username} required />
            <label for="password">Senha:</label>
            <input type="password" id="password" bind:value={password} required />
            <button type="submit">Entrar</button>
        </div>
  
        <div class="createAccount">
            <p>Novo por aqui? <a href="/register">Crie uma conta</a></p>
        </div>
    </form>
  </main>
  
  <style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }
  
    form {
        width: 40%;
        height: 60%;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #5A7302;
        color: black;
        border: 1px solid black;
        border-radius: 10px;
        position: relative;
    }
  
    .return {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        width: 100%;
        font-size: 1.5rem;
        padding: 0.5rem 1rem;
        background-color: #5A7302;
        border-top-right-radius: 10px;
        border-top-left-radius: 10px;
    }
  
    .return i {
        padding: 0.5rem;
        cursor: pointer;
    }
  
    input {
        padding: 0.5rem 0;
        margin: 0 2rem;
        font-size: 1rem;
        border: 1px black solid;
        border-radius: 10px;
    }
  
    button {
        background-color: #565151;
        border-style: none;
        padding: 1rem;
        margin: 0 2rem;
        font-size: 1rem;
        cursor: pointer;
        color: white;
        font-size: 30px;
        border-radius: 10px;
    }
  
    .inputs {
        flex-grow: 3;
        display: flex;
        width: 100%;
        flex-direction: column;
        justify-content: center;
        gap: 10px;
        background-color: #D9D9D9;
    }
  
    h1 {
        position: relative;
        bottom: 12%;
    }
  
    label {
        display: flex;
        margin: 0 2rem;
    }
  
    .createAccount {
        flex-grow: 2;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    a {
        color: white;
    }
  </style>
  