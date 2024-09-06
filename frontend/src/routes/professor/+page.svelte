<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
	import { token, user } from '../../store';

	$: currentUser = $user.username;

    let cadeiras = []
    let professores = []
    let salas = []
    let turmas = []

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
          
  console.log(turmas)
      } catch (error) {
          console.error('Erro ao carregar turmas:', error);
      }
  }

console.log(currentUser)
</script>

<main>
    <div id="turmas">
        <h1>Minhas Turmas</h1>
        {#each turmas as turma}
            {#if turma.nome_professor == currentUser}
                <div class="turma">
                    <p class="nome_disciplina">{turma.nome_cadeira} T{turma.n_turma}</p>
                    <p class="nome_sala">{turma.nome_sala}</p>
                </div>
            {/if}
        {/each}
    </div>
    <div id="feedback">
        <h2>Enviar feedback</h2>
        <p>Envie alguma sugestão para os coordenadores de como melhorar os horários das suas disciplinas</p>
    </div>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }

    h1, h2 {
        font-family: 'Times New Roman', Times, serif;
    }

    .turma {
        background-color: #5A7302;
        color: white;
        width: 33%;
        border-radius: 10px;
    }
</style>