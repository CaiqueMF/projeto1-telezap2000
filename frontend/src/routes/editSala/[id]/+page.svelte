<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
  
    let id;
    let nome = '';
    let tipos = '';
  
    $: id = $page.params.id;
  
    onMount(async () => {
      await fetchSala();
    });
  
    async function fetchSala() {
      try {
        const response = await axios.get(`http://localhost:5000/api/salas/${id}`);
        const sala = response.data;
        nome = sala.nome;
        tipos = sala.tipos
      } catch (error) {
        console.error(error);
      }
    }
  
    async function updateSala() {
      try {
        const updatedSala = {
          nome,
          tipos
        };
        await axios.put(`http://localhost:5000/api/salas/${id}`, updatedSala);
        goto('/salas');
      } catch (error) {
        console.error(error);
      }
    }
  </script>
  
  <main>
    <h1>Editar Cadeira</h1>
    <form on:submit|preventDefault={updateSala}>
        <input bind:value={nome} placeholder="Nome" required />
        <input bind:value={tipos} placeholder="Nome" required />
        <button type="submit">Atualizar</button>
    </form>
  </main>
  