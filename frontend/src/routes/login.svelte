<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { token, user } from '../store';
  
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
            goto('/turmas'); // Use goto for navigation
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
    <h1>Login</h1>
  
    <!-- Error message -->
    {#if error}
      <p style="color: red;">{error}</p>
    {/if}
  
    <!-- Login form -->
    <form on:submit|preventDefault={handleLogin}>
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" bind:value={username} required />
      </div>
  
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" bind:value={password} required />
      </div>
  
      <button type="submit">Login</button>
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
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  
    input {
      padding: 0.5rem;
      font-size: 1rem;
    }
  
    button {
      padding: 0.5rem 1rem;
      font-size: 1rem;
      cursor: pointer;
    }
  </style>
  