<script>
	import { onMount } from 'svelte';
	import axios from 'axios';
    import NavigationCoordenador from '../navigationCoordenador.svelte';
  
	let cadeiras = [];
	let nome = '';
	let necessidades_sala = '';
	let natureza = '';
	let semestre = '';
	let aulas_prolongadas = false;
	let curso = '';

	let addMode = 0;
	let editCadeiraById;
  
	let pesquisaNome = '';
	let pesquisaSemestre = '';
  
	onMount(async () => {
		await fetchCadeiras();
	});

	function changeMode() {
		addMode = 1;
	}

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
			natureza = '';
			semestre = '';
			aulas_prolongadas = false;
			curso = '';
			addMode = 0;
	  	} catch (error) {
			console.error(error);
	  	}
	}

	async function updateCadeira() {
    try {
        const updatedCadeira = {
            nome,
            necessidades_sala,
            natureza,
            semestre,
            aulas_prolongadas,
            curso,
        };
        await axios.put(`http://localhost:5000/api/cadeiras/${editCadeiraById}`, updatedCadeira);
        await fetchCadeiras(); // Atualiza a lista de cadeiras
		nome = '';
		necessidades_sala = '';
		natureza = '';
		semestre = '';
		aulas_prolongadas = false;
		curso = '';
		addMode = 0;
    	editCadeiraById = null;
    } catch (error) {
        console.error(error);
    }
}

	async function deletaCadeira(cadeira_id) {
		console.log(cadeira_id)
		try {
			await axios.delete(`http://localhost:5000/api/cadeiras/${cadeira_id}`);
			await fetchCadeiras();
		} catch (error) {
			console.error(error);
		}
	}

	async function updateMode(cadeira_id) {
    editCadeiraById = cadeira_id;
    try {
        const response = await axios.get(`http://localhost:5000/api/cadeiras/${cadeira_id}`);
        const cadeira = response.data;

        nome = cadeira.nome;
        necessidades_sala = cadeira.necessidades_sala;
        natureza = cadeira.natureza;
        semestre = cadeira.semestre;
        aulas_prolongadas = cadeira.aulas_prolongadas;
        curso = cadeira.curso;
    } catch (error) {
        console.error(error);
    }
}
</script>

