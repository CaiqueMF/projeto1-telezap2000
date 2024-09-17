<script>
  import { onMount } from 'svelte';
  import axios from 'axios';

  let nome = '';
  let cadeiras = [];
  let professores = [];
  let turmas = [];
  let pesquisaNome = "";

  onMount(async () => {
    await fetchOptions();
    await fetchTurmas();
    associateDataWithProfessors();
  });

  async function fetchOptions() {
    try {
      const [cadeiraRes, professorRes] = await Promise.all([
        axios.get('http://localhost:5000/api/cadeiras'),
        axios.get('http://localhost:5000/api/professores')
      ]);
      
      cadeiras = cadeiraRes.data;
      professores = professorRes.data.map(p => ({ ...p, turmas: [], disciplinas: [] })); // Inicializa as listas
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
        {professor.nome} - {professor.turmas.length} turmas - {professor.disciplinas.length} disciplinas
        <a href={`../editProfessor/${professor.id}`}>Editar</a>
      </li>
    {/if}
  {/each}
</ul>
