<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    let turmas = [];
    let selectedTurma = null;
  
    onMount(async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/turmas');
        turmas = response.data;
      } catch (error) {
        console.error('Erro ao buscar turmas:', error);
      }
    });
  
    async function fetchTurma(id) {
      try {
        const response = await axios.get(`http://localhost:5000/api/turmas/${id}`);
        selectedTurma = response.data;
      } catch (error) {
        console.error('Erro ao buscar turma:', error);
      }
    }
  </script>
  
  <h1>Turmas</h1>
  <ul>
    {#each turmas as turma (turma.id)}
      <li>
        Turma {turma.n_turma}
      </li>
    {/each}
  </ul>
  
  {#if selectedTurma}
    <h2>Detalhes da Turma</h2>
    <p><strong>ID:</strong> {selectedTurma.id}</p>
    <p><strong>ID Cadeira:</strong> {selectedTurma.id_cadeira}</p>
    <p><strong>ID Professor:</strong> {selectedTurma.id_professor}</p>
    <p><strong>ID Sala:</strong> {selectedTurma.id_sala}</p>
    <p><strong>Número da Turma:</strong> {selectedTurma.n_turma}</p>
    <p><strong>Número de Vagas:</strong> {selectedTurma.n_vagas}</p>
    <p><strong>Curso:</strong> {selectedTurma.curso}</p>
  {/if}
  