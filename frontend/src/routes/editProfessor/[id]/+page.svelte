<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
  
    let id;
    let nome = '';
  
    $: id = $page.params.id;
  
    onMount(async () => {
      await fetchProfessor();
    });
  
    async function fetchProfessor() {
      try {
        const response = await axios.get(`http://localhost:5000/api/professores/${id}`);
        const professor = response.data;
        nome = professor.nome;
      } catch (error) {
        console.error(error);
      }
    }
  
    async function updateProfessor() {
      try {
        const updatedProfessor = {
          nome
        };
        await axios.put(`http://localhost:5000/api/professores/${id}`, updatedProfessor);
        goto('/professores');
      } catch (error) {
        console.error(error);
      }
    }
  </script>
  
  <main>
    <h1>Editar Cadeira</h1>
    <form on:submit|preventDefault={updateProfessor}>
        <input bind:value={nome} placeholder="Nome" required />
        <button type="submit">Atualizar</button>
    </form>
  </main>
  