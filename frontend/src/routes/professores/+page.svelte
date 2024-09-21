<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  import NavigationCoordenador from '../navigationCoordenador.svelte';

  let nome = '';
  let login = ''
  let cadeiras = [];
  let professores = [];
  let turmas = [];
  let pesquisaNome = "";

  let addMode = 0
  let editProfessorById;

  onMount(async () => {
    await fetchOptions();
    await fetchTurmas();
    associateDataWithProfessors();
  });

  function changeMode() {
		addMode = 1;
	}
  

  async function updateProfessor() {
      try {
        const updatedProfessor = {
          nome,
          login
        };
        console.log(updatedProfessor)
        await axios.put(`http://localhost:5000/api/professores/${editProfessorById}`, updatedProfessor);
        goto('/professores');
      } catch (error) {
        console.error(error);
      }
    }

  async function fetchOptions() {
    try {
      const [cadeiraRes, professorRes] = await Promise.all([
        axios.get('http://localhost:5000/api/cadeiras'),
        axios.get('http://localhost:5000/api/professores')
      ]);
      
      cadeiras = cadeiraRes.data;
      professores = professorRes.data.map(p => ({ ...p, turmas: [], disciplinas: [] })); // Inicializa as listas
      console.log(professores)
    } catch (error) {
      console.error('Erro ao carregar opções:', error);
    }
  }

  async function fetchTurmas() {
    try {
      const response = await axios.get('http://localhost:5000/api/turmas');
      turmas = await Promise.all(response.data.map(async turma => {
        const cadeira = cadeiras.find(c => c.id === turma.id_cadeira);
        const professor = professores.find(p => p.id === turma.id_professor);

        return {
          ...turma,
          nome_cadeira: cadeira ? cadeira.nome : 'Desconhecido',
          nome_professor: professor ? professor.nome : 'Desconhecido'
        };
      }));
    } catch (error) {
      console.error('Erro ao carregar turmas:', error);
    }
  }

  async function addProfessor() {
    try {
      const newProfessor = { nome };
      await axios.post('http://localhost:5000/api/professores', newProfessor);
      await fetchOptions(); 
      nome = ''; 
    } catch (error) {
      console.error(error);
    }
    addMode = 0
  }

  function associateDataWithProfessors() {
    professores = professores.map(professor => {
      const turmasDoProfessor = turmas.filter(turma => turma.id_professor === professor.id);
      const disciplinasDoProfessor = turmasDoProfessor.map(turma => turma.nome_cadeira);
      const uniqueDisciplinas = [...new Set(disciplinasDoProfessor)];

      return { 
        ...professor, 
        turmas: turmasDoProfessor,
        disciplinas: uniqueDisciplinas 
      };
    });
  }

  async function updateMode(professor_id) {
    editProfessorById = professor_id;
    try {
        const response = await axios.get(`http://localhost:5000/api/professores/${professor_id}`);
        const professor = response.data;
        console.log(professor)
        nome = professor.nome;
        login = professor.login;   
    } catch (error) {
        console.error(error);
    }
}
</script>

<main>
	<NavigationCoordenador />
	<div class="professores">
		<h1>Professores</h1>
		<p>Aqui estão todas os professores cadastradas no sistema, e sua respectivas quantidade de turmas e disciplinas</p>
		<div class="info">
			<input type="text" bind:value={pesquisaNome} placeholder="🔍︎">
			<button on:click={() => {changeMode()}}><i class="fa-solid fa-plus"></i> Adicionar professor</button>
		</div>
    <table>
			<tr>
				<th>Professor</th>
				<th>Turmas</th>
				<th>Disciplinas</th>
				<th></th>
			</tr>
			{#if addMode == 1}
				<tr class="addLine">
					<td><input bind:value={nome} placeholder="Nome" required /></td>
          <td><input bind:value={login} placeholder="Nome" required /></td>
					<td>
						<button on:click={addProfessor}><i class="fa-solid fa-check"></i></button>
					</td>
				</tr>
			{/if}
			{#each professores as professor}
				{#if professor.nome.toLowerCase().includes(pesquisaNome.toLowerCase()) || pesquisaNome == ""}
						{#if editProfessorById == professor.id}
						<tr class="addLine">
							<td><input bind:value={nome} placeholder="Nome" required /></td>
              <td><input bind:value={login} placeholder="Login" required /></td>
							<td>
								<button on:click={updateProfessor}><i class="fa-solid fa-check"></i></button>
							</td>
						</tr>
						{:else}
						<tr>
							<td>{professor.nome}</td>
              <td>{professor.turmas.length}</td>
              <td>{professor.disciplinas.length}</td>
							<td>
								<button on:click={() => {updateMode(professor.id)}}><i class="fa-solid fa-pencil"></i></button>
							</td>
						</tr>
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
		padding: 0 20%;
		font-family: 'Outfit';
		font-weight: 400;
	}

  h1 {
		font-family: "Playfair Display";
		font-size: 42px;
	}

  .professores, .info {
    display: flex;
    align-items: center;
		width: 100%;
		background-color: white;
		border-radius: 20px;
		margin-top: 3%;
	}

  .professores {
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

  .info button, .info input{
		background-color: #BC4749;
		color: white;
		height: 30px;
		border-radius: 20px;
    border: none;
	}

  .info input {
    width: 80%;
  }

  .info input::placeholder {
        position: relative;
        top: 3%;
       	padding-left: 96%;
       	font-size: large;
       	color: white;
    }

  .info button {
    width: 20%;
  }

  .info i{
    color: white;
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

  button {
		border: none;
		background: none;
		color: #BC4749;
		font-size: 16px;
	}

  i {
		color: black;
	}
</style>