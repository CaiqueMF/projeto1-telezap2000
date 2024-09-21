<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  let salasLivres = '';
  let salasOcupadas = '';
  
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

<div class="livre">
  <h1>Que tal um lugar para estudar?</h1>
  <p class="veja">Veja as salas disponíveis agora para você</p>
  <div class="salas-container">
    {#each salasLivres as sala}
      <div class="sala">
        <p class="sala-nome">{sala.sala}</p>
        <p>{sala.disponivel}</p>
      </div>
    {/each}
  </div>
</div>

<div class="ocupado">
  <h1>Aulas Agora</h1>
  <div class="salas-container-ocupadas">
    {#each salasOcupadas as sala}
      <div class="sala-ocupada">
        <p>{sala.sala} ocupada até {sala.horario_termino}</p>
        <p>{sala.cadeira}</p>
      </div>
    {/each}
  </div>
</div>

<style>
  .livre, .ocupado {
    border: 1px black solid;
    padding: 10px;
    padding-left: 150px;
    padding-right: 50px;
  }

  h1 {
    font-family: "Playfair Display";
  }

  p {
    font-family: 'Outfit';
    font-weight: 400;
  }
  .livre {
    width: 60%;
    margin: 5% 0;
    border-bottom-right-radius: 10px;
    border-top-right-radius: 10px;
  }

  .veja {
    padding-bottom: 20px;
  }

  .salas-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }

  .salas-container .sala {
    flex: 1 1 calc(33.33% - 20px);
    padding: 10px;
    border-radius: 5px;
  }

  /* Salas ocupadas em linhas de 5 */
  .salas-container-ocupadas {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }

  .salas-container-ocupadas .sala-ocupada {
    flex: 1 1 calc(20% - 20px);
    border: 1px solid red;
    padding: 10px;
    text-align: center;
    border-radius: 5px;
  }

  .sala-nome {
    font-size: 2rem;
  }
</style>
