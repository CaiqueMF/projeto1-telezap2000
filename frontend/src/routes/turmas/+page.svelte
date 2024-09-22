<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  import NavigationCoordenador from '../navigationCoordenador.svelte';

  let id, dia, horario;
  let aulas_prolongadas = false
  let id_cadeira = '';
  let id_professor = '';
  let id_sala = '';
  let n_turma = '';
  let n_vagas = '';
  let curso = '';

  let addMode = 0
  let editSalaById;

  let cadeiras = [];
  let professores = [];
  let salas = [];
  let turmas = [];
  let alocacoes = []; // Lista de alocações
  let dicionario_dia = {
      "1":"Segunda feira",
      "2":"Terça feira",
      "3":"Quarta feira",
      "4":"Quinta feira",
      "5":"Sexta feira",
      "6":"Sábado",
    }
  onMount(async () => {
    await fetchOptions();
    await fetchTurmas();
    await fetchAlocacoes();
  });

  function changeMode() {
		addMode = 1;
	}

  async function fetchOptions() {
    try {
      const [cadeiraRes, professorRes, salaRes, alocacoesRes] = await Promise.all([
        axios.get('http://localhost:5000/api/cadeiras'),
        axios.get('http://localhost:5000/api/professores'),
        axios.get('http://localhost:5000/api/salas'),
        axios.get('http://localhost:5000/api/alocacoes')
      ]);

      cadeiras = cadeiraRes.data;
      professores = professorRes.data;
      salas = salaRes.data;
      alocacoes = alocacoesRes.data
    } catch (error) {
      console.error('Erro ao carregar opções:', error);
    }
  }

  async function fetchTurmas() {
    try {
      const response = await axios.get('http://localhost:5000/api/turmas');
      turmas = await Promise.all(
        response.data.map(async (turma) => {
          // Buscar os nomes com base nos IDs
          const cadeira = cadeiras.find((c) => c.id === turma.id_cadeira);
          const professor = professores.find((p) => p.id === turma.id_professor);
          const sala = salas.find((s) => s.id === turma.id_sala);

          return {
            ...turma,
            nome_cadeira: cadeira ? cadeira.nome : 'Desconhecido',
            nome_professor: professor ? professor.nome : 'Desconhecido',
            nome_sala: sala ? sala.nome : 'Desconhecido',
            alocacoes: []
          };
        })
      );
    } catch (error) {
      console.error('Erro ao carregar turmas:', error);
    }
  }

  async function fetchAlocacoes() {
    try {
      const response = await axios.get('http://localhost:5000/api/alocacoes');
      alocacoes = response.data;
      turmas = turmas.map(turma => {
        const alocacoesDaTurma = alocacoes.filter(alocacao => alocacao.id_turma === turma.id);
        return {
          ...turma,
          alocacoes: alocacoesDaTurma
        };
      });
    } catch (error) {
      console.error('Erro ao carregar alocações:', error);
    }
  }

  async function addTurma() {
    try {
      const newTurma = {
        id_cadeira,
        id_professor,
        id_sala,
        n_turma,
        n_vagas,
        curso
      };
      await axios.post('http://localhost:5000/api/turmas', newTurma);
      await fetchTurmas();
      id_cadeira = '';
      id_professor = '';
      id_sala = '';
      n_turma = '';
      n_vagas = '';
      curso = '';
    } catch (error) {
      console.error('Erro ao adicionar turma:', error);
    }
  }

  async function addAlocacao(id) {
		try {
			const newAlocacao = {
		  	id_turma: id,
		  	dia,
		  	horario,
        aulas_prolongadas
		};
			await axios.post('http://localhost:5000/api/alocacoes', newAlocacao);
			dia = ''
      horario = ''
      fetchOptions();
	  	} catch (error) {
			console.error(error);
	  }
	}

  async function updateTurma(turma_id) {
    console.log("rodou")
      try {
        const updatedTurma = {
            id_cadeira,
              id_professor,
              id_sala,
              n_turma,
              n_vagas,
              curso
        };
        await axios.put(`http://localhost:5000/api/turmas/${turma_id}`, updatedTurma);
        
      } catch (error) {
        console.error(error);
      }
      editSalaById = null
      fetchTurmas()
    }

    async function updateMode(turma_id) {
    editSalaById = turma_id;
    try {
        const response = await axios.get(`http://localhost:5000/api/turmas/${turma_id}`);
        const turma = response.data;
        id_cadeira = turma.id_cadeira
        id_professor = turma.id_professor
        id_sala = turma.id_sala
        n_turma = turma.n_turma
        n_vagas = turma.n_vagas
        curso = turma.curso
    } catch (error) {
        console.error(error);
    }
    }
</script>

