<script>
	import { onMount } from 'svelte';
	import axios from 'axios';
  
	let cadeiras = [];
	let nome = '';
	let necessidades_sala = '';
	let obrigatoria = false;
	let eletiva = false;
	let optativa = false;
	let semestre = '';
	let curso = '';

	let pesquisaNome = ''
	let pesquisaSemestre = ''
  
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
		  obrigatoria,
		  eletiva,
		  optativa,
		  semestre,
		  curso,
		};
		await axios.post('http://localhost:5000/api/cadeiras', newCadeira);
		await fetchCadeiras();
		nome = '';
		necessidades_sala = '';
		obrigatoria = false;
		eletiva = false;
		optativa = false;
		semestre = '';
		curso = '';
	  } catch (error) {
		console.error(error);
	  }
	}
  </script>
<input type="text" bind:value={pesquisaNome} placeholder="Buscar disciplina">
<input type="text" bind:value={pesquisaSemestre} placeholder="Buscar semestre">
<h2>Adicionar Disciplina</h2>
<form on:submit|preventDefault={addCadeira}>
	<input bind:value={nome} placeholder="Nome" required />
	<input bind:value={necessidades_sala} placeholder="Necessidades de Sala" required />
  	<input type="checkbox" bind:checked={obrigatoria} /> Obrigatória
  	<input type="checkbox" bind:checked={eletiva} /> Eletiva
  	<input type="checkbox" bind:checked={optativa} /> Optativa
	<input bind:value={semestre} placeholder="Semestre" required />
	<input bind:value={curso} placeholder="Curso"required  />
	<button type="submit">Adicionar</button>
</form>
<table>
	<tr>
		<th>Nome:</th>
		<th>Necessidades de Sala: </th>
		<th>Obrigatória: </th>
		<th>Eletiva:</th>
		<th>Optativa:</th>
		<th>Semestre:</th>
		<th>Curso:</th>
		<th>Edição</th>
	</tr>
	{#each cadeiras as cadeira}
		{#if cadeira.nome.toLowerCase().includes(pesquisaNome.toLowerCase()) || pesquisaNome == "" }
			{#if cadeira.semestre.toString() == pesquisaSemestre || pesquisaSemestre == "" }
				<tr>
					<td>{cadeira.nome}</td>
					<td>{cadeira.necessidades_sala}</td>
					<td>{cadeira.obrigatoria ? 'Sim' : 'Não'}</td>
					<td>{cadeira.eletiva ? 'Sim' : 'Não'}</td>
					<td>{cadeira.optativa ? 'Sim' : 'Não'}</td>
					<td>{cadeira.semestre}</td>
					<td>{cadeira.curso}</td>
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