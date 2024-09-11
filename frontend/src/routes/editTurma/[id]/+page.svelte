<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
  
    let id, dia, horario;
    let id_cadeira = '';
    let id_professor = '';
    let id_sala = '';
    let n_turma = '';
    let n_vagas = '';
    let curso = '';

    let cadeiras = [];
    let professores = [];
    let salas = [];
  
    $: id = $page.params.id;
  
    onMount(async () => {
      await fetchTurma();
      await fetchOptions();
    });

    async function addAlocacao() {
		try {
			const newAlocacao = {
		  	id_turma: id,
		  	dia,
		  	horario,
		};
			await axios.post('http://localhost:5000/api/alocacoes', newAlocacao);
			dia = ''
      horario = ''
	  	} catch (error) {
			console.error(error);
	  }
	}

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
  
    async function fetchTurma() {
      try {
        const response = await axios.get(`http://localhost:5000/api/turmas/${id}`);
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
  
    async function updateTurma() {
      try {
        const updatedTurma = {
            id_cadeira,
              id_professor,
              id_sala,
              n_turma,
              n_vagas,
              curso
        };
        await axios.put(`http://localhost:5000/api/turmas/${id}`, updatedTurma);
        goto('/turmas');
      } catch (error) {
        console.error(error);
      }
    }

    async function deleteTurma(params) {
      try {
        await axios.delete(`http://localhost:5000/api/turmas/${id}`)
        goto('/turmas');
      } catch (error) {
        console.error(error);
      }
    }
  </script>
  
  <main>
    <h1>Editar Turma</h1>
    <form on:submit|preventDefault={updateTurma}>
      <select bind:value={id_cadeira} required>
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
        <input bind:value={n_turma} placeholder="Numero da Turma" required />
        <input bind:value={n_vagas} placeholder="Vagas" required />
        <select bind:value={curso} required>
          <option value="" disabled selected>Curso</option>
          <option value="SMD Diurno">SMD Diurno</option>
          <option value="SMD Noturno">SMD Noturno</option>
          <option value="Tecnologia Educacional">Tecnologia Educacional</option>
        </select>
        <button type="submit">Atualizar</button>
    </form>
    <button on:click={deleteTurma}>Deletar</button>
    <h2>Alocar turma</h2>
    <form on:submit|preventDefault={addAlocacao}>
      <select bind:value={dia}>
        <option value="Segunda-feira">Segunda-feira</option>
        <option value="Terça-feira">Terça-feira</option>
        <option value="Quarta-feira">Quarta-feira</option>
        <option value="Quinta-feira">Quinta-feira</option>
        <option value="Sexta-feira">Sexta-feira</option>
        <option value="Sábado">Sábado</option>
      </select>
      <select bind:value={horario}>
        <option value="8:00">8:00</option>
        <option value="10:00">10:00</option>
        <option value="14:00">14:00</option>
        <option value="16:00">16:00</option>
        <option value="18:00">18:00</option>
        <option value="20:00">20:00</option>
      </select>
    <button type="submit">Alocar turma</button>
    </form>
  </main>
  