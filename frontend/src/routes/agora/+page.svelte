<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  let salas = ''
  onMount(async () => {
	  await fetchSalasLivres();
	});
    async function fetchSalasLivres() {
      try {
        const response = await axios.get(`http://localhost:5000/api/salasLivres`);
        salas = response.data.salas;
        console.log(salas)
      } catch (error) {
        console.error(error);
      }
    }
</script>

<div>
    <h1>
        Que tal um lugar para estudar?
    </h1>
    <p>Veja as salas disponíveis para você</p>
    {#each salas as sala}
        <p>{sala.sala} livre {sala.disponivel}</p>
    {/each}
</div>

<style>

</style>