<main>
	<NavigationCoordenador />
	<div class="cadeiras">
		<h1>Disciplinas</h1>
		<p>Aqui estão todas as disciplinas cadastradas no sistema</p>
		<div class="info">
			<input type="text" bind:value={pesquisaNome} placeholder="🔍︎">
			<select bind:value={pesquisaSemestre}>
				<option value="" selected>Filtrar por semestre</option>
				{#each Array(8).fill().map((_, i) => i + 1) as sem}
				<option value={sem}>Semestre: {sem}</option>
				{/each}
			</select>
			<button on:click={() => {changeMode()}}>+ Adicionar disciplina</button>
			<p>Disciplinas cadastradas: {cadeiras.length}</p>
		</div>
		<table>
			<tr>
				<th>Nome:</th>
				<th>Necessidades de Sala:</th>
				<th>Natureza:</th>
				<th>Semestre:</th>
				<th>Curso:</th>
				<th>Aulas prolongadas:</th>
				<th></th>
			</tr>
			{#if addMode == 1}
				<tr class="addLine">
					<td><input bind:value={nome} placeholder="Nome" required /></td>
					<td>
						<select bind:value={necessidades_sala} required>
							<option value="" disabled selected>Necessidade de Sala</option>
							<option value="Sala normal">Sala normal</option>
							<option value="Sala grande">Sala grande</option>
							<option value="Ateliê">Ateliê</option>
							<option value="Laboratório básico">Laboratório básico</option>
							<option value="Laboratório avançado">Laboratório avançado</option>
						</select>
					</td>
					<td>
						<select bind:value={natureza} required>
							<option value="" disabled selected>Natureza da disciplina</option>
							<option value="Obrigatória">Obrigatória</option>
							<option value="Eletiva">Eletiva</option>
							<option value="Optativa">Optativa</option>
						</select>
					</td>
					<td>
						<select bind:value={semestre} required>
							<option value="" disabled selected>Semestre</option>
							{#each Array(8).fill().map((_, i) => i + 1) as sem}
								<option value={sem}>{sem}</option>
							{/each}
						</select>
					</td>
					<td>
						<select bind:value={curso} required>
							<option value="" disabled selected>Curso</option>
							<option value="SMD">SMD</option>
							<option value="Tecnologia Educacional">Tecnologia Educacional</option>
						</select>
					</td>
					<td>
						<input type="checkbox" bind:checked={aulas_prolongadas} />
					</td>
					<td>
						<button on:click={addCadeira}><i class="fa-solid fa-check"></i></button>
					</td>
				</tr>
			{/if}
			{#each cadeiras as cadeira}
				{#if cadeira.nome.toLowerCase().includes(pesquisaNome.toLowerCase()) || pesquisaNome == ""}
					{#if cadeira.semestre.toString() == pesquisaSemestre || pesquisaSemestre == ""}
						{#if editCadeiraById == cadeira.id}
						<tr class="addLine">
							<td><input bind:value={nome} placeholder="Nome" required /></td>
							<td>
								<select bind:value={necessidades_sala} required>
									<option value="" disabled selected>Necessidade de Sala</option>
									<option value="Sala normal">Sala normal</option>
									<option value="Sala grande">Sala grande</option>
									<option value="Ateliê">Ateliê</option>
									<option value="Laboratório básico">Laboratório básico</option>
									<option value="Laboratório avançado">Laboratório avançado</option>
								</select>
							</td>
							<td>
								<select bind:value={natureza} required>
									<option value="" disabled selected>Natureza da disciplina</option>
									<option value="Obrigatória">Obrigatória</option>
									<option value="Eletiva">Eletiva</option>
									<option value="Optativa">Optativa</option>
								</select>
							</td>
							<td>
								<select bind:value={semestre} required>
									<option value="" disabled selected>Semestre</option>
									{#each Array(8).fill().map((_, i) => i + 1) as sem}
										<option value={sem}>{sem}</option>
									{/each}
								</select>
							</td>
							<td>
								<select bind:value={curso} required>
									<option value="" disabled selected>Curso</option>
									<option value="SMD">SMD</option>
									<option value="Tecnologia Educacional">Tecnologia Educacional</option>
								</select>
							</td>
							<td>
								<input type="checkbox" bind:checked={aulas_prolongadas} />
							</td>
							<td>
								<button on:click={updateCadeira}><i class="fa-solid fa-check"></i></button>
							</td>
						</tr>
						{:else}
						<tr>
							<td>{cadeira.nome}</td>
							<td>{cadeira.necessidades_sala}</td>
							<td>{cadeira.natureza}</td>
							<td>{cadeira.semestre}</td>
							<td>{cadeira.curso}</td>
							<td>{cadeira.aulas_prolongadas ? 'Sim' : 'Não'}</td>
							<td>
								<button on:click={() => {updateMode(cadeira.id)}}><i class="fa-solid fa-pencil"></i></button>
								<button on:click={() => {deletaCadeira(cadeira.id)}}><i class="fa-solid fa-trash"></i></button>
							</td>
						</tr>
						{/if}
					{/if}
				{/if}
			{/each}
		</table>
	</div>
</main>

<style>
	main {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0 10%;
		font-family: 'Outfit';
		font-weight: 400;
	}

	h1 {
		font-family: "Playfair Display";
		font-size: 42px;
	}

	.cadeiras, .info {
        display: flex;
        align-items: center;
		width: 100%;
		background-color: white;
		border-radius: 20px;
		margin-top: 3%;
	}

	button {
		border: none;
		background: none;
		color: #BC4749;
		font-size: 16px;
	}

	.cadeiras {
		flex-direction: column;
		align-items: normal;
		padding: 10px;
	}

	.info {
		margin-top: 1%;
		margin-bottom: 1%;
		display: flex;
		gap: 10px;
	}

	.info button, .info input, .info select {
		background-color: #BC4749;
		color: white;
		height: 30px;
		border-radius: 20px;
	}

	.info input {
		width: 40%;
        border-radius: 30px;
        border-style: none;
        padding-left: 3%;
	}

	.info input::placeholder {
        position: relative;
        top: 3%;
       	padding-left: 93%;
       	font-size: large;
       	color: white;
    }

	.info button {
		width: 20%;
	}

	.info button:hover {
		background-color: #a83f41;
	}

	.info select {
		width: 20%;
	}

	.info p {
		width: 20%;
		font-size: 16px;
	}

	table {
	  	font-family: arial, sans-serif;
	  	border-collapse: collapse;
	  	width: 100%;
	}
	
	td, th {
	  	text-align: left;
		padding: 8px;
	}

	th {
		background-color: #D9D9D9;
		border-right: 1px solid #666666;
		color: #666666;
	}

	th:first-child {
		border-top-left-radius: 15px;
		border-bottom-left-radius: 15px;
	}

	th:last-child {
		border-top-right-radius: 15px;
		border-bottom-right-radius: 15px;
		border: none;
	}

	tr:first-child, tr:last-child {
		border: none;
	}
 
	tr {
		border-bottom: 1px #666666 solid;
	}

	.addLine input, .addLine select{
		background-color: #D9D9D9;
		width: 100%;
		border-style: none;
		border-radius: 10px;
		padding: 5px;
	}

	i {
		color: black;
	}
</style>
  