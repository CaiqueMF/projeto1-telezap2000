<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  
  let id_cadeira = '';
  let id_professor = '';
  let id_sala = '';
  let n_turma = '';
  let n_vagas = '';
  let curso = '';

  let cadeiras = [];
  let professores = [];
  let salas = [];
  let turmas = [];

  onMount(async () => {
    await fetchOptions();
    await fetchTurmas();
  });

  async function fetchOptions() {
    try {
      const [cadeiraRes, professorRes, salaRes] = await Promise.all([
        axios.get('http://localhost:5000/api/cadeiras'),
        axios.get('http://localhost:5000/api/professores'),
        axios.get('http://localhost:5000/api/salas')
      ]);
      
      cadeiras = cadeiraRes.data;
      professores = professorRes.data;
      salas = salaRes.data;
    } catch (error) {
      console.error('Erro ao carregar opções:', error);
    }
  }

  async function fetchTurmas() {
      try {
          const response = await axios.get('http://localhost:5000/api/turmas');
          turmas = await Promise.all(response.data.map(async turma => {
            // Buscar os nomes com base nos IDs
            const cadeira = cadeiras.find(c => c.id === turma.id_cadeira);
            const professor = professores.find(p => p.id === turma.id_professor);
            const sala = salas.find(s => s.id === turma.id_sala);

            return {
              ...turma,
              nome_cadeira: cadeira ? cadeira.nome : 'Desconhecido',
              nome_professor: professor ? professor.nome : 'Desconhecido',
              nome_sala: sala ? sala.nome : 'Desconhecido'
            };
          }));
      } catch (error) {
          console.error('Erro ao carregar turmas:', error);
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
</script>

<h1>Turmas</h1>

<form on:submit|preventDefault={addTurma}>
  <select bind:value={id_cadeira} on:change={() => {
    curso = cadeiras[id_cadeira - 1].curso}} required>
    <option value="" disabled selected>Selecione a Disciplina</option>
    {#each cadeiras as cadeira}
      <option value={cadeira.id}>{cadeira.nome}</option>
    {/each}
  </select>

  <select bind:value={id_professor} required>
    <option value="" disabled selected>Selecione o Professor</option>
    {#each professores as professor}
      <option value={professor.id}>{professor.nome}</option>
    {/each}
  </select>

  <select bind:value={id_sala} required>
    <option value="" disabled selected>Selecione a Sala</option>
    {#each salas as sala}
      <option value={sala.id}>{sala.nome}</option>
    {/each}
  </select>

  <input bind:value={n_turma} placeholder="Número da Turma" required />
  <input bind:value={n_vagas} placeholder="Vagas" required />
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
    <th>Disciplina:</th>
    <th>Professor:</th>
    <th>Sala:</th>
    <th>Turma:</th>
    <th>Vagas:</th>
    <th>Curso:</th>
    <th>Edição</th>
  </tr>
  {#each turmas as turma (turma.id)}
    <tr>
        <td>{turma.nome_cadeira}</td>
        <td>{turma.nome_professor}</td>
        <td>{turma.nome_sala}</td>
        <td>{turma.n_turma}</td>
        <td>{turma.n_vagas}</td>
        <td>{turma.curso}</td>
        <td><a href={`../editTurma/${turma.id}`}>Editar</a></td>
    </tr>
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