<main>
<NavigationCoordenador/>
<div class="square">
  <h1>Turmas</h1>
  <p class="desc">Aqui estão todas as turmas alocadas no sistema</p>
  <div class="info">
  <button on:click={() => {changeMode()}}><i class="fa-solid fa-plus"></i> Adicionar turma</button>
  </div>
  <table>
    <tr>
      <th>Disciplina</th>
      <th>Professor</th>
      <th>Sala</th>
      <th>Turma</th>
      <th>Vagas</th>
      <th>Curso</th>
      <th>Alocações (Dia e Horário)</th>
      <th>Edição</th>
    </tr>
    {#if addMode == 1}
      <td>
        <select bind:value={id_cadeira} on:change={() => {
        curso = cadeiras[id_cadeira - 1].curso}} required>
        <option value="" disabled selected>Selecione a Disciplina</option>
        {#each cadeiras as cadeira}
          <option value={cadeira.id}>{cadeira.nome}</option>
        {/each}
      </select>
    </td>
      <td>
        <select bind:value={id_professor} required>
          <option value="" disabled selected>Selecione o Professor</option>
          {#each professores as professor}
            <option value={professor.id}>{professor.nome}</option>
          {/each}
        </select>
      </td>
      <td>
        <select bind:value={id_sala} required>
          <option value="" disabled selected>Selecione a Sala</option>
          {#each salas as sala}
            <option value={sala.id}>{sala.nome}</option>
          {/each}
        </select>
      </td>
      <td>
        <input bind:value={n_turma} placeholder="Número da Turma" required />
      </td>
      <td>
        <input bind:value={n_vagas} placeholder="Vagas" required />
      </td>
      <td>
        <select bind:value={curso} required>
          <option value="" disabled selected>Curso</option>
          <option value="SMD Diurno">SMD Diurno</option>
          <option value="SMD Noturno">SMD Noturno</option>
          <option value="Tecnologia Educacional">Tecnologia Educacional</option>
        </select>
      </td>
      <td>
        <button on:click={() => {
          addTurma()
          }}><i class="fa-solid fa-check"></i></button>
      </td>
    {/if}
    {#each turmas as turma (turma.id)}
    {#if turma.id == editSalaById}
    <td>
      <select bind:value={id_cadeira} on:change={() => {
      curso = cadeiras[id_cadeira - 1].curso}} required>
      <option value="" disabled selected>Selecione a Disciplina</option>
      {#each cadeiras as cadeira}
        <option value={cadeira.id}>{cadeira.nome}</option>
      {/each}
    </select>
  </td>
    <td>
      <select bind:value={id_professor} required>
        <option value="" disabled selected>Selecione o Professor</option>
        {#each professores as professor}
          <option value={professor.id}>{professor.nome}</option>
        {/each}
      </select>
    </td>
    <td>
      <select bind:value={id_sala} required>
        <option value="" disabled selected>Selecione a Sala</option>
        {#each salas as sala}
          <option value={sala.id}>{sala.nome}</option>
        {/each}
      </select>
    </td>
    <td>
      <input bind:value={n_turma} placeholder="Número da Turma" required />
    </td>
    <td>
      <input bind:value={n_vagas} placeholder="Vagas" required />
    </td>
    <td>
      <select bind:value={curso} required>
        <option value="" disabled selected>Curso</option>
        <option value="SMD Diurno">SMD Diurno</option>
        <option value="SMD Noturno">SMD Noturno</option>
        <option value="Tecnologia Educacional">Tecnologia Educacional</option>
      </select>
    </td>
    <td>
      <select bind:value={dia}>
        <option value="1">Segunda-feira</option>
        <option value="2">Terça-feira</option>
        <option value="3">Quarta-feira</option>
        <option value="4">Quinta-feira</option>
        <option value="5">Sexta-feira</option>
        <option value="6">Sábado</option>
      </select>
      <select bind:value={horario}>
        <option value="8">8:00</option>
        <option value="10">10:00</option>
        <option value="14">14:00</option>
        <option value="16">16:00</option>
        <option value="18">18:00</option>
        <option value="20">20:00</option>
      </select>
      <input type="checkbox" bind:checked={aulas_prolongadas} /> Aulas prolongadas
      <button on:click={addAlocacao(turma.id)}>adicionar horário</button>
    </td>
    <td>
      <button on:click={() => {
        updateTurma(turma.id)
        }}><i class="fa-solid fa-check"></i></button>
    </td>
    {:else}
    <tr>
      <td>{turma.nome_cadeira}</td>
      <td>{turma.nome_professor}</td>
      <td>{turma.nome_sala}</td>
      <td>{turma.n_turma}</td>
      <td>{turma.n_vagas}</td>
      <td>{turma.curso}</td>
      <td>
        {#if turma.alocacoes.length > 0}
          {#each turma.alocacoes as alocacao}
            {dicionario_dia[alocacao.dia]} - {alocacao.horario}:00 à {alocacao.horario+alocacao.duracao}:00
          {/each}
        {:else}
          <span>Sem alocação</span>
        {/if}
      </td>
      <td><button on:click={updateMode(turma.id)}><i class="fa-solid fa-pencil"></i></button></td>
    </tr>
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
    align-self: first baseline;
		font-size: 42px;
	}

  .desc {
    align-self: first baseline;
  }

  .square {
    border-radius: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 80%;
    margin-top: 3%;
    background-color: white;
    padding: 10px;
  }

  .info {
    display: flex;
    align-items: center;
		width: 100%;
		background-color: white;
		border-radius: 20px;
	}

  .info {
    justify-content: end;
    margin-top: 1%;
		margin-bottom: 1%;
		display: flex;
		gap: 10px;
  }

  .info button {
		background-color: #BC4749;
		color: white;
		height: 30px;
		border-radius: 20px;
    width: 20%;
    border: none;
	}

  .info button i {
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