<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    let nome = '';
    let professores = [];
    let pesquisaNome = ""
    onMount(async () => {
	    await fetchProfessor();
	});

    async function fetchProfessor() {
      try {
        const response = await axios.get(`http://localhost:5000/api/professores`);
        professores = response.data;
      } catch (error) {
        console.error(error);
      }
    }

    async function addProfessor() {
	  try {
		  const newProfessor = {
		    nome
		  };
		await axios.post('http://localhost:5000/api/professores', newProfessor);
		await fetchProfessor();
		nome = '';
	  } catch (error) {
		console.error(error);
	  }
	}
  
  </script>
<h1>Professores</h1>
<input type="text" bind:value={pesquisaNome} placeholder="Buscar professor">
<form on:submit|preventDefault={addProfessor}>
	<input bind:value={nome} placeholder="Nome" required />
	<button type="submit">Adicionar</button>
</form>
  
  <ul>
    {#each professores as professor (professor.id)}
      {#if professor.nome.toLowerCase().includes(pesquisaNome.toLowerCase()) || pesquisaNome == "" }
        <li>
          {professor.nome}
      </li>
      <a href={`../editProfessor/${professor.id}`}>Editar</a>
      {/if}
    {/each}
  </ul>