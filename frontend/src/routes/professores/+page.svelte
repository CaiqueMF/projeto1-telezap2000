<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    let professores = [];
    let selectedProfessor = null;
  
    onMount(async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/professores');
        professores = response.data;
      } catch (error) {
        console.error('Erro ao buscar professores:', error);
      }
    });
  
    async function fetchProfessor(id) {
      try {
        const response = await axios.get(`http://localhost:5000/api/professores/${id}`);
        selectedProfessor = response.data;
      } catch (error) {
        console.error('Erro ao buscar professor:', error);
      }
    }
  </script>
  
  <h1>Professores</h1>
  <ul>
    {#each professores as professor (professor.id)}
      <li>
          {professor.nome}
      </li>
    {/each}
  </ul>
  
  {#if selectedProfessor}
    <h2>Detalhes do Professor</h2>
    <p><strong>ID:</strong> {selectedProfessor.id}</p>
    <p><strong>Nome:</strong> {selectedProfessor.nome}</p>
  {/if}
  