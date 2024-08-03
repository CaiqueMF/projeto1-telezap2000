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

<h2>Adicionar Cadeira</h2>
	<form on:submit|preventDefault={addCadeira}>
		<input bind:value={nome} placeholder="Nome" required />
	  	<input bind:value={necessidades_sala} placeholder="Necessidades de Sala" />
	  	<input type="checkbox" bind:checked={obrigatoria} /> Obrigatória
	  	<input type="checkbox" bind:checked={eletiva} /> Eletiva
	  	<input type="checkbox" bind:checked={optativa} /> Optativa
	  	<input bind:value={semestre} placeholder="Semestre" />
	  	<input bind:value={curso} placeholder="Curso" />
	  	<button type="submit">Adicionar</button>
	</form>
	<ul>
		{#each cadeiras as cadeira}
		<li>
			<strong>{cadeira.nome}</strong>
			<p>Necessidades de Sala: {cadeira.necessidades_sala}</p>
			<p>Obrigatória: {cadeira.obrigatoria ? 'Sim' : 'Não'}</p>
			<p>Eletiva: {cadeira.eletiva ? 'Sim' : 'Não'}</p>
			<p>Optativa: {cadeira.optativa ? 'Sim' : 'Não'}</p>
			<p>Semestre: {cadeira.semestre}</p>
			<p>Curso: {cadeira.curso}</p>
			<a href={`../editCadeira/${cadeira.id}`}>Editar</a>
		</li>
		{/each}
	</ul>