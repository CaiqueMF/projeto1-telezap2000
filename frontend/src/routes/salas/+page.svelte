<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    import NavigationCoordenador from '../navigationCoordenador.svelte';
    import { goto } from '$app/navigation';
    import { token, user } from '../../store';

    let nome = ''
    let tipos = ''
    let salas = [];
    let editSalaById
    
    onMount(async () => {
	    await fetchSala();
      const currentUser = $user;
      if (!currentUser.isAuthenticated) {
           goto('/');
        }
	});

    async function fetchSala() {
      try {
        const response = await axios.get(`http://localhost:5000/api/salas`);
        salas = response.data;
      } catch (error) {
        console.error(error);
      }
    }

    async function updateMode(sala_id) {
    editSalaById = sala_id;
    try {
        const response = await axios.get(`http://localhost:5000/api/salas/${sala_id}`);
        const sala = response.data;
        nome = sala.nome;
        tipos = sala.tipo;   
    } catch (error) {
        console.error(error);
    }
    }

    async function updateSala() {
      try {
        const updatedSala = {
          nome,
          tipos
        };
        console.log("rodou")
        await axios.put(`http://localhost:5000/api/salas/${editSalaById}`, updatedSala);
        editSalaById = null
        fetchSala();
      } catch (error) {
        console.error(error);
      }
    }
  </script>
<main>
  <NavigationCoordenador />
  <div class="square">
     <div>
      <h1>Salas</h1>
      <p>Aqui estão todas as salas com suas especifidades</p>
      <h1>Laboratórios - 1º e 2º andar</h1>
      <div class="salas">
      {#each salas as sala}
      {#if editSalaById == sala.id && sala.tipos == "Laboratório básico" || editSalaById == sala.id && sala.tipos == "Laboratório avançado"}
      <div class="salaSquare">
        <div class="content">
          <input type="text" bind:value={nome}>
      <select bind:value={tipos} required>
        <option value="" disabled selected>Tipo de sala</option>
        <option value="Sala normal">Sala normal</option>
        <option value="Sala grande">Sala grande</option>
        <option value="Ateliê">Ateliê</option>
        <option value="Laboratório básico">Laboratório básico</option>
        <option value="Laboratório avançado">Laboratório avançado</option>
      </select>
      <button on:click={updateSala}><i class="fa-solid fa-check"></i></button>
        </div>
      </div>
      {:else}
        {#if sala.tipos == "Laboratório básico" || sala.tipos == "Laboratório avançado"}
        <div class="salaSquare">
          <div class="content">
            <p>{sala.nome}</p>
            {#if sala.tipos == "Laboratório básico"}
              <p class="tipo">Computadores Dell</p>
            {:else}
              <p class="tipo">Computadores Mac</p>
            {/if}
          </div>
        <button on:click={updateMode(sala.id)}><i class="fa-solid fa-pencil"></i></button>
        </div>
        {/if}
        {/if}
      {/each}
      </div>
    </div>
        <div>
            <h1>Salas - Térreo</h1>
            <div class="salas">
                {#each salas as sala}
                    {#if editSalaById == sala.id && sala.tipos == "Sala normal" || editSalaById == sala.id && sala.tipos == "Sala grande" || editSalaById == sala.id && sala.tipos == "Ateliê"}
                    <div class="salaSquare">
                      <div class="content">
                        <input type="text" bind:value={nome}>
                    <select bind:value={tipos} required>
                      <option value="" disabled selected>Tipo de sala</option>
                      <option value="Sala normal">Sala normal</option>
                      <option value="Sala grande">Sala grande</option>
                      <option value="Ateliê">Ateliê</option>
                      <option value="Laboratório básico">Laboratório básico</option>
                      <option value="Laboratório avançado">Laboratório avançado</option>
                    </select>
                    <button on:click={updateSala}><i class="fa-solid fa-check"></i></button>
                      </div>
                    </div>
                    {:else}
                    {#if sala.tipos == "Sala normal" || sala.tipos == "Sala grande" || sala.tipos == "Ateliê"}
                        <div class="salaSquare">
                            <div class="content">
                                <p>{sala.nome}</p>
                                {#if sala.tipos == "Sala normal" || sala.tipos == "Ateliê"}
                                    <p class="tipo">Para 30 alunos</p>
                                {:else}
                                    <p class="tipo">Para 60 alunos</p>
                                {/if}
                            </div>
                            <button on:click={updateMode(sala.id)}><i class="fa-solid fa-pencil"></i></button>
                        </div>
                    {/if}
                    {/if}
                {/each}
            </div>
        </div>
    </div>
</main>

<style>
    main {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0 10%;
		font-family: 'Outfit';
		font-weight: 400;
    background-image:linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),  url('Iurifoto5 1.png');
    height: 100vh;
    background-size: cover;
    background-position: center;
	}

  h1 {
		font-family: "Playfair Display";
		font-size: 42px;
	}

    .square {
        border: 1px solid black;
        padding: 15px;
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin-top: 3%;
        background-color: white;
    }

    .square div {
        width: 100%;
    }

    .salas {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px; 
        width: 100%;
        justify-items: center; 
    }

    .salaSquare {
        background-color: #CECECE;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        padding: 10px;
        height: 100px; 
        text-align: left; 
        justify-content: space-between; 
        align-items: flex-start; 
        position: relative; 
    }

    .salaSquare .content {
        flex: 1;
    }

    .salaSquare i {
        position: absolute;
        bottom: 10px;
        right: 10px;
        font-size: 16px;
        color: black;
    }

    .salaSquare p {
        margin: 0;
        font-weight: 400;
    }

    .tipo {
        font-size: 1rem;
    }

    button {
      border: none;
    }
    </style>
