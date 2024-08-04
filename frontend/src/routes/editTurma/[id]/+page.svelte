<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
  
    let id;
    let id_cadeira = '';
    let id_professor = '';
    let id_sala = '';
    let n_turma = '';
    let n_vagas = '';
    let curso = '';
  
    $: id = $page.params.id;
  
    onMount(async () => {
      await fetchTurma();
    });
  
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
  </script>
  
  <main>
    <h1>Editar Turma</h1>
    <form on:submit|preventDefault={updateTurma}>
        <input bind:value={id_cadeira} placeholder="ID da Cadeira" required />
        <input bind:value={id_professor} placeholder="ID do Professor" required />
        <input bind:value={id_sala} placeholder="ID da Sala" required />
        <input bind:value={n_turma} placeholder="Numero da Turma" required />
        <input bind:value={n_vagas} placeholder="Vagas" required />
        <input bind:value={curso} placeholder="Curso" required />
        <button type="submit">Atualizar</button>
    </form>
  </main>
  