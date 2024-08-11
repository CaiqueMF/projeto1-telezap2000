<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  
  let id_cadeira = '';
  let id_professor = '';
  let id_sala = '';
  let n_turma = '';
  let n_vagas = '';
  let curso = '';
  let turmas = [];

  onMount(async () => {
    await fetchTurma();
});

  async function fetchTurma() {
      try {
          const response = await axios.get('http://localhost:5000/api/turmas');
          turmas = response.data;
      } catch (error) {
          console.error(error);
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
          await axios.post('http://localhost:5000/api/turmas', newTurma)
          await fetchTurma();
          id_cadeira = ''
          id_professor = ''
          id_sala = ''
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
  <input bind:value={id_cadeira} placeholder="ID da Cadeira" required />
  <input bind:value={id_professor} placeholder="ID do Professor" required />
  <input bind:value={id_sala} placeholder="ID da Sala" required />
  <input bind:value={n_turma} placeholder="Numero da Turma" required />
  <input bind:value={n_vagas} placeholder="Vagas" required />
  <input bind:value={curso} placeholder="Curso" required />
  <button type="submit">Adicionar</button>
</form>

<ul>
  {#each turmas as turma (turma.id)}
    <li>
        {turma.n_turma} - {turma.n_vagas} - {turma.curso}
    </li>
    <a href={`../editTurma/${turma.id}`}>Editar</a>
  {/each}
</ul>
