<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    let nome = ''
    let tipos = ''
    let salas = [];
    let pesquisaNome = ""
    onMount(async () => {
	    await fetchSala();
	});

    async function fetchSala() {
      try {
        const response = await axios.get(`http://localhost:5000/api/salas`);
        salas = response.data;
      } catch (error) {
        console.error(error);
      }
    }

    async function addSala() {
	  try {
		  const newSala = {
		    nome,
        tipos
		  };
		await axios.post('http://localhost:5000/api/salas', newSala);
		await fetchSala();
		nome = '';
    tipos = ''
	  } catch (error) {
		console.error(error);
	  }
	}
  </script>
  
  <h1>Salas</h1>
  <input type="text" bind:value={pesquisaNome} placeholder="Buscar sala">
  <form on:submit|preventDefault={addSala}>
    <input bind:value={nome} placeholder="Nome" required />
    <select bind:value={tipos} required>
      <option value="" disabled selected>Tipo de sala</option>
      <option value="Sala normal">Sala normal</option>
      <option value="Sala grande">Sala grande</option>
      <option value="Ateliê">Ateliê</option>
      <option value="Laboratório básico">Laboratório básico</option>
      <option value="Laboratório avançado">Laboratório avançado</option>
    </select>
    <button type="submit">Adicionar</button>
  </form>
  <ul>
    {#each salas as sala (sala.id)}
      {#if sala.nome.toLowerCase().includes(pesquisaNome.toLowerCase()) || pesquisaNome == "" }
          <li>
            {sala.nome} - {sala.tipos}
        </li>
        <a href={`../editSala/${sala.id}`}>Editar</a>
      {/if} 
    {/each}
  </ul>  