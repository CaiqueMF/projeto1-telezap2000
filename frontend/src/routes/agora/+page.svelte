<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  let salasLivres = ''
  let salasOcupadas = ''
  onMount(async () => {
	  await fetchSalasLivres();
	});
    async function fetchSalasLivres() {
      try {
        const response = await axios.get(`http://localhost:5000/api/salasLivres`);
        salasLivres = response.data.salas;
        const response2 = await axios.get(`http://localhost:5000/api/salasOcupadasAgora`);
        salasOcupadas = response2.data.salas_ocupadas;
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
    {#each salasLivres as sala}
        <p>{sala.sala} livre até {sala.disponivel}</p>
    {/each}
</div>
<div>
  <h1>
      Aulas Agora
  </h1>
  {#each salasOcupadas as sala}
      <p>{sala.sala} ocupada até {sala.horario_termino}</p>
      <p>{sala.cadeira}</p>
  {/each}
</div>
<style>

</style>