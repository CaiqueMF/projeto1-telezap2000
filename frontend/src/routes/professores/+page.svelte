<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    let nome = '';
    let professores = [];
  
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

<form on:submit|preventDefault={addProfessor}>
	<input bind:value={nome} placeholder="Nome" required />
	<button type="submit">Adicionar</button>
</form>
  
  <h1>Professores</h1>
  <ul>
    {#each professores as professor (professor.id)}
      <li>
          {professor.nome}
      </li>
      <a href={`../editProfessor/${professor.id}`}>Editar</a>
    {/each}
  </ul>