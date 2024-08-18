<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
  
    let id;
    let nome = '';
    let necessidades_sala = '';
    let obrigatoria = false;
    let eletiva = false;
    let optativa = false;
    let semestre = '';
    let curso = '';
  
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
        obrigatoria = cadeira.obrigatoria;
        eletiva = cadeira.eletiva;
        optativa = cadeira.optativa;
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
          obrigatoria,
          eletiva,
          optativa,
          semestre,
          curso,
        };
        await axios.put(`http://localhost:5000/api/cadeiras/${id}`, updatedCadeira);
        goto('/cadeiras');
      } catch (error) {
        console.error(error);
      }
    }
  </script>
  
  <main>
    <h1>Editar Cadeira</h1>
    <form on:submit|preventDefault={updateCadeira}>
      <input bind:value={nome} placeholder="Nome" required />
      <input bind:value={necessidades_sala} placeholder="Necessidades de Sala" required />
      <input type="checkbox" bind:checked={obrigatoria} /> Obrigatória
      <input type="checkbox" bind:checked={eletiva} /> Eletiva
      <input type="checkbox" bind:checked={optativa} /> Optativa
      <input bind:value={semestre} placeholder="Semestre" required />
      <input bind:value={curso} placeholder="Curso" required />
      <button type="submit">Atualizar</button>
    </form>
  </main>
  