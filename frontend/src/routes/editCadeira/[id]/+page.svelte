<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
  
    let id;
    let nome = '';
    let necessidades_sala = '';
    let natureza = ''
    let semestre = '';
    let aulas_prolongadas = false;
    let curso = '';
    let error_message = false

    $: id = $page.params.id;
  
    onMount(async () => {
      await fetchCadeira();
    });
  
    async function fetchCadeira() {
      try {
        const response = await axios.get(`http://localhost:5000/api/cadeiras/${id}`);
        const cadeira = response.data;
        nome = cadeira.nome;
        necessidades_sala = cadeira.necessidades_sala;
        natureza = cadeira.natureza
        semestre = cadeira.semestre;
        curso = cadeira.curso;
      } catch (error) {
        console.error(error);
      }
    }
  
    async function updateCadeira() {
      try {
        const updatedCadeira = {
          nome,
          necessidades_sala,
          natureza,
          semestre,
          aulas_prolongadas,
          curso,
        };
        await axios.put(`http://localhost:5000/api/cadeiras/${id}`, updatedCadeira);
        goto('/cadeiras');
      } catch (error) {
        console.error(error);
      }
    }
    async function deletaCadeira(params) {
      try {
        await axios.delete(`http://localhost:5000/api/cadeiras/${id}`)
        goto('/cadeiras');
      } catch (error) {
        console.error(error);
        error_message = true
      }
    }
  </script>
  
  <main>
    <h1>Editar Cadeira</h1>
    <form on:submit|preventDefault={updateCadeira}>
      <input bind:value={nome} placeholder="Nome" required />
      <select bind:value={necessidades_sala} required>
        <option value="" disabled selected>Necessidade de Sala</option>
        <option value="Sala normal">Sala normal</option>
        <option value="Sala grande">Sala grande</option>
        <option value="Atelie">Ateliê</option>
        <option value="Laboratorio basico">Laboratório básico</option>
        <option value="Laboratorio avançado">Laboratório avançado</option>
      </select>
      <select bind:value={natureza} required>
        <option value="" disabled selected>Natureza da disciplina</option>
        <option value="Obrigatoria">Obrigatória</option>
        <option value="Eletiva">Eletiva</option>
		    <option value="Optativa">Optativa</option>
	    </select>
      <select bind:value={semestre} required>
        <option value="" disabled selected>Semestre</option>
        {#each Array(8).fill().map((_, i) => i + 1) as sem}
          <option value={sem}>{sem}</option>
          {/each}
      </select>
      <input type="checkbox" bind:checked={aulas_prolongadas} /> Aulas prolongadas
      <select bind:value={curso} required>
        <option value="" disabled selected>Curso</option>
        <option value="SMD Diurno">SMD Diurno</option>
        <option value="SMD Noturno">SMD Noturno</option>
        <option value="Tecnologia Educacional">Tecnologia Educacional</option>
      </select>
      <button type="submit">Atualizar</button>
    </form>
    <button on:click={deletaCadeira}>Deletar</button>
    {#if error_message}
      <p>A disciplina que você tentou deletar está alocada com uma turma, remova a alocação dessa disciplina para conseguir deletá-la</p>
    {/if}
  </main>
  