<script>
	import { onMount } from 'svelte';
	import axios from 'axios';
  
	let cadeiras = [];
	let nome = '';
	let necessidades_sala = '';
	let natureza = ""
	let semestre = '';
	let aulas_prolongadas = false;
	let curso = '';
  
	let pesquisaNome = '';
	let pesquisaSemestre = '';
  
	onMount(async () => {
	  await fetchCadeiras();
	});
  
	async function fetchCadeiras() {
		try {
			const response = await axios.get('http://localhost:5000/api/cadeiras');
			cadeiras = response.data;
	  	} catch (error) {
			console.error(error);
	  	}
	}
  
	async function addCadeira() {
		try {
			const newCadeira = {
		  	nome,
		  	necessidades_sala,
		  	natureza,
		  	semestre,
		  	aulas_prolongadas,
		  	curso,
		};
			await axios.post('http://localhost:5000/api/cadeiras', newCadeira);
			await fetchCadeiras();
			nome = '';
			necessidades_sala = '';
			natureza = ''
			semestre = '';
			aulas_prolongadas = false;
			curso = '';
	  	} catch (error) {
			console.error(error);
	  }
	}
</script>
  
<input type="text" bind:value={pesquisaNome} placeholder="Buscar disciplina">
<input type="text" bind:value={pesquisaSemestre} placeholder="Buscar semestre">
<p>Quantidade total de disciplinas: {cadeiras.length}</p>
<h2>Adicionar Disciplina</h2>
<form on:submit|preventDefault={addCadeira}>
	<input bind:value={nome} placeholder="Nome" required />
      <select bind:value={necessidades_sala} required>
        <option value="" disabled selected>Necessidade de Sala</option>
        <option value="Sala normal">Sala normal</option>
        <option value="Sala grande">Sala grande</option>
        <option value="Atelie">Ateliê</option>
        <option value="Laboratorio basico">Laboratório básico</option>
        <option value="Laboratorio avançado">Laboratório avançado</option>
      </select>
      <select bind:value={natureza} required>
        <option value="" disabled selected>Natureza da disciplina</option>
        <option value="Obrigatoria">Obrigatória</option>
        <option value="Eletiva">Eletiva</option>
		<option value="Optativa">Optativa</option>
	  </select>
      <select bind:value={semestre} required>
        <option value="" disabled selected>Semestre</option>
        {#each Array(8).fill().map((_, i) => i + 1) as sem}
          <option value={sem}>{sem}</option>
          {/each}
      </select>
      <input type="checkbox" bind:checked={aulas_prolongadas} /> Aulas prolongadas
      <select bind:value={curso} required>
        <option value="" disabled selected>Curso</option>
        <option value="SMD Diurno">SMD Diurno</option>
        <option value="SMD Noturno">SMD Noturno</option>
        <option value="Tecnologia Educacional">Tecnologia Educacional</option>
      </select>
	<button type="submit">Adicionar</button>
</form>
  
<table>
	<tr>
		<th>Nome:</th>
	  	<th>Necessidades de Sala:</th>
	 	<th>Natureza:</th>
	  	<th>Semestre:</th>
	  	<th>Curso:</th>
	  	<th>Aulas prolongadas:</th>
	  	<th>Edição</th>
	</tr>
	{#each cadeiras as cadeira}
		{#if cadeira.nome.toLowerCase().includes(pesquisaNome.toLowerCase()) || pesquisaNome == ""}
			{#if cadeira.semestre.toString() == pesquisaSemestre || pesquisaSemestre == ""}
				<tr>
					<td>{cadeira.nome}</td>
					<td>{cadeira.necessidades_sala}</td>
					<td>{cadeira.natureza}</td>
					<td>{cadeira.semestre}</td>
					<td>{cadeira.curso}</td>
					<td>{cadeira.aulas_prolongadas ? 'Sim' : 'Não'}</td>
					<td><a href={`../editCadeira/${cadeira.id}`}>Editar</a></td>
			  	</tr>
			{/if}
	    {/if}
	{/each}
</table>
  
<style>
	table {
	  font-family: arial, sans-serif;
	  border-collapse: collapse;
	  width: 100%;
	}
	
	td, th {
	  border: 1px solid #e0e0e0;
	  text-align: left;
	  padding: 8px;
	}
  
	tr:nth-child(even) {
	  background-color: #e0e0e0;
	}
</style>
  