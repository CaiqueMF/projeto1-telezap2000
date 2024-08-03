<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    let salas = [];
    let selectedSala = null;
  
    onMount(async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/salas');
        salas = response.data;
      } catch (error) {
        console.error('Erro ao buscar salas:', error);
      }
    });
  
    async function fetchSala(id) {
      try {
        const response = await axios.get(`http://localhost:5000/api/salas/${id}`);
        selectedSala = response.data;
      } catch (error) {
        console.error('Erro ao buscar sala:', error);
      }
    }
  </script>
  
  <h1>Salas</h1>
  <ul>
    {#each salas as sala (sala.id)}
      <li>
          {sala.nome}
      </li>
    {/each}
  </ul>
  
  {#if selectedSala}
    <h2>Detalhes da Sala</h2>
    <p><strong>ID:</strong> {selectedSala.id}</p>
    <p><strong>Nome:</strong> {selectedSala.nome}</p>
    <p><strong>Tipos:</strong> {selectedSala.tipos}</p>
  {/if}
  